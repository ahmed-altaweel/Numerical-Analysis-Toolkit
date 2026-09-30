from  models.algorithm_result import AlgorithmResult
from  utils.formatting import format_number as fmt

TABLE_COLUMNS = ["i", "xi", "yi", "Li(X)", "yi·Li(X)"]


def lagrange_interpolation(points: list[tuple[float, float]], x_value: float) -> AlgorithmResult:
    steps: list[str] = []
    rows: list[list[float]] = []
    warnings: list[str] = []
    total = 0.0

    steps.append(
        "صيغة لاجرنج:\n"
        "P(X) = Σ yi · Li(X)\n"
        "Li(X) = Π (X - xj) / (xi - xj) ، حيث j ≠ i"
    )
    steps.append(f"حساب دوال لاجرنج الأساسية عند X = {fmt(x_value)}:")

    for i, (xi, yi) in enumerate(points):
        basis = 1.0
        factors = []
        for j, (xj, _) in enumerate(points):
            if i == j:
                continue
            basis *= (x_value - xj) / (xi - xj)
            factors.append(f"({fmt(x_value)} - {fmt(xj)})/({fmt(xi)} - {fmt(xj)})")
        term = yi * basis
        total += term
        rows.append([i, xi, yi, basis, term])
        steps.append(
            f"L{i}(X) = {' · '.join(factors)} = {fmt(basis)}\n"
            f"y{i}·L{i}(X) = {fmt(yi)} × {fmt(basis)} = {fmt(term)}"
        )

    steps.append(
        "P(X) = " + " + ".join(f"({fmt(row[4])})" for row in rows) + f" = {fmt(total)}"
    )

    lowest = min(x for x, _ in points)
    highest = max(x for x, _ in points)
    if x_value < lowest or x_value > highest:
        warnings.append(
            "قيمة X تقع خارج مدى نقاط الإدخال، فالنتيجة استقراء خارجي (Extrapolation) وقد تكون أقل دقة."
        )

    return AlgorithmResult(
        success=True,
        result=total,
        steps=steps,
        table_columns=TABLE_COLUMNS,
        table_rows=rows,
        warnings=warnings,
        extra={"points": points, "x_value": x_value},
    )
