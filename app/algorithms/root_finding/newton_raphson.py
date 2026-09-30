import math
from typing import Callable

from  models.algorithm_result import AlgorithmResult
from  models.errors import EvaluationError
from  utils.formatting import format_number as fmt

TABLE_COLUMNS = ["Iteration", "x", "f(x)", "f'(x)", "Error"]
DERIVATIVE_TOLERANCE = 1e-12
DIVERGENCE_LIMIT = 1e12


def newton_raphson(
    function: Callable[[float], float],
    derivative: Callable[[float], float],
    x0: float,
    tolerance: float,
    max_iterations: int,
) -> AlgorithmResult:
    steps: list[str] = []
    rows: list[list[float]] = []
    path: list[float] = [x0]
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

    x = x0
    error = float("inf")
    converged = False
    try:
        for iteration in range(1, max_iterations + 1):
            fx = function(x)
            dfx = derivative(x)
            if abs(dfx) < DERIVATIVE_TOLERANCE:
                steps.append(
                    f"التكرار {iteration}: f'({fmt(x)}) = {fmt(dfx)} ≈ 0 ← لا يمكن القسمة على المشتقة"
                )
                return failure(
                    f"المشتقة f'(x) تساوي صفرًا أو قريبة جدًا منه عند x = {fmt(x)}، "
                    "لذلك لا يمكن إكمال طريقة نيوتن-رابسون. جرّب قيمة ابتدائية x0 مختلفة."
                )
            next_x = x - fx / dfx
            error = abs(next_x - x)
            rows.append([iteration, x, fx, dfx, error])
            steps.append(
                f"التكرار {iteration}: x{iteration} = x{iteration - 1} - f(x)/f'(x) = "
                f"{fmt(x)} - ({fmt(fx)})/({fmt(dfx)}) = {fmt(next_x)}\n"
                f"Error = |x{iteration} - x{iteration - 1}| = {fmt(error)}"
            )
            path.append(next_x)
            x = next_x
            if not math.isfinite(x) or abs(x) > DIVERGENCE_LIMIT:
                return failure(
                    "القيم تتباعد بسرعة ولا تتقارب إلى جذر. جرّب قيمة ابتدائية x0 أقرب إلى الجذر.",
                    result=x,
                )
            if error < tolerance:
                converged = True
                break
    except EvaluationError as exc:
        return failure(str(exc))

    if converged:
        return AlgorithmResult(
            success=True,
            result=x,
            error=error,
            iteration_count=len(rows),
            steps=steps,
            table_columns=TABLE_COLUMNS,
            table_rows=rows,
            extra=extra,
        )
    return failure(
        f"لم يحدث تقارب خلال {max_iterations} تكرار (الخطأ الحالي {fmt(error)} "
        f"أكبر من التسامح {fmt(tolerance)}). جرّب قيمة ابتدائية مختلفة أو زد عدد التكرارات.",
        result=x,
        error=error,
    )
