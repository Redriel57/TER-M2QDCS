from qualtran import Bloq, Signature, QBit, Register, BloqBuilder, Soquet

from helper.bit_manipulation import i2bl
from .Adder import Adder
from .NoCinAdder import NoCinAdder


class ConstAdder(Bloq):
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
    cst: int
    """Constant to add"""
    decomp: list[int]
    """Constant to add in binary list format"""

    def __init__(self, bitsize: int, cst: int):
        super().__init__()
        self.bitsize = bitsize
        self.cst = cst
        self.decomp = i2bl(bitsize, cst)

    @property
    def signature(self):
        return Signature(
            [
                Register("x", QBit(), (self.bitsize,)),
                Register("z", QBit(), (self.bitsize,)),
                Register("cout", QBit()),
                Register("ancilla", QBit(), (self.bitsize,)),
            ]
        )

    def build_composite_bloq(
        self,
        bb: BloqBuilder,
        *,
        x: list[Soquet],
        z: list[Soquet],
        cout: Soquet,
        ancilla: list[Soquet],
    ):
        # If we don't add anything:
        if self.cst == 0:
            return {"x": x, "z": z, "cout": cout, "ancilla": ancilla}

        # If we add something, then we decompose it in binary,
        # and perform "+1" operations using bigger controlled nots

        # First, to build the bigger controlled not, we keep what ancilla has what "ANDs" calculated
        # from Toffolis to reuse them as much as possible, and to be able to easily uncompute them to free the ancilla.
        ands = dict()
        keys = set()

        for current_power in range(self.bitsize):
            # If we don't need to +2^current_power, continue
            if self.decomp[current_power] == 0:
                continue

            keys.update(
                {
                    tuple(range(current_power, current_power + i))
                    for i in range(2, self.bitsize - current_power)
                }
            )

        # Using dynamic programming, we can find the most optimal combination of groups to fulfill
        # all needed "ANDs" for the incrementor

    def adjoint(self):
        return ConstAdderAdj(self.bitsize, self.cst)

    def pretty_name(self):
        return f"ConstAdder<{self.cst}>"


class ConstAdderAdj(Bloq):
    bitsize: int
    """Bit size of input"""
    cst: int
    """Constant to add"""
    decomp: list[int]
    """Constant to add in binary list format"""

    def __init__(self, bitsize: int, cst: int):
        super().__init__()
        self.bitsize = bitsize
        self.cst = cst
        self.decomp = i2bl(bitsize, cst)

    @property
    def signature(self):
        return Signature(
            [
                Register("cin", QBit()),
                Register("x", QBit(), (self.bitsize,)),
                Register("y", QBit(), (self.bitsize,)),
                Register("z", QBit(), (self.bitsize,)),
                Register("cout", QBit()),
                Register("ancilla", QBit(), (self.bitsize,)),
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
        cin, x[0], y[0], z[0], full_cout[0] = bb.add(
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
        return ConstAdder(self.bitsize, self.cst)

    def pretty_name(self) -> str:
        return f"ConstAdder<{self.cst}>†"
