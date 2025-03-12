from qualtran import Bloq, Signature, QBit, Register, BloqBuilder, Soquet
from qualtran.bloqs.basic_gates import Hadamard
from qualtran.bloqs.block_encoding import Unitary

from numpy.typing import NDArray
import numpy as np

from Phase import Phase
from QFT import QFT


Matrix = NDArray[np.complex128]


class QPE(Bloq):
    U: Matrix
    """Unitary to get the phase or the eigenvalues of"""
    precision: int
    """Number of qubits for eigenvalue precision."""
    N: int
    """Size of the unitary"""

    def __init__(self, U: Matrix, precision: int, N: int):
        super().__init__()
        self.U = U
        self.precision = precision
        self.N = N

    @property
    def signature(self):
        return Signature(
            [
                Register("eig", QBit(), (self.precision,)),
                Register("phi", QBit(), (self.N,)),
            ]
        )

    def build_composite_bloq(self, bb: BloqBuilder, *, eig: list[Soquet], phi: list[Soquet]):
        for i in range(self.N):
            eig[i] = bb.add(Hadamard(), q=eig[i])

        powers = [self.U]
        for i in range(self.N - 1):
            powers += [powers[-1] @ powers[-1]]

        for i, u in enumerate(powers):
            eig[i], phi = bb.add(Unitary(u).controlled(), ctrl=eig[i], target=phi)
        # POSSIBLY REMOVE eig[i] HERE ---------------------------------------------------------------------------
        eig = bb.add(QFT(self.N).adjoint(), targets=eig)

    def adjoint(self):
        return QPEAdj(self.precision, self.N, self.U)
    

class QPEAdj(Bloq):
    U: Matrix
    """Unitary to get the phase or the eigenvalues of."""
    precision: int
    """Number of qubits for eigenvalue precision."""
    N: int
    """Size of the unitary."""

    def __init__(self, U: Matrix, precision: int, N: int):
        super().__init__()
        self.U = U
        self.precision = precision
        self.N = N

    @property
    def signature(self):
        return Signature(
            [
                Register("eig", QBit(), (self.precision,)),
                Register("phi", QBit(), (self.N,)),
            ]
        )

    def build_composite_bloq(self, bb: BloqBuilder, *, eig: Soquet, phi: Soquet):
        eig = bb.add(QFT(self.precision), targets=eig)

        powers = [self.U]
        for i in range(self.precision - 1):
            powers.append(powers[-1] @ powers[-1])

        for i, u in enumerate(reversed(powers)):  # Reverse the order of unitaries
            eig[i], phi = bb.add(Unitary(u).controlled(), ctrl=eig[i], target=phi)
        # POSSIBLY REMOVE eig[i] HERE ---------------------------------------------------------------------------

        for i in range(self.precision - 1, -1, -1):
            eig[i] = bb.add(Hadamard(), q=eig[i])

    def adjoint(self):
        return QPE(self.precision, self.N, self.U)

def test_qpe_phase_estimation():
    # Setup parameters
    precision = 3  # Number of qubits for phase estimation
    N = 2          # Size of the unitary (we are using a 1x1 matrix)
    phase = np.pi / 4  # We want to estimate a phase of pi/4

    # Define the phase shift unitary (U = e^(i*phase))
    U = np.array([[1, 0], [0, np.exp(1j*phase)]])

    # Build the QPE Bloq
    qpe_bloq = QPE(U, precision, N)
    print(qpe_bloq.call_classically(eig=[0]*precision, phi=[0]*N))

# Function to extract the estimated phase from the eig register (simplified for this test)
def extract_phase(eig: Soquet):
    # Assuming the eig register is in computational basis, the phase can be extracted by analyzing the result
    # This is a simplified function, actual extraction might involve interpreting the state of the register
    return np.angle(eig[0].value)  # Placeholder: extract phase from eig[0]

# Run the test
test_qpe_phase_estimation()