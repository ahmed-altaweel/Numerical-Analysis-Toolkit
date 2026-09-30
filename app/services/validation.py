import math

import numpy as np

from  models.errors import ValidationError
from  utils.formatting import format_number
from  utils.normalization import normalize_text

MAX_ITERATIONS_LIMIT = 1000
MAX_SUBINTERVALS = 1000


def parse_float(text: str, name: str) -> float:
    cleaned = normalize_text(text)
    if not cleaned:
        raise ValidationError(f"الحقل «{name}» فارغ، يرجى إدخال قيمة.")
    try:
        value = float(cleaned)
    except ValueError as error:
        raise ValidationError(f"القيمة «{text.strip()}» في الحقل «{name}» ليست رقمًا صحيحًا.") from error
    if not math.isfinite(value):
        raise ValidationError(f"القيمة في الحقل «{name}» يجب أن تكون رقمًا منتهيًا.")
    return value


def parse_positive_int(text: str, name: str, maximum: int) -> int:
    cleaned = normalize_text(text)
    if not cleaned:
        raise ValidationError(f"الحقل «{name}» فارغ، يرجى إدخال قيمة.")
    try:
        value = int(cleaned)
    except ValueError as error:
        raise ValidationError(f"الحقل «{name}» يجب أن يكون عددًا صحيحًا موجبًا.") from error
    if value < 1 or value > maximum:
        raise ValidationError(f"الحقل «{name}» يجب أن يكون بين 1 و {maximum}.")
    return value


def parse_tolerance(text: str) -> float:
    value = parse_float(text, "Tolerance")
    if value <= 0:
        raise ValidationError("التسامح (Tolerance) يجب أن يكون رقمًا موجبًا أكبر من صفر، مثل 1e-6.")
    return value


def parse_max_iterations(text: str) -> int:
    return parse_positive_int(text, "Maximum Iterations", MAX_ITERATIONS_LIMIT)


def parse_subintervals(text: str) -> int:
    return parse_positive_int(text, "n", MAX_SUBINTERVALS)


def require_valid_interval(a: float, b: float) -> None:
    if not a < b:
        raise ValidationError(
            f"الفترة غير صالحة: يجب أن تكون a أصغر من b (المدخل: a = {format_number(a)}، b = {format_number(b)})."
        )


def parse_matrix(cells: list[list[str]]) -> np.ndarray:
    if not cells or not cells[0]:
        raise ValidationError("المصفوفة A فارغة.")
    if len({len(row) for row in cells}) != 1:
        raise ValidationError("أبعاد المصفوفة غير صالحة: يجب أن تحتوي كل الصفوف على العدد نفسه من الأعمدة.")
    values = [
        [parse_float(cell, f"A[{i + 1},{j + 1}]") for j, cell in enumerate(row)]
        for i, row in enumerate(cells)
    ]
    return np.array(values, dtype=float)


def parse_vector(cells: list[str], name: str) -> np.ndarray:
    if not cells:
        raise ValidationError(f"المتجه {name} فارغ.")
    return np.array([parse_float(cell, f"{name}[{i + 1}]") for i, cell in enumerate(cells)], dtype=float)


def require_linear_system(matrix: np.ndarray, vector: np.ndarray) -> None:
    rows, columns = matrix.shape
    if rows != columns:
        raise ValidationError(f"المصفوفة A يجب أن تكون مربعة، لكن أبعادها {rows}×{columns}.")
    if vector.shape[0] != rows:
        raise ValidationError(
            f"طول المتجه B ({vector.shape[0]}) لا يطابق عدد صفوف المصفوفة ({rows})."
        )


def parse_points(rows: list[tuple[str, str]]) -> list[tuple[float, float]]:
    points: list[tuple[float, float]] = []
    for index, (x_text, y_text) in enumerate(rows, start=1):
        x_empty = not normalize_text(x_text)
        y_empty = not normalize_text(y_text)
        if x_empty and y_empty:
            continue
        if x_empty or y_empty:
            raise ValidationError(f"الصف {index}: يجب إدخال قيمتي x و y معًا.")
        points.append(
            (parse_float(x_text, f"x (الصف {index})"), parse_float(y_text, f"y (الصف {index})"))
        )
    if len(points) < 2:
        raise ValidationError("يلزم إدخال نقطتين على الأقل.")
    seen: set[float] = set()
    for x, _ in points:
        if x in seen:
            raise ValidationError(f"القيمة x = {format_number(x)} مكررة، ويجب أن تكون قيم x مختلفة.")
        seen.add(x)
    return points
