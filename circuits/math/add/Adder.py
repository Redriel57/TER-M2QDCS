from qualtran.bloqs.basic_gates import CNOT, Toffoli
from qualtran import Bloq, Signature, QBit, Register, BloqBuilder, Soquet


class Adder(Bloq):
    """
    Single qubit adder with carry in

    Needed qubits
    -------------
    - cin: 1 qubit
    - x: 1 qubit
    - y: 1 qubit
    - z: 1 qubit
    - cout: 1 qubit
    """
    
    @property
    def signature(self):
        return Signature(
            [
                Register("cin", QBit()),
                Register("x", QBit()),
                Register("y", QBit()),
                Register("z", QBit()),
                Register("cout", QBit()),
            ]
        )

    def build_composite_bloq(
        self,
        bb: BloqBuilder,
        *,
        cin: Soquet,
        x: Soquet,
        y: Soquet,
        z: Soquet,
        cout: Soquet
    ):
        cin, z = bb.add(CNOT(), ctrl=cin, target=z)
        x, z = bb.add(CNOT(), ctrl=x, target=z)
        y, z = bb.add(CNOT(), ctrl=y, target=z)

        [cin, x], cout = bb.add(Toffoli(), ctrl=[cin, x], target=cout)
        [x, y], cout = bb.add(Toffoli(), ctrl=[x, y], target=cout)
        [cin, y], cout = bb.add(Toffoli(), ctrl=[cin, y], target=cout)
        return {"cin": cin, "x": x, "y": y, "z": z, "cout": cout}

    def adjoint(self):
        return AdderAdj()

class AdderAdj(Bloq):
    @property
    def signature(self):
        return Signature(
            [
                Register("cin", QBit()),
                Register("x", QBit()),
                Register("y", QBit()),
                Register("z", QBit()),
                Register("cout", QBit()),
            ]
        )

    def build_composite_bloq(
        self,
        bb: BloqBuilder,
        *,
        cin: Soquet,
        x: Soquet,
        y: Soquet,
        z: Soquet,
        cout: Soquet
    ):
        [cin, x], cout = bb.add(Toffoli(), ctrl=[cin, x], target=cout)
        [x, y], cout = bb.add(Toffoli(), ctrl=[x, y], target=cout)
        [cin, y], cout = bb.add(Toffoli(), ctrl=[cin, y], target=cout)
        
        y, z = bb.add(CNOT(), ctrl=y, target=z)
        x, z = bb.add(CNOT(), ctrl=x, target=z)
        cin, z = bb.add(CNOT(), ctrl=cin, target=z)

        return {"cin": cin, "x": x, "y": y, "z": z, "cout": cout}

    def adjoint(self):
        return Adder()

    def pretty_name(self) -> str:
        return 'Adder†'

