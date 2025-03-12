from typing import Literal, List


bit = Literal[0, 1]


def nat2bl(pad: int, f: float) -> List[bit]:
    """From natural to binary list"""
    if f == 0:
        return [0 for _ in range(pad)]
    elif f % 2 == 1:
        r = nat2bl(pad - 1, (f - 1) // 2)
        return r + [1]
    r = nat2bl(pad - 1, f // 2)
    return r + [0]


def bl2nat(l: list[bit]) -> float:
    """From binary list to natural"""
    if len(l) == 0:
        return 0
    return l.pop() + 2 * bl2nat(l)


def bl2bs(l: list[bit]) -> str:
    """From binary list to binary string"""
    if len(l) == 0:
        return ""
    a = l.pop()
    return bl2bs(l) + str(a)


def nat2bs(pad: int, f: float) -> str:
    """From natural to binary string"""
    return bl2bs(nat2bl(pad, f))


def bs2bl(s: str) -> list[bit]:
    """From binary string to binary list"""
    return [int(s[i]) for i in range(len(s))]


def bs2nat(s: str) -> float:
    """From binary string to natural"""
    return bl2nat(bs2bl(s))


def i2bl(pad: int, i: int) -> list[bit]:
    """From integer to binary list"""
    return list(map(int, bin(i)[2:].zfill(pad)))


def bl2i(l: list[bit]) -> int:
    """From binary list to integer"""
    v = 0
    p = 1
    for i in range(len(l)):
        v += p*l[-i-1]
        p *= 2
    return v
