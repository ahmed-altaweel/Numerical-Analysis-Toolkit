from  models.algorithm_result import AlgorithmResult
from  services.solver_service import solve_secant
from  ui.components.algorithm_page import AlgorithmPage
from  ui.components.input_field import InputField


class SecantPage(AlgorithmPage):
    title = "طريقة القاطع (Secant Method)"
    description = (
        "تشبه طريقة نيوتن لكنها لا تحتاج إلى المشتقة؛ إذ تستبدل المماس بخط قاطع يمر بآخر نقطتين، "
        "وتأخذ تقاطعه مع محور x كتقدير جديد."
    )
    result_label = "الجذر (Root)"

    def build_inputs(self) -> None:
        self.expression = self.add_expression_input("x**3 - x - 2")
        self.first = self.add_input(InputField("القيمة الأولى x0", "1"))
        self.second = self.add_input(InputField("القيمة الثانية x1", "2"))
        self.tolerance, self.max_iterations = self.add_convergence_inputs()

    def run_algorithm(self) -> AlgorithmResult:
        return solve_secant(
            self.expression.text(),
            self.first.text(),
            self.second.text(),
            self.tolerance.text(),
            self.max_iterations.text(),
        )
