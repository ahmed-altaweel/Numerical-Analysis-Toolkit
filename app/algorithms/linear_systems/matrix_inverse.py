import numpy as np

from  models.algorithm_result import AlgorithmResult
from  utils.formatting import format_matrix
from  utils.formatting import format_number as fmt
from  utils.linear_algebra import determinant

RELATIVE_PIVOT_TOLERANCE = 1e-12


def matrix_inverse_solve(matrix: np.ndarray, vector: np.ndarray) -> AlgorithmResult:
    """Solve AX = B using the matrix inverse: X = A⁻¹ · B."""
    size = matrix.shape[0]
    a = np.array(matrix, dtype=float)
    b = np.array(vector, dtype=float)

    steps: list[str] = [
        "المصفوفة A:\n" + format_matrix(a),
        "المتجه B:\n" + format_matrix(b.reshape(-1, 1)),
        "الطريقة: حل النظام AX = B باستخدام معكوس المصفوفة:\nX = A⁻¹ · B",
    ]

    # --- determinant check ---
    det_a = determinant(a)
    steps.append(f"حساب المحدد:\ndet(A) = {fmt(det_a)}")

    if det_a == 0.0:
        steps.append("det(A) = 0 ← المصفوفة منفردة ولا يوجد معكوس")
        return AlgorithmResult.failure(
            "محدد المصفوفة det(A) يساوي صفرًا، لذلك لا يمكن حساب المعكوس "
            "(النظام إما لا يملك حلًا أو يملك عددًا لا نهائيًا من الحلول).",
            steps=steps,
            extra={"determinant": 0.0},
        )

    # --- build augmented [A | I] ---
    identity = np.eye(size)
    augmented = np.hstack((a.copy(), identity))
    steps.append(
        "بناء المصفوفة الموسعة [A | I]:\n" + _format_augmented_inverse(augmented, size)
    )

    # --- forward elimination (to upper triangular) ---
    scale = max(1.0, float(np.max(np.abs(a))))
    threshold = RELATIVE_PIVOT_TOLERANCE * scale

    for k in range(size):
        # partial pivoting
        pivot_row = k + int(np.argmax(np.abs(augmented[k:, k])))
        if abs(augmented[pivot_row, k]) < threshold:
            return AlgorithmResult.failure(
                "المصفوفة منفردة: عنصر محوري يساوي صفرًا.",
                steps=steps,
            )
        if pivot_row != k:
            augmented[[k, pivot_row]] = augmented[[pivot_row, k]]
            steps.append(
                f"تبديل الصفين R{k + 1} ↔ R{pivot_row + 1}:\n"
                + _format_augmented_inverse(augmented, size)
            )

        # scale pivot row to make pivot = 1
        pivot = augmented[k, k]
        if pivot != 1.0:
            augmented[k, :] = augmented[k, :] / pivot
            steps.append(
                f"R{k + 1} = R{k + 1} / {fmt(pivot)}:\n"
                + _format_augmented_inverse(augmented, size)
            )

        # eliminate all other rows
        for i in range(size):
            if i == k:
                continue
            factor = augmented[i, k]
            if factor == 0.0:
                continue
            augmented[i, :] = augmented[i, :] - factor * augmented[k, :]
            augmented[i, k] = 0.0  # clean floating point noise
            steps.append(
                f"R{i + 1} = R{i + 1} - ({fmt(factor)})·R{k + 1}:\n"
                + _format_augmented_inverse(augmented, size)
            )

    # --- extract inverse ---
    inverse = augmented[:, size:]
    steps.append("المعكوس A⁻¹:\n" + format_matrix(inverse))

    # --- compute solution ---
    solution = inverse @ b
    steps.append("حساب الحل X = A⁻¹ · B:")

    terms_lines: list[str] = []
    for i in range(size):
        parts = " + ".join(
            f"{fmt(inverse[i, j])}×{fmt(b[j])}" for j in range(size)
        )
        terms_lines.append(f"x{i + 1} = {parts} = {fmt(solution[i])}")
    steps.append("\n".join(terms_lines))

    # --- table: show inverse matrix rows ---
    table_columns = ["المتغير"] + [f"A⁻¹ صف {i + 1}" for i in range(size)] + ["xi"]
    table_rows: list[list] = []
    for i in range(size):
        row: list = [f"x{i + 1}"]
        for j in range(size):
            row.append(inverse[i, j])
        row.append(solution[i])
        table_rows.append(row)

    return AlgorithmResult(
        success=True,
        result=solution,
        steps=steps,
        table_columns=table_columns,
        table_rows=table_rows,
        extra={"determinant": det_a, "inverse": inverse},
    )


def _format_augmented_inverse(augmented: np.ndarray, size: int) -> str:
    """Format [A | I] style matrix with a divider."""
    cells = [[fmt(v, 6) for v in row] for row in augmented]
    width = max(len(c) for row in cells for c in row)
    lines = []
    for row in cells:
        left = "  ".join(c.rjust(width) for c in row[:size])
        right = "  ".join(c.rjust(width) for c in row[size:])
        lines.append(f"[ {left}  |  {right} ]")
    return "\n".join(lines)
