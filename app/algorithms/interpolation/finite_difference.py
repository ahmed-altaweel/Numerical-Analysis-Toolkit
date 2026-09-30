import math

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


def backward_difference_name(order: int) -> str:
    if order == 0:
        return "f(x)"
    if order == 1:
        return "∇f"
    return "∇" + str(order).translate(SUPERSCRIPTS) + "f"


def central_difference_name(order: int) -> str:
    if order == 0:
        return "f(x)"
    if order == 1:
        return "δf"
    return "δ" + str(order).translate(SUPERSCRIPTS) + "f"


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


def newton_forward(points: list[tuple[float, float]], x_value: float) -> AlgorithmResult:
    """Newton Forward Difference Interpolation.

    Uses the difference table (first row deltas) plus the formula:
        P(x) = f₀ + C(s,1)·Δf₀ + C(s,2)·Δ²f₀ + …
    where  s = (x - x₀) / h  and  h = x₁ - x₀.
    """
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    n = len(points)
    warnings: list[str] = []

    # --- check equal spacing ---
    h = xs[1] - xs[0]
    tol = 1e-9 * max(1.0, abs(h))
    if any(abs((xs[i + 1] - xs[i]) - h) > tol for i in range(n - 1)):
        warnings.append(
            "المسافات بين قيم x غير متساوية؛ صيغة نيوتن الأمامية تتطلب قيم x متساوية البعد."
        )

    # --- build difference columns ---
    columns: list[list[float]] = [ys[:]]
    for order in range(1, n):
        prev = columns[-1]
        columns.append([prev[i + 1] - prev[i] for i in range(len(prev) - 1)])

    # --- compute s ---
    s = (x_value - xs[0]) / h

    # --- interpolation ---
    steps: list[str] = []
    steps.append(
        "صيغة نيوتن الأمامية للاستيفاء:\n"
        "P(x) = f₀ + C(s,1)·Δf₀ + C(s,2)·Δ²f₀ + …\n"
        "حيث s = (x − x₀) / h"
    )
    steps.append(f"h = {fmt(xs[1])} − {fmt(xs[0])} = {fmt(h)}")
    steps.append(f"s = ({fmt(x_value)} − {fmt(xs[0])}) / {fmt(h)} = {fmt(s)}")

    result_value = ys[0]
    binom = 1.0  # C(s, k) built incrementally
    term_parts: list[str] = [fmt(ys[0])]

    for k in range(1, n):
        if not columns[k]:
            break
        delta = columns[k][0]
        binom *= (s - (k - 1)) / k
        term = binom * delta
        result_value += term

        # pretty s-product
        s_factors = " · ".join(f"(s−{j})" if j > 0 else "s" for j in range(k))
        steps.append(
            f"الحد {k}: C(s,{k}) · {difference_name(k)}₀\n"
            f"  C(s,{k}) = {s_factors} / {k}! = {fmt(binom)}\n"
            f"  {difference_name(k)}₀ = {fmt(delta)}\n"
            f"  الحد = {fmt(binom)} × {fmt(delta)} = {fmt(term)}"
        )
        term_parts.append(f"({fmt(term)})")

    steps.append(f"P({fmt(x_value)}) = {' + '.join(term_parts)} = {fmt(result_value)}")

    # --- extrapolation warning ---
    if x_value < xs[0] or x_value > xs[-1]:
        warnings.append(
            "قيمة X تقع خارج مدى نقاط الإدخال، فالنتيجة استقراء خارجي (Extrapolation) وقد تكون أقل دقة."
        )

    # --- build table rows (same difference table) ---
    headers = ["x"] + [difference_name(order) for order in range(len(columns))]
    rows: list[list[float | None]] = []
    for i in range(n):
        row: list[float | None] = [xs[i]]
        for col in columns:
            row.append(col[i] if i < len(col) else None)
        rows.append(row)

    return AlgorithmResult(
        success=True,
        result=result_value,
        steps=steps,
        table_columns=headers,
        table_rows=rows,
        warnings=warnings,
    )


def newton_backward(points: list[tuple[float, float]], x_value: float) -> AlgorithmResult:
    """Newton Backward Difference Interpolation.

    Uses the last row deltas of the difference table:
        P(x) = fₙ + C(s,1)·∇fₙ + C(s,2)·∇²fₙ + …
    where  s = (x − xₙ) / h.
    """
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    n = len(points)
    warnings: list[str] = []

    # --- check equal spacing ---
    h = xs[1] - xs[0]
    tol = 1e-9 * max(1.0, abs(h))
    if any(abs((xs[i + 1] - xs[i]) - h) > tol for i in range(n - 1)):
        warnings.append(
            "المسافات بين قيم x غير متساوية؛ صيغة نيوتن الخلفية تتطلب قيم x متساوية البعد."
        )

    # --- build forward difference columns (same table, read from bottom) ---
    columns: list[list[float]] = [ys[:]]
    for order in range(1, n):
        prev = columns[-1]
        columns.append([prev[i + 1] - prev[i] for i in range(len(prev) - 1)])

    # --- s is measured from the last point ---
    s = (x_value - xs[-1]) / h

    # --- interpolation ---
    steps: list[str] = []
    steps.append(
        "صيغة نيوتن الخلفية للاستيفاء:\n"
        "P(x) = fₙ + C(s,1)·∇fₙ + C(s,2)·∇²fₙ + …\n"
        "حيث s = (x − xₙ) / h"
    )
    steps.append(f"h = {fmt(xs[1])} − {fmt(xs[0])} = {fmt(h)}")
    steps.append(f"s = ({fmt(x_value)} − {fmt(xs[-1])}) / {fmt(h)} = {fmt(s)}")

    result_value = ys[-1]
    binom = 1.0
    term_parts: list[str] = [fmt(ys[-1])]

    for k in range(1, n):
        if not columns[k]:
            break
        # last element of each column
        delta = columns[k][-1]
        binom *= (s + (k - 1)) / k
        term = binom * delta
        result_value += term

        s_factors = " · ".join(f"(s+{j})" if j > 0 else "s" for j in range(k))
        steps.append(
            f"الحد {k}: C(s,{k}) · {backward_difference_name(k)}ₙ\n"
            f"  C(s,{k}) = {s_factors} / {k}! = {fmt(binom)}\n"
            f"  {backward_difference_name(k)}ₙ = {fmt(delta)}\n"
            f"  الحد = {fmt(binom)} × {fmt(delta)} = {fmt(term)}"
        )
        term_parts.append(f"({fmt(term)})")

    steps.append(f"P({fmt(x_value)}) = {' + '.join(term_parts)} = {fmt(result_value)}")

    # --- extrapolation warning ---
    if x_value < xs[0] or x_value > xs[-1]:
        warnings.append(
            "قيمة X تقع خارج مدى نقاط الإدخال، فالنتيجة استقراء خارجي (Extrapolation) وقد تكون أقل دقة."
        )

    # --- table ---
    headers = ["x"] + [backward_difference_name(order) for order in range(len(columns))]
    rows: list[list[float | None]] = []
    for i in range(n):
        row: list[float | None] = [xs[i]]
        for col in columns:
            row.append(col[i] if i < len(col) else None)
        rows.append(row)

    return AlgorithmResult(
        success=True,
        result=result_value,
        steps=steps,
        table_columns=headers,
        table_rows=rows,
        warnings=warnings,
    )


def newton_central(points: list[tuple[float, float]], x_value: float) -> AlgorithmResult:
    """Stirling's Central Difference Interpolation (averaging forward and backward).

    Uses the central point as origin. When n is odd the middle index is n//2,
    when n is even we pick n//2 as the base index closest to x_value.
    """
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    n = len(points)
    warnings: list[str] = []

    if n < 3:
        return AlgorithmResult.failure(
            "صيغة الفروق المركزية تتطلب 3 نقاط على الأقل.",
        )

    # --- check equal spacing ---
    h = xs[1] - xs[0]
    tol = 1e-9 * max(1.0, abs(h))
    if any(abs((xs[i + 1] - xs[i]) - h) > tol for i in range(n - 1)):
        warnings.append(
            "المسافات بين قيم x غير متساوية؛ صيغة الفروق المركزية تتطلب قيم x متساوية البعد."
        )

    # --- build forward difference columns ---
    columns: list[list[float]] = [ys[:]]
    for order in range(1, n):
        prev = columns[-1]
        columns.append([prev[i + 1] - prev[i] for i in range(len(prev) - 1)])

    # --- pick central index ---
    mid = n // 2
    x0 = xs[mid]
    s = (x_value - x0) / h

    steps: list[str] = []
    steps.append(
        "صيغة ستيرلنغ للفروق المركزية:\n"
        "P(x) = f₀ + s·μδf₀ + s²/2!·δ²f₀ + s(s²−1)/3!·μδ³f₀ + …\n"
        "حيث μδᵏf₀ = (δᵏf₋½ + δᵏf₊½)/2 للرتب الفردية\n"
        "و s = (x − x₀) / h"
    )
    steps.append(f"النقطة المركزية: x₀ = {fmt(x0)} (الفهرس {mid})")
    steps.append(f"h = {fmt(h)}")
    steps.append(f"s = ({fmt(x_value)} − {fmt(x0)}) / {fmt(h)} = {fmt(s)}")

    result_value = ys[mid]
    term_parts: list[str] = [fmt(ys[mid])]

    # Stirling's formula mixes odd/even orders:
    # Even order k:  coefficient = s(s²-1)(s²-4)…(s²-(k/2-1)²) / k!  × δᵏf₀
    #   where δᵏf₀ = columns[k][mid - k//2]
    # Odd order k:   coefficient = same product / k!  × μδᵏf₀
    #   where μδᵏf₀ = (columns[k][mid - (k+1)//2] + columns[k][mid - (k-1)//2]) / 2

    max_order = n - 1
    coeff = 1.0  # accumulated product term

    for k in range(1, max_order + 1):
        if not columns[k]:
            break

        if k % 2 == 1:  # odd order
            idx_lower = mid - (k + 1) // 2
            idx_upper = mid - (k - 1) // 2
            if idx_lower < 0 or idx_upper >= len(columns[k]):
                break
            delta_avg = (columns[k][idx_lower] + columns[k][idx_upper]) / 2.0

            if k == 1:
                coeff_k = s
            else:
                # multiply by (s² - ((k-1)//2)²) then divide by k*(k-1)
                half = (k - 1) // 2
                coeff = coeff * (s * s - half * half) / (k * (k - 1))
                coeff_k = coeff * s

            term = coeff_k * delta_avg
            result_value += term

            steps.append(
                f"الحد {k} (رتبة فردية):\n"
                f"  μ{central_difference_name(k)}₀ = ({fmt(columns[k][idx_lower])} + {fmt(columns[k][idx_upper])}) / 2 = {fmt(delta_avg)}\n"
                f"  المعامل = {fmt(coeff_k)}\n"
                f"  الحد = {fmt(coeff_k)} × {fmt(delta_avg)} = {fmt(term)}"
            )
            term_parts.append(f"({fmt(term)})")

        else:  # even order
            idx = mid - k // 2
            if idx < 0 or idx >= len(columns[k]):
                break
            delta = columns[k][idx]

            half = k // 2 - 1
            if k == 2:
                coeff = s * s / 2.0
            else:
                coeff = coeff * (s * s - half * half) / (k * (k - 1))

            term = coeff * delta
            result_value += term

            steps.append(
                f"الحد {k} (رتبة زوجية):\n"
                f"  {central_difference_name(k)}₀ = {fmt(delta)}\n"
                f"  المعامل = {fmt(coeff)}\n"
                f"  الحد = {fmt(coeff)} × {fmt(delta)} = {fmt(term)}"
            )
            term_parts.append(f"({fmt(term)})")

    steps.append(f"P({fmt(x_value)}) = {' + '.join(term_parts)} = {fmt(result_value)}")

    if x_value < xs[0] or x_value > xs[-1]:
        warnings.append(
            "قيمة X تقع خارج مدى نقاط الإدخال، فالنتيجة استقراء خارجي (Extrapolation) وقد تكون أقل دقة."
        )

    # --- table ---
    headers = ["x"] + [central_difference_name(order) for order in range(len(columns))]
    rows_out: list[list[float | None]] = []
    for i in range(n):
        row: list[float | None] = [xs[i]]
        for col in columns:
            row.append(col[i] if i < len(col) else None)
        rows_out.append(row)

    return AlgorithmResult(
        success=True,
        result=result_value,
        steps=steps,
        table_columns=headers,
        table_rows=rows_out,
        warnings=warnings,
    )

