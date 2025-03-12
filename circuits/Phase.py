from qualtran import Bloq, Signature, QBit, Register, BloqBuilder, SoquetT
from qualtran.bloqs.block_encoding import Unitary
import numpy as np


class Phase(Bloq):
    angle: float
    """The phase angle to apply to the target qubit."""

    def __init__(self, angle: float):
        super().__init__()
        self.angle = angle

    @property
    def signature(self):
        return Signature(
            [
                Register("target", QBit()),
            ]
        )

    def build_composite_bloq(
        self,
        bb: BloqBuilder,
        *,
        target: SoquetT,
    ):
        phase_matrix = np.array([[1, 0], [0, np.exp(1j * self.angle)]])
        target = bb.add(Unitary(phase_matrix), target=target)
        return {"target": target}

    def adjoint(self):
        return Phase(-self.angle)
    
    def pretty_name(self):
        return f"Phase({self.angle})"
