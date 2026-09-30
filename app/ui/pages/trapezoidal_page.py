from  models.algorithm_result import AlgorithmResult
from  services.solver_service import solve_trapezoidal
from  ui.components.algorithm_page import AlgorithmPage
from  ui.components.input_field import InputField


class TrapezoidalPage(AlgorithmPage):
    title = "قاعدة أشباه المنحرفات (Trapezoidal Rule)"
    description = (
        "تقرّب التكامل المحدد بتقسيم [a, b] إلى n قطعة متساوية، وتجمع مساحات أشباه المنحرفات "
        "المكوّنة تحت المنحنى."
    )
    result_label = "التكامل (Integral)"
    error_label = "تقدير الخطأ"
    table_title = "جدول القيم"

    def build_inputs(self) -> None:
        self.expression = self.add_expression_input("x**2")
        self.lower = self.add_input(InputField("بداية التكامل a", "0"))
        self.upper = self.add_input(InputField("نهاية التكامل b", "1"))
        self.count = self.add_input(InputField("عدد القطع n", "10"), full_width=True)

    def run_algorithm(self) -> AlgorithmResult:
        return solve_trapezoidal(
            self.expression.text(),
            self.lower.text(),
            self.upper.text(),
            self.count.text(),
        )
