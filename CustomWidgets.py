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

from PySide.QtGui import (
    QIcon,
    QAction,
    QFontMetrics,
    QFont,
    QTextOption,
)
from PySide.QtWidgets import (
    QToolButton,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QMenu,
    QSpacerItem,
    QSizePolicy,
)
from PySide.QtCore import (
    Qt,
    QSize,
    QRect,
    QMargins,
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
        TextAlignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter,
        setWordWrap=True,
        ElideMode=Qt.TextElideMode.ElideMiddle,
        MaxNumberOfLines=2,
        Menu: QMenu = None,
        MenuButtonSpace=10,
    ):
        btn = QToolButton()
        CommandButton = QToolButton()
        ArrowButton = QToolButton()
        Layout = QVBoxLayout()
        #
        TextHeight = 0
        # Set the buttonSize
        CommandButton.setMaximumSize(ButtonSize)
        # Set the icon and its size
        CommandButton.setIcon(Icon)
        CommandButton.setIconSize(IconSize.expandedTo(CommandButton.size()))
        # Set the content margins to zero
        CommandButton.setContentsMargins(0, 0, 0, 0)
        if len(Menu.actions()) == 0:
            CommandButton.addAction(Action)
        CommandButton.setDefaultAction(Action)

        # If text must not be show, set the text to an empty string
        # Still create a label to set up the button properly
        if showText is False:
            Text = ""
        # Create a label
        Label_Text = QLabel()
        # Set the font
        Font = QFont()
        Font.setPointSize(FontSize)
        Label_Text.setFont(Font)
        Label_Text.setText(Text)
        # If there is no WordWrap, set the ElideMode and the max number of lines to 1.
        if setWordWrap is False:
            FontMetrics = QFontMetrics(Text)
            Text = FontMetrics.elidedText(Text, ElideMode, btn.width(), Qt.TextFlag.TextSingleLine)
            Label_Text.setText(Text)
            MaxNumberOfLines = 1
        # Set the textFormat
        Label_Text.setTextFormat(Qt.TextFormat.RichText)
        # Determine the height of a single row
        FontMetrics = QFontMetrics(Label_Text.text())
        SingleHeight = FontMetrics.tightBoundingRect(Label_Text.text()).height()
        # make sure that the label height is at least for two lines
        Label_Text.setMinimumHeight((SingleHeight * 1))
        Label_Text.setMaximumHeight((SingleHeight * MaxNumberOfLines) + 3)
        # Enable wordwrap
        Label_Text.setWordWrap(setWordWrap)
        # Set the width of the label based on the size of the button
        Label_Text.setFixedWidth(ButtonSize.width())
        # Adjust the size to be able to store the actual height
        Label_Text.adjustSize()
        # Set the textheight
        if setWordWrap is True:
            # Enable wordwrap
            Label_Text.setWordWrap(True)
            Label_Text.adjustSize()
            FontMetrics = QFontMetrics(Label_Text.text())
            textOption = QTextOption()
            textOption.setWrapMode(QTextOption.WrapMode.WordWrap)
            rect = FontMetrics.boundingRect(Text, textOption)
            TextHeight = rect.height()
        # Set the text alignment
        Label_Text.setAlignment(TextAlignment)
        # Define a vertical layout
        Layout = QVBoxLayout()
        # Add the command button
        Layout.addWidget(CommandButton)
        # Add the label with alignment
        Layout.addWidget(Label_Text)
        # Set the content margins to zero
        Layout.setContentsMargins(0, 0, 0, 0)

        if Menu is not None and len(Menu.actions()) > 1:
            # Define a menu
            ArrowButton.setMenu(Menu)
            ArrowButton.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)
            # Set the height according the space for the menubutton
            ArrowButton.setFixedHeight(MenuButtonSpace)
            # Set the width according the commandbutton
            ArrowButton.setFixedWidth(CommandButton.width())
            ArrowButton.adjustSize()
            # Set the arrow at the bottom
            ArrowButton.setArrowType(Qt.ArrowType.NoArrow)
            # remove the menuindicator from the stylesheet
            ArrowButton.setStyleSheet(
                "QToolButton::menu-indicator {padding-bottom: "
                + str(MenuButtonSpace)
                + "px;subcontrol-origin: padding;subcontrol-position: center bottom;}"
            )
            # Set the content margins
            ArrowButton.setContentsMargins(0, 0, 0, 0)
            # Add the Arrow button to the layout
            Layout.addWidget(ArrowButton)

            # Add the label to the area where the user can invoke the menu
            if showText is True:

                def mouseClickevent(event):
                    ArrowButton.animateClick()

                Label_Text.mousePressEvent = lambda mouseClick: mouseClickevent(mouseClick)
                ArrowButton.mousePressEvent = lambda mouseClick: mouseClickevent(mouseClick)
        else:

            def mouseClickevent(event):
                CommandButton.animateClick()

            Label_Text.mousePressEvent = lambda mouseClick: mouseClickevent(mouseClick)
            ArrowButton.mousePressEvent = lambda mouseClick: mouseClickevent(mouseClick)
            Label_Text.setToolTip(ArrowButton.toolTip())
            MenuButtonSpace = 0

        CommandButton.setMinimumHeight(ButtonSize.height() - MenuButtonSpace - TextHeight)
        Layout.setSpacing(0)
        btn.setLayout(Layout)

        # Set the stylesheet
        btn.setStyleSheet(
            StyleMapping.ReturnStyleSheet(
                control="toolbutton",
                radius="2px",
            )
        )
        CommandButton.setStyleSheet(btn.styleSheet())
        btn.setFixedWidth(CommandButton.width())
        btn.setFixedHeight(CommandButton.height() + TextHeight)
        return btn

    def CustomToolButton(
        Text: str,
        Action: QAction,
        Icon: QIcon,
        IconSize: QSize,
        ButtonSize: QSize,
        FontSize: int = 10,
        showText=True,
        TextAlignment=Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignLeft,
        TextPositionAlignment=Qt.AlignmentFlag.AlignLeft,
        setWordWrap=True,
        ElideMode=Qt.TextElideMode.ElideNone,
        MaxNumberOfLines=2,
        Menu: QMenu = None,
        MenuButtonSpace=10,
    ):
        btn = QToolButton()
        CommandButton = QToolButton()
        ArrowButton = QToolButton()
        Layout = QHBoxLayout()
        #
        TextWidth = 0
        Text = Text.strip()
        # Set the buttonSize
        CommandButton.setFixedSize(ButtonSize)
        # Set the icon and its size
        CommandButton.setIcon(Icon)
        CommandButton.setIconSize(IconSize)
        # Set the content margins to zero
        CommandButton.setContentsMargins(0, 0, 0, 0)
        if len(Menu.actions()) == 0:
            CommandButton.addAction(Action)
        CommandButton.setDefaultAction(Action)

        # If text must be shown wrapped, add a layout with label
        if showText is False:
            Text = ""
        # Create a label
        Label_Text = QLabel()
        # Set the font
        Font = QFont()
        Font.setPointSize(FontSize)
        Label_Text.setFont(Font)
        Label_Text.setText(Text)
        # Determine the dimensions of a single row
        FontMetrics = QFontMetrics(Text)
        SingleHeight = FontMetrics.boundingRect(Text).height()
        SingleWidth = 0
        for c in Text:
            SingleWidth = SingleWidth + FontMetrics.boundingRectChar(c).width()
        # Set the width of the label based on the size of the button
        Label_Text.setMaximumWidth(SingleWidth)
        # Adjust the size to be able to store the actual height
        Label_Text.adjustSize()
        if setWordWrap is True:
            # Enable wordwrap
            Label_Text.setWordWrap(True)
            Label_Text.adjustSize()
            SingleWidth = Label_Text.rect().width()
            TextAlignment = Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft
        # check if the icon is not too small for wrap
        if btn.height() < SingleHeight:
            setWordWrap = False
        # If there is no WordWrap, set the ElideMode and the max number of lines to 1.
        if setWordWrap is False and ElideMode == Qt.TextElideMode.ElideMiddle:
            Label_Text.setMaximumSize(ButtonSize.width() * 3, SingleHeight)
            Label_Text.adjustSize()
            ElidedText = FontMetrics.elidedText(Text, ElideMode, SingleWidth, Qt.TextFlag.TextSingleLine)
            Label_Text.setText(ElidedText)
            MaxNumberOfLines = 1
        # make sure that the label height is at least for two lines
        Label_Text.setMinimumHeight(SingleHeight * 1)
        Label_Text.setMaximumHeight(SingleHeight * MaxNumberOfLines)
        # Set the text alignment
        Label_Text.setAlignment(TextAlignment)
        TextWidth = SingleWidth + 5
        # Define a vertical layout
        Layout = QHBoxLayout()
        # Add the command button
        Layout.addWidget(CommandButton)
        # Add the label with alignment
        Layout.addWidget(Label_Text)
        Layout.setAlignment(TextPositionAlignment)
        # Set the content margins to zero
        Layout.setContentsMargins(0, 0, 0, 0)

        if Menu is not None and len(Menu.actions()) > 1:
            # Define a menu
            ArrowButton.setMenu(Menu)
            ArrowButton.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)
            # Set the height according the space for the menubutton
            ArrowButton.setFixedHeight(CommandButton.height())
            # Set the width according the commandbutton
            ArrowButton.setFixedWidth(MenuButtonSpace)
            ArrowButton.adjustSize()
            # Set the arrow at the bottom
            ArrowButton.setArrowType(Qt.ArrowType.NoArrow)
            # remove the menuindicator from the stylesheet
            ArrowButton.setStyleSheet(
                "QToolButton::menu-indicator {padding-right: "
                + str(MenuButtonSpace + TextWidth)
                + "px;subcontrol-origin: padding;subcontrol-position: center;}"
            )
            # Set the content margins
            ArrowButton.setContentsMargins(0, 0, 0, 0)
            # Add the Arrow button to the layout
            Layout.addWidget(ArrowButton)

            # Add the label to the area where the user can invoke the menu
            if showText is True:

                def mouseClickevent(event):
                    ArrowButton.animateClick()

                Label_Text.mousePressEvent = lambda mouseClick: mouseClickevent(mouseClick)
                ArrowButton.mousePressEvent = lambda mouseClick: mouseClickevent(mouseClick)
        else:
            # Add the label to the area where the user can invoke the menu
            if showText is True:

                def mouseClickevent(event):
                    CommandButton.animateClick()

                Label_Text.mousePressEvent = lambda mouseClick: mouseClickevent(mouseClick)
                ArrowButton.mousePressEvent = lambda mouseClick: mouseClickevent(mouseClick)
                Label_Text.setToolTip(ArrowButton.toolTip())
            MenuButtonSpace = 0

        CommandButton.setMinimumHeight(ButtonSize.height())
        Layout.setSpacing(3)
        btn.setLayout(Layout)

        btn.setStyleSheet(
            StyleMapping.ReturnStyleSheet(
                control="toolbutton",
                radius="2px",
            )
        )
        CommandButton.setStyleSheet(btn.styleSheet())
        btn.setFixedWidth(CommandButton.width() + MenuButtonSpace + TextWidth)
        btn.setFixedHeight(CommandButton.height())
        return btn
