from qualtran.bloqs.basic_gates import CNOT, Toffoli
from qualtran import Bloq, Signature, QBit, Register, BloqBuilder, Soquet


class NoCinAdder(Bloq):
    """
    Single bit adder without carry in

    Needed qubits
    -------------
    - x: 1 qubit
    - y: 1 qubit
    - z: 1 qubit
    - cout: 1 qubit
    """

    bitsize: int
    """Bit size of input"""

    def __init__(self, bitsize: int):
        super().__init__()
        self.bitsize = bitsize
        self.ancilla_size = 2 * bitsize + 1

    @property
    def signature(self):
        return Signature(
            [
                Register("x", QBit()),
                Register("y", QBit()),
                Register("z", QBit()),
                Register("cout", QBit()),
            ]
        )

    def build_composite_bloq(
        self, bb: BloqBuilder, *, x: Soquet, y: Soquet, z: Soquet, cout: Soquet
    ):
        x, z = bb.add(CNOT(), ctrl=x, target=z)
        y, z = bb.add(CNOT(), ctrl=y, target=z)

        [x, y], cout = bb.add(Toffoli(), ctrl=[x, y], target=cout)
        return {"x": x, "y": y, "z": z, "cout": cout}

    def adjoint(self):
        return NoCinAdderAdj()


class NoCinAdderAdj(Bloq):
    @property
    def signature(self):
        return Signature(
            [
                Register("x", QBit()),
                Register("y", QBit()),
                Register("z", QBit()),
                Register("cout", QBit()),
            ]
        )

    def build_composite_bloq(
        self, bb: BloqBuilder, *, x: Soquet, y: Soquet, z: Soquet, cout: Soquet
    ):
        [x, y], cout = bb.add(Toffoli(), ctrl=[x, y], target=cout)

        y, z = bb.add(CNOT(), ctrl=y, target=z)
        x, z = bb.add(CNOT(), ctrl=x, target=z)

        return {"x": x, "y": y, "z": z, "cout": cout}

    def adjoint(self):
        return NoCinAdder()

    def pretty_name(self) -> str:
        return "NoCinAdder†"
