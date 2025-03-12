from qualtran.bloqs.basic_gates import Swap
from qualtran import Bloq, Signature, QBit, Register, BloqBuilder, Soquet


class Doubler(Bloq):
    """Doubles a given encoded number.

    Parameters
    ----------
    bitsize : int
        How many qubits encode your numbers.
    force0 : bool
        If we should ensure first qubit is |0> (adds an ancilla).
        Otherwise, the greatest weight qubit will be moved to the lowest.
        

    Needed qubits
    -------------
    - x: `bitsize` qubits
    """

    bitsize: int
    """Bit size of input"""
    force0: bool
    """If we should ensure first qubit is |0> (adds an ancilla)"""

    def __init__(self, bitsize: int, force0: bool = False):
        super().__init__()
        self.bitsize = bitsize
        if self.force0: raise NotImplementedError("Force0 hasn't been implemented")
        self.force0 = force0

    @property
    def signature(self):
        a = [Register("ancilla", QBit())] if self.force0 else []
        return Signature(
            [
                Register("x", QBit(), (self.bitsize,)),
            ]
            + a
        )

    def build_composite_bloq(
        self,
        bb: BloqBuilder,
        *,
        x: list[Soquet],
    ):
        for i in range(self.bitsize - 2, 0, -1):
            x[i], x[i + 1] = bb.add(Swap(bitsize=1), x=x[i], y=x[i + 1])

        return {"x": x}

    def adjoint(self):
        return DoublerAdj(self.bitsize, self.force0)


class DoublerAdj(Bloq):
    bitsize: int
    """Bit size of input"""
    force0: bool
    """If we should ensure first qubit is |0> (adds an ancilla)"""

    def __init__(self, bitsize: int, force0: bool = False):
        super().__init__()
        self.bitsize = bitsize
        if self.force0: raise NotImplementedError("Force0 hasn't been implemented")
        self.force0 = force0

    @property
    def signature(self):
        a = [Register("ancilla", QBit())] if self.force0 else []
        return Signature(
            [
                Register("x", QBit(), (self.bitsize,)),
            ]
            + a
        )

    def build_composite_bloq(
        self,
        bb: BloqBuilder,
        *,
        x: Soquet,
    ):
        for i in range(self.bitsize - 1):
            x[i], x[i + 1] = bb.add(Swap(bitsize=1), x=x[i], y=x[i + 1])

        return {"x": x}

    def adjoint(self):
        return Doubler(self.bitsize, self.force0)

    def pretty_name(self) -> str:
        return "Doubler†"
