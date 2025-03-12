import pytest
import numpy as np
from .matrix_utils import is_hermitian, make_hermitian

def test_is_hermitian():
    M_hermitian = np.array([
        [1+0j, 2-1j],
        [2+1j, 3+0j]
    ])
    assert is_hermitian(M_hermitian) is True

    M_non_hermitian = np.array([
        [1+0j, 2+1j],
        [2+1j, 3+0j]
    ])
    assert is_hermitian(M_non_hermitian) is False


def test_make_hermitian():
    M = np.array([
        [1+2j, 3-4j],
        [5+6j, 7-8j]
    ])
    M_hermitian = make_hermitian(M)

    assert M_hermitian.shape == (2 * M.shape[0], 2 * M.shape[1])
    assert np.allclose(M_hermitian, M_hermitian.conj().T)
