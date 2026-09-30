import math
import re

import numpy as np
import sympy as sp
from sympy.parsing.sympy_parser import (
    convert_xor,
    implicit_multiplication_application,
    parse_expr,
    standard_transformations,
)

from  models.errors import EvaluationError, ValidationError
from  utils.formatting import format_number
from  utils.normalization import normalize_text

VARIABLE = sp.Symbol("x", real=True)

ALLOWED_NAMES = {
    "x": VARIABLE,
    "X": VARIABLE,
    "sin": sp.sin,
    "cos": sp.cos,
    "tan": sp.tan,
    "asin": sp.asin,
    "acos": sp.acos,
    "atan": sp.atan,
    "sinh": sp.sinh,
    "cosh": sp.cosh,
    "tanh": sp.tanh,
    "exp": sp.exp,
    "log": sp.log,
    "ln": sp.log,
    "sqrt": sp.sqrt,
    "abs": sp.Abs,
    "pi": sp.pi,
    "e": sp.E,
    "E": sp.E,
}

TRANSFORMATIONS = standard_transformations + (implicit_multiplication_application, convert_xor)
SAFE_PATTERN = re.compile(r"^[0-9A-Za-z_+\-*/^().,\s]+$")
IDENTIFIER_PATTERN = re.compile(r"[A-Za-z_][A-Za-z_0-9]*")
MAX_LENGTH = 200
IMAGINARY_TOLERANCE = 1e-12


class ParsedFunction:
    def __init__(self, expression: sp.Expr, source: str) -> None:
        self.expression = expression
        self.source = source
        self._callable = sp.lambdify(VARIABLE, expression, modules="numpy")

    def __call__(self, value: float) -> float:
        try:
            with np.errstate(all="ignore"):
                raw = self._callable(np.float64(value))
            number = complex(raw)
        except (ArithmeticError, ValueError, TypeError) as error:
            raise EvaluationError(
                f"تعذر حساب الدالة عند x = {format_number(value)}."
            ) from error
        if abs(number.imag) > IMAGINARY_TOLERANCE or not math.isfinite(number.real):
            raise EvaluationError(
                f"الدالة غير معرّفة أو ليست حقيقية عند x = {format_number(value)}."
            )
        return float(number.real)

    def evaluate_array(self, values: np.ndarray) -> np.ndarray:
        try:
            with np.errstate(all="ignore"):
                raw = np.asarray(self._callable(values), dtype=complex)
        except (ArithmeticError, ValueError, TypeError):
            return np.full(values.shape, np.nan)
        raw = np.broadcast_to(raw, values.shape)
        real = np.where(np.abs(raw.imag) < IMAGINARY_TOLERANCE, raw.real, np.nan)
        return np.where(np.isfinite(real), real, np.nan).astype(float)

    def derivative(self) -> "ParsedFunction":
        return ParsedFunction(sp.diff(self.expression, VARIABLE), f"d/dx[{self.source}]")

    def __str__(self) -> str:
        return str(self.expression)


class ExpressionParser:
    def parse(self, text: str) -> ParsedFunction:
        normalized = normalize_text(text)
        if not normalized:
            raise ValidationError("حقل الدالة فارغ، يرجى كتابة f(x) مثل: x**3 - x - 2")
        if len(normalized) > MAX_LENGTH:
            raise ValidationError(f"الدالة طويلة جدًا (الحد الأقصى {MAX_LENGTH} حرفًا).")
        if not SAFE_PATTERN.match(normalized):
            raise ValidationError(
                "تحتوي الدالة على رموز غير مسموح بها. المسموح: الأرقام والمتغير x "
                "والعمليات + - * / ** ^ والأقواس والدوال المعروفة."
            )
        unknown = sorted({name for name in IDENTIFIER_PATTERN.findall(normalized) if name not in ALLOWED_NAMES})
        if unknown:
            raise ValidationError(
                f"رموز أو دوال غير معروفة: {', '.join(unknown)}. المتغير الوحيد المسموح به هو x."
            )
        try:
            expression = parse_expr(
                normalized,
                local_dict=dict(ALLOWED_NAMES),
                transformations=TRANSFORMATIONS,
            )
        except Exception as error:
            raise ValidationError(
                f"صيغة الدالة غير صحيحة: «{text.strip()}». تأكد من الأقواس والعمليات، مثال: sin(x) + x**2"
            ) from error
        if not isinstance(expression, sp.Expr):
            raise ValidationError("التعبير المدخل ليس دالة رياضية صالحة.")
        if expression.free_symbols - {VARIABLE}:
            raise ValidationError("المتغير الوحيد المسموح به في الدالة هو x.")
        if expression.has(sp.zoo, sp.nan, sp.oo, -sp.oo):
            raise ValidationError("الدالة تحتوي على قيمة غير معرّفة (قسمة على صفر أو ما لا نهاية).")
        return ParsedFunction(expression, normalized)
