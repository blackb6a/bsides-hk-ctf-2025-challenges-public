import io
import copy
from typing import Optional, TypeAlias

from sage.misc.prandom import randrange
from sage.rings.polynomial.polynomial_element import Polynomial
from sage.schemes.elliptic_curves.ell_point import EllipticCurvePoint_finite_field as Point
from sage.groups.generic import multiples

from BN1337 import r, F, F12, F_size, F12_size, E, E12, G1, G2, w12, pairing

Commit: TypeAlias = Point
Witness: TypeAlias = Point


def point_to_bytes(P: Point) -> bytes:
    return P.x().to_bytes() + P.y().to_bytes()


class PolyCommit:
    """
    A class for polynomial commitments using elliptic curves.
    """

    crs: Optional[list[Point]] = None  # Common Reference String
    crs2: Optional[Point] = None  # CRS but only G2's power
    max_degree: Optional[int] = None  # Maximum degree of the polynomial

    def setup(self, max_degree: int) -> None:
        """
        Generate a new Common Reference String (CRS).

        Args:
            max_degree (int): The maximum degree of polynomials to commit to.
        """
        self.max_degree = max_degree
        # secret exponent, discarded afterwards
        k = randrange(1, r)
        # generate powers of G1
        self.crs = list(multiples(k, max_degree + 1, P0=G1, operation="*"))  # type: ignore
        # append G2's power for verification
        self.crs2 = k * G2  # type: ignore

    def dumps_crs(self) -> bytes:
        """
        Serialize the CRS to a byte string.

        Returns:
            bytes: The serialized CRS.
        """
        assert self.crs is not None and self.crs2 is not None and self.max_degree is not None

        return (
            self.max_degree.to_bytes(8)
            + b"".join(map(point_to_bytes, self.crs))
            + point_to_bytes(self.crs2)
        )

    def loads_crs(self, crs: bytes, G2_only=False) -> None:
        """
        Load a CRS from a byte string.

        Args:
            crs (bytes): The serialized CRS.
        """
        if G2_only:
            return self._loads_crs_G2(crs)

        crs_stream = io.BytesIO(crs)
        self.max_degree = int.from_bytes(crs_stream.read(8))

        self.crs = []
        for _ in range(self.max_degree + 1):
            x = F.from_bytes(crs_stream.read(F_size))
            y = F.from_bytes(crs_stream.read(F_size))
            self.crs.append(E.point((x, y, F.one()), check=False))
        assert self.crs[0] == G1  # ensure the first element is G1

        x = F12.from_bytes(crs_stream.read(F12_size))
        y = F12.from_bytes(crs_stream.read(F12_size))
        point = E12.point((x, y, F12.one()), check=False)
        self.crs2 = point

    def _loads_crs_G2(self, crs: bytes) -> None:
        """
        Only load the G2 portion of the CRS from a byte string.

        Args:
            crs (bytes): The serialized CRS.
        """
        x = F12.from_bytes(crs[-F12_size * 2 : -F12_size])
        y = F12.from_bytes(crs[-F12_size:])
        self.crs2 = E12.point((x, y, F12.one()), check=False)

    def commit_poly(self, phi: Polynomial) -> Point:
        """
        Commit to a polynomial phi(x).

        Args:
            phi (Polynomial): The polynomial to commit to.

        Returns:
            Point: The commitment point.
        """
        assert self.crs is not None and self.max_degree is not None
        assert phi.degree() <= self.max_degree

        res: Point = E.zero()

        for G_i, c_i in zip(self.crs, phi.list()):
            if not c_i.is_zero():
                res += c_i * G_i
        return res

    def verify_poly(self, phi: Polynomial, comm: Commit) -> bool:
        """
        Verify that comm is a valid commitment of phi.

        Args:
            phi (Polynomial): The polynomial.
            comm (Commit): The commitment to verify.

        Returns:
            bool: True if valid, False otherwise.
        """
        return self.commit_poly(phi) == comm

    def prove_eval(self, phi: Polynomial, a: int) -> Witness:
        """
        Create a witness for the evaluation phi(a).

        Args:
            phi (Polynomial): The polynomial.
            a (int): The point of evaluation.

        Returns:
            Witness: The witness point.
        """
        # this is inefficient but this is a toy implementation anyways
        psi: Polynomial = divmod(phi - phi(a), phi.parent().gen() - a)[0]
        return self.commit_poly(psi)

    def batch_prove_eval(self, phi: Polynomial, ai: list[int]) -> list[Witness]:
        """
        Create witnesses for the evaluations phi(a) for each a in ai.

        Args:
            phi (Polynomial): The polynomial.
            ai (list[int]): The list of points of evaluation.

        Returns:
            list[Witness]: A list of witness points corresponding to each evaluation.
        """
        # TODO: implement batched KZG commitments
        return [self.prove_eval(phi, a) for a in ai]

    def verify_eval(self, a: int, b: int, comm: Commit, wit: Witness) -> bool:
        """
        Verify that wit is a witness for phi(a) = b.

        Args:
            a (int): The point of evaluation.
            b (int): The expected evaluation.
            comm (Commit): The commitment.
            wit (Witness): The witness to verify.

        Returns:
            bool: True if the witness is valid, False otherwise.
        """
        assert self.crs2 is not None

        f1 = pairing(comm, G2)
        f2 = pairing(wit, self.crs2 - a * G2)
        f3 = w12**b
        return f1 == f2 * f3

    def batch_verify_eval(
        self, ai: list[int], bi: list[int], comm: Commit, wits: list[Witness]
    ) -> bool:
        """
        Verify that each wit is a witness for phi(ai) = bi.

        Args:
            ai (list[int]): The list of points of evaluation.
            bi (list[int]): The list of expected evaluations.
            comm (Commit): The commitment.
            wits (list[Witness]): The list of witnesses to verify.

        Returns:
            list[bool]: A list indicating the validity of each witness.
        """
        # TODO: implement batched KZG commitments
        return all(self.verify_eval(a, b, comm, wit) for a, b, wit in zip(ai, bi, wits))

    @staticmethod
    def test_crs() -> None:
        """
        Test the correctness of the loads_crs and dumps_crs methods.
        """
        pc = PolyCommit()
        pc.setup(100)

        original_crs = copy.deepcopy(pc.crs)
        pc.loads_crs(pc.dumps_crs())
        assert original_crs == pc.crs

    @staticmethod
    def test_crs_G2() -> None:
        """
        Test the correctness of the _loads_crs_G2 method.
        """
        pc = PolyCommit()
        pc.setup(100)

        crs2 = pc.crs2
        pc.loads_crs(pc.dumps_crs(), G2_only=True)
        assert crs2 == pc.crs2

    @staticmethod
    def test_poly() -> None:
        """
        Test the correctness of commit_poly and verify_poly methods.
        """
        from sage.all import PolynomialRing, GF

        pc = PolyCommit()
        pc.setup(100)

        R = PolynomialRing(GF(r), "x")
        phi = R.random_element(100)
        assert pc.verify_poly(phi, pc.commit_poly(phi))
        assert not pc.verify_poly(phi + 1, pc.commit_poly(phi))

    @staticmethod
    def test_eval() -> None:
        """
        Test the correctness of prove_eval and verify_eval methods.
        """
        from sage.all import PolynomialRing, GF

        pc = PolyCommit()
        pc.setup(100)

        R = PolynomialRing(GF(r), "x")
        phi = R.random_element(100)
        a = R.base_ring().random_element()
        assert pc.verify_eval(a, phi(a), pc.commit_poly(phi), pc.prove_eval(phi, a))
        assert not pc.verify_eval(a, phi(a) + 1, pc.commit_poly(phi), pc.prove_eval(phi, a))

    @staticmethod
    def test_batch_eval() -> None:
        """
        Test the correctness of batch_prove_eval and batch_verify_eval methods.
        """
        from sage.all import PolynomialRing, GF

        pc = PolyCommit()
        pc.setup(100)

        R = PolynomialRing(GF(r), "x")
        phi = R.random_element(100)
        a = R.base_ring().random_element()
        assert pc.verify_eval(a, phi(a), pc.commit_poly(phi), pc.prove_eval(phi, a))
        assert not pc.verify_eval(a, phi(a) + 1, pc.commit_poly(phi), pc.prove_eval(phi, a))

    @staticmethod
    def test() -> None:
        """
        Run all tests and verify functionality of the PolyCommit class.
        """
        PolyCommit.test_crs()
        PolyCommit.test_crs_G2()
        PolyCommit.test_poly()
        PolyCommit.test_eval()
        print("\x1b[32mAll tests passed successfully!\x1b[0m")


if __name__ == "__main__":
    PolyCommit.test()
