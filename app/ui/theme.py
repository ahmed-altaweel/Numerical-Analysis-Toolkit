# ══════════════════════════════════════════════════════════════
#  NUMERICAL ANALYSIS TOOLKIT — APPLICATION THEME
# ══════════════════════════════════════════════════════════════


# ══════════════════════════════════════════════════════════════
#  COLOUR PALETTE
# ══════════════════════════════════════════════════════════════

# Primary / Academic
C_DEEP     = "#163A5F"   # Deep academic blue
C_MID      = "#2563EB"   # Primary mathematical blue
C_MUTED    = "#64748B"   # Slate
C_SOFT     = "#DBEAFE"   # Light blue

# Surface / Background
C_BG_PAGE  = "#F4F7FA"
C_BG_CARD  = "#FFFFFF"
C_BG_INPUT = "#F8FAFC"
C_BG_ALT   = "#F8FAFC"

# Sidebar
C_SIDEBAR_BG      = "#102A43"
C_SIDEBAR_HEADER  = "rgba(0,0,0,0.16)"
C_SIDEBAR_BORDER  = "#243B53"
C_SIDEBAR_TEXT    = "#CBD5E1"
C_SIDEBAR_DIM     = "#829AB1"
C_SIDEBAR_HOVER   = "rgba(37, 99, 235, 0.18)"

C_SIDEBAR_ACTIVE = (
    "qlineargradient("
    "x1:0,y1:0,x2:1,y2:0,"
    f"stop:0 {C_MID},"
    "stop:1 #1D4ED8)"
)


# ══════════════════════════════════════════════════════════════
#  STATE COLOURS
# ══════════════════════════════════════════════════════════════

# Success
C_SUCCESS_BG      = "#ECFDF5"
C_SUCCESS_FG      = "#166534"
C_SUCCESS_BORDER  = "#A7F3D0"

# Warning
C_WARNING_BG      = "#FFFBEB"
C_WARNING_FG      = "#92400E"
C_WARNING_BORDER  = "#FDE68A"

# Error
C_ERROR_BG        = "#FEF2F2"
C_ERROR_FG        = "#991B1B"
C_ERROR_BORDER    = "#FECACA"

# Neutral
C_NEUTRAL_BG      = "#F1F5F9"
C_NEUTRAL_FG      = "#475569"
C_NEUTRAL_BORDER  = "#CBD5E1"


# ══════════════════════════════════════════════════════════════
#  TYPOGRAPHY
# ══════════════════════════════════════════════════════════════

C_TEXT_PRIMARY    = "#172B4D"
C_TEXT_SECONDARY  = "#64748B"


# ══════════════════════════════════════════════════════════════
#  NUMERICAL ANALYSIS / CHART COLOURS
# ══════════════════════════════════════════════════════════════

CHART_CURVE  = "#2563EB"
CHART_POINT  = "#0F766E"
CHART_GUIDE  = "#163A5F"
CHART_AXIS   = "#94A3B8"
CHART_FILL   = "#DBEAFE"


# ══════════════════════════════════════════════════════════════
#  RESULT COLOURS
# ══════════════════════════════════════════════════════════════

C_RESULT_BG       = "#EFF6FF"
C_RESULT_BORDER   = "#BFDBFE"
C_RESULT_FG       = "#1D4ED8"


# ══════════════════════════════════════════════════════════════
#  STYLESHEET
# ══════════════════════════════════════════════════════════════

STYLESHEET = f"""

/* ═════════════════════════════════════════════════════════════
   BASE
   ═════════════════════════════════════════════════════════════ */

QWidget {{
    font-family:
        "Segoe UI Variable Display",
        "Segoe UI",
        "Noto Sans Arabic",
        "Tahoma",
        "DejaVu Sans",
        sans-serif;

    font-size: 10.5pt;
    color: {C_TEXT_PRIMARY};
}}

QMainWindow,
QScrollArea,
#Page {{
    background: {C_BG_PAGE};
}}


/* ═════════════════════════════════════════════════════════════
   SCROLLBARS
   ═════════════════════════════════════════════════════════════ */

QScrollBar:vertical {{
    background: transparent;
    width: 7px;
    margin: 0;
}}

QScrollBar::handle:vertical {{
    background: #CBD5E1;
    border-radius: 3px;
    min-height: 28px;
}}

QScrollBar::handle:vertical:hover {{
    background: {C_MUTED};
}}

QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {{
    height: 0;
}}

QScrollBar::add-page:vertical,
QScrollBar::sub-page:vertical {{
    background: transparent;
}}


QScrollBar:horizontal {{
    background: transparent;
    height: 7px;
    margin: 0;
}}

QScrollBar::handle:horizontal {{
    background: #CBD5E1;
    border-radius: 3px;
    min-width: 28px;
}}

QScrollBar::handle:horizontal:hover {{
    background: {C_MUTED};
}}

QScrollBar::add-line:horizontal,
QScrollBar::sub-line:horizontal {{
    width: 0;
}}

QScrollBar::add-page:horizontal,
QScrollBar::sub-page:horizontal {{
    background: transparent;
}}


/* ═════════════════════════════════════════════════════════════
   SIDEBAR
   ═════════════════════════════════════════════════════════════ */

QFrame#Sidebar {{
    background: {C_SIDEBAR_BG};
    border-right: 1px solid {C_SIDEBAR_BORDER};
}}

QLabel#SidebarTitle {{
    color: #F8FAFC;
    font-size: 13pt;
    font-weight: bold;
    letter-spacing: 0.4px;
}}

QLabel#SidebarSubtitle {{
    color: #94A3B8;
    font-size: 9pt;
    letter-spacing: 0.2px;
}}

QListWidget#SidebarList {{
    background: transparent;
    border: none;
    outline: none;
    padding-bottom: 8px;
}}

QListWidget#SidebarList::item {{
    color: {C_SIDEBAR_TEXT};

    padding: 10px 16px;

    border-radius: 8px;

    margin: 2px 8px;

    font-size: 10pt;
}}

QListWidget#SidebarList::item:disabled {{
    color: {C_SIDEBAR_DIM};

    font-size: 7.5pt;
    font-weight: bold;

    letter-spacing: 1.2px;

    margin-top: 16px;
    margin-bottom: 2px;

    padding: 3px 18px;
}}

QListWidget#SidebarList::item:hover:!selected:!disabled {{
    background: {C_SIDEBAR_HOVER};
    color: #F1F5F9;
}}

QListWidget#SidebarList::item:selected {{
    background: {C_SIDEBAR_ACTIVE};

    color: #FFFFFF;

    font-weight: bold;
}}


/* ═════════════════════════════════════════════════════════════
   CARDS
   ═════════════════════════════════════════════════════════════ */

QFrame#Card {{
    background: {C_BG_CARD};

    border: 1px solid #E2E8F0;

    border-radius: 10px;
}}

QFrame#Card QLabel {{
    background: transparent;
}}


/* ═════════════════════════════════════════════════════════════
   PAGE TYPOGRAPHY
   ═════════════════════════════════════════════════════════════ */

QLabel#PageTitle {{
    font-size: 18pt;

    font-weight: bold;

    color: {C_DEEP};

    letter-spacing: 0.2px;
}}

QLabel#PageDescription {{
    color: {C_TEXT_SECONDARY};

    font-size: 10pt;
}}

QLabel#CardTitle {{
    font-size: 11pt;

    font-weight: bold;

    color: {C_DEEP};

    letter-spacing: 0.1px;
}}

QLabel#Note {{
    color: {C_MUTED};

    font-size: 8.5pt;
}}

QLabel#ResultName {{
    color: {C_TEXT_SECONDARY};

    font-size: 9.5pt;
}}

QLabel#ResultValue {{
    font-family:
        "Cascadia Code",
        "Consolas",
        "DejaVu Sans Mono",
        monospace;

    color: {C_RESULT_FG};

    font-size: 10.5pt;

    font-weight: bold;
}}

QLabel#ResultPrimaryName {{
    color: {C_TEXT_SECONDARY};

    font-size: 9.5pt;
}}

QLabel#ResultPrimaryValue {{
    font-family:
        "Cascadia Code",
        "Consolas",
        "DejaVu Sans Mono",
        monospace;

    color: {C_DEEP};

    font-size: 14pt;

    font-weight: bold;
}}


/* ═════════════════════════════════════════════════════════════
   LABELS
   ═════════════════════════════════════════════════════════════ */

QLabel#FieldLabel {{
    color: {C_SIDEBAR_BG};

    font-size: 11pt;

    font-weight: 700;
}}

QLabel#SectionLabel {{
    color: {C_DEEP};

    font-size: 10pt;

    font-weight: bold;
}}

QLabel#SecondaryLabel {{
    color: {C_TEXT_SECONDARY};

    font-size: 9pt;
}}


/* ═════════════════════════════════════════════════════════════
   TEXT INPUTS
   ═════════════════════════════════════════════════════════════ */

QLineEdit {{
    border: 1px solid #CBD5E1;

    border-radius: 7px;

    padding: 8px 12px;

    background: {C_BG_INPUT};

    color: {C_TEXT_PRIMARY};

    selection-background-color: {C_MID};
    selection-color: #FFFFFF;

    font-size: 10.5pt;
}}

QLineEdit:hover {{
    border-color: #94A3B8;

    background: #FFFFFF;
}}

QLineEdit:focus {{
    border: 1.5px solid {C_MID};

    background: #FFFFFF;
}}

QLineEdit[readOnly="true"] {{
    background: #F1F5F9;

    color: {C_MUTED};
}}


/* ═════════════════════════════════════════════════════════════
   TEXT EDIT
   ═════════════════════════════════════════════════════════════ */

QTextEdit {{
    border: 1px solid #CBD5E1;

    border-radius: 7px;

    padding: 8px 12px;

    background: {C_BG_INPUT};

    color: {C_TEXT_PRIMARY};

    selection-background-color: {C_MID};
    selection-color: #FFFFFF;
}}

QTextEdit:hover {{
    border-color: #94A3B8;
}}

QTextEdit:focus {{
    border-color: {C_MID};

    background: #FFFFFF;
}}


/* ═════════════════════════════════════════════════════════════
   SPIN BOX
   ═════════════════════════════════════════════════════════════ */

QSpinBox {{
    border: 1px solid #CBD5E1;

    border-radius: 7px;

    padding: 6px 10px;

    background: {C_BG_INPUT};

    color: {C_TEXT_PRIMARY};

    selection-background-color: {C_MID};

    min-width: 72px;

    font-weight: bold;
}}

QSpinBox:hover {{
    border-color: #94A3B8;

    background: #FFFFFF;
}}

QSpinBox:focus {{
    border-color: {C_MID};

    background: #FFFFFF;
}}

QSpinBox::up-button,
QSpinBox::down-button {{
    width: 22px;

    background: #E2E8F0;

    border-radius: 4px;

    border: none;

    subcontrol-origin: padding;

    margin: 2px;
}}

QSpinBox::up-button {{
    subcontrol-position: right;
}}

QSpinBox::down-button {{
    subcontrol-position: left;

    margin-right: 0;
}}

QSpinBox::up-arrow,
QSpinBox::down-arrow {{
    image: none;

    width: 0;
    height: 0;
}}

QSpinBox::up-button:hover,
QSpinBox::down-button:hover {{
    background: #CBD5E1;
}}


/* ═════════════════════════════════════════════════════════════
   DOUBLE SPIN BOX
   ═════════════════════════════════════════════════════════════ */

QDoubleSpinBox {{
    border: 1px solid #CBD5E1;

    border-radius: 7px;

    padding: 6px 10px;

    background: {C_BG_INPUT};

    color: {C_TEXT_PRIMARY};

    selection-background-color: {C_MID};

    min-width: 90px;

    font-weight: 600;
}}

QDoubleSpinBox:hover {{
    border-color: #94A3B8;

    background: #FFFFFF;
}}

QDoubleSpinBox:focus {{
    border-color: {C_MID};

    background: #FFFFFF;
}}

QDoubleSpinBox::up-button,
QDoubleSpinBox::down-button {{
    width: 22px;

    background: #E2E8F0;

    border-radius: 4px;

    border: none;

    subcontrol-origin: padding;

    margin: 2px;
}}

QDoubleSpinBox::up-button {{
    subcontrol-position: right;
}}

QDoubleSpinBox::down-button {{
    subcontrol-position: left;

    margin-right: 0;
}}

QDoubleSpinBox::up-arrow,
QDoubleSpinBox::down-arrow {{
    image: none;

    width: 0;
    height: 0;
}}


/* ═════════════════════════════════════════════════════════════
   COMBO BOX
   ═════════════════════════════════════════════════════════════ */

QComboBox {{
    border: 1px solid #CBD5E1;

    border-radius: 7px;

    padding: 8px 12px;

    background: {C_BG_INPUT};

    color: {C_TEXT_PRIMARY};

    min-height: 18px;

    font-size: 10.5pt;
}}

QComboBox:hover {{
    border-color: #94A3B8;

    background: #FFFFFF;
}}

QComboBox:focus {{
    border-color: {C_MID};

    background: #FFFFFF;
}}

QComboBox::drop-down {{
    border: none;

    width: 28px;
}}

QComboBox QAbstractItemView {{
    background: #FFFFFF;

    border: 1px solid #CBD5E1;

    selection-background-color: {C_MID};
    selection-color: #FFFFFF;

    padding: 4px;
}}


/* ═════════════════════════════════════════════════════════════
   BUTTONS
   ═════════════════════════════════════════════════════════════ */

QPushButton {{
    border: 1px solid #CBD5E1;

    border-radius: 7px;

    padding: 8px 20px;

    background: #FFFFFF;

    color: {C_TEXT_SECONDARY};

    font-weight: 600;
}}

QPushButton:hover {{
    background: #F1F5F9;

    border-color: #94A3B8;

    color: {C_DEEP};
}}

QPushButton:pressed {{
    background: #E2E8F0;
}}

QPushButton:disabled {{
    background: #F1F5F9;

    border-color: #E2E8F0;

    color: #94A3B8;
}}


/* ═════════════════════════════════════════════════════════════
   PRIMARY BUTTON
   ═════════════════════════════════════════════════════════════ */

QPushButton#PrimaryButton {{
    background: {C_SIDEBAR_BG};

    color: #FFFFFF;

    font-weight: bold;

    border: none;

    padding: 9px 24px;
}}

QPushButton#PrimaryButton:hover {{
    background: {C_SIDEBAR_BORDER};
}}

QPushButton#PrimaryButton:pressed {{
    background: #0A1F33;
}}

QPushButton#PrimaryButton:disabled {{
    background: #4A6A8A;

    color: #CBD5E1;
}}


/* ═════════════════════════════════════════════════════════════
   SECONDARY BUTTON
   ═════════════════════════════════════════════════════════════ */

QPushButton#SecondaryButton {{
    background: #FFFFFF;

    color: {C_DEEP};

    border: 1px solid #CBD5E1;

    font-weight: 600;
}}

QPushButton#SecondaryButton:hover {{
    background: #EFF6FF;

    border-color: {C_MID};

    color: {C_MID};
}}


/* ═════════════════════════════════════════════════════════════
   DANGER BUTTON
   ═════════════════════════════════════════════════════════════ */

QPushButton#DangerButton {{
    background: #FFFFFF;

    color: #B91C1C;

    border: 1px solid #FECACA;

    font-weight: 600;
}}

QPushButton#DangerButton:hover {{
    background: #FEF2F2;

    border-color: #FCA5A5;
}}


/* ═════════════════════════════════════════════════════════════
   METHOD SELECTOR TOGGLE BUTTONS
   ═════════════════════════════════════════════════════════════ */

QPushButton#MethodButton {{
    background: #FFFFFF;

    color: {C_TEXT_SECONDARY};

    border: 1px solid #CBD5E1;

    padding: 8px 22px;

    font-weight: 600;

    border-radius: 7px;

    min-width: 100px;
}}

QPushButton#MethodButton:hover {{
    background: #EFF6FF;

    color: {C_MID};

    border-color: {C_MID};
}}

QPushButton#MethodButton:checked {{
    background: {C_SIDEBAR_BG};

    color: #FFFFFF;

    border-color: {C_SIDEBAR_BG};

    font-weight: bold;
}}

QPushButton#MethodButton:checked:hover {{
    background: {C_SIDEBAR_BORDER};
}}

/* ═════════════════════════════════════════════════════════════
   STATUS MESSAGES
   ═════════════════════════════════════════════════════════════ */

QLabel#Message {{
    border-radius: 8px;

    padding: 11px 15px;

    font-size: 10pt;
}}

QLabel#Message[state="success"] {{
    background: {C_SUCCESS_BG};

    color: {C_SUCCESS_FG};

    border: 1px solid {C_SUCCESS_BORDER};
}}

QLabel#Message[state="warning"] {{
    background: {C_WARNING_BG};

    color: {C_WARNING_FG};

    border: 1px solid {C_WARNING_BORDER};
}}

QLabel#Message[state="error"] {{
    background: {C_ERROR_BG};

    color: {C_ERROR_FG};

    border: 1px solid {C_ERROR_BORDER};
}}

QLabel#Message[state="neutral"] {{
    background: {C_NEUTRAL_BG};

    color: {C_NEUTRAL_FG};

    border: 1px solid {C_NEUTRAL_BORDER};
}}


/* ═════════════════════════════════════════════════════════════
   TABLE
   ═════════════════════════════════════════════════════════════ */

QTableWidget {{
    background: #FFFFFF;

    alternate-background-color: #F0F5FF;

    gridline-color: #D1DCF0;

    border: 1.5px solid #B8CCEE;

    border-radius: 10px;

    selection-background-color: {C_MID};

    selection-color: #FFFFFF;

    font-size: 10pt;

    font-family:
        "Cascadia Code",
        "Consolas",
        "DejaVu Sans Mono",
        monospace;
}}

QTableWidget::item {{
    padding: 2px 4px;

    border: none;

    border-bottom: 1px solid #E8EFF8;

    color: {C_TEXT_PRIMARY};
}}


QTableWidget::item:alternate {{
    background: #F0F5FF;
}}

QTableWidget::item:hover {{
    background: #DBEAFE;

    color: {C_DEEP};
}}

QTableWidget::item:selected {{
    background: qlineargradient(
        x1:0, y1:0, x2:1, y2:0,
        stop:0 {C_MID},
        stop:1 #1D4ED8
    );

    color: #FFFFFF;
}}

QTableWidget::item:selected:hover {{
    background: #1D4ED8;

    color: #FFFFFF;
}}

QTableWidget QLineEdit {{
    border: 2px solid {C_MID};

    border-radius: 4px;

    padding: 0px 4px;

    margin: 0px;

    background: #FFFFFF;

    color: {C_TEXT_PRIMARY};

    selection-background-color: {C_MID};

    selection-color: #FFFFFF;

    font-size: 10pt;

    font-family:
        "Cascadia Code",
        "Consolas",
        "DejaVu Sans Mono",
        monospace;

    qproperty-alignment: 'AlignHCenter | AlignVCenter';
}}


QHeaderView {{
    border-radius: 0;
}}

QHeaderView::section {{
    background: qlineargradient(
        x1:0, y1:0, x2:0, y2:1,
        stop:0 #1E3A5F,
        stop:1 {C_DEEP}
    );

    padding: 11px 14px;

    border: none;

    border-right: 1px solid #2D5080;

    font-weight: bold;

    color: #E8F0FE;

    font-size: 9.5pt;

    letter-spacing: 0.5px;

    text-transform: uppercase;
}}

QHeaderView::section:hover {{
    background: qlineargradient(
        x1:0, y1:0, x2:0, y2:1,
        stop:0 #264D80,
        stop:1 #1E3A5F
    );

    color: #FFFFFF;
}}

QHeaderView::section:first {{
    border-top-left-radius: 9px;
}}

QHeaderView::section:last {{
    border-top-right-radius: 9px;

    border-right: none;
}}

QHeaderView::section:vertical {{
    background: qlineargradient(
        x1:0, y1:0, x2:1, y2:0,
        stop:0 #1E3A5F,
        stop:1 #263F6A
    );

    color: #CBD5E1;

    font-weight: bold;

    border-right: 2px solid #2D5080;

    border-bottom: 1px solid #2D5080;

    padding: 6px 10px;

    border-radius: 0;
}}


/* ═════════════════════════════════════════════════════════════
   STEPS / CALCULATION VIEW
   ═════════════════════════════════════════════════════════════ */

QTextEdit#StepsView {{
    background: #F8FAFC;

    border: none;

    padding: 14px 18px;

    color: {C_TEXT_PRIMARY};

    font-family:
        "Cascadia Code",
        "Consolas",
        "DejaVu Sans Mono",
        monospace;

    font-size: 9.5pt;

    selection-background-color: {C_MID};

    selection-color: #FFFFFF;
}}


/* ═════════════════════════════════════════════════════════════
   FORMULA / EQUATION
   ═════════════════════════════════════════════════════════════ */

QLabel#Formula {{
    background: #F8FAFC;

    border: 1px solid #E2E8F0;

    border-radius: 8px;

    padding: 12px 16px;

    color: {C_DEEP};

    font-family:
        "Cambria Math",
        "STIX Two Math",
        "DejaVu Serif",
        serif;

    font-size: 11pt;
}}


/* ═════════════════════════════════════════════════════════════
   RESULT CARD
   ═════════════════════════════════════════════════════════════ */

QFrame#ResultCard {{
    background: {C_RESULT_BG};

    border: 1px solid {C_RESULT_BORDER};

    border-radius: 10px;
}}

QLabel#ResultTitle {{
    color: {C_DEEP};

    font-size: 10pt;

    font-weight: bold;
}}

QLabel#ResultValue {{
    color: {C_RESULT_FG};

    font-size: 14pt;

    font-weight: bold;

    font-family:
        "Cascadia Code",
        "Consolas",
        "DejaVu Sans Mono",
        monospace;
}}


/* ═════════════════════════════════════════════════════════════
   ITERATION BADGE
   ═════════════════════════════════════════════════════════════ */

QLabel#IterationBadge {{
    background: {C_DEEP};

    color: #FFFFFF;

    border-radius: 6px;

    padding: 4px 9px;

    font-size: 9pt;

    font-weight: bold;
}}


/* ═════════════════════════════════════════════════════════════
   ITERATION CURRENT ROW
   ═════════════════════════════════════════════════════════════ */

QTableWidget::item[iteration="current"] {{
    background: #DBEAFE;

    color: {C_DEEP};

    font-weight: bold;
}}


/* ═════════════════════════════════════════════════════════════
   GRAPH / PLOT CARD
   ═════════════════════════════════════════════════════════════ */

QFrame#PlotCard {{
    background: #FFFFFF;

    border: 1px solid #E2E8F0;

    border-radius: 10px;
}}

QLabel#PlotTitle {{
    color: {C_DEEP};

    font-size: 10.5pt;

    font-weight: bold;
}}


/* ═════════════════════════════════════════════════════════════
   ALGORITHM HEADER
   ═════════════════════════════════════════════════════════════ */

QFrame#AlgorithmHeader {{
    background: #FFFFFF;

    border: 1px solid #E2E8F0;

    border-radius: 10px;
}}

QLabel#AlgorithmName {{
    color: {C_DEEP};

    font-size: 15pt;

    font-weight: bold;
}}

QLabel#AlgorithmDescription {{
    color: {C_TEXT_SECONDARY};

    font-size: 9.5pt;
}}


/* ═════════════════════════════════════════════════════════════
   STEPS HEADER
   ═════════════════════════════════════════════════════════════ */

QLabel#StepsTitle {{
    color: {C_DEEP};

    font-size: 11pt;

    font-weight: bold;
}}


/* ═════════════════════════════════════════════════════════════
   TABS
   ═════════════════════════════════════════════════════════════ */

QTabWidget::pane {{
    border: 1px solid #CBD5E1;

    background: #FFFFFF;

    border-radius: 9px;

    border-top-left-radius: 0;
}}

QTabBar::tab {{
    padding: 10px 22px;

    background: transparent;

    color: #64748B;

    font-size: 10pt;

    border-bottom: 2px solid transparent;

    margin-right: 3px;

    border-top-left-radius: 7px;

    border-top-right-radius: 7px;
}}

QTabBar::tab:hover:!selected {{
    color: {C_MID};

    background: rgba(37, 99, 235, 0.05);

    border-bottom: 2px solid {C_SOFT};
}}

QTabBar::tab:selected {{
    color: {C_DEEP};

    background: #EFF6FF;

    border-bottom: 2px solid {C_MID};

    font-weight: bold;
}}


/* ═════════════════════════════════════════════════════════════
   GROUP BOX
   ═════════════════════════════════════════════════════════════ */

QGroupBox {{
    background: #FFFFFF;

    border: 1px solid #E2E8F0;

    border-radius: 9px;

    margin-top: 14px;

    padding: 12px;
}}

QGroupBox::title {{
    subcontrol-origin: margin;

    left: 12px;

    padding: 0 7px;

    color: {C_DEEP};

    background: #FFFFFF;

    font-weight: bold;
}}


/* ═════════════════════════════════════════════════════════════
   PROGRESS BAR
   ═════════════════════════════════════════════════════════════ */

QProgressBar {{
    background: #E2E8F0;

    border: none;

    border-radius: 5px;

    height: 9px;

    text-align: center;
}}

QProgressBar::chunk {{
    background: {C_MID};

    border-radius: 5px;
}}


/* ═════════════════════════════════════════════════════════════
   CHECK BOX
   ═════════════════════════════════════════════════════════════ */

QCheckBox {{
    color: {C_TEXT_PRIMARY};

    spacing: 8px;
}}

QCheckBox::indicator {{
    width: 17px;

    height: 17px;

    border-radius: 4px;

    border: 1px solid #CBD5E1;

    background: #FFFFFF;
}}

QCheckBox::indicator:hover {{
    border-color: {C_MID};
}}

QCheckBox::indicator:checked {{
    background: {C_MID};

    border-color: {C_MID};
}}


/* ═════════════════════════════════════════════════════════════
   RADIO BUTTON
   ═════════════════════════════════════════════════════════════ */

QRadioButton {{
    color: {C_TEXT_PRIMARY};

    spacing: 8px;
}}

QRadioButton::indicator {{
    width: 17px;

    height: 17px;

    border-radius: 9px;

    border: 1px solid #CBD5E1;

    background: #FFFFFF;
}}

QRadioButton::indicator:hover {{
    border-color: {C_MID};
}}

QRadioButton::indicator:checked {{
    background: {C_MID};

    border: 4px solid #FFFFFF;

    outline: 1px solid {C_MID};
}}


/* ═════════════════════════════════════════════════════════════
   TOOLTIP
   ═════════════════════════════════════════════════════════════ */

QToolTip {{
    background: {C_DEEP};

    color: #FFFFFF;

    border: 1px solid #243B53;

    padding: 6px 9px;

    border-radius: 5px;

    font-size: 9pt;
}}


/* ═════════════════════════════════════════════════════════════
   MENU
   ═════════════════════════════════════════════════════════════ */

QMenu {{
    background: #FFFFFF;

    border: 1px solid #CBD5E1;

    padding: 5px;

    border-radius: 7px;
}}

QMenu::item {{
    padding: 7px 25px 7px 12px;

    border-radius: 5px;
}}

QMenu::item:selected {{
    background: #EFF6FF;

    color: {C_DEEP};
}}


/* ═════════════════════════════════════════════════════════════
   SEPARATOR
   ═════════════════════════════════════════════════════════════ */

QFrame#Separator {{
    background: #E2E8F0;

    max-height: 1px;
}}

"""


# ══════════════════════════════════════════════════════════════
#  EXPORT
# ══════════════════════════════════════════════════════════════

__all__ = [
    "C_DEEP",
    "C_MID",
    "C_MUTED",
    "C_SOFT",

    "C_BG_PAGE",
    "C_BG_CARD",
    "C_BG_INPUT",
    "C_BG_ALT",

    "C_SIDEBAR_BG",
    "C_SIDEBAR_HEADER",
    "C_SIDEBAR_BORDER",
    "C_SIDEBAR_TEXT",
    "C_SIDEBAR_DIM",
    "C_SIDEBAR_HOVER",
    "C_SIDEBAR_ACTIVE",

    "C_SUCCESS_BG",
    "C_SUCCESS_FG",
    "C_SUCCESS_BORDER",

    "C_WARNING_BG",
    "C_WARNING_FG",
    "C_WARNING_BORDER",

    "C_ERROR_BG",
    "C_ERROR_FG",
    "C_ERROR_BORDER",

    "C_NEUTRAL_BG",
    "C_NEUTRAL_FG",
    "C_NEUTRAL_BORDER",

    "C_TEXT_PRIMARY",
    "C_TEXT_SECONDARY",

    "CHART_CURVE",
    "CHART_POINT",
    "CHART_GUIDE",
    "CHART_AXIS",
    "CHART_FILL",

    "C_RESULT_BG",
    "C_RESULT_BORDER",
    "C_RESULT_FG",

    "STYLESHEET",
]