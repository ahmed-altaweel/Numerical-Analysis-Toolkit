import numpy as np

from  models.algorithm_result import AlgorithmResult
from  utils.formatting import format_matrix
from  utils.formatting import format_number as fmt
from  utils.linear_algebra import determinant, replace_column

TABLE_COLUMNS = ["Variable", "det(Ai)", "xi"]


def cramers_rule(matrix: np.ndarray, vector: np.ndarray) -> AlgorithmResult:
    size = matrix.shape[0]
    steps: list[str] = [
        "المصفوفة A:\n" + format_matrix(matrix),
        "المتجه B:\n" + format_matrix(vector.reshape(-1, 1)),
        "قاعدة كرامر: xi = det(Ai) / det(A) ، حيث Ai هي A بعد استبدال العمود i بالمتجه B.",
    ]
    det_a = determinant(matrix)
    steps.append(f"حساب المحدد الرئيسي:\ndet(A) = {fmt(det_a)}")

    if det_a == 0.0:
        steps.append("det(A) = 0 ← النظام إما بلا حل أو له عدد لا نهائي من الحلول")
        return AlgorithmResult.failure(
            "محدد المصفوفة det(A) يساوي صفرًا، لذلك لا يمكن تطبيق قاعدة كرامر "
            "(النظام إما لا يملك حلًا أو يملك عددًا لا نهائيًا من الحلول).",
            steps=steps,
            extra={"determinant": 0.0},
        )

    solution = np.zeros(size)
    rows: list[list[float | str]] = []
    determinants: list[float] = []
    for i in range(size):
        modified = replace_column(matrix, i, vector)
        det_i = determinant(modified)
        solution[i] = det_i / det_a
        determinants.append(det_i)
        rows.append([f"x{i + 1}", det_i, solution[i]])
        steps.append(
            f"استبدال العمود {i + 1} من A بالمتجه B:\n"
            f"A{i + 1} =\n{format_matrix(modified)}\n"
            f"det(A{i + 1}) = {fmt(det_i)}\n"
            f"x{i + 1} = det(A{i + 1}) / det(A) = {fmt(det_i)} / {fmt(det_a)} = {fmt(solution[i])}"
        )

    return AlgorithmResult(
        success=True,
        result=solution,
        steps=steps,
        table_columns=TABLE_COLUMNS,
        table_rows=rows,
        extra={"determinant": det_a, "determinants": determinants},
    )
