import typing

from PySide import QtCore, QtGui, QtWidgets
from PySide.QtGui import QIcon, QAction, QPixmap, QScrollEvent, QKeyEvent, QActionGroup


class RibbonMenu(QtWidgets.QMenu):
    @typing.overload
    def __init__(self, title: str = "", parent=None):
        pass

    @typing.overload
    def __init__(self, parent=None):
        pass

    def __init__(self, *args, **kwargs):
        """Create a new panel.

        :param title: The title of the menu.
        :param parent: The parent widget.
        """
        if (args and not isinstance(args[0], QtWidgets.QWidget)) or ("title" in kwargs):
            title = args[0] if len(args) > 0 else kwargs.get("title", "")
            parent = args[1] if len(args) > 1 else kwargs.get("parent", None)
        else:
            title = ""
            parent = args[0] if len(args) > 0 else kwargs.get("parent", None)
        super().__init__(title, parent)
        self.setFont(QtWidgets.QApplication.instance().font())  # type: ignore

    def addWidget(self, widget: QtWidgets.QWidget):
        """Add a widget to the menu.

        :param widget: The widget to add.
        """
        widgetAction = QtWidgets.QWidgetAction(self)
        widgetAction.setDefaultWidget(widget)
        self.addAction(widgetAction)

    def addHorizontalLayoutWidget(self) -> QtWidgets.QHBoxLayout:
        """Add a horizontal layout widget to the menu.

        :return: The horizontal layout.
        """
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        self.addWidget(widget)
        return layout

    def addVerticalLayoutWidget(self) -> QtWidgets.QVBoxLayout:
        """Add a vertical layout widget to the menu.

        :return: The vertical layout.
        """
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        self.addWidget(widget)
        return layout

    def addGridLayoutWidget(self) -> QtWidgets.QGridLayout:
        """Add a grid layout widget to the menu.

        :return: The grid layout.
        """
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QGridLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        self.addWidget(widget)
        return layout

    def addFormLayoutWidget(self) -> QtWidgets.QFormLayout:
        """Add a form layout widget to the menu.

        :return: The form layout.
        """
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QFormLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        self.addWidget(widget)
        return layout

    def addSpacing(self, spacing: int = 5):
        """Add spacing to the menu.

        :param spacing: The spacing.
        """
        spacer = QtWidgets.QLabel()
        spacer.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        spacer.setFixedHeight(spacing)
        self.addWidget(spacer)  # noqa

    def addLabel(self, text: str = "", alignment=QtCore.Qt.AlignmentFlag.AlignLeft):
        """Add a label to the menu.

        :param text: The text of the label.
        :param alignment: The alignment of the label.
        """
        label = QtWidgets.QLabel(text)
        label.setAlignment(alignment)
        self.addWidget(label)  # noqa


class RibbonPermanentMenu(RibbonMenu):
    """
    A permanent menu.
    """

    actionAdded = QtCore.Signal(QAction)

    def hideEvent(self, a0: QtGui.QHideEvent) -> None:
        self.show()

    def addAction(self, *args, **kwargs) -> QAction:
        action = super().addAction(*args, **kwargs)
        self.actionAdded.emit(action)
        return action
