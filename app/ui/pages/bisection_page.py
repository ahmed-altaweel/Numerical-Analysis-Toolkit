from  models.algorithm_result import AlgorithmResult
from  services.solver_service import solve_bisection
from  ui.components.algorithm_page import AlgorithmPage
from  ui.components.input_field import InputField


class BisectionPage(AlgorithmPage):
    title = "طريقة التنصيف (Bisection Method)"
    description = (
        "تبحث عن جذر الدالة f(x) داخل فترة [a, b] بتنصيفها مرارًا، "
        "مع الاحتفاظ في كل مرة بالنصف الذي تتغير فيه إشارة الدالة."
    )
    result_label = "الجذر (Root)"

    def build_inputs(self) -> None:
        self.expression = self.add_expression_input("x**3 - x - 2")
        self.lower = self.add_input(InputField("بداية الفترة a", "1"))
        self.upper = self.add_input(InputField("نهاية الفترة b", "2"))
        self.tolerance, self.max_iterations = self.add_convergence_inputs()

    def run_algorithm(self) -> AlgorithmResult:
        return solve_bisection(
            self.expression.text(),
            self.lower.text(),
            self.upper.text(),
            self.tolerance.text(),
            self.max_iterations.text(),
        )
