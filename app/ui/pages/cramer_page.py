from  models.algorithm_result import AlgorithmResult
from  services.solver_service import solve_cramer
from  ui.components.algorithm_page import AlgorithmPage
from  ui.components.linear_system_input import LinearSystemInput


class CramerPage(AlgorithmPage):
    title = "قاعدة كرامر (Cramer's Rule)"
    description = (
        "تحل النظام AX = B بحساب المحدد det(A)، ثم محدد كل مصفوفة تنتج من استبدال عمود من A بالمتجه B، "
        "وقسمة كل منها على det(A)."
    )
    result_label = "الحل (X)"
    table_title = "جدول المحددات"

    def build_inputs(self) -> None:
        self.system = self.add_input(LinearSystemInput(), full_width=True)

    def run_algorithm(self) -> AlgorithmResult:
        return solve_cramer(self.system.matrix_cells(), self.system.vector_cells())
