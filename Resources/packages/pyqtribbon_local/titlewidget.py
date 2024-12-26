import typing

from PySide.QtGui import QIcon, QMouseEvent
from PySide.QtWidgets import (
    QToolButton,
    QSizePolicy,
    QWidget,
    QHBoxLayout,
    QFrame,
    QLabel,
    QToolBar,
    QTabBar,
)
from PySide.QtCore import (
    Qt,
    QSize,
    Signal,
)

from .menu import RibbonMenu
from .tabbar import RibbonTabBar
from .utils import DataFile


class RibbonApplicationButton(QToolButton):
    """Application button in the ribbon bar."""

    def addFileMenu(self) -> RibbonMenu:
        """Add a new ribbon menu to the application button.

        :return: The new ribbon menu.
        """
        menu = RibbonMenu(self)
        self.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)
        self.setMenu(menu)
        return menu


class RibbonTitleLabel(QLabel):
    """Title label in the ribbon bar."""

    pass


class RibbonTitleWidget(QFrame):
    """The title widget of the ribbon."""

    #: Signal, the help button was clicked.
    helpButtonClicked = Signal(bool)
    #: Signal, the collapse button wa clicked.
    collapseRibbonButtonClicked = Signal(bool)

    #: Buttons
    _quickAccessButtons = []
    _rightToolButtons = []

    _quickAccessButtonHeight = 20
    _rightButtonHeight = 20

    # Mouse move events
    _start_point = None
    _window_point = None

    @typing.overload
    def __init__(self, title="PyQtRibbon", parent=None):
        pass

    @typing.overload
    def __init__(self, parent=None):
        pass

    def __init__(self, *args, **kwargs):
        """Initialize the ribbon title widget.

        :param title: The title of the ribbon.
        :param parent: The parent widget.
        """
        if (args and not isinstance(args[0], QWidget)) or ("title" in kwargs):
            title = args[0] if len(args) > 0 else kwargs.get("title", "PyQtRibbon")
            parent = args[1] if len(args) > 1 else kwargs.get("parent", None)
        else:
            title = "PyQtRibbon"
            parent = args[0] if len(args) > 0 else kwargs.get("parent", None)
        super().__init__(parent)
        # Tab bar layout
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)  # type: ignore
        self._tabBarLayout = QHBoxLayout(self)
        self._tabBarLayout.setContentsMargins(0, 0, 0, 0)
        self._tabBarLayout.setSpacing(0)

        # Application
        self._applicationButton = RibbonApplicationButton()  # type: ignore
        self._applicationButton.setIcon(QIcon(DataFile("icons/python.png")))
        self._applicationButton.setIconSize(QSize(self._quickAccessButtonHeight, self._quickAccessButtonHeight))
        self._applicationButton.setText("PyQtRibbon")
        self._applicationButton.setToolTip("PyQtRibbon")

        self._quickAccessToolBar = QToolBar()
        self._quickAccessToolBar.setIconSize(QSize(self._quickAccessButtonHeight, self._quickAccessButtonHeight))
        self._quickAccessToolBar.setOrientation(Qt.Orientation.Horizontal)
        self._quickAccessToolBar.setMovable(False)
        self._quickAccessToolBar.addWidget(self._applicationButton)
        self._quickAccessToolBarWidget = QWidget()
        self._quickAccessToolBarLayout = QHBoxLayout(self._quickAccessToolBarWidget)
        self._quickAccessToolBarLayout.setContentsMargins(0, 0, 0, 0)
        self._quickAccessToolBarLayout.setSpacing(0)
        self._quickAccessToolBarLayout.addWidget(self._quickAccessToolBar, 0, Qt.AlignmentFlag.AlignBottom)

        # right toolbar
        self._rightToolBar = QToolBar()
        self._rightToolBar.setOrientation(Qt.Orientation.Horizontal)
        self._rightToolBar.setIconSize(QSize(self._rightButtonHeight, self._rightButtonHeight))
        self._collapseRibbonButton = QToolButton(self)
        self._collapseRibbonButton.setIconSize(QSize(self._rightButtonHeight, self._rightButtonHeight))
        self._collapseRibbonButton.setIcon(QIcon(DataFile("icons/up.png")))
        self._collapseRibbonButton.setAutoRaise(True)
        self._collapseRibbonButton.setToolTip("Collapse Ribbon")
        self._collapseRibbonButton.clicked.connect(self.collapseRibbonButtonClicked)  # type: ignore
        self._helpButton = QToolButton(self)
        self._helpButton.setIconSize(QSize(self._rightButtonHeight, self._rightButtonHeight))
        self._helpButton.setIcon(QIcon(DataFile("icons/help.png")))
        self._helpButton.setAutoRaise(True)
        self._helpButton.setToolTip("Help")
        self._helpButton.clicked.connect(self.helpButtonClicked)  # type: ignore
        self.addRightToolButton(self._collapseRibbonButton)
        self.addRightToolButton(self._helpButton)

        # category tab bar
        self._tabBar = RibbonTabBar(self)
        self._tabBar.setExpanding(False)
        self._tabBar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)  # type: ignore
        font = self._tabBar.font()
        font.setPointSize(font.pointSize() + 3)
        self._tabBar.setFont(font)
        self._tabBar.setShape(QTabBar.Shape.RoundedNorth)
        self._tabBar.setDocumentMode(True)

        # Title label
        self._titleLabel = RibbonTitleLabel(self)
        self._titleLabel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)  # type: ignore
        self._titleLabel.setAlignment(Qt.AlignCenter | Qt.AlignBottom)  # type: ignore
        self._titleLabel.setText(title)
        font = self._titleLabel.font()
        font.setPointSize(font.pointSize() + 3)
        self._titleLabel.setFont(font)

        self._tabBarLayout.addWidget(self._quickAccessToolBarWidget, 0, Qt.AlignmentFlag.AlignVCenter)
        self._tabBarLayout.addWidget(self._tabBar, 0, Qt.AlignmentFlag.AlignVCenter)
        self._tabBarLayout.addWidget(self._titleLabel, 1, Qt.AlignmentFlag.AlignVCenter)
        self._tabBarLayout.addWidget(self._rightToolBar, 0, Qt.AlignmentFlag.AlignVCenter)

    def applicationButton(self) -> RibbonApplicationButton:
        """Return the application button."""
        return self._applicationButton

    def setApplicationIcon(self, icon: QIcon):
        """Set the application icon.

        :param icon: The icon to set.
        """
        self._applicationButton.setIcon(icon)

    def addTitleWidget(self, widget: QWidget):
        """Add a widget to the title layout.

        :param widget: The widget to add.
        """
        self._tabBarLayout.addWidget(widget)

    def insertTitleWidget(self, index: int, widget: QWidget):
        """Insert a widget to the title layout.

        :param index: The index to insert the widget.
        :param widget: The widget to insert.
        """
        self._tabBarLayout.insertWidget(index, widget)

    def removeTitleWidget(self, widget: QWidget):
        """Remove a widget from the title layout.

        :param widget: The widget to remove.
        """
        self._tabBarLayout.removeWidget(widget)

    def tabBar(self) -> RibbonTabBar:
        """Return the tab bar of the ribbon.

        :return: The tab bar of the ribbon.
        """
        return self._tabBar

    def quickAccessToolBar(self) -> QToolBar:
        """Return the quick access toolbar of the ribbon.

        :return: The quick access toolbar of the ribbon.
        """
        return self._quickAccessToolBar

    def quickAccessButtons(self) -> typing.List[QToolButton]:
        """Return the quick access buttons of the ribbon.

        :return: The quick access buttons of the ribbon.
        """
        return self._quickAccessButtons

    def addQuickAccessButton(self, button: QToolButton):
        """Add a widget to the quick access bar.

        :param button: The button to add.
        """
        button.setIconSize(QSize(self._quickAccessButtonHeight, self._quickAccessButtonHeight))
        self._quickAccessButtons.append(button)
        self._quickAccessToolBar.addWidget(button)

    def setQuickAccessButtonHeight(self, height: int):
        """Set the height of the quick access buttons.

        :param height: The height to set.
        """
        self._quickAccessButtonHeight = height
        self._applicationButton.setIcon(self._applicationButton.icon().pixmap(height, height))
        self._quickAccessToolBar.setIconSize(QSize(height, height))

    def title(self) -> str:
        """Return the title of the ribbon.

        :return: The title of the ribbon.
        """
        return self._titleLabel.text()

    def setTitle(self, title: str):
        """Set the title of the ribbon.

        :param title: The title to set.
        """
        self._titleLabel.setText(title)

    def rightToolBar(self) -> QToolBar:
        """Return the right toolbar of the ribbon.

        :return: The right toolbar of the ribbon.
        """
        return self._rightToolBar

    def addRightToolButton(self, button: QToolButton):
        """Add a widget to the right button bar.

        :param button: The button to add.
        """
        button.setIconSize(QSize(self._rightButtonHeight, self._rightButtonHeight))
        self._rightToolButtons.append(button)
        self._rightToolBar.addWidget(button)

    def setRightToolBarHeight(self, height: int):
        """Set the height of the right buttons.

        :param height: The height to set.
        """
        self._rightButtonHeight = height
        self._rightToolBar.setIconSize(QSize(height, height))

    def helpRibbonButton(self) -> QToolButton:
        """Return the help ribbon button.

        :return: The help ribbon button.
        """
        return self._helpButton

    def setHelpButtonIcon(self, icon: QIcon):
        """Set the icon of the help button.

        :param icon: The icon to set.
        """
        self._helpButton.setIcon(icon)

    def removeHelpButton(self):
        """Remove the help button from the ribbon."""
        self._helpButton.setVisible(False)

    def setCollapseButtonIcon(self, icon: QIcon):
        """Set the icon of the min button.

        :param icon: The icon to set.
        """
        self._collapseRibbonButton.setIcon(icon)

    def removeCollapseButton(self):
        """Remove the min button from the ribbon."""
        self._collapseRibbonButton.setVisible(False)

    def collapseRibbonButton(self) -> QToolButton:
        """Return the collapse ribbon button.

        :return: The collapse ribbon button.
        """
        return self._collapseRibbonButton

    def setTitleWidgetHeight(self, height: int):
        """Set the height of the title widget.

        :param height: The height to set.
        """
        self.setQuickAccessButtonHeight(height)
        self.setRightToolBarHeight(height)

    def topLevelWidget(self) -> QWidget:
        widget = self
        try:
            while widget.parentWidget():
                widget = widget.parentWidget()
        except Exception:
            pass
        return widget

    def mousePressEvent(self, e: QMouseEvent):
        try:
            self._start_point = e.pos()
            self._window_point = self.topLevelWidget().frameGeometry().topLeft()
        except Exception:
            pass

    def mouseMoveEvent(self, e: QMouseEvent):
        try:
            relpos = e.pos() - self._start_point if self._start_point else None
            (self.topLevelWidget().move(self._window_point + relpos) if self._window_point and relpos else None)
            self.topLevelWidget().windowHandle().startSystemMove()
        except Exception:
            pass

    def mouseDoubleClickEvent(self, e: QMouseEvent):
        try:
            mainwindow = self.topLevelWidget()
            (mainwindow.showNormal() if mainwindow.isMaximized() else mainwindow.showMaximized())
        except Exception:
            pass
