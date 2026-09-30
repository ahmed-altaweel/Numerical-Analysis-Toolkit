from  models.algorithm_result import AlgorithmResult
from  services.solver_service import solve_newton_raphson
from  ui.components.algorithm_page import AlgorithmPage
from  ui.components.input_field import InputField


class NewtonRaphsonPage(AlgorithmPage):
    title = "طريقة نيوتن-رابسون (Newton-Raphson Method)"
    description = (
        "تقترب من الجذر باستخدام المماس: في كل تكرار تُحسب نقطة تقاطع مماس الدالة مع محور x "
        "لتكون التقدير الجديد. تُشتق الدالة تلقائيًا باستخدام SymPy."
    )
    result_label = "الجذر (Root)"

    def build_inputs(self) -> None:
        self.expression = self.add_expression_input("x**3 - x - 2")
        self.initial = self.add_input(InputField("القيمة الابتدائية x0", "1.5"), full_width=True)
        self.tolerance, self.max_iterations = self.add_convergence_inputs()

    def run_algorithm(self) -> AlgorithmResult:
        return solve_newton_raphson(
            self.expression.text(),
            self.initial.text(),
            self.tolerance.text(),
            self.max_iterations.text(),
        )
