from qualtran.bloqs.basic_gates import CNOT
from qualtran import Bloq, Signature, QBit, Register, BloqBuilder, Soquet


class Copy(Bloq):
    """
    Copies using CNOTs from orig to trgt

    Parameters:
    bitsize: How many qubits to copy

    Needed qubits:
    - orig: <bitsize> qubits
    - trgt: <bitsize> qubits
    """

    bitsize: int
    """Bit size of input"""

    def __init__(self, bitsize: int):
        super().__init__()
        self.bitsize = bitsize

    @property
    def signature(self):
        return Signature(
            [
                Register("orig", QBit(), (self.bitsize,)),
                Register("trgt", QBit(), (self.bitsize,)),
            ]
        )

    def build_composite_bloq(
        self,
        bb: BloqBuilder,
        *,
        orig: list[Soquet],
        trgt: list[Soquet],
    ):
        for i in range(self.bitsize):
            orig[i], trgt[i] = bb.add(CNOT(), ctrl=orig[i], target=trgt[i])

        return {"orig": orig, "trgt": trgt}

    def adjoint(self):
        return Copy(self.bitsize)
