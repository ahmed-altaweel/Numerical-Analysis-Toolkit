from functools import wraps
from typing import Callable

from  algorithms.integration.trapezoidal import trapezoidal_rule
from  algorithms.interpolation.finite_difference import finite_differences
from  algorithms.interpolation.lagrange import lagrange_interpolation
from  algorithms.linear_systems.cramer import cramers_rule
from  algorithms.linear_systems.gaussian import gaussian_elimination
from  algorithms.linear_systems.jacobi import jacobi
from  algorithms.root_finding.bisection import bisection
from  algorithms.root_finding.newton_raphson import newton_raphson
from  algorithms.root_finding.secant import secant
from  models.algorithm_result import AlgorithmResult
from  models.errors import NumericalError, ValidationError
from  services.expression_parser import ExpressionParser
from  services.validation import (
    parse_float,
    parse_matrix,
    parse_max_iterations,
    parse_points,
    parse_subintervals,
    parse_tolerance,
    parse_vector,
    require_linear_system,
    require_valid_interval,
)

_parser = ExpressionParser()


def safe_run(function: Callable[..., AlgorithmResult]) -> Callable[..., AlgorithmResult]:
    @wraps(function)
    def wrapper(*args, **kwargs) -> AlgorithmResult:
        try:
            return function(*args, **kwargs)
        except NumericalError as error:
            return AlgorithmResult.failure(str(error))
        except ArithmeticError:
            return AlgorithmResult.failure(
                "حدث خطأ حسابي أثناء التنفيذ (قسمة على صفر أو قيم كبيرة جدًا). تحقق من المدخلات."
            )

    return wrapper


@safe_run
def solve_bisection(expression: str, a: str, b: str, tolerance: str, max_iterations: str) -> AlgorithmResult:
    function = _parser.parse(expression)
    lower = parse_float(a, "a")
    upper = parse_float(b, "b")
    require_valid_interval(lower, upper)
    tol = parse_tolerance(tolerance)
    limit = parse_max_iterations(max_iterations)
    result = bisection(function, lower, upper, tol, limit)
    result.extra["function"] = function
    return result


@safe_run
def solve_newton_raphson(expression: str, x0: str, tolerance: str, max_iterations: str) -> AlgorithmResult:
    function = _parser.parse(expression)
    derivative = function.derivative()
    start = parse_float(x0, "x0")
    tol = parse_tolerance(tolerance)
    limit = parse_max_iterations(max_iterations)
    result = newton_raphson(function, derivative, start, tol, limit)
    result.steps.insert(
        0,
        f"الدالة f(x) = {function}\nالمشتقة f'(x) = {derivative} (تم اشتقاقها باستخدام SymPy)",
    )
    result.extra["function"] = function
    return result


@safe_run
def solve_secant(expression: str, x0: str, x1: str, tolerance: str, max_iterations: str) -> AlgorithmResult:
    function = _parser.parse(expression)
    first = parse_float(x0, "x0")
    second = parse_float(x1, "x1")
    if first == second:
        raise ValidationError("يجب أن تكون القيمتان x0 و x1 مختلفتين.")
    tol = parse_tolerance(tolerance)
    limit = parse_max_iterations(max_iterations)
    result = secant(function, first, second, tol, limit)
    result.extra["function"] = function
    return result


@safe_run
def solve_lagrange(rows: list[tuple[str, str]], x_value: str) -> AlgorithmResult:
    points = parse_points(rows)
    target = parse_float(x_value, "X المطلوب")
    return lagrange_interpolation(points, target)


@safe_run
def solve_finite_differences(rows: list[tuple[str, str]]) -> AlgorithmResult:
    points = parse_points(rows)
    ordered = sorted(points)
    result = finite_differences(ordered)
    if ordered != points:
        result.warnings.append("تم ترتيب النقاط تصاعديًا حسب x قبل بناء جدول الفروق.")
    return result


@safe_run
def solve_cramer(matrix_cells: list[list[str]], vector_cells: list[str]) -> AlgorithmResult:
    matrix = parse_matrix(matrix_cells)
    vector = parse_vector(vector_cells, "B")
    require_linear_system(matrix, vector)
    return cramers_rule(matrix, vector)


@safe_run
def solve_gaussian(matrix_cells: list[list[str]], vector_cells: list[str]) -> AlgorithmResult:
    matrix = parse_matrix(matrix_cells)
    vector = parse_vector(vector_cells, "B")
    require_linear_system(matrix, vector)
    return gaussian_elimination(matrix, vector)


@safe_run
def solve_jacobi(
    matrix_cells: list[list[str]],
    vector_cells: list[str],
    initial_cells: list[str],
    tolerance: str,
    max_iterations: str,
) -> AlgorithmResult:
    matrix = parse_matrix(matrix_cells)
    vector = parse_vector(vector_cells, "B")
    initial = parse_vector(initial_cells, "X0")
    require_linear_system(matrix, vector)
    tol = parse_tolerance(tolerance)
    limit = parse_max_iterations(max_iterations)
    return jacobi(matrix, vector, initial, tol, limit)


@safe_run
def solve_trapezoidal(expression: str, a: str, b: str, n: str) -> AlgorithmResult:
    function = _parser.parse(expression)
    lower = parse_float(a, "a")
    upper = parse_float(b, "b")
    require_valid_interval(lower, upper)
    count = parse_subintervals(n)
    result = trapezoidal_rule(function, lower, upper, count)
    result.extra["function"] = function
    return result
