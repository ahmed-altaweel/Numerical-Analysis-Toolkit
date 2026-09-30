from typing import Any

from PySide6.QtWidgets import (
    QFrame,
    QLayout,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QScrollArea,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from  models.algorithm_result import AlgorithmResult
from  ui.components.input_field import InputField
from  ui.components.result_panel import ResultPanel
from  ui.components.steps_panel import StepsPanel
from  ui.components.steps_table import StepsTable
from  ui.widgets.app_button import AppButton


FUNCTION_NOTE = "اكتب الدالة بصيغة SymPy، والمتغير الوحيد المسموح به هو x. الدوال والثوابت المدعومة:"
FUNCTION_NAMES = "sin  cos  tan  asin  acos  atan  sinh  cosh  tanh  exp  log  ln  sqrt  abs  pi  e"


class AlgorithmPage(QWidget):
    title = ""
    description = ""
    result_label = "النتيجة"
    error_label = "الخطأ النهائي"
    table_title = "جدول التكرارات"

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._resettable: list[Any] = []
        self._grid_row = 0
        self._grid_column = 0
        self._build_layout()
        self.build_inputs()
        self.reset_output()

    def build_inputs(self) -> None:
        raise NotImplementedError

    def run_algorithm(self) -> AlgorithmResult:
        raise NotImplementedError

    def _build_layout(self) -> None:
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        outer.addWidget(scroll)
        content = QWidget()
        content.setObjectName("Page")
        scroll.setWidget(content)
        layout = QVBoxLayout(content)
        layout.setContentsMargins(28, 24, 28, 24)
        layout.setSpacing(16)
        layout.setSizeConstraint(QLayout.SetMinimumSize)

        title_label = QLabel(self.title)
        title_label.setObjectName("PageTitle")
        description_label = QLabel(self.description)
        description_label.setObjectName("PageDescription")
        description_label.setWordWrap(True)
        layout.addWidget(title_label)
        layout.addWidget(description_label)

        input_card = QFrame()
        input_card.setObjectName("Card")
        card_layout = QVBoxLayout(input_card)
        card_layout.setContentsMargins(18, 16, 18, 16)
        card_layout.setSpacing(12)
        heading = QLabel("المدخلات (Input)")
        heading.setObjectName("CardTitle")
        self._grid = QGridLayout()
        self._grid.setHorizontalSpacing(16)
        self._grid.setVerticalSpacing(10)
        self._grid.setColumnStretch(0, 1)
        self._grid.setColumnStretch(1, 1)
        buttons = QHBoxLayout()
        calculate_button = AppButton("احسب (Calculate)", variant="primary")
        reset_button = AppButton("مسح / إعادة تعيين (Reset)")

        calculate_button.clicked.connect(lambda: self.calculate())
        reset_button.clicked.connect(lambda: self.reset())
        buttons.addWidget(calculate_button)
        buttons.addWidget(reset_button)
        buttons.addStretch(1)
        card_layout.addWidget(heading)
        card_layout.addLayout(self._grid)
        card_layout.addLayout(buttons)
        layout.addWidget(input_card)

        self.result_panel = ResultPanel()
        layout.addWidget(self.result_panel)

        self.tabs = QTabWidget()
        self.tabs.setMinimumHeight(420)
        self.tabs.tabBar().setUsesScrollButtons(False)
        self.table = StepsTable()
        self.steps_panel = StepsPanel()
        self.tabs.addTab(self.table, self.table_title)
        self.tabs.addTab(self.steps_panel, "خطوات الحل (Steps)")
        layout.addWidget(self.tabs)
        layout.addStretch(1)

    def _place(self, widget: QWidget, full_width: bool) -> None:
        if full_width and self._grid_column != 0:
            self._grid_row += 1
            self._grid_column = 0
        span = 2 if full_width else 1
        self._grid.addWidget(widget, self._grid_row, self._grid_column, 1, span)
        if full_width or self._grid_column == 1:
            self._grid_row += 1
            self._grid_column = 0
        else:
            self._grid_column = 1

    def add_input(self, widget: Any, full_width: bool = False) -> Any:
        self._place(widget, full_width)
        self._resettable.append(widget)
        if isinstance(widget, InputField):
            widget.submitted.connect(self.calculate)
        return widget

    def add_note(self, text: str) -> None:
        label = QLabel(text)
        label.setObjectName("Note")
        label.setWordWrap(True)
        self._place(label, True)

    def add_expression_input(self, default: str) -> InputField:
        field = self.add_input(InputField("الدالة f(x)", default, "مثال: x**3 - x - 2"), full_width=True)
        self.add_note(FUNCTION_NOTE)
        self.add_note(FUNCTION_NAMES)
        return field

    def add_convergence_inputs(
        self, tolerance: str = "1e-6", max_iterations: str = "50"
    ) -> tuple[InputField, InputField]:
        tolerance_field = self.add_input(InputField("التسامح (Tolerance)", tolerance))
        iterations_field = self.add_input(InputField("أقصى عدد تكرارات (Maximum Iterations)", max_iterations))
        return tolerance_field, iterations_field

    def calculate(self) -> None:
        self.display(self.run_algorithm())

    def display(self, result: AlgorithmResult) -> None:
        self.result_panel.show_result(result, self.result_label, self.error_label)
        has_table = bool(result.table_rows)
        has_steps = bool(result.steps)
        if has_table:
            self.table.show_table(result.table_columns, result.table_rows)
        if has_steps:
            self.steps_panel.show_steps(result.steps)
        visibility = [has_table, has_steps]
        for index, visible in enumerate(visibility):
            self.tabs.setTabVisible(index, visible)
        first_visible = next((index for index, visible in enumerate(visibility) if visible), None)
        if first_visible is None:
            self.tabs.hide()
        else:
            self.tabs.setCurrentIndex(first_visible)
            self.tabs.show()

    def reset_output(self) -> None:
        self.result_panel.show_placeholder()
        self.tabs.hide()

    def reset(self) -> None:
        for widget in self._resettable:
            widget.reset()
        self.reset_output()
