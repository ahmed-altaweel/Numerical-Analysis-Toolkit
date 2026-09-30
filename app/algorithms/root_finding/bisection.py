from typing import Callable

from  models.algorithm_result import AlgorithmResult
from  models.errors import EvaluationError
from  utils.formatting import format_number as fmt

TABLE_COLUMNS = ["Iteration", "a", "b", "c", "f(c)", "Error"]


def bisection(
    function: Callable[[float], float],
    a: float,
    b: float,
    tolerance: float,
    max_iterations: int,
) -> AlgorithmResult:
    steps: list[str] = []
    rows: list[list[float]] = []
    extra: dict = {"interval": (a, b)}

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

    current = a
    error = abs(b - a)
    converged = False
    final_error = error
    try:
        fa = function(a)
        fb = function(b)
        steps.append(
            "حساب قيمة الدالة عند طرفي الفترة:\n"
            f"f(a) = f({fmt(a)}) = {fmt(fa)}\n"
            f"f(b) = f({fmt(b)}) = {fmt(fb)}"
        )
        if fa * fb >= 0:
            steps.append(f"f(a)·f(b) = {fmt(fa * fb)} ≥ 0 ← لا يوجد تغيّر مؤكد في الإشارة")
            return failure(
                f"شرط البداية f(a)·f(b) < 0 غير متحقق (الناتج {fmt(fa * fb)}). "
                "اختر فترة [a, b] تتغير عندها إشارة الدالة حتى يُضمن وجود جذر بداخلها."
            )
        steps.append(f"f(a)·f(b) = {fmt(fa * fb)} < 0 ← الشرط متحقق، يوجد جذر داخل الفترة")
        for iteration in range(1, max_iterations + 1):
            c = (a + b) / 2
            fc = function(c)
            error = (b - a) / 2
            rows.append([iteration, a, b, c, fc, error])
            current = c
            steps.append(
                f"التكرار {iteration}: c = (a + b) / 2 = ({fmt(a)} + {fmt(b)}) / 2 = {fmt(c)}\n"
                f"f(c) = {fmt(fc)}"
            )
            if fc == 0 or error < tolerance:
                converged = True
                final_error = 0.0 if fc == 0 else error
                steps.append(
                    f"Error = (b - a) / 2 = {fmt(error)} < Tolerance = {fmt(tolerance)} ← توقف"
                    if fc != 0
                    else "f(c) = 0 ← تم الوصول إلى الجذر بدقة"
                )
                break
            if fa * fc < 0:
                b, fb = c, fc
                steps.append("f(a)·f(c) < 0 ← الجذر في [a, c] ⇒ b = c")
            else:
                a, fa = c, fc
                steps.append("f(a)·f(c) > 0 ← الجذر في [c, b] ⇒ a = c")
    except EvaluationError as exc:
        return failure(str(exc))

    if converged:
        return AlgorithmResult(
            success=True,
            result=current,
            error=final_error,
            iteration_count=len(rows),
            steps=steps,
            table_columns=TABLE_COLUMNS,
            table_rows=rows,
            extra=extra,
        )
    return failure(
        f"لم يحدث تقارب خلال {max_iterations} تكرار (الخطأ الحالي {fmt(error)} "
        f"أكبر من التسامح {fmt(tolerance)}). زد عدد التكرارات أو خفّف التسامح.",
        result=current,
        error=error,
    )
