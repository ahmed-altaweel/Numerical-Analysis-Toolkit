from  models.algorithm_result import AlgorithmResult
from  services.solver_service import solve_gaussian
from  ui.components.algorithm_page import AlgorithmPage
from  ui.components.linear_system_input import LinearSystemInput


class GaussianPage(AlgorithmPage):
    title = "الحذف الغاوسي (Gaussian Elimination)"
    description = (
        "تحوّل المصفوفة الموسعة إلى مصفوفة مثلثية عليا بعمليات على الصفوف مع اختيار المحور الجزئي "
        "(Partial Pivoting)، ثم تحل النظام بالتعويض الخلفي."
    )
    result_label = "الحل (X)"

    def build_inputs(self) -> None:
        self.system = self.add_input(LinearSystemInput(), full_width=True)

    def run_algorithm(self) -> AlgorithmResult:
        return solve_gaussian(self.system.matrix_cells(), self.system.vector_cells())
