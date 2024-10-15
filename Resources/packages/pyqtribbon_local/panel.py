from __future__ import annotations

import functools
import re
from typing import Any, Callable, Dict, List, Union, overload

import numpy as np

from PySide.QtGui import QIcon, QKeySequence
from PySide.QtWidgets import (
    QToolButton,
    QSizePolicy,
    QWidget,
    QHBoxLayout,
    QFrame,
    QListWidget,
    QVBoxLayout,
    QLabel,
    QLayout,
    QGridLayout,
    QCheckBox,
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
    QSize,
    Signal,
)


from .constants import (
    ColumnWise,
    Large,
    Medium,
    RibbonButtonStyle,
    RibbonSpaceFindMode,
    Small,
)
from .gallery import RibbonGallery
from .separator import RibbonSeparator
from .toolbutton import RibbonToolButton
from .utils import DataFile


class RibbonPanelTitle(QLabel):
    """Widget to display the title of a panel."""

    pass


class RibbonGridLayoutManager(object):
    """Grid Layout Manager."""

    def __init__(self, rows: int):
        """Create a new grid layout manager.

        :param rows: The number of rows in the grid layout.
        """
        self.rows = rows
        self.cells = np.ones((rows, 1), dtype=bool)

    def request_cells(
        self, rowSpan: int = 1, colSpan: int = 1, mode: RibbonSpaceFindMode = ColumnWise
    ):
        """Request a number of available cells from the grid.

        :param rowSpan: The number of rows the cell should span.
        :param colSpan: The number of columns the cell should span.
        :param mode: The mode of the grid.
        :return: row, col, the row and column of the requested cell.
        """
        if rowSpan > self.rows:
            raise ValueError("RowSpan is too large")
        if mode == ColumnWise:
            for row in range(self.cells.shape[0] - rowSpan + 1):
                for col in range(self.cells.shape[1] - colSpan + 1):
                    if self.cells[row : row + rowSpan, col : col + colSpan].all():
                        self.cells[row : row + rowSpan, col : col + colSpan] = False
                        return row, col
        else:
            for col in range(self.cells.shape[1]):
                if self.cells[0, col:].all():
                    if self.cells.shape[1] - col < colSpan:
                        self.cells = np.append(
                            self.cells,
                            np.ones(
                                (self.rows, colSpan - (self.cells.shape[1] - col)),
                                dtype=bool,
                            ),
                            axis=1,
                        )
                    self.cells[0, col:] = False
                    return 0, col
        cols = self.cells.shape[1]
        colSpan1 = colSpan
        if self.cells[:, -1].all():
            cols -= 1
            colSpan1 -= 1
        self.cells = np.append(
            self.cells, np.ones((self.rows, colSpan1), dtype=bool), axis=1
        )
        self.cells[:rowSpan, cols : cols + colSpan] = False
        return 0, cols


class RibbonPanelItemWidget(QFrame):
    """Widget to display a panel item."""

    def __init__(self, parent=None):
        """Create a new panel item.

        :param parent: The parent widget.
        """
        super().__init__(parent)
        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(0)
        self.layout().setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout().setSizeConstraint(QLayout.SizeConstraint.SetMaximumSize)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)  # type: ignore

    def addWidget(self, widget):
        """Add a widget to the panel item.

        :param widget: The widget to add.
        """
        self.layout().addWidget(widget)


class RibbonPanelOptionButton(QToolButton):
    """Button to display the options of a panel."""

    pass


class RibbonPanel(QFrame):
    """Panel in the ribbon category."""

    #: maximal number of rows
    _maxRows: int = 6
    #: rows for large widgets
    _largeRows: int = 6
    #: rows for medium widgets
    _mediumRows: int = 3
    #: rows for small widgets
    _smallRows: int = 2
    #: GridLayout manager to request available cells.
    _gridLayoutManager: RibbonGridLayoutManager
    #: whether to show the panel option button
    _showPanelOptionButton: bool

    #: widgets that are added to the panel
    _widgets: List[QWidget] = []

    # height of the title widget
    _titleHeight: int = 15

    # Panel options signal
    panelOptionClicked = Signal(bool)

    @overload
    def __init__(
        self, title: str = "", maxRows: int = 6, showPanelOptionButton=True, parent=None
    ):
        pass

    @overload
    def __init__(self, parent=None):
        pass

    def __init__(self, *args, **kwargs):
        """Create a new panel.

        :param title: The title of the panel.
        :param maxRows: The maximal number of rows in the panel.
        :param showPanelOptionButton: Whether to show the panel option button.
        :param parent: The parent widget.
        """
        if (args and not isinstance(args[0], QWidget)) or (
            "title" in kwargs or "maxRows" in kwargs
        ):
            title = args[0] if len(args) > 0 else kwargs.get("title", "")
            maxRows = args[1] if len(args) > 1 else kwargs.get("maxRows", 6)
            showPanelOptionButton = (
                args[2] if len(args) > 2 else kwargs.get("showPanelOptionButton", True)
            )
            parent = args[3] if len(args) > 3 else kwargs.get("parent", None)
        else:
            title = ""
            maxRows = 6
            showPanelOptionButton = True
            parent = args[0] if len(args) > 0 else kwargs.get("parent", None)
        super().__init__(parent)
        self._maxRows = maxRows
        self._largeRows = maxRows
        self._mediumRows = max(round(maxRows / 2), 1)
        self._smallRows = max(round(maxRows / 3), 1)
        self._gridLayoutManager = RibbonGridLayoutManager(self._maxRows)
        self._widgets = []
        self._showPanelOptionButton = showPanelOptionButton

        # Main layout
        self._mainLayout = QVBoxLayout(self)
        self._mainLayout.setContentsMargins(0, 0, 0, 0)
        self._mainLayout.setSpacing(0)

        # Actions layout
        self._actionsLayout = QGridLayout()
        self._actionsLayout.setContentsMargins(5, 5, 5, 5)
        self._actionsLayout.setSpacing(0)
        self._mainLayout.addLayout(self._actionsLayout, 1)

        # Title layout
        self._titleWidget = QWidget()
        self._titleWidget.setFixedHeight(self._titleHeight)
        self._titleLayout = QHBoxLayout(self._titleWidget)
        self._titleLayout.setContentsMargins(0, 0, 0, 0)
        self._titleLayout.setSpacing(0)
        self._titleLabel = RibbonPanelTitle()  # type: ignore
        self._titleLabel.setText(title)
        self._titleLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._titleLayout.addWidget(self._titleLabel, 1)

        # Panel option button
        if showPanelOptionButton:
            self._panelOption = RibbonPanelOptionButton()  # type: ignore
            self._panelOption.setAutoRaise(True)
            self._panelOption.setIcon(QIcon(DataFile("icons/linking.png")))
            self._panelOption.setIconSize(QSize(self._titleHeight, self._titleHeight))
            self._panelOption.setToolTip("Panel options")
            self._panelOption.clicked.connect(self.panelOptionClicked)  # type: ignore
            self._titleLayout.addWidget(self._panelOption, 0)

        self._mainLayout.addWidget(self._titleWidget, 0)

    def maximumRows(self) -> int:
        """Return the maximal number of rows in the panel.

        :return: The maximal number of rows in the panel.
        """
        return self._maxRows

    def largeRows(self) -> int:
        """Return the number of span rows for large widgets.

        :return: The number of span rows for large widgets.
        """
        return self._largeRows

    def mediumRows(self) -> int:
        """Return the number of span rows for medium widgets.

        :return: The number of span rows for medium widgets.
        """
        return self._mediumRows

    def smallRows(self) -> int:
        """Return the number of span rows for small widgets.

        :return: The number of span rows for small widgets.
        """
        return self._smallRows

    def setMaximumRows(self, maxRows: int):
        """Set the maximal number of rows in the panel.

        :param maxRows: The maximal number of rows in the panel.
        """
        self._maxRows = maxRows
        self._largeRows = maxRows
        self._mediumRows = max(round(maxRows / 2), 1)
        self._smallRows = max(round(maxRows / 3), 1)

    def setLargeRows(self, rows: int):
        """Set the number of span rows for large widgets.

        :param rows: The number of span rows for large widgets.
        """
        assert rows <= self._maxRows, "Invalid number of rows"
        self._largeRows = rows

    def setMediumRows(self, rows: int):
        """Set the number of span rows for medium widgets.

        :param rows: The number of span rows for medium widgets.
        """
        assert 0 < rows <= self._maxRows, "Invalid number of rows"
        self._mediumRows = rows

    def setSmallRows(self, rows: int):
        """Set the number of span rows for small widgets.

        :param rows: The number of span rows for small widgets.
        """
        assert 0 < rows <= self._maxRows, "Invalid number of rows"
        self._smallRows = rows

    def defaultRowSpan(self, rowSpan: Union[int, RibbonButtonStyle]) -> int:
        """Return the number of span rows for the given widget type.

        :param rowSpan: row span or type.
        :return: The number of span rows for the given widget type.
        """
        if not isinstance(rowSpan, RibbonButtonStyle):
            return rowSpan
        if rowSpan == Large:
            return self._largeRows
        elif rowSpan == Medium:
            return self._mediumRows
        elif rowSpan == Small:
            return self._smallRows
        else:
            raise ValueError("Invalid row span")

    def panelOptionButton(self) -> RibbonPanelOptionButton:
        """Return the panel option button.

        :return: The panel option button.
        """
        return self._panelOption

    def setPanelOptionToolTip(self, text: str):
        """Set the tooltip of the panel option button.

        :param text: The tooltip text.
        """
        self._panelOption.setToolTip(text)

    def rowHeight(self) -> int:
        """Return the height of a row."""
        return int(
            (
                self.size().height()
                - self._mainLayout.contentsMargins().top()
                - self._mainLayout.contentsMargins().bottom()
                - self._mainLayout.spacing()
                - self._titleWidget.height()
                - self._actionsLayout.contentsMargins().top()
                - self._actionsLayout.contentsMargins().bottom()
                - self._actionsLayout.verticalSpacing()
                * (self._gridLayoutManager.rows - 1)
            )
            / self._gridLayoutManager.rows
        )

    def setTitle(self, title: str):
        """Set the title of the panel.

        :param title: The title to set.
        """
        self._titleLabel.setText(title)

    def title(self):
        """Get the title of the panel.

        :return: The title.
        """
        return self._titleLabel.text()

    def setTitleHeight(self, height: int):
        """Set the height of the title widget.

        :param height: The height to set.
        """
        self._titleHeight = height
        self._titleWidget.setFixedHeight(height)
        self._panelOption.setIconSize(QSize(height, height))

    def titleHeight(self) -> int:
        """Get the height of the title widget.

        :return: The height of the title widget.
        """
        return self._titleHeight

    def addWidgetsBy(self, data: Dict[str, Dict]) -> Dict[str, QWidget]:
        """Add widgets to the panel.

        :param data: The data to add. The dict is of the form:

            .. code-block:: python

                {
                    "widget-name": {
                        "type": "Button",
                        "args": (),
                        "kwargs": {  # or "arguments" for backward compatibility
                            "key1": "value1",
                            "key2": "value2"
                        }
                    },
                }

            Possible types are: Button, SmallButton, MediumButton, LargeButton,
            ToggleButton, SmallToggleButton, MediumToggleButton, LargeToggleButton, ComboBox, FontComboBox,
            LineEdit, TextEdit, PlainTextEdit, Label, ProgressBar, SpinBox, DoubleSpinBox, DataEdit, TimeEdit,
            DateTimeEdit, TableWidget, TreeWidget, ListWidget, CalendarWidget, Separator, HorizontalSeparator,
            VerticalSeparator, Gallery.
        :return: A dictionary of the added widgets.
        """
        widgets = {}  # type: Dict[str, QWidget]
        for key, widget_data in data.items():
            type = widget_data.pop("type", "").capitalize()
            method = getattr(self, f"add{type}", None)  # type: Callable
            assert callable(
                method
            ), f"Method add{type} is not callable or does not exist"
            args = widget_data.get("args", ())
            kwargs = widget_data.get("kwargs", widget_data.get("arguments", {}))
            widgets[key] = method(*args, **kwargs)
        return widgets

    def addWidget(
        self,
        widget: QWidget,
        *,
        rowSpan: Union[int, RibbonButtonStyle] = Small,
        colSpan: int = 1,
        mode: RibbonSpaceFindMode = ColumnWise,
        alignment: Qt.AlignmentFlag = Qt.AlignmentFlag.AlignCenter,
        fixedHeight: Union[bool, float] = False,
    ) -> QWidget | Any:
        """Add a widget to the panel.

        :param widget: The widget to add.
        :param rowSpan: The number of rows the widget should span, 2: small, 3: medium, 6: large.
        :param colSpan: The number of columns the widget should span.
        :param mode: The mode to find spaces.
        :param alignment: The alignment of the widget.
        :param fixedHeight: Whether to fix the height of the widget, it can be a boolean, a percentage or a fixed
                            height, when a boolean is given, the height is fixed to the maximum height allowed if the
                            value is True, when a percentage is given (0 < percentage < 1) the height is calculated
                            from the height of the maximum height allowed, depends on the number of rows to span. The
                            minimum height is 40% of the maximum height allowed.
        :return: The added widget.
        """
        rowSpan = self.defaultRowSpan(rowSpan)
        self._widgets.append(widget)
        row, col = self._gridLayoutManager.request_cells(rowSpan, colSpan, mode)
        maximumHeight = (
            self.rowHeight() * rowSpan
            + self._actionsLayout.verticalSpacing() * (rowSpan - 2)
        )
        widget.setMaximumHeight(maximumHeight)
        if fixedHeight is True or fixedHeight > 0:
            fixedHeight = (
                int(fixedHeight * maximumHeight)
                if 0 < fixedHeight <= 1
                else fixedHeight if 1 < fixedHeight < maximumHeight else maximumHeight
            )
            fixedHeight = max(
                fixedHeight, 0.4 * maximumHeight
            )  # minimum height is 40% of the maximum height
            widget.setFixedHeight(fixedHeight)
        item = RibbonPanelItemWidget(self)
        item.addWidget(widget)
        self._actionsLayout.addWidget(item, row, col, rowSpan, colSpan, alignment)  # type: ignore
        return widget

    addSmallWidget = functools.partialmethod(addWidget, rowSpan=Small)
    addMediumWidget = functools.partialmethod(addWidget, rowSpan=Medium)
    addLargeWidget = functools.partialmethod(addWidget, rowSpan=Large)

    def removeWidget(self, widget: QWidget):
        """Remove a widget from the panel."""
        self._actionsLayout.removeWidget(widget)

    def widget(self, index: int) -> QWidget:
        """Get the widget at the given index.

        :param index: The index of the widget, starting from 0.
        :return: The widget at the given index.
        """
        return self._widgets[index]

    def widgets(self) -> List[QWidget]:
        """Get all the widgets in the panel.

        :return: A list of all the widgets in the panel.
        """
        return self._widgets

    def addButton(
        self,
        text: str = None,
        icon: QIcon = None,
        showText: bool = True,
        slot: Callable = None,
        shortcut: Qt.Key | QKeySequence | QKeySequence.StandardKey | str | int = None,
        tooltip: str = None,
        statusTip: str = None,
        checkable: bool = False,
        *,
        rowSpan: RibbonButtonStyle = Large,
        **kwargs,
    ) -> RibbonToolButton:
        """Add a button to the panel.

        :param text: The text of the button.
        :param icon: The icon of the button.
        :param showText: Whether to show the text of the button.
        :param slot: The slot to call when the button is clicked.
        :param shortcut: The shortcut of the button.
        :param tooltip: The tooltip of the button.
        :param statusTip: The status tip of the button.
        :param checkable: Whether the button is checkable.
        :param rowSpan: The type of the button corresponding to the number of rows it should span.
        :param kwargs: keyword arguments to control the properties of the widget on the ribbon bar.

        :return: The button that was added.
        """
        assert isinstance(
            rowSpan, RibbonButtonStyle
        ), "rowSpan must be an instance of RibbonButtonStyle"
        style = rowSpan
        button = RibbonToolButton(self)
        button.setButtonStyle(style)
        button.setText(text) if text else None
        button.setIcon(icon) if icon else None
        button.clicked.connect(slot) if slot else None  # type: ignore
        button.setShortcut(shortcut) if shortcut else None
        button.setToolTip(tooltip) if tooltip else None
        button.setStatusTip(statusTip) if statusTip else None
        maximumHeight = (
            self.height()
            - self._titleLabel.sizeHint().height()
            - self._mainLayout.spacing()
            - self._mainLayout.contentsMargins().top()
            - self._mainLayout.contentsMargins().bottom()
        )
        button.setMaximumHeight(maximumHeight)
        if style == Large:
            fontSize = max(button.font().pointSize() * 4 / 3, button.font().pixelSize())
            arrowSize = fontSize
            maximumIconSize = max(maximumHeight - fontSize * 2 - arrowSize, 48)
            button.setMaximumIconSize(int(maximumIconSize))
        if not showText:
            button.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonIconOnly)
        button.setCheckable(checkable)
        kwargs["rowSpan"] = (
            self.defaultRowSpan(Small)
            if style == Small
            else (
                self.defaultRowSpan(Medium)
                if style == Medium
                else self.defaultRowSpan(Large)
            )
        )
        self.addWidget(button, **kwargs)  # noqa
        return button

    addSmallButton = functools.partialmethod(addButton, rowSpan=Small)
    addMediumButton = functools.partialmethod(addButton, rowSpan=Medium)
    addLargeButton = functools.partialmethod(addButton, rowSpan=Large)
    addToggleButton = functools.partialmethod(addButton, checkable=True)
    addSmallToggleButton = functools.partialmethod(addToggleButton, rowSpan=Small)
    addMediumToggleButton = functools.partialmethod(addToggleButton, rowSpan=Medium)
    addLargeToggleButton = functools.partialmethod(addToggleButton, rowSpan=Large)

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
    ) -> QWidget:
        """Add any widget to the panel.

        :param cls: The class of the widget to add.
        :param initializer: The initializer function of the widget to add.
        :param args: The arguments passed to the initializer.
        :param rowSpan: The number of rows the widget should span, 2: small, 3: medium, 6: large.
        :param colSpan: The number of columns the widget should span.
        :param mode: The mode to find spaces.
        :param alignment: The alignment of the widget.
        :param fixedHeight: Whether to fix the height of the widget, it can be a boolean, a percentage or a fixed
                            height, when a boolean is given, the height is fixed to the maximum height allowed if the
                            value is True, when a percentage is given (0 < percentage < 1) the height is calculated
                            from the height of the maximum height allowed, depends on the number of rows to span. The
                            minimum height is 40% of the maximum height allowed.
        :param kwargs: The keyword arguments are passed to the initializer
        """
        widget = cls(self)
        if callable(initializer):
            initializer(widget, *args, **kwargs)
        elif args or kwargs:
            raise ValueError("Arguments are provided but the initializer is not set")
        return self.addWidget(
            widget,
            rowSpan=rowSpan,
            colSpan=colSpan,
            mode=mode,
            alignment=alignment,
            fixedHeight=fixedHeight,
        )

    def __getattr__(self, method: str) -> Callable:
        """Get the dynamic method `add[Small|Medium|Large][Widget]`.

        :param method: The name of the method to get.
        :return: The method of the widget to add.
        """
        # Match the method name
        match = re.match(r"add(Small|Medium|Large)(\w+)", method)
        assert match, "Invalid method name"

        # Get the widget class and the size
        size = match.group(1)
        base_method_name = f"add{match.group(2)}"
        assert hasattr(
            self, base_method_name
        ), f"Invalid method name {base_method_name}"

        # Get the base method
        base_method = getattr(self, base_method_name)
        rowSpan = Small if size == "Small" else Medium if size == "Medium" else Large

        # Create the new method
        return functools.partial(base_method, rowSpan=rowSpan)

    addCheckBox = functools.partialmethod(
        _addAnyWidget, cls=QCheckBox, initializer=QCheckBox.setText
    )
    addComboBox = functools.partialmethod(
        _addAnyWidget, cls=QComboBox, initializer=QComboBox.addItems
    )
    addFontComboBox = functools.partialmethod(_addAnyWidget, cls=QFontComboBox)
    addLineEdit = functools.partialmethod(_addAnyWidget, cls=QLineEdit)
    addTextEdit = functools.partialmethod(_addAnyWidget, cls=QTextEdit)
    addPlainTextEdit = functools.partialmethod(_addAnyWidget, cls=QPlainTextEdit)
    addLabel = functools.partialmethod(
        _addAnyWidget, cls=QLabel, initializer=QLabel.setText
    )
    addProgressBar = functools.partialmethod(_addAnyWidget, cls=QProgressBar)
    addSlider = functools.partialmethod(_addAnyWidget, cls=QSlider)
    addSpinBox = functools.partialmethod(_addAnyWidget, cls=QSpinBox)
    addDoubleSpinBox = functools.partialmethod(_addAnyWidget, cls=QDoubleSpinBox)
    addDateEdit = functools.partialmethod(_addAnyWidget, cls=QDateEdit)
    addTimeEdit = functools.partialmethod(_addAnyWidget, cls=QTimeEdit)
    addDateTimeEdit = functools.partialmethod(_addAnyWidget, cls=QDateTimeEdit)
    addTableWidget = functools.partialmethod(
        _addAnyWidget, cls=QTableWidget, rowSpan=Large
    )
    addTreeWidget = functools.partialmethod(
        _addAnyWidget, cls=QTreeWidget, rowSpan=Large
    )
    addListWidget = functools.partialmethod(
        _addAnyWidget, cls=QListWidget, rowSpan=Large
    )
    addCalendarWidget = functools.partialmethod(
        _addAnyWidget, cls=QCalendarWidget, rowSpan=Large
    )

    def addSeparator(
        self, orientation=Qt.Orientation.Vertical, width=6, **kwargs
    ) -> RibbonSeparator:
        """Add a separator to the panel.

        :param orientation: The orientation of the separator.
        :param width: The width of the separator.
        :param kwargs: keyword arguments to control the properties of the widget on the ribbon bar.

        :return: The separator.
        """
        kwargs["rowSpan"] = Large if "rowSpan" not in kwargs else kwargs["rowSpan"]
        return self.addWidget(RibbonSeparator(orientation, width), **kwargs)

    addHorizontalSeparator = functools.partialmethod(
        addSeparator, orientation=Qt.Orientation.Horizontal
    )
    addVerticalSeparator = functools.partialmethod(
        addSeparator, orientation=Qt.Orientation.Vertical
    )

    def addGallery(
        self, minimumWidth=800, popupHideOnClick=False, **kwargs
    ) -> RibbonGallery:
        """Add a gallery to the panel.

        :param minimumWidth: The minimum width of the gallery.
        :param popupHideOnClick: Whether the gallery popup should be hidden when a user clicks on it.
        :param kwargs: keyword arguments to control the properties of the widget on the ribbon bar.

        :return: The gallery.
        """
        kwargs["rowSpan"] = Large if "rowSpan" not in kwargs else kwargs["rowSpan"]
        rowSpan = self.defaultRowSpan(kwargs["rowSpan"])
        gallery = RibbonGallery(minimumWidth, popupHideOnClick, self)
        maximumHeight = (
            self.rowHeight() * rowSpan
            + self._actionsLayout.verticalSpacing() * (rowSpan - 2)
        )
        gallery.setFixedHeight(maximumHeight)
        return self.addWidget(gallery, **kwargs)
