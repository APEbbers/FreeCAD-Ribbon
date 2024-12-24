# *************************************************************************
# *                                                                       *
# * Copyright (c) 2019-2024 Hakan Seven, Geolta, Paul Ebbers              *
# *                                                                       *
# * This program is free software; you can redistribute it and/or modify  *
# * it under the terms of the GNU Lesser General Public License (LGPL)    *
# * as published by the Free Software Foundation; either version 3 of     *
# * the License, or (at your option) any later version.                   *
# * for detail see the LICENCE text file.                                 *
# *                                                                       *
# * This program is distributed in the hope that it will be useful,       *
# * but WITHOUT ANY WARRANTY; without even the implied warranty of        *
# * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
# * GNU Library General Public License for more details.                  *
# *                                                                       *
# * You should have received a copy of the GNU Library General Public     *
# * License along with this program; if not, write to the Free Software   *
# * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
# * USA                                                                   *
# *                                                                       *
# *************************************************************************
import FreeCAD as App
import FreeCADGui as Gui
from pathlib import Path

from PySide6.QtGui import (
    QIcon,
    QAction,
    QFontMetrics,
)
from PySide6.QtWidgets import (
    QToolButton,
    QVBoxLayout,
    QLabel,
    QMenu,
)
from PySide6.QtCore import (
    Qt,
    QSize,
    QRect,
)

import os
import sys
import Parameters_Ribbon
import Standard_Functions_RIbbon as StandardFunctions
import StyleMapping

# Get the resources
pathIcons = Parameters_Ribbon.ICON_LOCATION
pathStylSheets = Parameters_Ribbon.STYLESHEET_LOCATION
pathUI = Parameters_Ribbon.UI_LOCATION
pathScripts = os.path.join(os.path.dirname(__file__), "Scripts")
pathPackages = os.path.join(os.path.dirname(__file__), "Resources", "packages")
sys.path.append(pathIcons)
sys.path.append(pathStylSheets)
sys.path.append(pathUI)
sys.path.append(pathPackages)

translate = App.Qt.translate


class CustomControls:
    def LargeCustomToolButton(
        Text: str,
        Action: QAction,
        Icon: QIcon,
        IconSize: QSize,
        ButtonSize: QSize,
        FontSize: int = 10,
        showText=True,
        TextAlignment=Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignHCenter,
        TextPositionAlignment=Qt.AlignmentFlag.AlignBottom,
        setWordWrap=True,
        MaxNumberOfLines=2,
        Menu: QMenu = None,
    ):
        btn = QToolButton()
        # Set the buttonSize
        btn.setFixedSize(ButtonSize)
        # Set the icon and its size
        btn.setIcon(Icon)
        btn.setIconSize(IconSize.expandedTo(btn.geometry().size()))
        # Set the content margins to zero
        btn.setContentsMargins(0, 0, 0, 0)
        if Menu is None:
            btn.addAction(Action)
        btn.setDefaultAction(Action)
        if Menu is not None:
            btn.setMenu(Menu)
            btn.setPopupMode(QToolButton.ToolButtonPopupMode.MenuButtonPopup)
            btn.setDefaultAction(btn.actions()[0])
            btn.setStyleSheet(StyleMapping.ReturnStyleSheet("toolbutton", "2px", f"{10}px"))
            btn.setFixedWidth(btn.width() + 10)

        # If text must be shown wrapped, add a layout with label
        if showText is True and setWordWrap is True:
            # Create a label
            Label_Text = QLabel(Text)
            # Set the textFormat
            Label_Text.setTextFormat(Qt.TextFormat.RichText)
            # Determine the height of a single row
            FontMetrics = QFontMetrics(Text)
            SingleHeight = FontMetrics.boundingRect(Text).height()
            # make sure that the label height is at least for two lines
            Label_Text.setMinimumHeight((SingleHeight * 2))
            Label_Text.setMaximumHeight((SingleHeight * MaxNumberOfLines))
            # Enable wordwrap
            Label_Text.setWordWrap(True)
            # Set the width of the label based on the size of the button
            Label_Text.setFixedWidth(ButtonSize.width())
            # Adjust the size to be able to store the actual height
            Label_Text.adjustSize()
            # Set the font
            Font = Label_Text.font()
            Font.setPixelSize(FontSize)
            Label_Text.setFont(Font)
            # Set the text alignment
            Label_Text.setAlignment(TextAlignment)
            # Define a vertical layout
            Layout = QVBoxLayout()
            # Add the label with alignment
            Layout.addWidget(Label_Text)
            Layout.setAlignment(TextPositionAlignment)
            # Set the content margins to zero
            Layout.setContentsMargins(0, 0, 0, 0)
            # Add the layout to the button
            btn.setLayout(Layout)
            # Add padding to the bottom. This makes room for the label
            TextHeight = Label_Text.height()
            btn.setStyleSheet(
                """QToolButton {
                padding-bottom: """
                + str(TextHeight)
                + """px;}"""
            )
        # If text must be shown on one line, use the normal way
        if showText is True and setWordWrap is False:
            btn.setText(Text)

        return btn
