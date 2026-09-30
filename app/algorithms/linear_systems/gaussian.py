import numpy as np

from  models.algorithm_result import AlgorithmResult
from  utils.formatting import format_matrix
from  utils.formatting import format_number as fmt

RELATIVE_PIVOT_TOLERANCE = 1e-12


def gaussian_elimination(matrix: np.ndarray, vector: np.ndarray) -> AlgorithmResult:
    size = vector.shape[0]
    augmented = np.hstack((np.array(matrix, dtype=float), np.array(vector, dtype=float).reshape(-1, 1)))
    steps: list[str] = ["المصفوفة الموسعة الابتدائية [A | B]:\n" + format_matrix(augmented, True)]
    threshold = RELATIVE_PIVOT_TOLERANCE * max(1.0, float(np.max(np.abs(augmented[:, :size]))))
    swaps = 0

    for k in range(size):
        pivot_row = k + int(np.argmax(np.abs(augmented[k:, k])))
        pivot_value = augmented[pivot_row, k]
        if abs(pivot_value) < threshold:
            steps.append(f"العمود {k + 1}: كل العناصر تحت القطر تساوي صفرًا ← عنصر محوري صفري (Zero Pivot)")
            return AlgorithmResult.failure(
                "المصفوفة منفردة (Singular): وُجد عنصر محوري يساوي صفرًا ولا يمكن تبديل الصفوف لتفاديه، "
                "لذلك لا يوجد حل وحيد للنظام.",
                steps=steps,
            )
        if pivot_row != k:
            augmented[[k, pivot_row]] = augmented[[pivot_row, k]]
            swaps += 1
            steps.append(
                f"اختيار العنصر المحوري (Partial Pivoting) في العمود {k + 1}: "
                f"الأكبر بالقيمة المطلقة في الصف {pivot_row + 1} ← تبديل الصفين:\n"
                f"R{k + 1} ↔ R{pivot_row + 1}\n" + format_matrix(augmented, True)
            )
        for i in range(k + 1, size):
            factor = augmented[i, k] / augmented[k, k]
            if factor == 0:
                continue
            augmented[i, k:] = augmented[i, k:] - factor * augmented[k, k:]
            augmented[i, k] = 0.0
            steps.append(
                f"R{i + 1} = R{i + 1} - ({fmt(factor)})·R{k + 1}\n" + format_matrix(augmented, True)
            )

    steps.append("المصفوفة المثلثية العليا:\n" + format_matrix(augmented, True))
    steps.append("التعويض الخلفي (Back Substitution):")

    solution = np.zeros(size)
    for i in range(size - 1, -1, -1):
        rhs = augmented[i, size]
        terms = " + ".join(
            f"{fmt(augmented[i, j])}·({fmt(solution[j])})" for j in range(i + 1, size)
        )
        known = sum(augmented[i, j] * solution[j] for j in range(i + 1, size))
        solution[i] = (rhs - known) / augmented[i, i]
        numerator = f"{fmt(rhs)} - ({terms})" if terms else fmt(rhs)
        steps.append(f"x{i + 1} = ({numerator}) / {fmt(augmented[i, i])} = {fmt(solution[i])}")

    return AlgorithmResult(
        success=True,
        result=solution,
        steps=steps,
        extra={"triangular": augmented, "row_swaps": swaps},
    )
