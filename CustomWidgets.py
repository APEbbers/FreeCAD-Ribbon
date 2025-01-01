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
import textwrap

from PySide.QtGui import QIcon, QAction, QFontMetrics, QFont, QTextOption, QCursor, QPalette, QEnterEvent
from PySide.QtWidgets import (
    QToolButton,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QMenu,
    QSpacerItem,
    QSizePolicy,
    QTextEdit,
    QStyleOption,
    QFrame,
    QGraphicsEffect,
)
from PySide.QtCore import Qt, QSize, QRect, QMargins, QEvent

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
        TextAlignment=Qt.AlignmentFlag.AlignCenter,
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

        # Define a vertical layout
        Layout = QVBoxLayout()
        # Add the command button
        Layout.addWidget(CommandButton)
        Layout.setAlignment(TextAlignment)
        # Set the content margins to zero
        Layout.setContentsMargins(0, 0, 0, 0)

        # If text must not be show, set the text to an empty string
        # Still create a label to set up the button properly
        if showText is True:
            # Create a label with the correct properties
            Label_Text = QTextEdit()
            Label_Text.setReadOnly(True)
            Label_Text.setFrameShape(QFrame.Shape.NoFrame)
            Label_Text.setFrameShadow(QFrame.Shadow.Plain)
            Label_Text.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)
            Label_Text.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
            Label_Text.document().setDocumentMargin(0)
            Label_Text.viewport().setCursor(Qt.CursorShape.ArrowCursor)
            Label_Text.setFocusPolicy(Qt.FocusPolicy.NoFocus)
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
            # Determine the height of a single row
            SingleHeight = QFontMetrics(Font).boundingRect(Text).height() + 3
            # make sure that the label height is at least for two lines
            Label_Text.setMinimumHeight((SingleHeight * 1))
            Label_Text.setMaximumHeight((SingleHeight * MaxNumberOfLines) + 3)
            # # Enable wordwrap
            # Label_Text.setWordWrap(setWordWrap)
            # Set the width of the label based on the size of the button
            Label_Text.setFixedWidth(ButtonSize.width())
            # Adjust the size to be able to store the actual height
            Label_Text.adjustSize()
            # Set the textheight
            if setWordWrap is True:
                # Determine the maximum length per line
                FontMetrics = QFontMetrics(Text)
                maxWidth = 0
                maxLength = 0
                for c in Text:
                    maxWidth = maxWidth + FontMetrics.boundingRectChar(c).width()
                    if maxWidth < ButtonSize.width():
                        maxLength = maxLength + 1
                    if maxWidth >= ButtonSize.width():
                        break
                Label_Text.setText(StandardFunctions.ReturnWrappedText(Text, maxWidth, MaxNumberOfLines, False))
                Label_Text.setMaximumHeight((SingleHeight * MaxNumberOfLines) - 3)
                Label_Text.setAlignment(TextAlignment)
                Label_Text.adjustSize()
                TextHeight = Label_Text.height()
            # Add the label with alignment
            Layout.addWidget(Label_Text)
            # # Set the content margins to zero
            # Layout.setContentsMargins(0, 0, 0, 0)

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
                # Create custom events
                #
                # Peform a menu click when clicked on the label
                def mouseClickevent(event):
                    ArrowButton.animateClick()

                Label_Text.mousePressEvent = lambda mouseClick: mouseClickevent(mouseClick)
                ArrowButton.mousePressEvent = lambda mouseClick: mouseClickevent(mouseClick)

                # Change the background color for commandbutton and label on hovering
                def enterEventCustom(event):
                    if ArrowButton.underMouse():
                        Label_Text.setStyleSheet(
                            "background-color: " + StyleMapping.ReturnStyleItem("Background_Color_Hover")
                        )
                    if Label_Text.underMouse():
                        ArrowButton.setStyleSheet(
                            "QToolButton::menu-indicator {padding-bottom: "
                            + str(MenuButtonSpace)
                            + "px;subcontrol-origin: padding;subcontrol-position: center bottom;}"
                            + "QToolButton { background-color: "
                            + StyleMapping.ReturnStyleItem("Background_Color_Hover")
                            + ";}"
                        )

                Label_Text.enterEvent = lambda enterEvent: enterEventCustom(enterEvent)
                ArrowButton.enterEvent = lambda enterEvent: enterEventCustom(enterEvent)

                # restore the stylesheets on leaving
                def leaveEventCustom(event):
                    ArrowButton.setStyleSheet(
                        "QToolButton::menu-indicator {padding-bottom: "
                        + str(MenuButtonSpace)
                        + "px;subcontrol-origin: padding;subcontrol-position: center bottom;}"
                    )
                    Label_Text.setStyleSheet(
                        StyleMapping.ReturnStyleSheet(
                            control="toolbutton",
                            radius="2px",
                        )
                    )

                Label_Text.leaveEvent = lambda leaveEvent: leaveEventCustom(leaveEvent)
                ArrowButton.leaveEvent = lambda leaveEvent: leaveEventCustom(leaveEvent)
        else:
            if showText is True:
                # Create custom events
                #
                # Peform a menu click when clicked on the label
                def mouseClickevent(event):
                    CommandButton.animateClick()

                Label_Text.mousePressEvent = lambda mouseClick: mouseClickevent(mouseClick)
                ArrowButton.mousePressEvent = lambda mouseClick: mouseClickevent(mouseClick)

                # Change the background color for commandbutton and label on hovering
                def enterEventCustom(event):
                    CommandButton.setStyleSheet(
                        "background-color: " + StyleMapping.ReturnStyleItem("Background_Color_Hover")
                    )

                    Label_Text.setStyleSheet(
                        "background-color: " + StyleMapping.ReturnStyleItem("Background_Color_Hover")
                    )

                Label_Text.enterEvent = lambda enterEvent: enterEventCustom(enterEvent)
                CommandButton.enterEvent = lambda enterEvent: enterEventCustom(enterEvent)

                # restore the stylesheets on leaving
                def leaveEventCustom(event):
                    CommandButton.setStyleSheet(
                        StyleMapping.ReturnStyleSheet(
                            control="toolbutton",
                            radius="2px",
                        )
                    )
                    Label_Text.setStyleSheet(
                        StyleMapping.ReturnStyleSheet(
                            control="toolbutton",
                            radius="2px",
                        )
                    )

                Label_Text.leaveEvent = lambda leaveEvent: leaveEventCustom(leaveEvent)
                CommandButton.leaveEvent = lambda leaveEvent: leaveEventCustom(leaveEvent)

                Label_Text.setToolTip(CommandButton.toolTip())

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
        TextAlignment=Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft,
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

        # Define a vertical layout
        Layout = QHBoxLayout()
        # Add the command button
        Layout.addWidget(CommandButton)
        Layout.setAlignment(TextPositionAlignment)
        # Set the content margins to zero
        Layout.setContentsMargins(0, 0, 0, 0)

        # If text must be shown wrapped, add a layout with label
        if showText is True:
            # Create a label
            Label_Text = QTextEdit()
            Label_Text.setReadOnly(True)
            Label_Text.setFrameShape(QFrame.Shape.NoFrame)
            Label_Text.setFrameShadow(QFrame.Shadow.Plain)
            Label_Text.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)
            Label_Text.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
            Label_Text.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
            Label_Text.document().setDocumentMargin(0)
            Label_Text.viewport().setCursor(Qt.CursorShape.ArrowCursor)
            Label_Text.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            Label_Text.setSizeAdjustPolicy(QTextEdit.SizeAdjustPolicy.AdjustToContents)
            Label_Text.setFixedHeight(ButtonSize.height())
            # Set the font
            Font = QFont()
            Font.setPointSize(FontSize)
            Label_Text.setFont(Font)
            FontMetrics = QFontMetrics(Font)
            if setWordWrap is True:
                Label_Text.setWordWrapMode(QTextOption.WrapMode.WordWrap)
                # Determine the maximum length per line
                FontMetrics = QFontMetrics(Text)
                maxWidth = 0
                maxLength = 0
                for c in Text:
                    maxWidth = maxWidth + FontMetrics.boundingRectChar(c).width()
                    if maxWidth < ButtonSize.width() * 2:
                        maxLength = maxLength + 1
                    if maxWidth >= ButtonSize.width() * 2:
                        break
                Label_Text.setText(StandardFunctions.ReturnWrappedText(Text, maxLength, MaxNumberOfLines, False))
                Label_Text.adjustSize()

                line1 = StandardFunctions.ReturnWrappedText(Text, maxLength, MaxNumberOfLines, True)[0]
                try:
                    line2 = StandardFunctions.ReturnWrappedText(Text, maxLength, MaxNumberOfLines, True)[1]
                    if FontMetrics.boundingRect(line1).width() > FontMetrics.boundingRect(line2).width():
                        TextWidth = FontMetrics.tightBoundingRect(textwrap.dedent(line1)).width()
                    else:
                        TextWidth = FontMetrics.tightBoundingRect(textwrap.dedent(line2)).width()
                except Exception:
                    TextWidth = FontMetrics.tightBoundingRect(textwrap.dedent(line1)).width()

            if setWordWrap is False:
                if ElideMode != Qt.TextElideMode.ElideNone:
                    Text = FontMetrics.elidedText(Text, ElideMode, ButtonSize.width() * 3, Qt.TextFlag.TextSingleLine)
                MaxNumberOfLines = 1
                Label_Text.setWordWrapMode(QTextOption.WrapMode.NoWrap)
                Label_Text.setText(" " + Text)
                Label_Text.adjustSize()
                Label_Text.setFixedHeight(CommandButton.height())
                marginCorrection = (CommandButton.height() - FontMetrics.boundingRect(Text).height()) / 2
                Label_Text.setViewportMargins(0, marginCorrection, 0, 0)
                TextWidth = FontMetrics.boundingRect(Text).width() + 6
            # Set the text alignment
            TextAlignment = Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft
            Label_Text.setAlignment(TextAlignment)
            # # Define a vertical layout
            # Layout = QHBoxLayout()
            # # Add the command button
            # Layout.addWidget(CommandButton)
            # Add the label with alignment
            Layout.addWidget(Label_Text)
            # Layout.setAlignment(TextPositionAlignment)
            # # Set the content margins to zero
            # Layout.setContentsMargins(0, 0, 0, 0)

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
                # Create custom events
                #
                # Peform a menu click when clicked on the label
                def mouseClickevent(event):
                    ArrowButton.animateClick()

                Label_Text.mousePressEvent = lambda mouseClick: mouseClickevent(mouseClick)
                ArrowButton.mousePressEvent = lambda mouseClick: mouseClickevent(mouseClick)

                # Change the background color for commandbutton and label on hovering
                def enterEventCustom(event):
                    if ArrowButton.underMouse():
                        Label_Text.setStyleSheet(
                            "background-color: " + StyleMapping.ReturnStyleItem("Background_Color_Hover")
                        )
                    if Label_Text.underMouse():
                        ArrowButton.setStyleSheet(
                            "QToolButton::menu-indicator {padding-right: "
                            + str(MenuButtonSpace + TextWidth)
                            + "px;subcontrol-origin: padding;subcontrol-position: center;}"
                            + "QToolButton { background-color: "
                            + StyleMapping.ReturnStyleItem("Background_Color_Hover")
                            + ";}"
                        )

                Label_Text.enterEvent = lambda enterEvent: enterEventCustom(enterEvent)
                ArrowButton.enterEvent = lambda enterEvent: enterEventCustom(enterEvent)

                # restore the stylesheets on leaving
                def leaveEventCustom(event):
                    ArrowButton.setStyleSheet(
                        "QToolButton::menu-indicator {padding-right: "
                        + str(MenuButtonSpace + TextWidth)
                        + "px;subcontrol-origin: padding;subcontrol-position: center;}"
                    )
                    Label_Text.setStyleSheet(
                        StyleMapping.ReturnStyleSheet(
                            control="toolbutton",
                            radius="2px",
                        )
                    )

                Label_Text.leaveEvent = lambda leaveEvent: leaveEventCustom(leaveEvent)
                ArrowButton.leaveEvent = lambda leaveEvent: leaveEventCustom(leaveEvent)
        else:
            # Add the label to the area where the user can invoke the menu
            if showText is True:
                # Create custom events
                #
                # Peform a menu click when clicked on the label
                def mouseClickevent(event):
                    CommandButton.animateClick()

                Label_Text.mousePressEvent = lambda mouseClick: mouseClickevent(mouseClick)
                ArrowButton.mousePressEvent = lambda mouseClick: mouseClickevent(mouseClick)

                # Change the background color for commandbutton and label on hovering
                def enterEventCustom(event):
                    CommandButton.setStyleSheet(
                        "QToolButton, QTextEdit { background-color: "
                        + StyleMapping.ReturnStyleItem("Background_Color_Hover")
                        + ";}"
                    )

                    Label_Text.setStyleSheet(
                        "QToolButton, QTextEdit { background-color: "
                        + StyleMapping.ReturnStyleItem("Background_Color_Hover")
                        + ";}"
                    )

                Label_Text.enterEvent = lambda enterEvent: enterEventCustom(enterEvent)
                CommandButton.enterEvent = lambda enterEvent: enterEventCustom(enterEvent)

                # restore the stylesheets on leaving
                def leaveEventCustom(event):
                    CommandButton.setStyleSheet(
                        StyleMapping.ReturnStyleSheet(
                            control="toolbutton",
                            radius="2px",
                        )
                    )
                    Label_Text.setStyleSheet(
                        StyleMapping.ReturnStyleSheet(
                            control="toolbutton",
                            radius="2px",
                        )
                    )

                Label_Text.leaveEvent = lambda leaveEvent: leaveEventCustom(leaveEvent)
                CommandButton.leaveEvent = lambda leaveEvent: leaveEventCustom(leaveEvent)

                # Copy the tooltip from the commandbutton to the label
                Label_Text.setToolTip(CommandButton.toolTip())

            # Set the menubutton space to zero because there is no menu
            MenuButtonSpace = 0
        # Set the minimum height for the button
        CommandButton.setMinimumHeight(ButtonSize.height())
        # Set spacing to zero (highlighting will be strange otherwise)
        Layout.setSpacing(0)
        # Add the layout
        btn.setLayout(Layout)
        # Set the stylesheet for the whole button
        btn.setStyleSheet(
            StyleMapping.ReturnStyleSheet(
                control="toolbutton",
                radius="2px",
            )
        )
        # Set the correct dimensions
        btn.setFixedWidth(CommandButton.width() + MenuButtonSpace + TextWidth)
        btn.setFixedHeight(CommandButton.height())

        # return the new button
        return btn
