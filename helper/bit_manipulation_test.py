import pytest
from .bit_manipulation import nat2bl, bl2nat, bl2bs, nat2bs, bs2bl, bs2nat, i2bl, bl2i


def test_nat2bl():
    assert nat2bl(4, 6) == [0, 1, 1, 0]
    assert nat2bl(5, 3) == [0, 0, 0, 1, 1]


def test_bl2nat():
    assert bl2nat([1, 0, 1]) == 5
    assert bl2nat([0, 1, 1, 0]) == 6


def test_bl2bs():
    assert bl2bs([1, 0, 1]) == "101"
    assert bl2bs([0, 1, 1, 0]) == "0110"


def test_nat2bs():
    assert nat2bs(4, 6) == "0110"
    assert nat2bs(5, 3) == "00011"


def test_bs2bl():
    assert bs2bl("0110") == [0, 1, 1, 0]
    assert bs2bl("00011") == [0, 0, 0, 1, 1]


def test_bs2nat():
    assert bs2nat("0110") == 6
    assert bs2nat("00011") == 3


def test_i2bl():
    assert i2bl(4, 6) == [0, 1, 1, 0]
    assert i2bl(5, 3) == [0, 0, 0, 1, 1]


def test_bl2i():
    assert bl2i([1, 0, 1]) == 5
    assert bl2i([0, 1, 1, 0]) == 6
