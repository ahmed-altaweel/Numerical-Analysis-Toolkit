import math
from typing import Any, Sequence


def format_number(value: Any, digits: int = 8) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, bool):
        return str(value)
    number = float(value)
    if math.isnan(number):
        return "NaN"
    if math.isinf(number):
        return "∞" if number > 0 else "-∞"
    if number == 0:
        return "0"
    if number == int(number) and abs(number) < 1e12:
        return str(int(number))
    return f"{number:.{digits}g}"


def format_matrix(rows: Sequence[Sequence[float]], augmented: bool = False) -> str:
    cells = [[format_number(value, 6) for value in row] for row in rows]
    width = max(len(cell) for row in cells for cell in row)
    lines = []
    for row in cells:
        parts = [cell.rjust(width) for cell in row]
        if augmented:
            body = "  ".join(parts[:-1]) + "  |  " + parts[-1]
        else:
            body = "  ".join(parts)
        lines.append(f"[ {body} ]")
    return "\n".join(lines)


def starts_with_arabic(text: str) -> bool:
    stripped = text.lstrip()
    return bool(stripped) and "\u0600" <= stripped[0] <= "\u06ff"
