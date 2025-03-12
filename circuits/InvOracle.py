from qualtran import Bloq, Signature, QBit, Register, BloqBuilder, Soquet
from qualtran.bloqs.basic_gates import Hadamard

class InvOracle(Bloq):
    cond: float
    """Condition number of the matrix."""

    def __init__(self, cond: float):
        super().__init__()
        self.cond = cond

    @property
    def signature(self):
        return Signature(
            [
                Register("eigenvalue_register", QBit()),
                Register("state", QBit()),
                Register("auxiliary", QBit()),
            ]
        )

    def build_composite_bloq(
        self,
        bb: BloqBuilder,
        *,
        eigenvalue_register: Soquet,
        state: Soquet,
        auxiliary: Soquet
    ):
        # Step 1: Controlled rotations on the auxiliary qubit based on eigenvalues
        auxiliary = bb.add(ControlledRotation(), ctrl=eigenvalue_register, target=auxiliary, cond=self.cond)

        # Step 2: Apply conditional operations to invert eigenvalues
        state = bb.add(ControlledScaling(self.cond), ctrl=auxiliary, target=state)

        return {"eigenvalue_register": eigenvalue_register, "state": state, "auxiliary": auxiliary}

    def adjoint(self):
        return InvOracle(self.cond)
