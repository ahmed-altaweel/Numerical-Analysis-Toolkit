import math
from typing import Callable

from  models.algorithm_result import AlgorithmResult
from  models.errors import EvaluationError
from  utils.formatting import format_number as fmt

TABLE_COLUMNS = ["Iteration", "x0", "x1", "x2", "f(x2)", "Error"]
DENOMINATOR_TOLERANCE = 1e-14
DIVERGENCE_LIMIT = 1e12


def secant(
    function: Callable[[float], float],
    x0: float,
    x1: float,
    tolerance: float,
    max_iterations: int,
) -> AlgorithmResult:
    steps: list[str] = []
    rows: list[list[float]] = []
    path: list[float] = [x0, x1]
    extra: dict = {"path": path}

    def failure(message: str, **fields) -> AlgorithmResult:
        return AlgorithmResult.failure(
            message,
            steps=steps,
            table_columns=TABLE_COLUMNS,
            table_rows=rows,
            iteration_count=len(rows),
            extra=extra,
            **fields,
        )

    error = float("inf")
    converged = False
    latest = x1
    try:
        f0 = function(x0)
        f1 = function(x1)
        steps.append(
            "حساب قيمة الدالة عند نقطتي البداية:\n"
            f"f(x0) = {fmt(f0)}\n"
            f"f(x1) = {fmt(f1)}"
        )
        for iteration in range(1, max_iterations + 1):
            denominator = f1 - f0
            if abs(denominator) < DENOMINATOR_TOLERANCE:
                steps.append(
                    f"التكرار {iteration}: f(x1) - f(x0) = {fmt(denominator)} ≈ 0 ← المقام يقترب من الصفر"
                )
                return failure(
                    "المقام f(x1) - f(x0) يساوي صفرًا أو قريب جدًا منه، "
                    "فلا يمكن حساب النقطة التالية. جرّب قيمتين ابتدائيتين مختلفتين."
                )
            x2 = x1 - f1 * (x1 - x0) / denominator
            f2 = function(x2)
            error = abs(x2 - x1)
            rows.append([iteration, x0, x1, x2, f2, error])
            steps.append(
                f"التكرار {iteration}: x2 = x1 - f(x1)·(x1 - x0) / (f(x1) - f(x0))\n"
                f"x2 = {fmt(x1)} - ({fmt(f1)})·({fmt(x1)} - {fmt(x0)}) / ({fmt(f1)} - ({fmt(f0)})) = {fmt(x2)}\n"
                f"f(x2) = {fmt(f2)} ، Error = |x2 - x1| = {fmt(error)}"
            )
            path.append(x2)
            latest = x2
            if not math.isfinite(x2) or abs(x2) > DIVERGENCE_LIMIT:
                return failure(
                    "القيم تتباعد بسرعة ولا تتقارب إلى جذر. جرّب قيمتين ابتدائيتين أقرب إلى الجذر.",
                    result=x2,
                )
            if error < tolerance or f2 == 0:
                converged = True
                break
            x0, f0 = x1, f1
            x1, f1 = x2, f2
    except EvaluationError as exc:
        return failure(str(exc))

    if converged:
        return AlgorithmResult(
            success=True,
            result=latest,
            error=error,
            iteration_count=len(rows),
            steps=steps,
            table_columns=TABLE_COLUMNS,
            table_rows=rows,
            extra=extra,
        )
    return failure(
        f"لم يحدث تقارب خلال {max_iterations} تكرار (الخطأ الحالي {fmt(error)} "
        f"أكبر من التسامح {fmt(tolerance)}). جرّب قيمتين ابتدائيتين مختلفتين أو زد عدد التكرارات.",
        result=latest,
        error=error,
    )
