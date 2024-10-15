from __future__ import annotations

from typing import Any, Callable, Dict, Iterable, List, Union, overload

import numpy as np
from PySide import QtCore, QtGui, QtWidgets

from .constants import ColumnWise, Large, RibbonButtonStyle, RibbonSpaceFindMode, Small
from .gallery import RibbonGallery
from .separator import RibbonSeparator
from .toolbutton import RibbonToolButton

class RibbonPanelTitle(QtWidgets.QLabel): ...

class RibbonGridLayoutManager(object):
    rows: int
    cells: np.ndarray

    def __init__(self, rows: int): ...
    def request_cells(self, rowSpan: int = 1, colSpan: int = 1, mode: RibbonSpaceFindMode = ColumnWise): ...

class RibbonPanelItemWidget(QtWidgets.QFrame):
    def __init__(self, parent=None): ...
    def addWidget(self, widget): ...

class RibbonPanelOptionButton(QtWidgets.QToolButton): ...

class RibbonPanel(QtWidgets.QFrame):
    _maxRows: int = 6
    _largeRows: int = 6
    _mediumRows: int = 3
    _smallRows: int = 2
    _gridLayoutManager: RibbonGridLayoutManager
    _showPanelOptionButton: bool

    _widgets: List[QtWidgets.QWidget] = []

    _titleHeight: int = 20

    panelOptionClicked = QtCore.Signal(bool)

    _mainLayout: QtWidgets.QVBoxLayout
    _actionsLayout: QtWidgets.QGridLayout
    _titleWidget: QtWidgets.QWidget
    _titleLayout: QtWidgets.QHBoxLayout
    _titleLabel: RibbonPanelTitle
    _panelOption: RibbonPanelOptionButton

    @overload
    def __init__(self, title: str = "", maxRows: int = 6, showPanelOptionButton=True, parent=None): ...
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
    def addWidgetsBy(self, data: Dict[str, Dict]) -> Dict[str, QtWidgets.QWidget]: ...
    def addWidget(
        self,
        widget: QtWidgets.QWidget,
        *,
        rowSpan: Union[int, RibbonButtonStyle] = Small,
        colSpan: int = 1,
        mode: RibbonSpaceFindMode = ColumnWise,
        alignment: QtCore.Qt.AlignmentFlag = QtCore.Qt.AlignmentFlag.AlignCenter,
        fixedHeight: Union[bool, float] = False,
    ) -> QtWidgets.QWidget | Any: ...
    def addSmallWidget(
        self,
        widget: QtWidgets.QWidget,
        *,
        colSpan: int = 1,
        mode: RibbonSpaceFindMode = ColumnWise,
        alignment: QtCore.Qt.AlignmentFlag = QtCore.Qt.AlignmentFlag.AlignCenter,
        fixedHeight: Union[bool, float] = False,
    ) -> QtWidgets.QWidget | Any: ...
    def addMediumWidget(
        self,
        widget: QtWidgets.QWidget,
        *,
        colSpan: int = 1,
        mode: RibbonSpaceFindMode = ColumnWise,
        alignment: QtCore.Qt.AlignmentFlag = QtCore.Qt.AlignmentFlag.AlignCenter,
        fixedHeight: Union[bool, float] = False,
    ) -> QtWidgets.QWidget | Any: ...
    def addLargeWidget(
        self,
        widget: QtWidgets.QWidget,
        *,
        colSpan: int = 1,
        mode: RibbonSpaceFindMode = ColumnWise,
        alignment: QtCore.Qt.AlignmentFlag = QtCore.Qt.AlignmentFlag.AlignCenter,
        fixedHeight: Union[bool, float] = False,
    ) -> QtWidgets.QWidget | Any: ...
    def removeWidget(self, widget: QtWidgets.QWidget): ...
    def widget(self, index: int) -> QtWidgets.QWidget: ...
    def widgets(self) -> List[QtWidgets.QWidget]: ...
    def addButton(
        self,
        text: str = None,
        icon: QtGui.QIcon = None,
        showText: bool = True,
        slot: Callable = None,
        shortcut: (
            QtCore.Qt.Key | QtGui.QKeySequence | QtCore.QKeyCombination | QtGui.QKeySequence.StandardKey | str | int
        ) = None,
        tooltip: str = None,
        statusTip: str = None,
        checkable: bool = False,
        *,
        rowSpan: RibbonButtonStyle = Large,
        colSpan: int = 1,
        mode: RibbonSpaceFindMode = ColumnWise,
        alignment: QtCore.Qt.AlignmentFlag = QtCore.Qt.AlignmentFlag.AlignCenter,
        fixedHeight: Union[bool, float] = False,
    ) -> RibbonToolButton: ...
    def addSmallButton(
        self,
        text: str = None,
        icon: QtGui.QIcon = None,
        showText: bool = True,
        slot: Callable = None,
        shortcut: (
            QtCore.Qt.Key | QtGui.QKeySequence | QtCore.QKeyCombination | QtGui.QKeySequence.StandardKey | str | int
        ) = None,
        tooltip: str = None,
        statusTip: str = None,
        checkable: bool = False,
        *,
        colSpan: int = 1,
        mode: RibbonSpaceFindMode = ColumnWise,
        alignment: QtCore.Qt.AlignmentFlag = QtCore.Qt.AlignmentFlag.AlignCenter,
        fixedHeight: Union[bool, float] = False,
    ) -> RibbonToolButton: ...
    def addMediumButton(
        self,
        text: str = None,
        icon: QtGui.QIcon = None,
        showText: bool = True,
        slot: Callable = None,
        shortcut: (
            QtCore.Qt.Key | QtGui.QKeySequence | QtCore.QKeyCombination | QtGui.QKeySequence.StandardKey | str | int
        ) = None,
        tooltip: str = None,
        statusTip: str = None,
        checkable: bool = False,
        *,
        colSpan: int = 1,
        mode: RibbonSpaceFindMode = ColumnWise,
        alignment: QtCore.Qt.AlignmentFlag = QtCore.Qt.AlignmentFlag.AlignCenter,
        fixedHeight: Union[bool, float] = False,
    ) -> RibbonToolButton: ...
    def addLargeButton(
        self,
        text: str = None,
        icon: QtGui.QIcon = None,
        showText: bool = True,
        slot: Callable = None,
        shortcut: (
            QtCore.Qt.Key | QtGui.QKeySequence | QtCore.QKeyCombination | QtGui.QKeySequence.StandardKey | str | int
        ) = None,
        tooltip: str = None,
        statusTip: str = None,
        checkable: bool = False,
        *,
        colSpan: int = 1,
        mode: RibbonSpaceFindMode = ColumnWise,
        alignment: QtCore.Qt.AlignmentFlag = QtCore.Qt.AlignmentFlag.AlignCenter,
        fixedHeight: Union[bool, float] = False,
    ) -> RibbonToolButton: ...
    def addToggleButton(
        self,
        text: str = None,
        icon: QtGui.QIcon = None,
        showText: bool = True,
        slot: Callable = None,
        shortcut: (
            QtCore.Qt.Key | QtGui.QKeySequence | QtCore.QKeyCombination | QtGui.QKeySequence.StandardKey | str | int
        ) = None,
        tooltip: str = None,
        statusTip: str = None,
        *,
        rowSpan: RibbonButtonStyle = Large,
        colSpan: int = 1,
        mode: RibbonSpaceFindMode = ColumnWise,
        alignment: QtCore.Qt.AlignmentFlag = QtCore.Qt.AlignmentFlag.AlignCenter,
        fixedHeight: Union[bool, float] = False,
    ) -> RibbonToolButton: ...
    def addSmallToggleButton(
        self,
        text: str = None,
        icon: QtGui.QIcon = None,
        showText: bool = True,
        slot: Callable = None,
        shortcut: (
            QtCore.Qt.Key | QtGui.QKeySequence | QtCore.QKeyCombination | QtGui.QKeySequence.StandardKey | str | int
        ) = None,
        tooltip: str = None,
        statusTip: str = None,
        *,
        colSpan: int = 1,
        mode: RibbonSpaceFindMode = ColumnWise,
        alignment: QtCore.Qt.AlignmentFlag = QtCore.Qt.AlignmentFlag.AlignCenter,
        fixedHeight: Union[bool, float] = False,
    ) -> RibbonToolButton: ...
    def addMediumToggleButton(
        self,
        text: str = None,
        icon: QtGui.QIcon = None,
        showText: bool = True,
        slot: Callable = None,
        shortcut: (
            QtCore.Qt.Key | QtGui.QKeySequence | QtCore.QKeyCombination | QtGui.QKeySequence.StandardKey | str | int
        ) = None,
        tooltip: str = None,
        statusTip: str = None,
        *,
        colSpan: int = 1,
        mode: RibbonSpaceFindMode = ColumnWise,
        alignment: QtCore.Qt.AlignmentFlag = QtCore.Qt.AlignmentFlag.AlignCenter,
        fixedHeight: Union[bool, float] = False,
    ) -> RibbonToolButton: ...
    def addLargeToggleButton(
        self,
        text: str = None,
        icon: QtGui.QIcon = None,
        showText: bool = True,
        slot: Callable = None,
        shortcut: (
            QtCore.Qt.Key | QtGui.QKeySequence | QtCore.QKeyCombination | QtGui.QKeySequence.StandardKey | str | int
        ) = None,
        tooltip: str = None,
        statusTip: str = None,
        *,
        colSpan: int = 1,
        mode: RibbonSpaceFindMode = ColumnWise,
        alignment: QtCore.Qt.AlignmentFlag = QtCore.Qt.AlignmentFlag.AlignCenter,
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
        alignment: QtCore.Qt.AlignmentFlag = QtCore.Qt.AlignmentFlag.AlignCenter,
        fixedHeight: Union[bool, float] = False,
        **kwargs,
    ) -> QtWidgets.QWidget: ...
    def __getattr__(self, method: str) -> Callable: ...
    def addComboBox(
        self,
        items: Iterable[str],
        *,
        rowSpan: Union[int, RibbonButtonStyle] = Small,
        colSpan: int = 1,
        mode: RibbonSpaceFindMode = ColumnWise,
        alignment: QtCore.Qt.AlignmentFlag = QtCore.Qt.AlignmentFlag.AlignCenter,
        fixedHeight: Union[bool, float] = False,
    ) -> QtWidgets.QComboBox: ...
    addSmallComboBox = RibbonPanel.addComboBox
    addMediumComboBox = RibbonPanel.addComboBox
    addLargeComboBox = RibbonPanel.addComboBox
    def addFontComboBox(
        self,
        *,
        rowSpan: Union[int, RibbonButtonStyle] = Small,
        colSpan: int = 1,
        mode: RibbonSpaceFindMode = ColumnWise,
        alignment: QtCore.Qt.AlignmentFlag = QtCore.Qt.AlignmentFlag.AlignCenter,
        fixedHeight: Union[bool, float] = False,
    ) -> QtWidgets.QFontComboBox: ...
    addSmallFontComboBox = RibbonPanel.addFontComboBox
    addMediumFontComboBox = RibbonPanel.addFontComboBox
    addLargeFontComboBox = RibbonPanel.addFontComboBox
    def addLineEdit(
        self,
        *,
        rowSpan: Union[int, RibbonButtonStyle] = Small,
        colSpan: int = 1,
        mode: RibbonSpaceFindMode = ColumnWise,
        alignment: QtCore.Qt.AlignmentFlag = QtCore.Qt.AlignmentFlag.AlignCenter,
        fixedHeight: Union[bool, float] = False,
    ) -> QtWidgets.QLineEdit: ...
    addSmallLineEdit = RibbonPanel.addLineEdit
    addMediumLineEdit = RibbonPanel.addLineEdit
    addLargeLineEdit = RibbonPanel.addLineEdit
    def addTextEdit(
        self,
        *,
        rowSpan: Union[int, RibbonButtonStyle] = Small,
        colSpan: int = 1,
        mode: RibbonSpaceFindMode = ColumnWise,
        alignment: QtCore.Qt.AlignmentFlag = QtCore.Qt.AlignmentFlag.AlignCenter,
        fixedHeight: Union[bool, float] = False,
    ) -> QtWidgets.QTextEdit: ...
    addSmallTextEdit = RibbonPanel.addTextEdit
    addMediumTextEdit = RibbonPanel.addTextEdit
    addLargeTextEdit = RibbonPanel.addTextEdit
    def addPlainTextEdit(
        self,
        *,
        rowSpan: Union[int, RibbonButtonStyle] = Small,
        colSpan: int = 1,
        mode: RibbonSpaceFindMode = ColumnWise,
        alignment: QtCore.Qt.AlignmentFlag = QtCore.Qt.AlignmentFlag.AlignCenter,
        fixedHeight: Union[bool, float] = False,
    ) -> QtWidgets.QPlainTextEdit: ...
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
        alignment: QtCore.Qt.AlignmentFlag = QtCore.Qt.AlignmentFlag.AlignCenter,
        fixedHeight: Union[bool, float] = False,
    ) -> QtWidgets.QLabel: ...
    addSmallLabel = RibbonPanel.addLabel
    addMediumLabel = RibbonPanel.addLabel
    addLargeLabel = RibbonPanel.addLabel
    def addProgressBar(
        self,
        *,
        rowSpan: Union[int, RibbonButtonStyle] = Small,
        colSpan: int = 1,
        mode: RibbonSpaceFindMode = ColumnWise,
        alignment: QtCore.Qt.AlignmentFlag = QtCore.Qt.AlignmentFlag.AlignCenter,
        fixedHeight: Union[bool, float] = False,
    ) -> QtWidgets.QProgressBar: ...
    addSmallProgressBar = RibbonPanel.addProgressBar
    addMediumProgressBar = RibbonPanel.addProgressBar
    addLargeProgressBar = RibbonPanel.addProgressBar
    def addSlider(
        self,
        *,
        rowSpan: Union[int, RibbonButtonStyle] = Small,
        colSpan: int = 1,
        mode: RibbonSpaceFindMode = ColumnWise,
        alignment: QtCore.Qt.AlignmentFlag = QtCore.Qt.AlignmentFlag.AlignCenter,
        fixedHeight: Union[bool, float] = False,
    ) -> QtWidgets.QSlider: ...
    addSmallSlider = RibbonPanel.addSlider
    addMediumSlider = RibbonPanel.addSlider
    addLargeSlider = RibbonPanel.addSlider
    def addSpinBox(
        self,
        *,
        rowSpan: Union[int, RibbonButtonStyle] = Small,
        colSpan: int = 1,
        mode: RibbonSpaceFindMode = ColumnWise,
        alignment: QtCore.Qt.AlignmentFlag = QtCore.Qt.AlignmentFlag.AlignCenter,
        fixedHeight: Union[bool, float] = False,
    ) -> QtWidgets.QSpinBox: ...
    addSmallSpinBox = RibbonPanel.addSpinBox
    addMediumSpinBox = RibbonPanel.addSpinBox
    addLargeSpinBox = RibbonPanel.addSpinBox
    def addDoubleSpinBox(
        self,
        *,
        rowSpan: Union[int, RibbonButtonStyle] = Small,
        colSpan: int = 1,
        mode: RibbonSpaceFindMode = ColumnWise,
        alignment: QtCore.Qt.AlignmentFlag = QtCore.Qt.AlignmentFlag.AlignCenter,
        fixedHeight: Union[bool, float] = False,
    ) -> QtWidgets.QDoubleSpinBox: ...
    addSmallDoubleSpinBox = RibbonPanel.addDoubleSpinBox
    addMediumDoubleSpinBox = RibbonPanel.addDoubleSpinBox
    addLargeDoubleSpinBox = RibbonPanel.addDoubleSpinBox
    def addDateEdit(
        self,
        *,
        rowSpan: Union[int, RibbonButtonStyle] = Small,
        colSpan: int = 1,
        mode: RibbonSpaceFindMode = ColumnWise,
        alignment: QtCore.Qt.AlignmentFlag = QtCore.Qt.AlignmentFlag.AlignCenter,
        fixedHeight: Union[bool, float] = False,
    ) -> QtWidgets.QDateEdit: ...
    addSmallDateEdit = RibbonPanel.addDateEdit
    addMediumDateEdit = RibbonPanel.addDateEdit
    addLargeDateEdit = RibbonPanel.addDateEdit
    def addTimeEdit(
        self,
        *,
        rowSpan: Union[int, RibbonButtonStyle] = Small,
        colSpan: int = 1,
        mode: RibbonSpaceFindMode = ColumnWise,
        alignment: QtCore.Qt.AlignmentFlag = QtCore.Qt.AlignmentFlag.AlignCenter,
        fixedHeight: Union[bool, float] = False,
    ) -> QtWidgets.QTimeEdit: ...
    addSmallTimeEdit = RibbonPanel.addTimeEdit
    addMediumTimeEdit = RibbonPanel.addTimeEdit
    addLargeTimeEdit = RibbonPanel.addTimeEdit
    def addDateTimeEdit(
        self,
        *,
        rowSpan: Union[int, RibbonButtonStyle] = Small,
        colSpan: int = 1,
        mode: RibbonSpaceFindMode = ColumnWise,
        alignment: QtCore.Qt.AlignmentFlag = QtCore.Qt.AlignmentFlag.AlignCenter,
        fixedHeight: Union[bool, float] = False,
    ) -> QtWidgets.QDateTimeEdit: ...
    addSmallDateTimeEdit = RibbonPanel.addDateTimeEdit
    addMediumDateTimeEdit = RibbonPanel.addDateTimeEdit
    addLargeDateTimeEdit = RibbonPanel.addDateTimeEdit
    def addTableWidget(
        self,
        *,
        rowSpan: Union[int, RibbonButtonStyle] = Large,
        colSpan: int = 1,
        mode: RibbonSpaceFindMode = ColumnWise,
        alignment: QtCore.Qt.AlignmentFlag = QtCore.Qt.AlignmentFlag.AlignCenter,
        fixedHeight: Union[bool, float] = False,
    ) -> QtWidgets.QTableWidget: ...
    addSmallTableWidget = RibbonPanel.addTableWidget
    addMediumTableWidget = RibbonPanel.addTableWidget
    addLargeTableWidget = RibbonPanel.addTableWidget
    def addTreeWidget(
        self,
        *,
        rowSpan: Union[int, RibbonButtonStyle] = Large,
        colSpan: int = 1,
        mode: RibbonSpaceFindMode = ColumnWise,
        alignment: QtCore.Qt.AlignmentFlag = QtCore.Qt.AlignmentFlag.AlignCenter,
        fixedHeight: Union[bool, float] = False,
    ) -> QtWidgets.QTreeWidget: ...
    addSmallTreeWidget = RibbonPanel.addTreeWidget
    addMediumTreeWidget = RibbonPanel.addTreeWidget
    addLargeTreeWidget = RibbonPanel.addTreeWidget
    def addListWidget(
        self,
        *,
        rowSpan: Union[int, RibbonButtonStyle] = Large,
        colSpan: int = 1,
        mode: RibbonSpaceFindMode = ColumnWise,
        alignment: QtCore.Qt.AlignmentFlag = QtCore.Qt.AlignmentFlag.AlignCenter,
        fixedHeight: Union[bool, float] = False,
    ) -> QtWidgets.QListWidget: ...
    addSmallListWidget = RibbonPanel.addListWidget
    addMediumListWidget = RibbonPanel.addListWidget
    addLargeListWidget = RibbonPanel.addListWidget
    def addCalendarWidget(
        self,
        *,
        rowSpan: Union[int, RibbonButtonStyle] = Large,
        colSpan: int = 1,
        mode: RibbonSpaceFindMode = ColumnWise,
        alignment: QtCore.Qt.AlignmentFlag = QtCore.Qt.AlignmentFlag.AlignCenter,
        fixedHeight: Union[bool, float] = False,
    ) -> QtWidgets.QCalendarWidget: ...
    addSmallCalendarWidget = RibbonPanel.addCalendarWidget
    addMediumCalendarWidget = RibbonPanel.addCalendarWidget
    addLargeCalendarWidget = RibbonPanel.addCalendarWidget
    def addSeparator(
        self,
        orientation=QtCore.Qt.Orientation.Vertical,
        width=6,
        *,
        rowSpan: Union[int, RibbonButtonStyle] = Large,
        colSpan: int = 1,
        mode: RibbonSpaceFindMode = ColumnWise,
        alignment: QtCore.Qt.AlignmentFlag = QtCore.Qt.AlignmentFlag.AlignCenter,
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
        alignment: QtCore.Qt.AlignmentFlag = QtCore.Qt.AlignmentFlag.AlignCenter,
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
        alignment: QtCore.Qt.AlignmentFlag = QtCore.Qt.AlignmentFlag.AlignCenter,
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
        alignment: QtCore.Qt.AlignmentFlag = QtCore.Qt.AlignmentFlag.AlignCenter,
        fixedHeight: Union[bool, float] = False,
    ) -> RibbonGallery: ...
    addSmallGallery = RibbonPanel.addGallery
    addMediumGallery = RibbonPanel.addGallery
    addLargeGallery = RibbonPanel.addGallery
