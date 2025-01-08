import typing

from PySide.QtGui import QPaintEvent, QPen, QColor, QPainter
from PySide.QtWidgets import (
    QSizePolicy,
    QFrame,
    QWidget,
)
from PySide.QtCore import Qt, QSize, QPoint


class RibbonSeparator(QFrame):
    """The RibbonSeparator is a separator that can be used to separate widgets in a ribbon."""

    _topMargins: int = 4
    _bottomMargins: int = 4
    _leftMargins: int = 4
    _rightMargins: int = 4
    _orientation: Qt.Orientation

    @typing.overload
    def __init__(self, orientation=Qt.Orientation.Vertical, width=6, parent=None):
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
        if (args and not isinstance(args[0], QWidget)) or (
            "orientation" in kwargs or "width" in kwargs
        ):
            orientation = (
                args[0]
                if len(args) > 0
                else kwargs.get("orientation", Qt.Orientation.Vertical)
            )
            width = args[1] if len(args) > 1 else kwargs.get("width", 6)
            parent = args[2] if len(args) > 2 else kwargs.get("parent", None)
        else:
            orientation = Qt.Orientation.Vertical
            width = 6
            parent = args[0] if len(args) > 0 else kwargs.get("parent", None)
        super().__init__(parent=parent)
        self._orientation = orientation
        if orientation == Qt.Orientation.Horizontal:
            self.setFixedHeight(width)
            self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)  # type: ignore
        else:
            self.setFixedWidth(width)
            self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)  # type: ignore

    def sizeHint(self) -> QSize:
        """Return the size hint."""
        return self.size()

    def setTopBottomMargins(self, top: int, bottom: int) -> None:
        """Set the top and bottom margins."""
        self._topMargins = top
        self._bottomMargins = bottom

    def paintEvent(self, event: QPaintEvent) -> None:
        """Paint the separator."""
        painter = QPainter(self)
        pen = QPen()
        pen.setColor(QColor(Qt.GlobalColor.gray))
        painter.setPen(pen)
        if self._orientation == Qt.Orientation.Vertical:
            x1 = self.rect().center().x()
            painter.drawLine(
                QPoint(x1, self.rect().top() + self._topMargins),
                QPoint(x1, self.rect().bottom() - self._bottomMargins),
            )
        else:
            y1 = self.rect().center().y()
            painter.drawLine(
                QPoint(self.rect().left() + self._leftMargins, y1),
                QPoint(self.rect().right() - self._rightMargins, y1),
            )


class RibbonHorizontalSeparator(RibbonSeparator):
    """Horizontal separator."""

    def __init__(self, width: int = 6, parent=None) -> None:
        """Create a new horizontal separator.

        :param width: The width of the separator.
        :param parent: The parent widget.
        """
        super().__init__(Qt.Orientation.Horizontal, width, parent)


class RibbonVerticalSeparator(RibbonSeparator):
    """Vertical separator."""

    def __init__(self, width: int = 6, parent=None) -> None:
        """Create a new vertical separator.

        :param width: The width of the separator.
        :param parent: The parent widget.
        """
        super().__init__(Qt.Orientation.Vertical, width, parent)
