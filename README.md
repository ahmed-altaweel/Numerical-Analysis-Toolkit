# Numerical Analysis Toolkit

## Project Overview

تطبيق سطح مكتب أكاديمي لمادة **التحليل العددي (Numerical Analysis)**، مبني بلغة Python وواجهة PySide6.
الهدف منه ليس مجرد حاسبة، بل توضيح **كيف تعمل الخوارزمية ولماذا وصلت إلى النتيجة**: يدخل الطالب البيانات، ثم يشاهد خطوات الحساب وجدول التكرارات والنتيجة النهائية والخطأ والرسم البياني.

جميع الخوارزميات مكتوبة يدويًا لأغراض تعليمية، دون استخدام SciPy أو أي خوارزميات جاهزة.

## Features

- صفحة مستقلة لكل خوارزمية مع وصف مختصر ومدخلات وأزرار Calculate / Reset.
- عرض خطوات الحل تفصيليًا (بما في ذلك المصفوفة بعد كل عملية صفية في الحذف الغاوسي).
- جداول التكرارات وجداول الفروق والمحددات.
- رسوم بيانية تعليمية (Matplotlib) للتنصيف ونيوتن والقاطع وأشباه المنحرفات.
- إدخال الدوال كنص (مثل `sin(x) + x**2`) وتحليلها بأمان عبر SymPy دون استخدام `eval()`.
- رسائل تحقق وأخطاء واضحة باللغة العربية.
- فصل كامل بين الخوارزميات والواجهة، وسهولة إضافة خوارزميات جديدة.

## Algorithms

| القسم                 | الخوارزميات                                 |
| --------------------- | ------------------------------------------- |
| Root Finding          | Bisection, Newton-Raphson, Secant           |
| Interpolation         | Lagrange, Finite Differences                |
| Linear Systems        | Cramer's Rule, Gaussian Elimination, Jacobi |
| Numerical Integration | Trapezoidal Rule                            |

## Technologies

- Python 3.11+
- PySide6
- NumPy
- SymPy
- Matplotlib

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

على Windows استخدم `.venv\Scripts\activate` بدلًا من أمر التفعيل أعلاه.

## Running the Application

```bash
python -m  main
```

## Project Structure

```text
numerical-analysis/
├── app/
│   ├── main.py
│   ├── algorithms/
│   │   ├── root_finding/      bisection.py, newton_raphson.py, secant.py
│   │   ├── interpolation/     lagrange.py, finite_difference.py
│   │   ├── linear_systems/    cramer.py, gaussian.py, jacobi.py
│   │   └── integration/       trapezoidal.py
│   ├── models/                algorithm_result.py, errors.py
│   ├── services/              expression_parser.py, validation.py, solver_service.py
│   ├── ui/
│   │   ├── main_window.py
│   │   ├── page_registry.py
│   │   ├── theme.py
│   │   ├── pages/             صفحة لكل خوارزمية
│   │   ├── components/        AlgorithmPage, InputField, MatrixInput, PointsInput,
│   │   │                      LinearSystemInput, ResultPanel, StepsTable, StepsPanel,
│   │   │                      ErrorMessage, GraphWidget
│   │   └── widgets/           sidebar.py, plotters.py
│   └── utils/                 formatting.py, normalization.py, linear_algebra.py
├── requirements.txt
├── README.md
└── .gitignore
```

مسار البيانات:

```text
UI  →  solver_service  →  Algorithm  →  AlgorithmResult  →  UI
```

## Usage Examples

**التنصيف:** الدالة `x**3 - x - 2` على الفترة `[1, 2]` بتسامح `1e-6` تعطي جذرًا قريبًا من `1.52138`.

**نيوتن-رابسون:** الدالة نفسها مع `x0 = 1.5` تتقارب في 3 تكرارات تقريبًا.

**لاجرنج:** النقاط `(1,2) (2,3) (3,5) (4,8)` عند `X = 2.5` تعطي `3.875`.

**الحذف الغاوسي:** النظام الافتراضي 3×3 يعطي `x = (1, 2, -1)`.

**إضافة خوارزمية جديدة:** أنشئ الخوارزمية في `app/algorithms`، ودالة تشغيل في `solver_service.py`، وصفحة ترث من `AlgorithmPage`، ثم سجّلها في `page_registry.py`.
