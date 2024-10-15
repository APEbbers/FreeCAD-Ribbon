import typing

from PySide import QtCore, QtGui, QtWidgets


class RibbonSeparator(QtWidgets.QFrame):
    """The RibbonSeparator is a separator that can be used to separate widgets in a ribbon."""

    _topMargins: int = 4
    _bottomMargins: int = 4
    _leftMargins: int = 4
    _rightMargins: int = 4
    _orientation: QtCore.Qt.Orientation

    @typing.overload
    def __init__(self, orientation=QtCore.Qt.Orientation.Vertical, width=6, parent=None):
        pass

    @typing.overload
    def __init__(self, parent=None):
        pass

    def __init__(self, *args, **kwargs):
        """Create a new separator.

        :param orientation: The orientation of the separator.
        :param width: The width of the separator.
        :param parent: The parent widget.
        """
        if (args and not isinstance(args[0], QtWidgets.QWidget)) or ("orientation" in kwargs or "width" in kwargs):
            orientation = args[0] if len(args) > 0 else kwargs.get("orientation", QtCore.Qt.Orientation.Vertical)
            width = args[1] if len(args) > 1 else kwargs.get("width", 6)
            parent = args[2] if len(args) > 2 else kwargs.get("parent", None)
        else:
            orientation = QtCore.Qt.Orientation.Vertical
            width = 6
            parent = args[0] if len(args) > 0 else kwargs.get("parent", None)
        super().__init__(parent=parent)
        self._orientation = orientation
        if orientation == QtCore.Qt.Orientation.Horizontal:
            self.setFixedHeight(width)
            self.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)  # type: ignore
        else:
            self.setFixedWidth(width)
            self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)  # type: ignore

    def sizeHint(self) -> QtCore.QSize:
        """Return the size hint."""
        return self.size()

    def setTopBottomMargins(self, top: int, bottom: int) -> None:
        """Set the top and bottom margins."""
        self._topMargins = top
        self._bottomMargins = bottom

    def paintEvent(self, event: QtGui.QPaintEvent) -> None:
        """Paint the separator."""
        painter = QtGui.QPainter(self)
        pen = QtGui.QPen()
        pen.setColor(QtGui.QColor(QtCore.Qt.GlobalColor.gray))
        painter.setPen(pen)
        if self._orientation == QtCore.Qt.Orientation.Vertical:
            x1 = self.rect().center().x()
            painter.drawLine(
                QtCore.QPoint(x1, self.rect().top() + self._topMargins),
                QtCore.QPoint(x1, self.rect().bottom() - self._bottomMargins),
            )
        else:
            y1 = self.rect().center().y()
            painter.drawLine(
                QtCore.QPoint(self.rect().left() + self._leftMargins, y1),
                QtCore.QPoint(self.rect().right() - self._rightMargins, y1),
            )


class RibbonHorizontalSeparator(RibbonSeparator):
    """Horizontal separator."""

    def __init__(self, width: int = 6, parent=None) -> None:
        """Create a new horizontal separator.

        :param width: The width of the separator.
        :param parent: The parent widget.
        """
        super().__init__(QtCore.Qt.Orientation.Horizontal, width, parent)


class RibbonVerticalSeparator(RibbonSeparator):
    """Vertical separator."""

    def __init__(self, width: int = 6, parent=None) -> None:
        """Create a new vertical separator.

        :param width: The width of the separator.
        :param parent: The parent widget.
        """
        super().__init__(QtCore.Qt.Orientation.Vertical, width, parent)
