from  models.algorithm_result import AlgorithmResult
from  utils.formatting import format_number as fmt

SUPERSCRIPTS = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")
CONSTANT_TOLERANCE = 1e-9


def difference_name(order: int) -> str:
    if order == 0:
        return "f(x)"
    if order == 1:
        return "Δf"
    return "Δ" + str(order).translate(SUPERSCRIPTS) + "f"


def finite_differences(points: list[tuple[float, float]]) -> AlgorithmResult:
    xs = [point[0] for point in points]
    columns: list[list[float]] = [[point[1] for point in points]]
    steps: list[str] = ["الفروق الأمامية: Δf(i) = f(i+1) - f(i) ، وكل رتبة جديدة تُحسب من فروق الرتبة السابقة."]
    warnings: list[str] = []
    constant_reported = False

    for order in range(1, len(points)):
        previous = columns[-1]
        current = [previous[i + 1] - previous[i] for i in range(len(previous) - 1)]
        columns.append(current)
        name = difference_name(order)
        lines = [f"حساب فروق الرتبة {order}:"]
        for i, value in enumerate(current):
            lines.append(f"{name}{i} = {fmt(previous[i + 1])} - {fmt(previous[i])} = {fmt(value)}")
        steps.append("\n".join(lines))
        if not constant_reported and len(current) >= 2:
            spread = max(current) - min(current)
            if spread <= CONSTANT_TOLERANCE * max(1.0, max(abs(v) for v in current)):
                constant_reported = True
                steps.append(
                    f"فروق الرتبة {order} ثابتة تقريبًا ← البيانات تنتمي إلى كثير حدود من الدرجة {order}."
                )

    if len(xs) >= 2:
        spacing = xs[1] - xs[0]
        tolerance = 1e-9 * max(1.0, abs(spacing))
        if any(abs((xs[i + 1] - xs[i]) - spacing) > tolerance for i in range(len(xs) - 1)):
            warnings.append(
                "المسافات بين قيم x غير متساوية؛ جدول الفروق الأمامية يُستخدم عادةً مع قيم x متساوية البعد."
            )

    headers = ["x"] + [difference_name(order) for order in range(len(columns))]
    rows: list[list[float | None]] = []
    for i in range(len(points)):
        row: list[float | None] = [xs[i]]
        for column in columns:
            row.append(column[i] if i < len(column) else None)
        rows.append(row)

    return AlgorithmResult(
        success=True,
        steps=steps,
        table_columns=headers,
        table_rows=rows,
        warnings=warnings,
        extra={"columns": columns},
    )
