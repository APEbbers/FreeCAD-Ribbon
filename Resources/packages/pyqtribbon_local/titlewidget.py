import typing

from PySide import QtCore, QtGui, QtWidgets

from .menu import RibbonMenu
from .tabbar import RibbonTabBar
from .utils import DataFile


class RibbonApplicationButton(QtWidgets.QToolButton):
    """Application button in the ribbon bar."""

    def addFileMenu(self) -> RibbonMenu:
        """Add a new ribbon menu to the application button.

        :return: The new ribbon menu.
        """
        menu = RibbonMenu(self)
        self.setPopupMode(QtWidgets.QToolButton.ToolButtonPopupMode.InstantPopup)
        self.setMenu(menu)
        return menu


class RibbonTitleLabel(QtWidgets.QLabel):
    """Title label in the ribbon bar."""

    pass


class RibbonTitleWidget(QtWidgets.QFrame):
    """The title widget of the ribbon."""

    #: Signal, the help button was clicked.
    helpButtonClicked = QtCore.Signal(bool)
    #: Signal, the collapse button wa clicked.
    collapseRibbonButtonClicked = QtCore.Signal(bool)

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
        if (args and not isinstance(args[0], QtWidgets.QWidget)) or ("title" in kwargs):
            title = args[0] if len(args) > 0 else kwargs.get("title", "PyQtRibbon")
            parent = args[1] if len(args) > 1 else kwargs.get("parent", None)
        else:
            title = "PyQtRibbon"
            parent = args[0] if len(args) > 0 else kwargs.get("parent", None)
        super().__init__(parent)
        # Tab bar layout
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)  # type: ignore
        self._tabBarLayout = QtWidgets.QHBoxLayout(self)
        self._tabBarLayout.setContentsMargins(0, 0, 0, 0)
        self._tabBarLayout.setSpacing(0)

        # Application
        self._applicationButton = RibbonApplicationButton()  # type: ignore
        self._applicationButton.setIcon(QtGui.QIcon(DataFile("icons/python.png")))
        self._applicationButton.setIconSize(QtCore.QSize(self._quickAccessButtonHeight, self._quickAccessButtonHeight))
        self._applicationButton.setText("PyQtRibbon")
        self._applicationButton.setToolTip("PyQtRibbon")

        self._quickAccessToolBar = QtWidgets.QToolBar()
        self._quickAccessToolBar.setIconSize(QtCore.QSize(self._quickAccessButtonHeight, self._quickAccessButtonHeight))
        self._quickAccessToolBar.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self._quickAccessToolBar.setMovable(False)
        self._quickAccessToolBar.addWidget(self._applicationButton)
        self._quickAccessToolBarWidget = QtWidgets.QWidget()
        self._quickAccessToolBarLayout = QtWidgets.QHBoxLayout(self._quickAccessToolBarWidget)
        self._quickAccessToolBarLayout.setContentsMargins(0, 0, 0, 0)
        self._quickAccessToolBarLayout.setSpacing(0)
        self._quickAccessToolBarLayout.addWidget(self._quickAccessToolBar, 0, QtCore.Qt.AlignmentFlag.AlignBottom)

        # right toolbar
        self._rightToolBar = QtWidgets.QToolBar()
        self._rightToolBar.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self._rightToolBar.setIconSize(QtCore.QSize(self._rightButtonHeight, self._rightButtonHeight))
        self._collapseRibbonButton = QtWidgets.QToolButton(self)
        self._collapseRibbonButton.setIconSize(QtCore.QSize(self._rightButtonHeight, self._rightButtonHeight))
        self._collapseRibbonButton.setIcon(QtGui.QIcon(DataFile("icons/up.png")))
        self._collapseRibbonButton.setAutoRaise(True)
        self._collapseRibbonButton.setToolTip("Collapse Ribbon")
        self._collapseRibbonButton.clicked.connect(self.collapseRibbonButtonClicked)  # type: ignore
        self._helpButton = QtWidgets.QToolButton(self)
        self._helpButton.setIconSize(QtCore.QSize(self._rightButtonHeight, self._rightButtonHeight))
        self._helpButton.setIcon(QtGui.QIcon(DataFile("icons/help.png")))
        self._helpButton.setAutoRaise(True)
        self._helpButton.setToolTip("Help")
        self._helpButton.clicked.connect(self.helpButtonClicked)  # type: ignore
        self.addRightToolButton(self._collapseRibbonButton)
        self.addRightToolButton(self._helpButton)

        # category tab bar
        self._tabBar = RibbonTabBar(self)
        self._tabBar.setExpanding(False)
        self._tabBar.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)  # type: ignore
        font = self._tabBar.font()
        font.setPointSize(font.pointSize() + 3)
        self._tabBar.setFont(font)
        self._tabBar.setShape(QtWidgets.QTabBar.Shape.RoundedNorth)
        self._tabBar.setDocumentMode(True)

        # Title label
        self._titleLabel = RibbonTitleLabel(self)
        self._titleLabel.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)  # type: ignore
        self._titleLabel.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignBottom)  # type: ignore
        self._titleLabel.setText(title)
        font = self._titleLabel.font()
        font.setPointSize(font.pointSize() + 3)
        self._titleLabel.setFont(font)

        self._tabBarLayout.addWidget(self._quickAccessToolBarWidget, 0, QtCore.Qt.AlignmentFlag.AlignVCenter)
        self._tabBarLayout.addWidget(self._tabBar, 0, QtCore.Qt.AlignmentFlag.AlignVCenter)
        self._tabBarLayout.addWidget(self._titleLabel, 1, QtCore.Qt.AlignmentFlag.AlignVCenter)
        self._tabBarLayout.addWidget(self._rightToolBar, 0, QtCore.Qt.AlignmentFlag.AlignVCenter)

    def applicationButton(self) -> RibbonApplicationButton:
        """Return the application button."""
        return self._applicationButton

    def setApplicationIcon(self, icon: QtGui.QIcon):
        """Set the application icon.

        :param icon: The icon to set.
        """
        self._applicationButton.setIcon(icon)

    def addTitleWidget(self, widget: QtWidgets.QWidget):
        """Add a widget to the title layout.

        :param widget: The widget to add.
        """
        self._tabBarLayout.addWidget(widget)

    def insertTitleWidget(self, index: int, widget: QtWidgets.QWidget):
        """Insert a widget to the title layout.

        :param index: The index to insert the widget.
        :param widget: The widget to insert.
        """
        self._tabBarLayout.insertWidget(index, widget)

    def removeTitleWidget(self, widget: QtWidgets.QWidget):
        """Remove a widget from the title layout.

        :param widget: The widget to remove.
        """
        self._tabBarLayout.removeWidget(widget)

    def tabBar(self) -> RibbonTabBar:
        """Return the tab bar of the ribbon.

        :return: The tab bar of the ribbon.
        """
        return self._tabBar

    def quickAccessToolBar(self) -> QtWidgets.QToolBar:
        """Return the quick access toolbar of the ribbon.

        :return: The quick access toolbar of the ribbon.
        """
        return self._quickAccessToolBar

    def quickAccessButtons(self) -> typing.List[QtWidgets.QToolButton]:
        """Return the quick access buttons of the ribbon.

        :return: The quick access buttons of the ribbon.
        """
        return self._quickAccessButtons

    def addQuickAccessButton(self, button: QtWidgets.QToolButton):
        """Add a widget to the quick access bar.

        :param button: The button to add.
        """
        button.setIconSize(QtCore.QSize(self._quickAccessButtonHeight, self._quickAccessButtonHeight))
        self._quickAccessButtons.append(button)
        self._quickAccessToolBar.addWidget(button)

    def setQuickAccessButtonHeight(self, height: int):
        """Set the height of the quick access buttons.

        :param height: The height to set.
        """
        self._quickAccessButtonHeight = height
        self._applicationButton.setIcon(self._applicationButton.icon().pixmap(height, height))
        self._quickAccessToolBar.setIconSize(QtCore.QSize(height, height))

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

    def rightToolBar(self) -> QtWidgets.QToolBar:
        """Return the right toolbar of the ribbon.

        :return: The right toolbar of the ribbon.
        """
        return self._rightToolBar

    def addRightToolButton(self, button: QtWidgets.QToolButton):
        """Add a widget to the right button bar.

        :param button: The button to add.
        """
        button.setIconSize(QtCore.QSize(self._rightButtonHeight, self._rightButtonHeight))
        self._rightToolButtons.append(button)
        self._rightToolBar.addWidget(button)

    def setRightToolBarHeight(self, height: int):
        """Set the height of the right buttons.

        :param height: The height to set.
        """
        self._rightButtonHeight = height
        self._rightToolBar.setIconSize(QtCore.QSize(height, height))

    def helpRibbonButton(self) -> QtWidgets.QToolButton:
        """Return the help ribbon button.

        :return: The help ribbon button.
        """
        return self._helpButton

    def setHelpButtonIcon(self, icon: QtGui.QIcon):
        """Set the icon of the help button.

        :param icon: The icon to set.
        """
        self._helpButton.setIcon(icon)

    def removeHelpButton(self):
        """Remove the help button from the ribbon."""
        self._helpButton.setVisible(False)

    def setCollapseButtonIcon(self, icon: QtGui.QIcon):
        """Set the icon of the min button.

        :param icon: The icon to set.
        """
        self._collapseRibbonButton.setIcon(icon)

    def removeCollapseButton(self):
        """Remove the min button from the ribbon."""
        self._collapseRibbonButton.setVisible(False)

    def collapseRibbonButton(self) -> QtWidgets.QToolButton:
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

    def topLevelWidget(self) -> QtWidgets.QWidget:
        widget = self
        while widget.parentWidget():
            widget = widget.parentWidget()
        return widget

    def mousePressEvent(self, e: QtGui.QMouseEvent):
        self._start_point = e.pos()
        self._window_point = self.topLevelWidget().frameGeometry().topLeft()

    def mouseMoveEvent(self, e: QtGui.QMouseEvent):
        relpos = e.pos() - self._start_point if self._start_point else None
        (self.topLevelWidget().move(self._window_point + relpos) if self._window_point and relpos else None)
        self.topLevelWidget().windowHandle().startSystemMove()

    def mouseDoubleClickEvent(self, e: QtGui.QMouseEvent):
        mainwindow = self.topLevelWidget()
        (mainwindow.showNormal() if mainwindow.isMaximized() else mainwindow.showMaximized())
