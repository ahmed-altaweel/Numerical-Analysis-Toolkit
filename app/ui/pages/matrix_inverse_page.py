from  models.algorithm_result import AlgorithmResult
from  services.solver_service import solve_matrix_inverse
from  ui.components.algorithm_page import AlgorithmPage
from  ui.components.linear_system_input import LinearSystemInput


class MatrixInversePage(AlgorithmPage):
    title = "معكوس المصفوفة (Matrix Inverse)"
    description = (
        "تحل النظام AX = B بحساب معكوس المصفوفة A⁻¹ باستخدام طريقة غاوس-جوردن على المصفوفة الموسعة [A | I]، "
        "ثم ضرب المعكوس في المتجه B للحصول على الحل: X = A⁻¹ · B."
    )
    result_label = "الحل (X)"
    table_title = "جدول المعكوس والحل"

    def build_inputs(self) -> None:
        self.system = self.add_input(LinearSystemInput(), full_width=True)

    def run_algorithm(self) -> AlgorithmResult:
        return solve_matrix_inverse(self.system.matrix_cells(), self.system.vector_cells())
