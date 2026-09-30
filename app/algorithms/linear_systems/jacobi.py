import numpy as np

from  models.algorithm_result import AlgorithmResult
from  utils.formatting import format_number as fmt

DIAGONAL_TOLERANCE = 1e-12
DIVERGENCE_LIMIT = 1e15


def is_diagonally_dominant(matrix: np.ndarray) -> bool:
    size = matrix.shape[0]
    for i in range(size):
        off_diagonal = sum(abs(matrix[i, j]) for j in range(size) if j != i)
        if abs(matrix[i, i]) <= off_diagonal:
            return False
    return True


def jacobi(
    matrix: np.ndarray,
    vector: np.ndarray,
    initial: np.ndarray,
    tolerance: float,
    max_iterations: int,
) -> AlgorithmResult:
    size = vector.shape[0]
    columns = ["Iteration"] + [f"x{i + 1}" for i in range(size)] + ["Error"]
    rows: list[list[float | None]] = [[0] + [float(v) for v in initial] + [None]]
    steps: list[str] = []
    warnings: list[str] = []

    def failure(message: str, **fields) -> AlgorithmResult:
        return AlgorithmResult.failure(
            message,
            steps=steps,
            table_columns=columns,
            table_rows=rows,
            iteration_count=len(rows) - 1,
            warnings=warnings,
            **fields,
        )

    if any(abs(matrix[i, i]) < DIAGONAL_TOLERANCE for i in range(size)):
        steps.append("يوجد عنصر يساوي صفرًا على القطر الرئيسي ← لا يمكن القسمة عليه في صيغة جاكوبي")
        return AlgorithmResult.failure(
            "يوجد عنصر صفري على القطر الرئيسي، ولا يمكن تطبيق طريقة جاكوبي. "
            "حاول إعادة ترتيب المعادلات بحيث تصبح عناصر القطر غير صفرية.",
            steps=steps,
        )

    if not is_diagonally_dominant(matrix):
        warnings.append(
            "المصفوفة ليست مهيمنة قطريًا بشكل صارم (Strictly Diagonally Dominant)، "
            "لذلك قد لا تتقارب طريقة جاكوبي، حتى لو كان للنظام حل."
        )

    formulas = ["صيغة جاكوبي: xi(k+1) = (bi - Σ aij·xj(k)) / aii ، حيث j ≠ i"]
    for i in range(size):
        terms = " - ".join(f"({fmt(matrix[i, j])})·x{j + 1}" for j in range(size) if j != i)
        expression = f"{fmt(vector[i])} - {terms}" if terms else fmt(vector[i])
        formulas.append(f"x{i + 1} = ({expression}) / {fmt(matrix[i, i])}")
    steps.append("\n".join(formulas))
    steps.append("X(0) = [" + ", ".join(fmt(v) for v in initial) + "]")

    current = np.array(initial, dtype=float)
    error = float("inf")
    converged = False
    for iteration in range(1, max_iterations + 1):
        updated = np.zeros(size)
        for i in range(size):
            total = 0.0
            for j in range(size):
                if j != i:
                    total += matrix[i, j] * current[j]
            updated[i] = (vector[i] - total) / matrix[i, i]
        error = float(np.max(np.abs(updated - current)))
        rows.append([iteration] + [float(v) for v in updated] + [error])
        steps.append(
            f"التكرار {iteration}: X = [" + ", ".join(fmt(v) for v in updated) + "]\n"
            f"Error = max|X(k) - X(k-1)| = {fmt(error)}"
        )
        current = updated
        if not np.all(np.isfinite(current)) or error > DIVERGENCE_LIMIT:
            return failure(
                "القيم تتباعد ولا تتقارب إلى حل، فطريقة جاكوبي غير مناسبة لهذا النظام بالترتيب الحالي.",
                result=current,
            )
        if error < tolerance:
            converged = True
            break

    if converged:
        return AlgorithmResult(
            success=True,
            result=current,
            error=error,
            iteration_count=len(rows) - 1,
            steps=steps,
            table_columns=columns,
            table_rows=rows,
            warnings=warnings,
        )
    return failure(
        f"لم يحدث تقارب خلال {max_iterations} تكرار (الخطأ الحالي {fmt(error)} "
        f"أكبر من التسامح {fmt(tolerance)}). زد عدد التكرارات أو تحقق من شروط التقارب.",
        result=current,
        error=error,
    )
