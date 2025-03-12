from qualtran import Bloq, Signature, QBit, Register, BloqBuilder, Soquet


class HHL(Bloq):
    qpe: Bloq
    oracle: Bloq

    def __init__(self, qpe: Bloq, oracle: Bloq):
        super().__init__()
        self.qpe = qpe
        self.oracle = oracle

    @property
    def signature(self):
        return Signature(
            [
                Register("b", QBit()),
                Register("x", QBit()),
                Register("eigenvalue_register", QBit(self.qpe.precision)),
                Register("auxiliary", QBit()),
            ]
        )

    def build_composite_bloq(
        self,
        bb: BloqBuilder,
        *,
        b: Soquet,
        x: Soquet,
        eigenvalue_register: Soquet,
        auxiliary: Soquet
    ):

        return {
            "b": b,
            "x": x,
            "eigenvalue_register": eigenvalue_register,
            "auxiliary": auxiliary,
        }

    def adjoint(self):
        # TODO
        return HHL(self.qpe.adjoint(), self.oracle.adjoint())
