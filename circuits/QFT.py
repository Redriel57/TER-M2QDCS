from qualtran import Bloq, Signature, QBit, Register, BloqBuilder, Soquet
from qualtran.bloqs.basic_gates import Hadamard, Swap
from math import pi

from Phase import Phase

class QFT(Bloq):
    n_qubits: int
    """Number of qubits for the QFT."""

    def __init__(self, n_qubits: int):
        super().__init__()
        self.n_qubits = n_qubits

    @property
    def signature(self):
        return Signature(
            [
                Register("targets", QBit(), (self.n_qubits,)),
            ]
        )

    def build_composite_bloq(
        self,
        bb: BloqBuilder,
        *,
        targets: Soquet,
    ):
        for i in range(self.n_qubits):
            targets[i] = bb.add(Hadamard(), q=targets[i])
            
            for j in range(i + 1, self.n_qubits):
                angle = 2 * pi / (2 ** (j - i + 1))
                targets[j] = bb.add(Phase(angle).controlled(), ctrl=targets[i], target=targets[j])

        for i in range(self.n_qubits // 2):
            targets[i], targets[self.n_qubits - 1 - i] = bb.add(Swap(), target1=targets[i], target2=targets[self.n_qubits - 1 - i])

        return {"targets": targets}

    def adjoint(self):
        return QFTAdj(self.n_qubits)


class QFTAdj(Bloq):
    n_qubits: int
    """Number of qubits for the inverse QFT."""

    def __init__(self, n_qubits: int):
        super().__init__()
        self.n_qubits = n_qubits

    @property
    def signature(self):
        return Signature(
            [
                Register("targets", QBit(), (self.n_qubits,)),
            ]
        )

    def build_composite_bloq(
        self,
        bb: BloqBuilder,
        *,
        targets: Soquet,
    ):
        for i in range(self.n_qubits // 2):
            targets[i], targets[self.n_qubits - 1 - i] = bb.add(Swap(), target1=targets[i], target2=targets[self.n_qubits - 1 - i])

        for i in reversed(range(self.n_qubits)):
            for j in range(i + 1, self.n_qubits):
                angle = -2 * pi / (2 ** (j - i + 1))
                targets[j] = bb.add(Phase(angle).controlled(), ctrl=targets[i], target=targets[j])

            targets[i] = bb.add(Hadamard(), q=targets[i])

        return {"targets": targets}

    def adjoint(self):
        return QFT(self.n_qubits)
    
    def pretty_name(self):
        return "QFT†"