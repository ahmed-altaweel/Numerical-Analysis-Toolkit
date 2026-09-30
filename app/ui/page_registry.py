from dataclasses import dataclass
from typing import Callable

from  ui.components.algorithm_page import AlgorithmPage
from  ui.pages.bisection_page import BisectionPage
from  ui.pages.cramer_page import CramerPage
from  ui.pages.finite_differences_page import FiniteDifferencesPage
from  ui.pages.gaussian_page import GaussianPage
from  ui.pages.jacobi_page import JacobiPage
from  ui.pages.lagrange_page import LagrangePage
from  ui.pages.matrix_inverse_page import MatrixInversePage
from  ui.pages.newton_raphson_page import NewtonRaphsonPage
from  ui.pages.secant_page import SecantPage
from  ui.pages.trapezoidal_page import TrapezoidalPage


@dataclass(frozen=True)
class PageEntry:
    title: str
    factory: Callable[[], AlgorithmPage]


@dataclass(frozen=True)
class Section:
    title: str
    entries: tuple[PageEntry, ...]


SECTIONS: tuple[Section, ...] = (
    Section(
        "إيجاد الجذور (Root Finding)",
        (
            PageEntry("التنصيف (Bisection)", BisectionPage),
            PageEntry("نيوتن-رابسون (Newton-Raphson)", NewtonRaphsonPage),
            PageEntry("القاطع (Secant)", SecantPage),
        ),
    ),
    Section(
        "الاستيفاء (Interpolation)",
        (
            PageEntry("لاجرنج (Lagrange)", LagrangePage),
            PageEntry("الفروق المنتهية (Finite Differences)", FiniteDifferencesPage),
        ),
    ),
    Section(
        "الأنظمة الخطية (Linear Systems)",
        (
            PageEntry("كرامر (Cramer)", CramerPage),
            PageEntry("الحذف الغاوسي (Gaussian)", GaussianPage),
            PageEntry("معكوس المصفوفة (Matrix Inverse)", MatrixInversePage),
            PageEntry("جاكوبي (Jacobi)", JacobiPage),
        ),
    ),
    Section(
        "التكامل العددي (Numerical Integration)",
        (PageEntry("أشباه المنحرفات (Trapezoidal)", TrapezoidalPage),),
    ),
)
