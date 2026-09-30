from typing import Callable

from  models.algorithm_result import AlgorithmResult
from  utils.formatting import format_number as fmt

TABLE_COLUMNS = ["i", "xi", "f(xi)"]


def composite_trapezoid(function: Callable[[float], float], a: float, b: float, n: int) -> float:
    h = (b - a) / n
    total = function(a) + function(b)
    for i in range(1, n):
        total += 2 * function(a + i * h)
    return h / 2 * total


def trapezoidal_rule(function: Callable[[float], float], a: float, b: float, n: int) -> AlgorithmResult:
    h = (b - a) / n
    nodes = [a + i * h for i in range(n + 1)]
    nodes[-1] = b
    values = [function(x) for x in nodes]
    rows = [[i, nodes[i], values[i]] for i in range(n + 1)]
    interior = sum(values[1:-1])
    integral = h / 2 * (values[0] + 2 * interior + values[-1])
    refined = composite_trapezoid(function, a, b, 2 * n)
    error_estimate = abs(refined - integral) / 3

    steps = [
        f"حساب طول الخطوة:\nh = (b - a) / n = ({fmt(b)} - {fmt(a)}) / {n} = {fmt(h)}",
        "حساب العقد xi = a + i·h وقيم الدالة f(xi) (موضحة في الجدول).",
        "قاعدة أشباه المنحرفات:\nT = (h/2)·[f(x0) + 2·(f(x1) + ... + f(x(n-1))) + f(xn)]",
        f"مجموع القيم الداخلية f(x1) + ... + f(x(n-1)) = {fmt(interior)}",
        f"T = ({fmt(h)}/2)·[{fmt(values[0])} + 2·({fmt(interior)}) + {fmt(values[-1])}] = {fmt(integral)}",
        "تقدير الخطأ بمقارنة T(n) مع T(2n):\n"
        f"T(2n) = {fmt(refined)}\n"
        f"Error ≈ |T(2n) - T(n)| / 3 = {fmt(error_estimate)}",
    ]

    return AlgorithmResult(
        success=True,
        result=integral,
        error=error_estimate,
        steps=steps,
        table_columns=TABLE_COLUMNS,
        table_rows=rows,
        extra={"nodes": nodes, "values": values, "a": a, "b": b, "n": n},
    )
