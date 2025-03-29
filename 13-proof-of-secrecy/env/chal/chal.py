import os
import zlib
import secrets
import hashlib
from KZG import PolyCommit, point_to_bytes, E, F, F_size, r, Point
from sage.all import PolynomialRing, ZZ, GF, randrange


banner = """
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣄⣠⣄⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢿⣿⠏⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⣀⣀⡀⠀⠀⠀⠀⠀⠀⠈⠀⠀⠀
⠀⠀⠀⠀⣀⡤⣤⠶⠛⠉⠉⠀⠀⠉⠉⠛⠲⣤⣤⣄⠀⠀⠀⠀⠀
⠀⠀⠀⡼⠃⠈⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠁⠈⢧⠀⠀⠀⠀
⠀⠀⡼⢁⡆⠀⢀⡀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡄⠀⢰⡈⢧⠀⠀⠀
⢀⡞⠁⣸⠁⠀⢠⠬⠓⠀⣀⠀⠀⢀⠀⠛⠥⣄⠀⠀⡇⠈⢳⡀⠀
⡞⠀⠀⠹⣆⢰⣒⠆⠀⠀⠓⠊⠙⠚⠁⠀⠸⠭⠇⣰⠇⠀⠀⢻⠀
⣇⠀⠀⠀⠈⣹⠶⠦⠤⠤⣤⣤⣤⡤⠤⠤⠴⠶⣏⠁⠀⠀⠀⣸⠁
⠈⠓⠲⠖⠚⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠓⠲⠶⠚⠁⠀
"""


def stylish_input() -> str:
    return input("( -_•)▄︻テحكـ━一💥 ")


def read_comm() -> Point:
    point_bytes = bytes.fromhex(stylish_input())
    return E(F.from_bytes(point_bytes[:F_size]), F.from_bytes(point_bytes[F_size:]))


def print_comm(point) -> None:
    print(point_to_bytes(point).hex())


def part1(pc: PolyCommit) -> bool:
    # generate a secret ᕙ( •̀ ᗜ •́ )ᕗ
    secret = secrets.randbelow(r)

    # generate a proof (,,>﹏<,,)
    R = PolynomialRing(GF(r), "x")
    phi = R.random_element(2**12)
    comm = pc.commit_poly(phi)
    print_comm(comm)

    # generate a second proof ٩(ˊᗜˋ*)و ♡
    psi = phi * secret + 1337
    comm = pc.commit_poly(psi)
    print_comm(comm)

    # generate a third proof ( ˶°ㅁ°) !!
    psi = phi * 1337 + secret
    comm = pc.commit_poly(psi)
    print_comm(comm)

    # give me a proof (,,>﹏<,,)
    psi = phi * (secret * 1337) + (secret * 1337)
    comm = read_comm()
    return pc.verify_poly(psi, comm)


def part2(pc: PolyCommit) -> bool:
    # challenge with my favourite number! ( • ̀ω•́ )✧
    deg = 69
    R = PolynomialRing(ZZ, "x")
    while not (phi := R.random_element(deg, x=0, y=r, monic=True)).is_irreducible():
        pass
    print(phi.list())

    eval_points = [secrets.randbelow(r) for _ in range(deg + 2)]
    print(eval_points)

    # commit to two polynomials... ('. • ᵕ •. `)
    comm1 = read_comm()
    comm2 = read_comm()

    # commit to the evaluations... ('. • ᵕ •. `)
    wit1 = [read_comm() for _ in range(deg + 2)]
    wit2 = [read_comm() for _ in range(deg + 2)]

    # give me the evaluations... ('. • ᵕ •. `)
    eval1 = [ZZ(stylish_input()) for _ in range(deg + 2)]
    eval2 = [ZZ(stylish_input()) for _ in range(deg + 2)]

    # ensure the evaluations make sense (っ‘ω`c)
    if not pc.batch_verify_eval(eval_points, eval1, comm1, wit1):
        return False

    if not pc.batch_verify_eval(eval_points, eval2, comm2, wit2):
        return False

    # now I will check p1 * p2 = phi (# ﾟДﾟ) ﾑｯ!
    for v1, v2, pt in zip(eval1, eval2, eval_points):
        if v1 * v2 != phi(pt):
            print("!!!", v1, v2, pt, phi(pt))
            return False
    if not all(v1 * v2 == phi(pt) for v1, v2, pt in zip(eval1, eval2, eval_points)):
        print("hmm 3")
        return False

    # of course, making sure neither are constant (•؎ •)
    if len(set(eval1)) == 1 or len(set(eval2)) == 1:
        return False

    # oh yeah, check the commits too ( ‘• ω • `)
    psi1 = R(list(stylish_input().split(",")))  # type: ignore
    psi2 = R(list(stylish_input().split(",")))  # type: ignore

    return pc.verify_poly(psi1, comm1) and pc.verify_poly(psi2, comm2)


def part3(pc: PolyCommit) -> bool:
    PARTIES = 32
    NEEDED = PARTIES // 2

    R = PolynomialRing(GF(r), "x")

    for _ in range(16):
        secret = secrets.randbelow(r)
        phi_coeffs = [secret] + [secrets.randbelow(r) for _ in range(NEEDED - 1)]
        phi = R(phi_coeffs)  # type: ignore

        # we are committed! to the polynomial ( • ̀ω•́ )✧
        print_comm(pc.commit_poly(phi))

        # generating shares (っ‘ω`c)
        shares = [phi(x) for x in range(1, PARTIES + 1)]

        idx = randrange(NEEDED)
        shares[idx] += shares[NEEDED + idx]

        # come get your shares (•؎ •)
        for _ in range(NEEDED + 2):
            cmd = stylish_input()
            if cmd == "redeal":
                shares = [phi(x) for x in range(1, PARTIES + 1)]
                print("すみません")
            elif cmd.startswith("share"):
                idx = int(stylish_input())
                if 1 <= idx <= NEEDED:
                    print(shares[idx - 1])
                    print_comm(pc.prove_eval(phi, idx))
                else:
                    print(secrets.randbelow(r))
                    print_comm(E.random_point())
            else:
                break

        # what is my secret ヽ(^◇^*)/
        if secret != int(stylish_input()):
            return False

    return True


def part4(pc: PolyCommit) -> bool:
    PARTIES = 32
    NEEDED = PARTIES // 2

    R = PolynomialRing(GF(r), "x")

    # tell me your name (っ‘ω`c)
    name = stylish_input()
    parties = [name.encode()] + [os.urandom(PARTIES - 1)]
    eval_points = [int.from_bytes(hashlib.sha256(name).digest()[:2]) for name in parties]

    for _ in range(16):
        secret = secrets.randbelow(r)
        phi_coeffs = [secret] + [secrets.randbelow(r) for _ in range(NEEDED - 1)]
        phi = R(phi_coeffs)  # type: ignore

        # we are committed! to the polynomial ( • ̀ω•́ )✧
        print_comm(pc.commit_poly(phi))

        # here is your share. go talk to other parties (•؎ •)
        shares = [(phi(point), pc.prove_eval(phi, point)) for point in eval_points]
        print(shares[0][0])
        print_comm(shares[0][1])

        # what is my secret ヽ(^◇^*)/
        if secret != int(stylish_input()):
            return False

    return True


if __name__ == "__main__":
    # load CRS string
    pc = PolyCommit()
    with open("KZG_4096.crs", "rb") as crs_file:
        crs_data = crs_file.read()
        assert zlib.crc32(crs_data) == 1514964631
        pc.loads_crs(crs_data)

    print(banner)
    assert part1(pc)
    assert part2(pc)
    assert part3(pc)
    assert part4(pc)

    FLAG = os.getenv("FLAG") or "bsideshk{placeholder_flag}"
    print("❤︎", FLAG)
