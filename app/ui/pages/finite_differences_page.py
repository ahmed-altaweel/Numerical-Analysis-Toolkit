from  models.algorithm_result import AlgorithmResult
from  services.solver_service import solve_finite_differences
from  ui.components.algorithm_page import AlgorithmPage
from  ui.components.points_input import PointsInput


class FiniteDifferencesPage(AlgorithmPage):
    title = "جدول الفروق (Finite Differences)"
    description = (
        "تبني جدول الفروق الأمامية: كل عمود يُحسب من الفروق المتتالية للعمود السابق، "
        "ويتغير عدد الأعمدة حسب عدد النقاط المُدخلة."
    )
    table_title = "جدول الفروق"

    def build_inputs(self) -> None:
        self.points = self.add_input(PointsInput(), full_width=True)

    def run_algorithm(self) -> AlgorithmResult:
        return solve_finite_differences(self.points.points())
