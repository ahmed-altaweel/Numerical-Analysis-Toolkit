from  models.algorithm_result import AlgorithmResult
from  services.solver_service import solve_lagrange
from  ui.components.algorithm_page import AlgorithmPage
from  ui.components.input_field import InputField
from  ui.components.points_input import PointsInput


class LagrangePage(AlgorithmPage):
    title = "استيفاء لاجرنج (Lagrange Interpolation)"
    description = (
        "تبني كثير حدود يمر بكل النقاط المعطاة، وتُقدّر قيمة الدالة عند X المطلوب "
        "بجمع حدود yi·Li(X)، حيث Li دوال لاجرنج الأساسية."
    )
    result_label = "P(X)"
    table_title = "جدول حدود لاجرنج"

    def build_inputs(self) -> None:
        self.points = self.add_input(PointsInput(), full_width=True)
        self.x_value = self.add_input(InputField("قيمة X المطلوبة", "2.5"), full_width=True)

    def run_algorithm(self) -> AlgorithmResult:
        return solve_lagrange(self.points.points(), self.x_value.text())
