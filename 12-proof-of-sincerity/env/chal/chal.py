import os
import secrets
from KZG import PolyCommit, r, G1, G2

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


def main() -> bool:
    for _ in range(32):
        # binary -> bit, ternary -> tit
        tit = secrets.randbelow(3)

        # generate new CRS ('. • ᵕ •. `)
        pc = PolyCommit()
        pc.setup(32)
        assert pc.crs and pc.crs2

        if tit == 1:
            pc.crs[secrets.randbelow(32)] *= secrets.randbelow(r)
        elif tit == 2:
            pc.crs2 *= secrets.randbelow(r)

        print(pc.dumps_crs().hex())

        # i wonder what bit is... (•؎ •)
        if int(stylish_input()) != tit:
            return False

    return True


if __name__ == "__main__":
    print(banner)
    assert main()

    FLAG = os.getenv("FLAG") or "bsideshk{placeholder_flag}"
    print("❤︎", FLAG)
