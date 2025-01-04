from __future__ import annotations

from typing import Any, Callable, Dict, Iterable, List, Union, overload

import numpy as np
from PySide.QtGui import QIcon, QKeySequence
from PySide.QtWidgets import (
    QToolButton,
    QWidget,
    QHBoxLayout,
    QFrame,
    QListWidget,
    QVBoxLayout,
    QLabel,
    QGridLayout,
    QComboBox,
    QFontComboBox,
    QLineEdit,
    QTextEdit,
    QPlainTextEdit,
    QProgressBar,
    QSlider,
    QSpinBox,
    QDoubleSpinBox,
    QDateTimeEdit,
    QDateEdit,
    QTimeEdit,
    QTableWidget,
    QTreeWidget,
    QCalendarWidget,
)
from PySide.QtCore import (
    Qt,
    Signal,
    QKeyCombination,
)

from .constants import ColumnWise, Large, RibbonButtonStyle, RibbonSpaceFindMode, Small
from .gallery import RibbonGallery
from .separator import RibbonSeparator
from .toolbutton import RibbonToolButton

class RibbonPanelTitle(QLabel): ...

class RibbonGridLayoutManager(object):
    rows: int
    cells: np.ndarray

    def __init__(self, rows: int): ...
    def request_cells(
        self, rowSpan: int = 1, colSpan: int = 1, mode: RibbonSpaceFindMode = ColumnWise
    ): ...

class RibbonPanelItemWidget(QFrame):
    def __init__(self, parent=None): ...
    def addWidget(self, widget): ...

class RibbonPanelOptionButton(QToolButton): ...

class RibbonPanel(QFrame):
    _maxRows: int = 6
    _largeRows: int = 6
    _mediumRows: int = 3
    _smallRows: int = 2
    _gridLayoutManager: RibbonGridLayoutManager
    _showPanelOptionButton: bool

    _widgets: List[QWidget] = []

    _titleHeight: int = 20

    panelOptionClicked = Signal(bool)

    _mainLayout: QVBoxLayout
    _actionsLayout: QGridLayout
    _titleWidget: QWidget
    _titleLayout: QHBoxLayout
    _titleLabel: RibbonPanelTitle
    _panelOption: RibbonPanelOptionButton

    @overload
    def __init__(
        self, title: str = "", maxRows: int = 6, showPanelOptionButton=True, parent=None
    ): ...
    @overload
    def __init__(self, parent=None): ...
    def __init__(self, *args, **kwargs): ...
    def maximumRows(self) -> int: ...
    def largeRows(self) -> int: ...
    def mediumRows(self) -> int: ...
    def smallRows(self) -> int: ...
    def setMaximumRows(self, maxRows: int): ...
    def setLargeRows(self, rows: int): ...
    def setMediumRows(self, rows: int): ...
    def setSmallRows(self, rows: int): ...
    def defaultRowSpan(self, rowSpan: Union[int, RibbonButtonStyle]) -> int: ...
    def panelOptionButton(self) -> RibbonPanelOptionButton: ...
    def setPanelOptionToolTip(self, text: str): ...
    def rowHeight(self) -> int: ...
    def setTitle(self, title: str): ...
    def title(self) -> str: ...
    def setTitleHeight(self, height: int): ...
    def titleHeight(self) -> int: ...
    def addWidgetsBy(self, data: Dict[str, Dict]) -> Dict[str, QWidget]: ...
    def addWidget(
        self,
        widget: QWidget,
        *,
        rowSpan: Union[int, RibbonButtonStyle] = Small,
        colSpan: int = 1,
        mode: RibbonSpaceFindMode = ColumnWise,
        alignment: Qt.AlignmentFlag = Qt.AlignmentFlag.AlignCenter,
        fixedHeight: Union[bool, float] = False,
    ) -> QWidget | Any: ...
    def addSmallWidget(
        self,
        widget: QWidget,
        *,
        colSpan: int = 1,
        mode: RibbonSpaceFindMode = ColumnWise,
        alignment: Qt.AlignmentFlag = Qt.AlignmentFlag.AlignCenter,
        fixedHeight: Union[bool, float] = False,
    ) -> QWidget | Any: ...
    def addMediumWidget(
        self,
        widget: QWidget,
        *,
        colSpan: int = 1,
        mode: RibbonSpaceFindMode = ColumnWise,
        alignment: Qt.AlignmentFlag = Qt.AlignmentFlag.AlignCenter,
        fixedHeight: Union[bool, float] = False,
    ) -> QWidget | Any: ...
    def addLargeWidget(
        self,
        widget: QWidget,
        *,
        colSpan: int = 1,
        mode: RibbonSpaceFindMode = ColumnWise,
        alignment: Qt.AlignmentFlag = Qt.AlignmentFlag.AlignCenter,
        fixedHeight: Union[bool, float] = False,
    ) -> QWidget | Any: ...
    def removeWidget(self, widget: QWidget): ...
    def widget(self, index: int) -> QWidget: ...
    def widgets(self) -> List[QWidget]: ...
    def addButton(
        self,
        text: str = None,
        icon: QIcon = None,
        showText: bool = True,
        slot: Callable = None,
        shortcut: (
            Qt.Key
            | QKeySequence
            | QKeyCombination
            | QKeySequence.StandardKey
            | str
            | int
        ) = None,
        tooltip: str = None,
        statusTip: str = None,
        checkable: bool = False,
        *,
        rowSpan: RibbonButtonStyle = Large,
        colSpan: int = 1,
        mode: RibbonSpaceFindMode = ColumnWise,
        alignment: Qt.AlignmentFlag = Qt.AlignmentFlag.AlignCenter,
        fixedHeight: Union[bool, float] = False,
    ) -> RibbonToolButton: ...
    def addSmallButton(
        self,
        text: str = None,
        icon: QIcon = None,
        showText: bool = True,
        slot: Callable = None,
        shortcut: (
            Qt.Key
            | QKeySequence
            | QKeyCombination
            | QKeySequence.StandardKey
            | str
            | int
        ) = None,
        tooltip: str = None,
        statusTip: str = None,
        checkable: bool = False,
        *,
        colSpan: int = 1,
        mode: RibbonSpaceFindMode = ColumnWise,
        alignment: Qt.AlignmentFlag = Qt.AlignmentFlag.AlignCenter,
        fixedHeight: Union[bool, float] = False,
    ) -> RibbonToolButton: ...
    def addMediumButton(
        self,
        text: str = None,
        icon: QIcon = None,
        showText: bool = True,
        slot: Callable = None,
        shortcut: (
            Qt.Key
            | QKeySequence
            | QKeyCombination
            | QKeySequence.StandardKey
            | str
            | int
        ) = None,
        tooltip: str = None,
        statusTip: str = None,
        checkable: bool = False,
        *,
        colSpan: int = 1,
        mode: RibbonSpaceFindMode = ColumnWise,
        alignment: Qt.AlignmentFlag = Qt.AlignmentFlag.AlignCenter,
        fixedHeight: Union[bool, float] = False,
    ) -> RibbonToolButton: ...
    def addLargeButton(
        self,
        text: str = None,
        icon: QIcon = None,
        showText: bool = True,
        slot: Callable = None,
        shortcut: (
            Qt.Key
            | QKeySequence
            | QKeyCombination
            | QKeySequence.StandardKey
            | str
            | int
        ) = None,
        tooltip: str = None,
        statusTip: str = None,
        checkable: bool = False,
        *,
        colSpan: int = 1,
        mode: RibbonSpaceFindMode = ColumnWise,
        alignment: Qt.AlignmentFlag = Qt.AlignmentFlag.AlignCenter,
        fixedHeight: Union[bool, float] = False,
    ) -> RibbonToolButton: ...
    def addToggleButton(
        self,
        text: str = None,
        icon: QIcon = None,
        showText: bool = True,
        slot: Callable = None,
        shortcut: (
            Qt.Key
            | QKeySequence
            | QKeyCombination
            | QKeySequence.StandardKey
            | str
            | int
        ) = None,
        tooltip: str = None,
        statusTip: str = None,
        *,
        rowSpan: RibbonButtonStyle = Large,
        colSpan: int = 1,
        mode: RibbonSpaceFindMode = ColumnWise,
        alignment: Qt.AlignmentFlag = Qt.AlignmentFlag.AlignCenter,
        fixedHeight: Union[bool, float] = False,
    ) -> RibbonToolButton: ...
    def addSmallToggleButton(
        self,
        text: str = None,
        icon: QIcon = None,
        showText: bool = True,
        slot: Callable = None,
        shortcut: (
            Qt.Key
            | QKeySequence
            | QKeyCombination
            | QKeySequence.StandardKey
            | str
            | int
        ) = None,
        tooltip: str = None,
        statusTip: str = None,
        *,
        colSpan: int = 1,
        mode: RibbonSpaceFindMode = ColumnWise,
        alignment: Qt.AlignmentFlag = Qt.AlignmentFlag.AlignCenter,
        fixedHeight: Union[bool, float] = False,
    ) -> RibbonToolButton: ...
    def addMediumToggleButton(
        self,
        text: str = None,
        icon: QIcon = None,
        showText: bool = True,
        slot: Callable = None,
        shortcut: (
            Qt.Key
            | QKeySequence
            | QKeyCombination
            | QKeySequence.StandardKey
            | str
            | int
        ) = None,
        tooltip: str = None,
        statusTip: str = None,
        *,
        colSpan: int = 1,
        mode: RibbonSpaceFindMode = ColumnWise,
        alignment: Qt.AlignmentFlag = Qt.AlignmentFlag.AlignCenter,
        fixedHeight: Union[bool, float] = False,
    ) -> RibbonToolButton: ...
    def addLargeToggleButton(
        self,
        text: str = None,
        icon: QIcon = None,
        showText: bool = True,
        slot: Callable = None,
        shortcut: (
            Qt.Key
            | QKeySequence
            | QKeyCombination
            | QKeySequence.StandardKey
            | str
            | int
        ) = None,
        tooltip: str = None,
        statusTip: str = None,
        *,
        colSpan: int = 1,
        mode: RibbonSpaceFindMode = ColumnWise,
        alignment: Qt.AlignmentFlag = Qt.AlignmentFlag.AlignCenter,
        fixedHeight: Union[bool, float] = False,
    ) -> RibbonToolButton: ...

    ribbonArguments = ["rowSpan", "colSpan", "mode", "alignment", "fixedHeight"]

    def _addAnyWidget(
        self,
        *args,
        cls,
        initializer: Callable = None,
        rowSpan: Union[int, RibbonButtonStyle] = Small,
        colSpan: int = 1,
        mode: RibbonSpaceFindMode = ColumnWise,
        alignment: Qt.AlignmentFlag = Qt.AlignmentFlag.AlignCenter,
        fixedHeight: Union[bool, float] = False,
        **kwargs,
    ) -> QWidget: ...
    def __getattr__(self, method: str) -> Callable: ...
    def addComboBox(
        self,
        items: Iterable[str],
        *,
        rowSpan: Union[int, RibbonButtonStyle] = Small,
        colSpan: int = 1,
        mode: RibbonSpaceFindMode = ColumnWise,
        alignment: Qt.AlignmentFlag = Qt.AlignmentFlag.AlignCenter,
        fixedHeight: Union[bool, float] = False,
    ) -> QComboBox: ...
    addSmallComboBox = RibbonPanel.addComboBox
    addMediumComboBox = RibbonPanel.addComboBox
    addLargeComboBox = RibbonPanel.addComboBox
    def addFontComboBox(
        self,
        *,
        rowSpan: Union[int, RibbonButtonStyle] = Small,
        colSpan: int = 1,
        mode: RibbonSpaceFindMode = ColumnWise,
        alignment: Qt.AlignmentFlag = Qt.AlignmentFlag.AlignCenter,
        fixedHeight: Union[bool, float] = False,
    ) -> QFontComboBox: ...
    addSmallFontComboBox = RibbonPanel.addFontComboBox
    addMediumFontComboBox = RibbonPanel.addFontComboBox
    addLargeFontComboBox = RibbonPanel.addFontComboBox
    def addLineEdit(
        self,
        *,
        rowSpan: Union[int, RibbonButtonStyle] = Small,
        colSpan: int = 1,
        mode: RibbonSpaceFindMode = ColumnWise,
        alignment: Qt.AlignmentFlag = Qt.AlignmentFlag.AlignCenter,
        fixedHeight: Union[bool, float] = False,
    ) -> QLineEdit: ...
    addSmallLineEdit = RibbonPanel.addLineEdit
    addMediumLineEdit = RibbonPanel.addLineEdit
    addLargeLineEdit = RibbonPanel.addLineEdit
    def addTextEdit(
        self,
        *,
        rowSpan: Union[int, RibbonButtonStyle] = Small,
        colSpan: int = 1,
        mode: RibbonSpaceFindMode = ColumnWise,
        alignment: Qt.AlignmentFlag = Qt.AlignmentFlag.AlignCenter,
        fixedHeight: Union[bool, float] = False,
    ) -> QTextEdit: ...
    addSmallTextEdit = RibbonPanel.addTextEdit
    addMediumTextEdit = RibbonPanel.addTextEdit
    addLargeTextEdit = RibbonPanel.addTextEdit
    def addPlainTextEdit(
        self,
        *,
        rowSpan: Union[int, RibbonButtonStyle] = Small,
        colSpan: int = 1,
        mode: RibbonSpaceFindMode = ColumnWise,
        alignment: Qt.AlignmentFlag = Qt.AlignmentFlag.AlignCenter,
        fixedHeight: Union[bool, float] = False,
    ) -> QPlainTextEdit: ...
    addSmallPlainTextEdit = RibbonPanel.addPlainTextEdit
    addMediumPlainTextEdit = RibbonPanel.addPlainTextEdit
    addLargePlainTextEdit = RibbonPanel.addPlainTextEdit
    def addLabel(
        self,
        text: str,
        *,
        rowSpan: Union[int, RibbonButtonStyle] = Small,
        colSpan: int = 1,
        mode: RibbonSpaceFindMode = ColumnWise,
        alignment: Qt.AlignmentFlag = Qt.AlignmentFlag.AlignCenter,
        fixedHeight: Union[bool, float] = False,
    ) -> QLabel: ...
    addSmallLabel = RibbonPanel.addLabel
    addMediumLabel = RibbonPanel.addLabel
    addLargeLabel = RibbonPanel.addLabel
    def addProgressBar(
        self,
        *,
        rowSpan: Union[int, RibbonButtonStyle] = Small,
        colSpan: int = 1,
        mode: RibbonSpaceFindMode = ColumnWise,
        alignment: Qt.AlignmentFlag = Qt.AlignmentFlag.AlignCenter,
        fixedHeight: Union[bool, float] = False,
    ) -> QProgressBar: ...
    addSmallProgressBar = RibbonPanel.addProgressBar
    addMediumProgressBar = RibbonPanel.addProgressBar
    addLargeProgressBar = RibbonPanel.addProgressBar
    def addSlider(
        self,
        *,
        rowSpan: Union[int, RibbonButtonStyle] = Small,
        colSpan: int = 1,
        mode: RibbonSpaceFindMode = ColumnWise,
        alignment: Qt.AlignmentFlag = Qt.AlignmentFlag.AlignCenter,
        fixedHeight: Union[bool, float] = False,
    ) -> QSlider: ...
    addSmallSlider = RibbonPanel.addSlider
    addMediumSlider = RibbonPanel.addSlider
    addLargeSlider = RibbonPanel.addSlider
    def addSpinBox(
        self,
        *,
        rowSpan: Union[int, RibbonButtonStyle] = Small,
        colSpan: int = 1,
        mode: RibbonSpaceFindMode = ColumnWise,
        alignment: Qt.AlignmentFlag = Qt.AlignmentFlag.AlignCenter,
        fixedHeight: Union[bool, float] = False,
    ) -> QSpinBox: ...
    addSmallSpinBox = RibbonPanel.addSpinBox
    addMediumSpinBox = RibbonPanel.addSpinBox
    addLargeSpinBox = RibbonPanel.addSpinBox
    def addDoubleSpinBox(
        self,
        *,
        rowSpan: Union[int, RibbonButtonStyle] = Small,
        colSpan: int = 1,
        mode: RibbonSpaceFindMode = ColumnWise,
        alignment: Qt.AlignmentFlag = Qt.AlignmentFlag.AlignCenter,
        fixedHeight: Union[bool, float] = False,
    ) -> QDoubleSpinBox: ...
    addSmallDoubleSpinBox = RibbonPanel.addDoubleSpinBox
    addMediumDoubleSpinBox = RibbonPanel.addDoubleSpinBox
    addLargeDoubleSpinBox = RibbonPanel.addDoubleSpinBox
    def addDateEdit(
        self,
        *,
        rowSpan: Union[int, RibbonButtonStyle] = Small,
        colSpan: int = 1,
        mode: RibbonSpaceFindMode = ColumnWise,
        alignment: Qt.AlignmentFlag = Qt.AlignmentFlag.AlignCenter,
        fixedHeight: Union[bool, float] = False,
    ) -> QDateEdit: ...
    addSmallDateEdit = RibbonPanel.addDateEdit
    addMediumDateEdit = RibbonPanel.addDateEdit
    addLargeDateEdit = RibbonPanel.addDateEdit
    def addTimeEdit(
        self,
        *,
        rowSpan: Union[int, RibbonButtonStyle] = Small,
        colSpan: int = 1,
        mode: RibbonSpaceFindMode = ColumnWise,
        alignment: Qt.AlignmentFlag = Qt.AlignmentFlag.AlignCenter,
        fixedHeight: Union[bool, float] = False,
    ) -> QTimeEdit: ...
    addSmallTimeEdit = RibbonPanel.addTimeEdit
    addMediumTimeEdit = RibbonPanel.addTimeEdit
    addLargeTimeEdit = RibbonPanel.addTimeEdit
    def addDateTimeEdit(
        self,
        *,
        rowSpan: Union[int, RibbonButtonStyle] = Small,
        colSpan: int = 1,
        mode: RibbonSpaceFindMode = ColumnWise,
        alignment: Qt.AlignmentFlag = Qt.AlignmentFlag.AlignCenter,
        fixedHeight: Union[bool, float] = False,
    ) -> QDateTimeEdit: ...
    addSmallDateTimeEdit = RibbonPanel.addDateTimeEdit
    addMediumDateTimeEdit = RibbonPanel.addDateTimeEdit
    addLargeDateTimeEdit = RibbonPanel.addDateTimeEdit
    def addTableWidget(
        self,
        *,
        rowSpan: Union[int, RibbonButtonStyle] = Large,
        colSpan: int = 1,
        mode: RibbonSpaceFindMode = ColumnWise,
        alignment: Qt.AlignmentFlag = Qt.AlignmentFlag.AlignCenter,
        fixedHeight: Union[bool, float] = False,
    ) -> QTableWidget: ...
    addSmallTableWidget = RibbonPanel.addTableWidget
    addMediumTableWidget = RibbonPanel.addTableWidget
    addLargeTableWidget = RibbonPanel.addTableWidget
    def addTreeWidget(
        self,
        *,
        rowSpan: Union[int, RibbonButtonStyle] = Large,
        colSpan: int = 1,
        mode: RibbonSpaceFindMode = ColumnWise,
        alignment: Qt.AlignmentFlag = Qt.AlignmentFlag.AlignCenter,
        fixedHeight: Union[bool, float] = False,
    ) -> QTreeWidget: ...
    addSmallTreeWidget = RibbonPanel.addTreeWidget
    addMediumTreeWidget = RibbonPanel.addTreeWidget
    addLargeTreeWidget = RibbonPanel.addTreeWidget
    def addListWidget(
        self,
        *,
        rowSpan: Union[int, RibbonButtonStyle] = Large,
        colSpan: int = 1,
        mode: RibbonSpaceFindMode = ColumnWise,
        alignment: Qt.AlignmentFlag = Qt.AlignmentFlag.AlignCenter,
        fixedHeight: Union[bool, float] = False,
    ) -> QListWidget: ...
    addSmallListWidget = RibbonPanel.addListWidget
    addMediumListWidget = RibbonPanel.addListWidget
    addLargeListWidget = RibbonPanel.addListWidget
    def addCalendarWidget(
        self,
        *,
        rowSpan: Union[int, RibbonButtonStyle] = Large,
        colSpan: int = 1,
        mode: RibbonSpaceFindMode = ColumnWise,
        alignment: Qt.AlignmentFlag = Qt.AlignmentFlag.AlignCenter,
        fixedHeight: Union[bool, float] = False,
    ) -> QCalendarWidget: ...
    addSmallCalendarWidget = RibbonPanel.addCalendarWidget
    addMediumCalendarWidget = RibbonPanel.addCalendarWidget
    addLargeCalendarWidget = RibbonPanel.addCalendarWidget
    def addSeparator(
        self,
        orientation=Qt.Orientation.Vertical,
        width=6,
        *,
        rowSpan: Union[int, RibbonButtonStyle] = Large,
        colSpan: int = 1,
        mode: RibbonSpaceFindMode = ColumnWise,
        alignment: Qt.AlignmentFlag = Qt.AlignmentFlag.AlignCenter,
        fixedHeight: Union[bool, float] = False,
    ) -> RibbonSeparator: ...
    addSmallSeparator = RibbonPanel.addSeparator
    addMediumSeparator = RibbonPanel.addSeparator
    addLargeSeparator = RibbonPanel.addSeparator
    def addHorizontalSeparator(
        self,
        width=6,
        *,
        rowSpan: Union[int, RibbonButtonStyle] = Small,
        colSpan: int = 2,
        mode: RibbonSpaceFindMode = ColumnWise,
        alignment: Qt.AlignmentFlag = Qt.AlignmentFlag.AlignCenter,
        fixedHeight: Union[bool, float] = False,
    ) -> RibbonSeparator: ...
    addSmallHorizontalSeparator = RibbonPanel.addHorizontalSeparator
    addMediumHorizontalSeparator = RibbonPanel.addHorizontalSeparator
    addLargeHorizontalSeparator = RibbonPanel.addHorizontalSeparator
    def addVerticalSeparator(
        self,
        width=6,
        *,
        rowSpan: Union[int, RibbonButtonStyle] = Large,
        colSpan: int = 1,
        mode: RibbonSpaceFindMode = ColumnWise,
        alignment: Qt.AlignmentFlag = Qt.AlignmentFlag.AlignCenter,
        fixedHeight: Union[bool, float] = False,
    ) -> RibbonSeparator: ...
    addSmallVerticalSeparator = RibbonPanel.addVerticalSeparator
    addMediumVerticalSeparator = RibbonPanel.addVerticalSeparator
    addLargeVerticalSeparator = RibbonPanel.addVerticalSeparator
    def addGallery(
        self,
        minimumWidth=800,
        popupHideOnClick=False,
        *,
        rowSpan: Union[int, RibbonButtonStyle] = Large,
        colSpan: int = 1,
        mode: RibbonSpaceFindMode = ColumnWise,
        alignment: Qt.AlignmentFlag = Qt.AlignmentFlag.AlignCenter,
        fixedHeight: Union[bool, float] = False,
    ) -> RibbonGallery: ...
    addSmallGallery = RibbonPanel.addGallery
    addMediumGallery = RibbonPanel.addGallery
    addLargeGallery = RibbonPanel.addGallery
