import numpy as np
from numpy.typing import NDArray

Matrix = NDArray[np.complex128]


def is_hermitian(M: Matrix):
    return np.allclose(M, M.conj().T)


def make_hermitian(M: Matrix):
    zero_block = np.zeros_like(M, dtype=np.complex128)
    M_dagger = M.conj().T
    return np.block([[zero_block, M], [M_dagger, zero_block]])
