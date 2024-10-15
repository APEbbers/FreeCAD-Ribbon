from PySide.QtWidgets import QToolButton
from PySide.QtCore import (
    Qt,
    QSize,
)

from .constants import RibbonButtonStyle
from .menu import RibbonMenu


class RibbonToolButton(QToolButton):
    """Tool button that is showed in the ribbon."""

    _buttonStyle: RibbonButtonStyle

    _largeButtonIconSize = 64
    _mediumButtonIconSize = 48
    _smallButtonIconSize = 32

    _maximumIconSize = 64

    def __init__(self, parent=None):
        """Create a new ribbon tool button.

        :param parent: The parent widget.
        """
        super().__init__(parent)

        # Styles
        self.setButtonStyle(RibbonButtonStyle.Large)
        self.setAutoRaise(True)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)

    def setMaximumIconSize(self, size: int):
        """Set the maximum icon size of the button.

        :param size: The maximum icon size of the button.
        """
        self._maximumIconSize = size
        self.setButtonStyle(self._buttonStyle)

    def maximumIconSize(self) -> int:
        """Get the maximum icon size of the button.

        :return: The maximum icon size of the button.
        """
        return self._maximumIconSize

    def setButtonStyle(self, style: RibbonButtonStyle):
        """Set the button style of the button.

        :param style: The button style of the button.
        """
        self._buttonStyle = style
        if style == RibbonButtonStyle.Small:
            height = self._smallButtonIconSize
            height = min(height, self._maximumIconSize)
            self.setIconSize(QSize(height, height))
            self.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
            self.setStyleSheet(
                """
                RibbonToolButton::menu-indicator {
                    subcontrol-origin: padding;
                    subcontrol-position: right;
                    right: -5px;
                }
                """
            )
        elif style == RibbonButtonStyle.Medium:
            height = self._mediumButtonIconSize
            height = min(height, self._maximumIconSize)
            self.setIconSize(QSize(height, height))
            self.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
            self.setStyleSheet(
                """
                RibbonToolButton::menu-indicator {
                    subcontrol-origin: padding;
                    subcontrol-position: right;
                    right: -5px;
                }
                """
            )
        elif style == RibbonButtonStyle.Large:
            height = self._largeButtonIconSize
            height = min(height, self._maximumIconSize)
            self.setIconSize(QSize(height, height))
            self.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
            self.setStyleSheet(
                """
                RibbonToolButton[popupMode="0"]::menu-indicator {
                    subcontrol-origin: padding;
                    subcontrol-position: bottom;
                    bottom: -5px;
                }
                RibbonToolButton[popupMode="2"]::menu-indicator {
                    subcontrol-origin: padding;
                    subcontrol-position: bottom;
                    bottom: -5px;
                }
                """
            )

    def buttonStyle(self) -> RibbonButtonStyle:
        """Get the button style of the button.

        :return: The button style of the button.
        """
        return self._buttonStyle

    def addRibbonMenu(self) -> RibbonMenu:
        """Add a ribbon menu for the button.

        :return: The added ribbon menu.
        """
        menu = RibbonMenu()
        self.setMenu(menu)
        return menu
