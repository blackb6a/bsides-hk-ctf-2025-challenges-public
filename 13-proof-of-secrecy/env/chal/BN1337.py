from sage.all import EllipticCurve, GF, ZZ
from sage.groups.generic import has_order

p = ZZ(3754213587383997421)
modulus = [
    ZZ(1903955209848875692),
    ZZ(580200876007969624),
    ZZ(1868838931335540206),
    ZZ(2438428199543377684),
    ZZ(1722342269211969597),
    ZZ(1379610505854700636),
    ZZ(1226675346099764568),
    ZZ(1817440843858358744),
    ZZ(2896118133381603053),
    ZZ(758419574978819632),
    ZZ(3513707464005747814),
    ZZ(1156609658669228863),
    ZZ(1),
]
r = ZZ(3754213585446472021)

F = GF(p)
F12 = GF((p, 12), modulus=modulus, name="z12")

F_size = (F.order().nbits() + 7) // 8
F12_size = (F12.order().nbits() + 7) // 8

# Pairing-friendly curve
# Genereated using the Barreto-Naehrig construction
b = F(512565911644471536)
E = EllipticCurve(F, [0, b])
E12 = E.change_ring(F12)

# Pairing points
G1 = E.lift_x(F(13333333337))
assert has_order(G1, r)

G2 = E12.lift_x(F12.gen() ** 133337) * (E12.order() // r**2)
assert has_order(G2, r)


def pairing(P, Q):
    return E12(P).weil_pairing(E12(Q), r)


w12 = pairing(G1, G2)
