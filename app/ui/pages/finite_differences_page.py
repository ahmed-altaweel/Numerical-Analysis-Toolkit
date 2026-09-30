from  models.algorithm_result import AlgorithmResult
from  services.solver_service import (
    solve_newton_backward,
    solve_newton_central,
    solve_newton_forward,
)
from  ui.components.algorithm_page import AlgorithmPage
from  ui.components.input_field import InputField
from  ui.components.points_input import PointsInput
from  ui.widgets.method_selector import MethodSelector

METHODS = [
    ("أمامي (Forward)", "forward"),
    ("خلفي (Backward)", "backward"),
    ("مركزي (Central)", "central"),
]

_SOLVERS = {
    "forward": solve_newton_forward,
    "backward": solve_newton_backward,
    "central": solve_newton_central,
}


class FiniteDifferencesPage(AlgorithmPage):
    title = "استيفاء الفروق المنتهية (Finite Difference Interpolation)"
    description = (
        "تحسب قيمة الاستيفاء عند X المطلوب باستخدام جدول الفروق المنتهية. "
        "اختر الطريقة المناسبة: أمامي (بداية الجدول) أو خلفي (نهاية الجدول) أو مركزي (ستيرلنغ)."
    )
    result_label = "P(X)"
    table_title = "جدول الفروق"

    def build_inputs(self) -> None:
        self.points = self.add_input(PointsInput(), full_width=True)
        self.method = self.add_input(
            MethodSelector(METHODS, label="اختر الطريقة (Method)"),
            full_width=True,
        )
        self.x_value = self.add_input(
            InputField("قيمة X المطلوبة", "2.5"), full_width=True
        )

    def run_algorithm(self) -> AlgorithmResult:
        solver = _SOLVERS[self.method.value()]
        return solver(self.points.points(), self.x_value.text())
