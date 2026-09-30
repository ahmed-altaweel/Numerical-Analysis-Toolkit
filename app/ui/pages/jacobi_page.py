from  models.algorithm_result import AlgorithmResult
from  services.solver_service import solve_jacobi
from  ui.components.algorithm_page import AlgorithmPage
from  ui.components.linear_system_input import LinearSystemInput


class JacobiPage(AlgorithmPage):
    title = "طريقة جاكوبي (Jacobi Method)"
    description = (
        "طريقة تكرارية تحسب كل مجهول من قيم التكرار السابق فقط، وتتوقف عندما يصبح "
        "الفرق بين تكرارين متتاليين أصغر من التسامح."
    )
    result_label = "الحل (X)"

    def build_inputs(self) -> None:
        self.system = self.add_input(LinearSystemInput(with_initial=True), full_width=True)
        self.tolerance, self.max_iterations = self.add_convergence_inputs("1e-6", "100")

    def run_algorithm(self) -> AlgorithmResult:
        return solve_jacobi(
            self.system.matrix_cells(),
            self.system.vector_cells(),
            self.system.initial_cells(),
            self.tolerance.text(),
            self.max_iterations.text(),
        )
