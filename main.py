from qualtran.drawing import ClassicalSimGraphDrawer, show_counts_sigma
from qualtran import BloqBuilder
import numpy as np
from numpy.typing import NDArray
from sympy import Symbol

from circuits.math.add import CarryAdder
from circuits import HHL
from helper import i2bl, is_hermitian, make_hermitian, Matrix


def tests():
    n = 5
    x = 11
    y = 19

    bb = BloqBuilder()
    qubits = {
        "x": bb.add_register("x", n),
        "y": bb.add_register("y", n),
        "z_out": bb.add_register("z_out", n),
        "cout": bb.add_register("cout", 1),
        "ancilla": bb.add_register("ancilla", (n - 1) + n),
    }
    bb.add(CarryAdder(n), x=qubits["x"], y=qubits["y"], z=qubits["z"])

    # ---------------------------------------------

    inputs = {
        "x": i2bl(n, x)[::-1],
        "y": i2bl(n, y)[::-1],
        "z": [0] * n,
        "cout": 0,
        "ancilla": [0] * (n - 1),
    }

    sym_inputs = {
        "x": [Symbol(f"X{i}") for i in range(n)],
        "y": [Symbol(f"Y{i}") for i in range(n)],
        "z": [0] * n,
        "cout": 0,
        "ancilla": [0] * (n - 1),
    }

    bb.finalize().call_classically(**inputs)
    # print(gate.call_classically(**sym_inputs))

    # drawer = ClassicalSimGraphDrawer(gate.decompose_bloq().flatten(), vals=inputs)

    # with open("./graph.txt", "w") as f:
    #     f.write(drawer.get_graph().to_string())
    #     print("Written graph to ./graph.txt\n")


def main():
    N: int = 3
    epsilon: float = 1e-12
    hermitian_thresh: float = 1e-3

    # INITIALIZATION MATRIX A --------------------------------------------------------------
    A: Matrix = np.array([[1, 2 + 1j, 5 - 4j], [2 - 1j, 4, 6j], [7, -6j, 2]])

    # Check if A is Hermitian
    is_A_Hermitian = is_hermitian(A)
    if not is_A_Hermitian:
        # If not, change it so it is
        # Two solutions are possible: A = (A+A.t)/2 if A is close to an Hermitian matrix, or double the matrix size if not.
        hermitian_part = (A + A.conj().T) / 2
        frob_diff = np.linalg.norm(A - hermitian_part, ord="fro")
        frob_A = np.linalg.norm(A, ord="fro")
        if frob_diff / frob_A <= hermitian_thresh:
            print(
                "Given matrix is close enough to being Hermitian: using the (A + AT)/2"
            )
            A = hermitian_part
        else:
            print("Given matrix is not close to being Hermitian: doubling size")
            N *= 2
            A = make_hermitian(A)

    # Check if the matrix has only nonzero eigenvalues
    eigenvalues = np.linalg.eigvalsh(A)
    rank = np.count_nonzero(eigenvalues)
    if rank != N:
        raise ValueError("Cannot apply HHL: The matrix is of invalid rank")

    # INITIALIZATION VECTOR B --------------------------------------------------------------
    B: Matrix = np.array([1, 2, 3])

    # INITIALIZATION PRECISIONS ------------------------------------------------------------
    # p => number of qubits to encode the eigenvalues
    # Should be big enough to distinguish all eigenvalues
    # Let's take p = 1 + log_2(1/(smallest differences in eigenvalues))
    # Added safeguard if two eigenvalues are equal
    sorted_eig = sorted(eigenvalues)
    min_diff = min(
        [
            sorted_eig[i + 1] - sorted_eig[i]
            for i in range(N - 1)
            if sorted_eig[i + 1] - sorted_eig[i] > epsilon
        ],
        default=epsilon,
    )
    p = 1 + np.log2(1 / min_diff)

    # q => number of qubits to encode x
    # q should be proportional to log_2(κ(A))
    # q = log_2(max(sing_A)/min(sing_A))
    # q = log_2(max(|eig_A|)/min(|eig_A|)) as A is Hermitian
    abs_eig = abs(eigenvalues)
    cond_A = max(abs_eig) / min(abs_eig)
    q = np.log2(cond_A)

    # Normalize A using its condition
    A /= cond_A

    # Normalize b using its norm
    # Normalize b
    norm_B = np.linalg.norm(B)
    B /= norm_B

    # Prepare r
    r = np.random.Generator()

    norm_r = np.linalg.norm(r)
    r /= norm_r
    # Run HHL

    # Denormalize


if __name__ == "__main__":
    tests()
