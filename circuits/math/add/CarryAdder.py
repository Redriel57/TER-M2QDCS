from qualtran import Bloq, Signature, QBit, Register, BloqBuilder, Soquet
from .Adder import Adder
from .NoCinAdder import NoCinAdder


class CarryAdder(Bloq):
    """Full carry adder.

    Parameters
    ----------
    bitsize : int
        How many qubits encode your numbers.

    Needed qubits
    -------------
    - x : `bitsize` qubit(s)
    - y : `bitsize` qubit(s)
    - z : `bitsize` qubit(s)
    - cout : 1 qubit
    - ancilla : (`bitsize` - 1) qubit(s)
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
                Register("x", QBit(), (self.bitsize,)),
                Register("y", QBit(), (self.bitsize,)),
                Register("z", QBit(), (self.bitsize,)),
                Register("cout", QBit()),
                Register("ancilla", QBit(), (self.bitsize - 1,)),
            ]
        )

    def build_composite_bloq(
        self,
        bb: BloqBuilder,
        *,
        x: list[Soquet],
        y: list[Soquet],
        z: list[Soquet],
        cout: Soquet,
        ancilla: list[Soquet],
    ):
        full_cout = ancilla + [cout]
        x[0], y[0], z[0], full_cout[0] = bb.add(
            NoCinAdder(), x=x[0], y=y[0], z=z[0], cout=full_cout[0]
        )
        for i in range(1, self.bitsize):
            cout[i - 1], x[i], y[i], z[i], full_cout[i] = bb.add(
                Adder(), cin=cout[i - 1], x=x[i], y=y[i], z=z[i], cout=full_cout[i]
            )

        return {
            "x": x,
            "y": y,
            "z": z,
            "cout": full_cout[-1],
            "ancilla": full_cout[:-1],
        }

    def adjoint(self):
        return CarryAdderAdj(self.bitsize)


class CarryAdderAdj(Bloq):
    bitsize: int
    """Bit size of input"""

    def __init__(self, bitsize: int):
        super().__init__()
        self.bitsize = bitsize

    @property
    def signature(self):
        return Signature(
            [
                Register("x", QBit(), (self.bitsize,)),
                Register("y", QBit(), (self.bitsize,)),
                Register("z", QBit(), (self.bitsize,)),
                Register("cout", QBit()),
                Register("ancilla", QBit(), (self.bitsize - 1,)),
            ]
        )

    def build_composite_bloq(
        self,
        bb: BloqBuilder,
        *,
        x: list[Soquet],
        y: list[Soquet],
        z: list[Soquet],
        cout: Soquet,
        ancilla: list[Soquet],
    ):
        full_cout = ancilla + [cout]
        for i in range(self.bitsize - 1, 0, -1):
            cout[i - 1], x[i], y[i], z[i], full_cout[i] = bb.add(
                Adder().adjoint(),
                cin=cout[i - 1],
                x=x[i],
                y=y[i],
                z=z[i],
                cout=full_cout[i],
            )

        x[0], y[0], z[0], full_cout[0] = bb.add(
            NoCinAdder().adjoint(), x=x[0], y=y[0], z=z[0], cout=full_cout[0]
        )

        return {
            "x": x,
            "y": y,
            "z": z,
            "cout": full_cout[-1],
            "ancilla": full_cout[:-1],
        }

    def adjoint(self):
        return CarryAdder(self.bitsize)

    def pretty_name(self) -> str:
        return f"CarryAdder†(bitsize={self.bitsize})"
