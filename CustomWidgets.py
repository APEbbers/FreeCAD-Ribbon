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
from inspect import Traceback
from types import TracebackType
import FreeCAD as App
import FreeCADGui as Gui
from pathlib import Path
import textwrap
import typing

import sys

from PySide.QtGui import (
    QIcon,
    QAction,
    QFontMetrics,
    QFont,
    QTextOption,
    QCursor,
    QDrag,
    QPixmap,
    QColor,
    QBrush,
    QPaintEvent,
    QPen,
    QPainter,
)
from PySide.QtWidgets import (
    QComboBox,
    QSizePolicy,
    QSpinBox,
    QToolButton,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QMenu,
    QTextEdit,
    QFrame,
    QCheckBox,
    QWidget,
    QWidgetAction,
)
from PySide.QtCore import (
    Qt,
    QSize,
    QMimeData,
    QPoint,
    QPointF,
    QRectF,
    QEasingCurve,
    QPropertyAnimation,
    QSequentialAnimationGroup,
    Slot,
    Property,
    Signal,
)

import os
import sys
import Parameters_Ribbon
import Standard_Functions_Ribbon as StandardFunctions
import StyleMapping_Ribbon

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


import pyqtribbon_local as pyqtribbon
from pyqtribbon_local.ribbonbar import RibbonMenu, RibbonBar
from pyqtribbon_local.panel import RibbonPanel, RibbonPanelItemWidget
from pyqtribbon_local.toolbutton import RibbonToolButton
from pyqtribbon_local.separator import RibbonSeparator
from pyqtribbon_local.category import RibbonCategoryLayoutButton

translate = App.Qt.translate


class CustomControls(RibbonToolButton):
    def mouseMoveEvent(self, e):
        if e.buttons() == Qt.MouseButton.LeftButton:
            try:
                drag = QDrag(self)
                mime = QMimeData()
                drag.setMimeData(mime)
                pixmap = QPixmap(self.size())
                self.render(pixmap)
                drag.setPixmap(pixmap)

                if drag is not None:
                    drag.exec(Qt.DropAction.MoveAction)
            except Exception as e:
                print(e)

    def LargeCustomToolButton(
        Text: str,
        Action: QAction,
        Icon: QIcon,
        IconSize: QSize,
        ButtonSize: QSize,
        FontSize: int = 11,
        showText=True,
        TextAlignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter,
        setWordWrap=True,
        MaxNumberOfLines=2,
        Menu: QMenu = None,
        MenuButtonSpace=10,
        parent=None,
    ):
        # Define the controls
        btn = RibbonToolButton()
        CommandButton = QToolButton()
        ArrowButton = QToolButton()
        Layout = QVBoxLayout()
        Label_Text = QLabel()

        # Set the default stylesheet
        StyleSheet_Addition_Button = (
            "QToolButton, QToolButton:hover {background-color: "
            + StyleMapping_Ribbon.ReturnStyleItem("Background_Color")
            + ";border: none"
            + ";}"
        )
        btn.setStyleSheet(StyleSheet_Addition_Button)
        # Define the parameters
        CommandButtonHeight = 0
        TextWidth = 0
        Space = 6
        if showText is False:
            Space = 0
        # Remove any trailing spaces
        Text = Text.strip()
        # # Set the buttonSize
        # CommandButton.setFixedSize(ButtonSize)
        # CommandButtonHeight = ButtonSize.height()
        # Set the icon and its size
        CommandButton.setIcon(Icon)
        CommandButton.setIconSize(IconSize.expandedTo(CommandButton.size()))
        # Set the content margins to zero
        CommandButton.setContentsMargins(0, 0, 0, 0)
        # Add a actions if there is only one
        if Menu is not None:
            if len(Menu.actions()) == 0:
                CommandButton.addAction(Action)
        CommandButton.setDefaultAction(Action)
        
        CommandButton.setObjectName("CommandButton")
        ArrowButton.setObjectName("MenuButton")

        # Define a vertical layout
        Layout = QVBoxLayout()
        # Add the command button
        Layout.addWidget(CommandButton)
        Layout.setAlignment(TextAlignment)
        # Set the content margins to zero
        Layout.setContentsMargins(0, 0, 0, 0)

        # if showText is False:
        if MenuButtonSpace < 10:
            MenuButtonSpace = 10

        # If text must not be show, set the text to an empty string
        # Still create a label to set up the button properly
        # Determine the height of a single row
        # Set the font
        Font = QFont()
        Font.setPixelSize(FontSize)
        Label_Text.setFont(Font)
        SingleHeight = QFontMetrics(Font).boundingRect("Text").height() + 3
        Label_Text.setMinimumHeight(SingleHeight * 1)
        Label_Text.setMaximumHeight(SingleHeight * MaxNumberOfLines)
        # Set the width of the label based on the size of the button
        Label_Text.setFixedWidth(ButtonSize.width())
        if Text != "":
            # Create a label with the correct properties
            # Label_Text = QTextEdit()
            # Label_Text.setReadOnly(True)
            Label_Text.setFrameShape(QFrame.Shape.NoFrame)
            Label_Text.setFrameShadow(QFrame.Shadow.Plain)
            Label_Text.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)
            # Label_Text.setHorizontalScrollBarPolicy(
            #     Qt.ScrollBarPolicy.ScrollBarAlwaysOff
            # )
            # Label_Text.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
            # Label_Text.document().setDocumentMargin(0)
            # Label_Text.viewport().setCursor(Qt.CursorShape.ArrowCursor)
            Label_Text.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            # # Set the font
            # Font = QFont()
            # Font.setPixelSize(FontSize)
            # Label_Text.setFont(Font)
            # change the menubutton space because text is included in the click area
            MenuButtonSpace = 10
            # # Determine the height of a single row
            # SingleHeight = QFontMetrics(Font).boundingRect(Text).height() + 3
            # Label_Text.setMinimumHeight(SingleHeight * 1)
            # Label_Text.setMaximumHeight(SingleHeight * MaxNumberOfLines)
            # # Set the width of the label based on the size of the button
            # Label_Text.setFixedWidth(ButtonSize.width())

            # If there is no WordWrap, set the ElideMode and the max number of lines to 1.
            if setWordWrap is False:
                # Determine the maximum length per line
                FontMetrics = QFontMetrics(Text)
                maxWidth = 0
                maxLength = 0
                for c in Text:
                    maxWidth = maxWidth + FontMetrics.horizontalAdvance(c, -1)
                    if maxWidth < ButtonSize.width():
                        maxLength = maxLength + 1
                    if maxWidth >= ButtonSize.width():
                        limit = maxLength - 3
                        Text = Text[:limit].strip() + "..."
                        break
                # Set the text with a placeholder
                Label_Text.setWordWrap(False)
                Label_Text.setText(Text)
                # Set the maximum number of lines to 1
                MaxNumberOfLines = 1
                # Set the proper alignment
                Label_Text.setAlignment(TextAlignment)
                # # Lower the height when there is a menu
                # if Menu is not None and len(Menu.actions()) > 1:
                #     Label_Text.setFixedHeight(SingleHeight)
                # else:
                #     Label_Text.setFixedHeight(SingleHeight + Space)

            # If wordwrap is enabled, set the text and height accordingly
            if setWordWrap is True:
                # Set the wrap mode
                Label_Text.setWordWrap(True)
                # Determine the maximum length per line
                FontMetrics = QFontMetrics(Font)
                maxWidth = 0
                maxLength = 0
                for c in Text:
                    maxWidth = maxWidth + FontMetrics.horizontalAdvance(c, -1)
                    if maxWidth < ButtonSize.width():
                        maxLength = maxLength + 1
                    if maxWidth >= ButtonSize.width():
                        break
                # maxLength = maxLength + 3 
                maxLength = maxLength

                # Get the first text line
                line1 = StandardFunctions.ReturnWrappedText(
                    Text, maxLength, MaxNumberOfLines, True
                )[0]
                # Set the alignment
                Label_Text.setAlignment(TextAlignment)
                # Add the line
                Label_Text.setText(line1)
                # get the text width
                TextWidth = FontMetrics.tightBoundingRect(line1).width()
                # Try to get the second line if there is one
                try:
                    line2 = StandardFunctions.ReturnWrappedText(
                        Text, maxLength, MaxNumberOfLines, True
                    )[1]
                    # Set the alignment
                    Label_Text.setAlignment(TextAlignment)
                    # Add the line
                    Label_Text.setText(line1 + "\n" +line2)
                    # Update the text width if neccesary
                    if FontMetrics.tightBoundingRect(line2).width() > TextWidth:
                        TextWidth = FontMetrics.tightBoundingRect(line2).width()
                except Exception as e:
                    # print(e.with_traceback(None))
                    pass

            # Add the label with alignment
            Layout.addWidget(Label_Text)
            CommandButtonHeight = CommandButtonHeight - Label_Text.height()

        if Menu is not None and len(Menu.actions()) > 1:
            # Define a menu
            Menu.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
            StyleSheet_Menu = (
                "QMenu::item, QMenu::menuAction, QMenuBar::item, QMenu>QLabel {font-size: "
                + str(Parameters_Ribbon.FONTSIZE_MENUS)
                + "px;}"
            )
            Menu.setStyleSheet(StyleSheet_Menu)
            ArrowButton.setMenu(Menu)
            ArrowButton.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)
            # Set the height according the space for the menubutton
            ArrowButton.setFixedHeight(MenuButtonSpace)
            # Set the width according the commandbutton
            ArrowButton.setFixedWidth(ButtonSize.width() + Space)
            ArrowButton.adjustSize()
            # Set the arrow to none
            ArrowButton.setArrowType(Qt.ArrowType.NoArrow)
            # Set the content margins
            ArrowButton.setContentsMargins(0, 0, 0, 0)
            # Add the Arrow button to the layout
            Layout.addWidget(ArrowButton)

            # # Add the label to the area where the user can invoke the menu
            def mouseClickevent(event):
                ArrowButton.animateClick()

            Label_Text.mousePressEvent = lambda mouseClick: mouseClickevent(
                mouseClick
            )
            ArrowButton.mousePressEvent = lambda mouseClick: mouseClickevent(
                mouseClick
            )

            # Change the background color for commandbutton and label on hovering (CSS)
            def enterEventCustom(event):
                BorderColor = StyleMapping_Ribbon.ReturnStyleItem("Border_Color")
                if Parameters_Ribbon.CUSTOM_COLORS_ENABLED:
                    BorderColor = Parameters_Ribbon.COLOR_BORDERS
                if Parameters_Ribbon.BORDER_TRANSPARANT:
                    BorderColor = StyleMapping_Ribbon.ReturnStyleItem(
                        "Background_Color_Hover"
                    )
                if showText is False:
                    StyleSheet_Addition_Arrow = (
                        "QToolButton, QLabel {background-color: "
                        + StyleMapping_Ribbon.ReturnStyleItem("Background_Color_Hover")
                        + ";border: 0.5px solid "
                        + BorderColor
                        # + ";border-top: 0.5px solid "
                        # + StyleMapping_Ribbon.ReturnStyleItem("Background_Color_Hover")
                        + ";border-top-left-radius: 2px;border-bottom-left-radius: 2px;"
                        + "border-top-right-radius: 2px;border-bottom-right-radius: 2px"
                        + ";margin: 0px"
                        + ";spacing: 0px"
                        + ";}"
                        + """QToolButton::menu-indicator {
                                subcontrol-origin: padding;
                                subcontrol-position: center top;
                            }"""
                    )
                    StyleSheet_Addition_Label = (
                        "QToolButton, QLabel {background-color: "
                        + StyleMapping_Ribbon.ReturnStyleItem("Background_Color_Hover")
                        + ";border: 0.5px solid "
                        + BorderColor
                        # + ";border-bottom: 0.5px solid "
                        # + StyleMapping_Ribbon.ReturnStyleItem("Background_Color_Hover")
                        + ";border-top-left-radius: 2px;border-bottom-left-radius: 2px;"
                        + "border-top-right-radius: 2px;border-bottom-right-radius: 2px"
                        + ";margin: 0px"
                        + ";spacing: 0px"
                        + ";}"
                    )
                if showText is True:
                    StyleSheet_Addition_Arrow = (
                        "QToolButton, QLabel {background-color: "
                        + StyleMapping_Ribbon.ReturnStyleItem("Background_Color_Hover")
                        + ";border: 0.5px solid "
                        + BorderColor
                        + ";border-top: 0.5px solid "
                        + StyleMapping_Ribbon.ReturnStyleItem("Background_Color_Hover")
                        + ";border-top-left-radius: 0px;border-bottom-left-radius: 2px;"
                        + "border-top-right-radius: 0px;border-bottom-right-radius: 2px"
                        + ";margin: 0px"
                        + ";spacing: 0px"
                        + ";}"
                        + """QToolButton::menu-indicator {
                                subcontrol-origin: padding;
                                subcontrol-position: center top;
                            }"""
                    )
                    StyleSheet_Addition_Label = (
                        "QToolButton, QLabel {background-color: "
                        + StyleMapping_Ribbon.ReturnStyleItem("Background_Color_Hover")
                        + ";border: 0.5px solid "
                        + BorderColor
                        + ";border-bottom: 0.5px solid "
                        + StyleMapping_Ribbon.ReturnStyleItem("Background_Color_Hover")
                        + ";border-top-left-radius: 2px;border-bottom-left-radius: 0px;"
                        + "border-top-right-radius: 2px;border-bottom-right-radius: 0px"
                        + ";margin: 0px"
                        + ";spacing: 0px"
                        + ";}"
                    )
                StyleSheet_Addition_Button = (
                    "QToolButton, QLabel, RibbonToolButton {background-color: "
                    + StyleMapping_Ribbon.ReturnStyleItem("Background_Color")
                    + ";border: "
                    + BorderColor
                    + ";margin: 0px"
                    + ";spacing: 0px"
                    + ";}"
                )
                btn.setStyleSheet(StyleSheet_Addition_Button)
                if ArrowButton.underMouse():
                    Label_Text.setStyleSheet(StyleSheet_Addition_Label)
                    ArrowButton.setStyleSheet(StyleSheet_Addition_Arrow)
                if Label_Text.underMouse():
                    Label_Text.setStyleSheet(StyleSheet_Addition_Label)
                    ArrowButton.setStyleSheet(StyleSheet_Addition_Arrow)

                if parent is not None:
                    # Set the value in the parent for detecting that the menu is entered.
                    # Needed for keeping the ribbon open while showing a dropdown menu
                    parent.MenuEntered = True

            Label_Text.enterEvent = lambda enterEvent: enterEventCustom(enterEvent)
            ArrowButton.enterEvent = lambda enterEvent: enterEventCustom(enterEvent)

            # restore the stylesheets on leaving
            def leaveEventCustom(event):
                StyleSheet = StyleMapping_Ribbon.ReturnStyleSheet(
                    control="toolbutton",
                    radius="2px",
                )
                StyleSheet_Addition = """QToolButton::menu-indicator {
                    subcontrol-origin: padding;
                    subcontrol-position: center top;
                }"""
                Label_Text.setStyleSheet(StyleSheet)
                ArrowButton.setStyleSheet(StyleSheet_Addition + StyleSheet)

                # If the menu is hidden, set the value in the parent for detecting that the menu is entered to False.
                if Menu.isHidden():
                    if parent is not None:
                        parent.MenuEntered = False

            Label_Text.leaveEvent = lambda leaveEvent: leaveEventCustom(leaveEvent)
            ArrowButton.leaveEvent = lambda leaveEvent: leaveEventCustom(leaveEvent)

            # Set MenuEntered to False. This allows the ribbon to fold after leaving the menu and the ribbon.
            def SetToFoldRibbon():
                if parent is not None:
                    # If the menu is hidden, set the value in the parent for detecting that the menu is entered to False.
                    parent.MenuEntered = False
                    pos = QCursor.pos()
                    if parent.geometry().contains(pos) is False:
                        parent.FoldRibbon()

            Menu.aboutToHide.connect(SetToFoldRibbon)

            CommandButtonHeight = CommandButtonHeight - ArrowButton.height()
        else:
            MenuButtonSpace = 0
            # if showText is True:
            # Create custom events
            #
            # Peform a menu click when clicked on the label
            def mouseClickevent(event):
                CommandButton.animateClick()

            Label_Text.mousePressEvent = lambda mouseClick: mouseClickevent(
                mouseClick
            )

            # Change the background color for commandbutton and label on hovering (CSS)
            def enterEventCustom(event):
                BorderColor = StyleMapping_Ribbon.ReturnStyleItem("Border_Color")
                if Parameters_Ribbon.CUSTOM_COLORS_ENABLED:
                    BorderColor = Parameters_Ribbon.COLOR_BORDERS
                if Parameters_Ribbon.BORDER_TRANSPARANT:
                    BorderColor = StyleMapping_Ribbon.ReturnStyleItem(
                        "Background_Color_Hover"
                    )
                if showText is False:
                    StyleSheet_Addition_Label = (
                        "QToolButton, QLabel {background-color: "
                        + StyleMapping_Ribbon.ReturnStyleItem("Background_Color_Hover")
                        + ";border: 0.5px solid"
                        + BorderColor
                        # + ";border-top: 0px solid"
                        # + StyleMapping_Ribbon.ReturnStyleItem("Background_Color_Hover")
                        + ";border-top-left-radius: 2px;border-bottom-left-radius: 2px;"
                        + "border-top-right-radius: 2px;border-bottom-right-radius: 2px"
                        + ";margin: 0px"
                        + ";spacing: 0px"
                        + ";}"
                    )
                    StyleSheet_Addition_Command = (
                        "QToolButton, QLabel {background-color: "
                        + StyleMapping_Ribbon.ReturnStyleItem("Background_Color_Hover")
                        + ";border: 0.5px solid"
                        + BorderColor
                        # + ";border-bottom: 0px solid"
                        # + StyleMapping_Ribbon.ReturnStyleItem("Background_Color_Hover")
                        + ";border-top-left-radius: 2px;border-bottom-left-radius: 2px;"
                        + "border-top-right-radius: 2px;border-bottom-right-radius: 2px"
                        + ";margin: 0px"
                        + ";spacing: 0px"
                        + ";}"
                    )
                if showText is True:
                    StyleSheet_Addition_Label = (
                        "QToolButton, QLabel {background-color: "
                        + StyleMapping_Ribbon.ReturnStyleItem("Background_Color_Hover")
                        + ";border: 0.5px solid"
                        + BorderColor
                        + ";border-top: 0px solid"
                        + StyleMapping_Ribbon.ReturnStyleItem("Background_Color_Hover")
                        + ";border-top-left-radius: 0px;border-bottom-left-radius: 2px;"
                        + "border-top-right-radius: 0px;border-bottom-right-radius: 2px"
                        + ";margin: 0px"
                        + ";spacing: 0px"
                        + ";}"
                    )
                    StyleSheet_Addition_Command = (
                        "QToolButton, QLabel {background-color: "
                        + StyleMapping_Ribbon.ReturnStyleItem("Background_Color_Hover")
                        + ";border: 0.5px solid"
                        + BorderColor
                        + ";border-bottom: 0px solid"
                        + StyleMapping_Ribbon.ReturnStyleItem("Background_Color_Hover")
                        + ";border-top-left-radius: 2px;border-bottom-left-radius: 0px;"
                        + "border-top-right-radius: 2px;border-bottom-right-radius: 0px"
                        + ";margin: 0px"
                        + ";spacing: 0px"
                        + ";}"
                    )
                StyleSheet_Addition_Button = (
                    "QToolButton, QLabel {background-color: "
                    + StyleMapping_Ribbon.ReturnStyleItem("Background_Color")
                    + ";border: "
                    + BorderColor
                    + ";margin: 0px"
                    + ";spacing: 0px"
                    + ";}"
                )
                btn.setStyleSheet(StyleSheet_Addition_Button)
                if CommandButton.underMouse():
                    Label_Text.setStyleSheet(StyleSheet_Addition_Label)
                    CommandButton.setStyleSheet(StyleSheet_Addition_Command)
                if Label_Text.underMouse():
                    Label_Text.setStyleSheet(StyleSheet_Addition_Label)
                    CommandButton.setStyleSheet(StyleSheet_Addition_Command)

            Label_Text.enterEvent = lambda enterEvent: enterEventCustom(enterEvent)
            CommandButton.enterEvent = lambda enterEvent: enterEventCustom(
                enterEvent
            )

            if showText is False:
                # Hide the text and set the width
                Label_Text.setHidden(True)
                TextWidth = 0

            # restore the stylesheets on leaving
            def leaveEventCustom(event):
                StyleSheet = StyleMapping_Ribbon.ReturnStyleSheet(
                    control="toolbutton",
                    radius="2px",
                )
                StyleSheet_Addition = (
                    "QToolButton, QToolButton:hover, QLabel, QLabel:hover {background-color: "
                    + StyleMapping_Ribbon.ReturnStyleItem("Background_Color")
                    + ";border: 0.5px solid"
                    + StyleMapping_Ribbon.ReturnStyleItem("Background_Color")
                    + ";}"
                )
                Label_Text.setStyleSheet(StyleSheet_Addition + StyleSheet)
                CommandButton.setStyleSheet(StyleSheet)

            Label_Text.leaveEvent = lambda leaveEvent: leaveEventCustom(leaveEvent)
            CommandButton.leaveEvent = lambda leaveEvent: leaveEventCustom(leaveEvent)
            # Set the tooltip for the label equeal to that of the commandbutton
            Label_Text.setToolTip(CommandButton.toolTip())

        btn.mouseMoveEvent = lambda mouseEvent: CustomControls.mouseMoveEvent(
            btn, mouseEvent
        )

        # Set the spacing to zero. If not, the CSS styling will show gaps
        Layout.setSpacing(0)
        # Add the layout to the button
        btn.setLayout(Layout)
        
        if showText is False:
            # Hide the text and set the width
            Label_Text.setHidden(True)
            TextWidth = 0

        # Set the stylesheet
        StyleSheet = StyleMapping_Ribbon.ReturnStyleSheet(
            control="toolbutton", radius="2px"
        )
        # StyleSheet_Addition_Label = (
        #     "QToolButton, QLabel {background-color: "
        #     + StyleMapping_Ribbon.ReturnStyleItem("Background_Color")
        #     # + ";border: 0.5px solid"
        #     # + StyleMapping_Ribbon.ReturnStyleItem("Background_Color")
        #     # + ";border-top: 0px solid"
        #     # + StyleMapping_Ribbon.ReturnStyleItem("Background_Color")
        #     # + ";border-radius: 2px"
        #     + ";margin: 0px"
        #     + ";spacing: 0px"
        #     + ";}"
        # )
        # StyleSheet_Addition_Command = (
        #     "QToolButton, QLabel {background-color: "
        #     + StyleMapping_Ribbon.ReturnStyleItem("Background_Color")
        #     # + ";border: 0.5px solid"
        #     # + StyleMapping_Ribbon.ReturnStyleItem("Background_Color")
        #     # + ";border-bottom: 0px solid"
        #     # + StyleMapping_Ribbon.ReturnStyleItem("Background_Color")
        #     # + ";border-radius: 2px"
        #     + ";margin: 0px"
        #     + ";spacing: 0px"
        #     + ";}"
        # )
        # StyleSheet_Addition_Button = (
        #     "QToolButton, QLabel {background-color: "
        #     + StyleMapping_Ribbon.ReturnStyleItem("Background_Color")
        #     + ";border: none"
        #     + ";}"
        # )
        StyleSheet_Addition_Arrow = (
            "QToolButton, QLabel {background-color: "
            + StyleMapping_Ribbon.ReturnStyleItem("Background_Color")
            # + ";border: 0.5px solid"
            # + StyleMapping_Ribbon.ReturnStyleItem("Background_Color")
            # + ";border-top: 0px solid"
            # + StyleMapping_Ribbon.ReturnStyleItem("Background_Color")
            # + ";border-radius: 2px"
            + ";margin: 0px"
            + ";spacing: 0px"
            + ";}"
            + """QToolButton::menu-indicator {
                    subcontrol-origin: padding;
                    subcontrol-position: center top;
                }"""
        )
        # CommandButton.setStyleSheet(StyleSheet_Addition_Command + StyleSheet)
        ArrowButton.setStyleSheet(StyleSheet_Addition_Arrow + StyleSheet)
        # Label_Text.setStyleSheet(StyleSheet_Addition_Label + StyleSheet)
        # btn.setStyleSheet(StyleSheet_Addition_Button + StyleSheet)
        CommandButton.setStyleSheet(StyleSheet)
        # ArrowButton.setStyleSheet(StyleSheet)
        Label_Text.setStyleSheet(StyleSheet)
        btn.setStyleSheet(StyleSheet)

        # Set the final sizes
        width = ButtonSize.width()
        # if TextWidth == 0 or TextWidth < CommandButtonHeight + Space:
        #     width = CommandButtonHeight + Space
        # if TextWidth > 0 and TextWidth > CommandButtonHeight + Space:
        #     width = TextWidth + Space
        Label_Text.setFixedWidth(width)
        if len(Menu.actions()) <= 1:
            Label_Text.setFixedHeight(Label_Text.height()+ MenuButtonSpace)
        ArrowButton.setFixedWidth(width)
        # CommandButton.setFixedSize(QSize(width, CommandButtonHeight))
        CommandButton.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        btn.setFixedSize(QSize(width, ButtonSize.height()))

        # Return the button
        btn.setObjectName("CustomWidget_Large")
        return btn

    def CustomToolButton(
        Text: str,
        Action: QAction,
        Icon: QIcon,
        IconSize: QSize,
        ButtonSize: QSize,
        FontSize: int = 11,
        showText=True,
        TextAlignment=Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft,
        TextPositionAlignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft,
        setWordWrap=True,
        ElideMode=False,
        MaxNumberOfLines=2,
        Menu: QMenu = None,
        MenuButtonSpace=16,
        parent=None,
    ):
        # Define the controls
        btn = RibbonToolButton()
        CommandButton = QToolButton()
        ArrowButton = QToolButton()
        Layout = QHBoxLayout()
        Label_Text = QLabel()
        # Set the default stylesheet
        StyleSheet_Addition_Button = (
            "QToolButton, QToolButton:hover, RibbonToolButton, RibbonToolButton:hover {background-color: "
            + StyleMapping_Ribbon.ReturnStyleItem("Background_Color")
            + ";border: none"
            + ";}"
        )
        btn.setStyleSheet(StyleSheet_Addition_Button)
        # Define the parameters
        TextWidth = 0
        space = 6
        # Remove any trailing spaces
        Text = Text.strip()
        # Set the buttonSize
        CommandButton.setFixedWidth(ButtonSize.width())
        # Set the icon and its size
        CommandButton.setIcon(Icon)
        CommandButton.setIconSize(IconSize)
        # Set the content margins to zero
        CommandButton.setContentsMargins(0, 0, 0, 0)
        # Add a actions if there is only one
        if Menu is not None:
            if len(Menu.actions()) == 0:
                CommandButton.addAction(Action)
        CommandButton.setDefaultAction(Action)
        
        CommandButton.setObjectName("CommandButton")
        ArrowButton.setObjectName("MenuButton")

        # Define a vertical layout
        Layout = QHBoxLayout()
        # Add the command button
        Layout.addWidget(CommandButton)
        Layout.setAlignment(TextPositionAlignment)

        # Set the content margins to zero
        Layout.setContentsMargins(0, 0, 0, 0)

        # if showText is False:
        if MenuButtonSpace < 12:
            MenuButtonSpace = 12

        # If text must be shown wrapped, add a layout with label
        if Text != "":
            # Create a label
            Label_Text.setFrameShape(QFrame.Shape.NoFrame)
            Label_Text.setFrameShadow(QFrame.Shadow.Plain)
            Label_Text.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            # Label_Text.setFixedHeight(ButtonSize.height())
            # Set the font
            Font = QFont()
            Font.setPixelSize(FontSize)
            Label_Text.setFont(Font)
            FontMetrics = QFontMetrics(Font)
            if setWordWrap is True:
                Label_Text.setWordWrap(True)
                # Determine the maximum length per line
                FontMetrics = QFontMetrics(Font)
                maxWidth = 0
                maxLength = 0
                for c in Text:
                    maxWidth = maxWidth + FontMetrics.horizontalAdvance(c, -1)
                    if maxWidth < ButtonSize.width() * 2:
                        maxLength = maxLength + 1
                    if maxWidth >= ButtonSize.width() * 2:
                        break
                # Get the first text line
                line1 = StandardFunctions.ReturnWrappedText(
                    Text, maxLength, MaxNumberOfLines, True
                )[0]
                # Add the line with a space to avoid te need to set spacing. (Spacing breaks the hover background)
                Label_Text.setText(" " + line1)
                # Try to get the second line if there is one
                try:
                    line2 = StandardFunctions.ReturnWrappedText(
                        Text, maxLength, MaxNumberOfLines, True
                    )[1]
                    # Add the line with a space to avoid te need to set spacing. (Spacing breaks the hover background)
                    Label_Text.setText(Label_Text.text() + "\n" +" " + line2)
                    if (
                        FontMetrics.tightBoundingRect(line1).width()
                        > FontMetrics.tightBoundingRect(line2).width()
                    ):
                        # Update a parameter for the width
                        TextWidth = FontMetrics.tightBoundingRect(line1).width()
                    else:
                        # Update a parameter for the width
                        TextWidth = FontMetrics.tightBoundingRect(line2).width()
                except Exception:
                    # Correct the margin to set the arrow vertical center (bug in Qt)
                    marginCorrection = (
                        CommandButton.height() - FontMetrics.boundingRect(Text).height()
                    ) / 2
                    # Update a parameter for the width
                    TextWidth = FontMetrics.tightBoundingRect(line1).width()

                # Adjust the size
                Label_Text.setMaximumWidth(TextWidth + space)
                # Update a parameter for the width
                TextWidth = TextWidth + space

                # If the text is higher than the commandbutton, switch to no wrap
                if (
                    FontMetrics.boundingRect(line1).height() * MaxNumberOfLines
                ) > ButtonSize.height():
                    setWordWrap = False
                    # reset the values
                    TextWidth = 0
                    Label_Text.setMaximumWidth(
                        FontMetrics.tightBoundingRect(line1).width()
                    )  # set to a extra large value to avoid clipping
                    StandardFunctions.Print(
                        "Medium button is too small for text wrap!\n wrap setting is ignored",
                        "Warning",
                    )

            if setWordWrap is False:
                # if the text must be elided, return a updated text
                if ElideMode is True:
                    # Determine the maximum length per line
                    FontMetrics = QFontMetrics(Text)
                    maxWidth = 0
                    maxLength = 0
                    for c in Text:
                        maxWidth = maxWidth + FontMetrics.horizontalAdvance(c, -1)
                        if maxWidth < ButtonSize.width() * 3:
                            maxLength = maxLength + 1
                        if maxWidth >= ButtonSize.width() * 3:
                            limit = maxLength - 3
                            Text = Text[:limit].strip() + "..."
                            break
                # Set the number of lines to 1 and disable wrap
                MaxNumberOfLines = 1
                Label_Text.setWordWrap(False)
                # Add the line with a space to avoid te need to set spacing. (Spacing breaks the hover background)
                Label_Text.setText(" " + Text)
                # Update the size
                # Label_Text.setFixedHeight(ButtonSize.height())
                # Label_Text.adjustSize()
                # Correct the margin to set the arrow vertical center (bug in Qt)
                # marginCorrection = (
                #     CommandButton.height() - FontMetrics.boundingRect(Text).height()
                # ) / 2
                # Label_Text.setViewportMargins(0, marginCorrection, 0, 0)
                # Update the width parameter
                TextWidth = FontMetrics.boundingRect(Text).width() + space
                Label_Text.setMaximumWidth(TextWidth)
            # Set the text alignment
            TextAlignment = Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft
            Label_Text.setAlignment(TextAlignment)
            # Set the margins to zero
            Label_Text.setContentsMargins(0, 0, 0, 0)
            # Add the label with alignment
            Layout.addWidget(Label_Text)

        if Menu is not None and len(Menu.actions()) > 1:
            # Define a menu
            ArrowButton.setMenu(Menu)
            Menu.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
            StyleSheet_Menu = (
                "QMenu::item, QMenu::menuAction, QMenuBar::item, QMenu>QLabel {font-size: "
                + str(Parameters_Ribbon.FONTSIZE_MENUS)
                + "px;}"
            )
            Menu.setStyleSheet(StyleSheet_Menu)
            ArrowButton.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)
            # Set the height according the space for the menubutton
            ArrowButton.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
            # Set the width according the commandbutton
            ArrowButton.setFixedWidth(MenuButtonSpace)
            ArrowButton.adjustSize()
            # Set the arrow to none. It will be defined via CSS
            ArrowButton.setArrowType(Qt.ArrowType.NoArrow)
            # Set the content margins
            ArrowButton.setContentsMargins(0, 0, 0, 0)
            # Add the Arrow button to the layout
            Layout.addWidget(ArrowButton)

            # Add the label to the area where the user can invoke the menu
            # Create custom events
            #
            # Peform a menu click when clicked on the label
            def mouseClickevent(event):
                ArrowButton.animateClick()

            Label_Text.mousePressEvent = lambda mouseClick: mouseClickevent(
                mouseClick
            )
            ArrowButton.mousePressEvent = lambda mouseClick: mouseClickevent(
                mouseClick
            )

            # Change the background color for commandbutton and label on hovering (CSS)
            def enterEventCustom(event):
                BorderColor = StyleMapping_Ribbon.ReturnStyleItem("Border_Color")
                if Parameters_Ribbon.CUSTOM_COLORS_ENABLED:
                    BorderColor = Parameters_Ribbon.COLOR_BORDERS
                if Parameters_Ribbon.BORDER_TRANSPARANT:
                    BorderColor = StyleMapping_Ribbon.ReturnStyleItem(
                        "Background_Color_Hover"
                    )     
                StyleSheet_Addition_Arrow = ""
                StyleSheet_Addition_Label = ""   
                if showText is False:        
                    StyleSheet_Addition_Arrow = (
                        "QToolButton, QLabel {"
                        + "background-color: "
                        + StyleMapping_Ribbon.ReturnStyleItem("Background_Color_Hover")
                        + ";border: 0.5px solid"
                        + BorderColor
                        # + ";border-left: 0.5 px solid"
                        # + StyleMapping_Ribbon.ReturnStyleItem("Background_Color_Hover")
                        + ";border-top-left-radius: 2px;border-bottom-left-radius: 2px;"
                        + "border-top-right-radius: 2px;border-bottom-right-radius: 2px"
                        + ";margin: 0px"
                        + ";spacing: 0px"
                        + ";}"
                    )
                    StyleSheet_Addition_Label = (
                        "QToolButton, QLabel {background-color: "
                        + StyleMapping_Ribbon.ReturnStyleItem("Background_Color_Hover")
                        + ";border: 0.5px solid"
                        + BorderColor
                        # + ";border-right: 0.5px solid"
                        # + StyleMapping_Ribbon.ReturnStyleItem("Background_Color_Hover")
                        + ";border-top-left-radius: 2px;border-bottom-left-radius: 2px;"
                        + "border-top-right-radius: 2px;border-bottom-right-radius: 2px"
                        + ";margin: 0px"
                        + ";spacing: 0px"
                        + ";}"
                    )
                if showText is True:        
                    StyleSheet_Addition_Arrow = (
                        "QToolButton, QLabel {background-color: "
                        + StyleMapping_Ribbon.ReturnStyleItem("Background_Color_Hover")
                        + ";border: 0.5px solid"
                        + BorderColor
                        + ";border-left: 0.5 px solid"
                        + StyleMapping_Ribbon.ReturnStyleItem("Background_Color_Hover")
                        + ";border-top-left-radius: 0px;border-bottom-left-radius: 0px;"
                        + "border-top-right-radius: 2px;border-bottom-right-radius: 2px"
                        + ";margin: 0px"
                        + ";spacing: 0px"
                        + ";}"
                    )
                    StyleSheet_Addition_Label = (
                        "QToolButton, QLabel {background-color: "
                        + StyleMapping_Ribbon.ReturnStyleItem("Background_Color_Hover")
                        + ";border: 0.5px solid"
                        + BorderColor
                        + ";border-right: 0.5px solid"
                        + StyleMapping_Ribbon.ReturnStyleItem("Background_Color_Hover")
                        + ";border-top-left-radius: 2px;border-bottom-left-radius: 2px;"
                        + "border-top-right-radius: 0px;border-bottom-right-radius: 0px"
                        + ";margin: 0px"
                        + ";spacing: 0px"
                        + ";}"
                    )
                StyleSheet_Addition_Button = (
                    "QToolButton, QLabel {background-color: "
                    + StyleMapping_Ribbon.ReturnStyleItem("Background_Color")
                    + ";border: "
                    + BorderColor
                    + ";margin: 0px"
                    + ";spacing: 0px"
                    + ";}"
                )
                btn.setStyleSheet(StyleSheet_Addition_Button)
                if ArrowButton.underMouse():
                    Label_Text.setStyleSheet(StyleSheet_Addition_Label)
                    ArrowButton.setStyleSheet(StyleSheet_Addition_Arrow)
                if Label_Text.underMouse():
                    Label_Text.setStyleSheet(StyleSheet_Addition_Label)
                    ArrowButton.setStyleSheet(StyleSheet_Addition_Arrow)

                if parent is not None:
                    # Set the value in the parent for detecting that the menu is entered.
                    # Needed for keeping the ribbon open while showing a dropdown menu
                    parent.MenuEntered = True

                Label_Text.enterEvent = lambda enterEvent: enterEventCustom(enterEvent)
                ArrowButton.enterEvent = lambda enterEvent: enterEventCustom(enterEvent)

            Label_Text.enterEvent = lambda enterEvent: enterEventCustom(enterEvent)
            CommandButton.enterEvent = lambda enterEvent: enterEventCustom(
                enterEvent
            )

            # restore the stylesheets on leaving
            def leaveEventCustom(event):
                StyleSheet = StyleMapping_Ribbon.ReturnStyleSheet(
                    control="toolbutton",
                    radius="2px",
                )
                Label_Text.setStyleSheet(StyleSheet)
                ArrowButton.setStyleSheet(StyleSheet)

                if parent is not None:
                    # If the menu is hidden, set the value in the parent for detecting that the menu is entered to False.
                    if Menu.isHidden():
                        parent.MenuEntered = False

            Label_Text.leaveEvent = lambda leaveEvent: leaveEventCustom(leaveEvent)
            ArrowButton.leaveEvent = lambda leaveEvent: leaveEventCustom(leaveEvent)

            # Set MenuEntered to False. This allows the ribbon to fold after leaving the menu and the ribbon.
            def SetToFoldRibbon():
                if parent is not None:
                    # If the menu is hidden, set the value in the parent for detecting that the menu is entered to False.
                    parent.MenuEntered = False
                    pos = QCursor.pos()
                    if parent.geometry().contains(pos) is False:
                        parent.FoldRibbon()

            Menu.aboutToHide.connect(SetToFoldRibbon)
        else:
            # Add the label to the area where the user can invoke the command
            def mouseClickevent(event):
                CommandButton.animateClick()

            Label_Text.mousePressEvent = lambda mouseClick: mouseClickevent(
                mouseClick
            )
            ArrowButton.mousePressEvent = lambda mouseClick: mouseClickevent(
                mouseClick
            )

            # Change the background color for commandbutton and label on hovering (CSS)
            def enterEventCustom(event):
                BorderColor = StyleMapping_Ribbon.ReturnStyleItem("Border_Color")
                if Parameters_Ribbon.CUSTOM_COLORS_ENABLED:
                    BorderColor = Parameters_Ribbon.COLOR_BORDERS
                if Parameters_Ribbon.BORDER_TRANSPARANT:
                    BorderColor = StyleMapping_Ribbon.ReturnStyleItem(
                        "Background_Color_Hover"
                    )
                if showText is False:
                    StyleSheet_Addition_Label = (
                        "QToolButton, QLabel, RibbonToolButton {background-color: "
                        + StyleMapping_Ribbon.ReturnStyleItem("Background_Color_Hover")
                        + ";border: 0.5px solid"
                        + BorderColor
                        # + ";border-left: 0.5px solid"
                        # + StyleMapping_Ribbon.ReturnStyleItem("Background_Color_Hover")
                        + ";border-top-left-radius: 2px;border-bottom-left-radius: 2px;"
                        + "border-top-right-radius: 2px;border-bottom-right-radius: 2px"
                        + ";margin: 0px"
                        + ";spacing: 0px"
                        + ";}"
                    )
                    StyleSheet_Addition_Command = (
                        "QToolButton, QLabel, RibbonToolButton {background-color: "
                        + StyleMapping_Ribbon.ReturnStyleItem("Background_Color_Hover")
                        + ";border: 0.5px solid"
                        + BorderColor
                        # + ";border-right: 0.5px solid"
                        # + StyleMapping_Ribbon.ReturnStyleItem("Background_Color_Hover")
                        + ";border-top-left-radius: 2px;border-bottom-left-radius: 2px;"
                        + "border-top-right-radius: 2px;border-bottom-right-radius: 2px"
                        + ";margin: 0px"
                        + ";spacing: 0px"
                        + ";}"
                    )
                if showText is True:
                    StyleSheet_Addition_Label = (
                        "QToolButton, QLabel, RibbonToolButton {background-color: "
                        + StyleMapping_Ribbon.ReturnStyleItem("Background_Color_Hover")
                        + ";border: 0.5px solid"
                        + BorderColor
                        + ";border-left: 0.5px solid"
                        + StyleMapping_Ribbon.ReturnStyleItem("Background_Color_Hover")
                        + ";border-top-left-radius: 0px;border-bottom-left-radius: 0px;"
                        + "border-top-right-radius: 2px;border-bottom-right-radius: 2px"
                        + ";margin: 0px"
                        + ";spacing: 0px"
                        + ";}"
                    )
                    StyleSheet_Addition_Command = (
                        "QToolButton, QLabel, RibbonToolButton {background-color: "
                        + StyleMapping_Ribbon.ReturnStyleItem("Background_Color_Hover")
                        + ";border: 0.5px solid"
                        + BorderColor
                        + ";border-right: 0.5px solid"
                        + StyleMapping_Ribbon.ReturnStyleItem("Background_Color_Hover")
                        + ";border-top-left-radius: 2px;border-bottom-left-radius: 2px;"
                        + "border-top-right-radius: 0px;border-bottom-right-radius: 0px"
                        + ";margin: 0px"
                        + ";spacing: 0px"
                        + ";}"
                    )
                StyleSheet_Addition_Button = (
                    "QToolButton, QLabel, RibbonToolButton {background-color: "
                    + StyleMapping_Ribbon.ReturnStyleItem("Background_Color")
                    + ";border: "
                    + BorderColor
                    + ";margin: 0px"
                    + ";spacing: 0px"
                    + ";}"
                )
                btn.setStyleSheet(StyleSheet_Addition_Button)
                if CommandButton.underMouse():
                    Label_Text.setStyleSheet(StyleSheet_Addition_Label)
                    CommandButton.setStyleSheet(StyleSheet_Addition_Command)
                if Label_Text.underMouse():
                    Label_Text.setStyleSheet(StyleSheet_Addition_Label)
                    CommandButton.setStyleSheet(StyleSheet_Addition_Command)

            Label_Text.enterEvent = lambda enterEvent: enterEventCustom(enterEvent)
            CommandButton.enterEvent = lambda enterEvent: enterEventCustom(
                enterEvent
            )
                
            # restore the stylesheets on leaving
            def leaveEventCustom(event):
                StyleSheet = StyleMapping_Ribbon.ReturnStyleSheet(
                    control="toolbutton",
                    radius="2px",
                )
                StyleSheet_Addition = (
                    "QToolButton, QToolButton:hover, QLabel, QLabel:hover, RibbonToolButton, RibbonToolButton:hover {background-color: "
                    + StyleMapping_Ribbon.ReturnStyleItem("Background_Color")
                    + ";border: 0.5px solid"
                    + StyleMapping_Ribbon.ReturnStyleItem("Background_Color")
                    + ";}"
                )
                Label_Text.setStyleSheet(StyleSheet + StyleSheet_Addition)
                CommandButton.setStyleSheet(StyleSheet + StyleSheet_Addition)

            Label_Text.leaveEvent = lambda leaveEvent: leaveEventCustom(leaveEvent)
            CommandButton.leaveEvent = lambda leaveEvent: leaveEventCustom(leaveEvent)

            # Copy the tooltip from the commandbutton to the label
            Label_Text.setToolTip(CommandButton.toolTip())

            # Set the menubutton space to zero because there is no menu
            MenuButtonSpace = 0

        btn.mouseMoveEvent = lambda mouseEvent: CustomControls.mouseMoveEvent(
            btn, mouseEvent
        )
        
        # Hide the text if set in preferences
        if showText is False:
            Label_Text.setHidden(True)
            TextWidth = 0

        # Set spacing to zero (highlight background will have gaps otherwise)
        Layout.setSpacing(0)

        # Add the layout
        btn.setLayout(Layout)
        # Set the stylesheet for the controls
        StyleSheet = StyleMapping_Ribbon.ReturnStyleSheet(control="toolbutton")
        CommandButton.setStyleSheet(StyleSheet)
        ArrowButton.setStyleSheet(StyleSheet)
        Label_Text.setStyleSheet(StyleSheet)
        btn.setStyleSheet(StyleSheet)

        # Set the correct dimensions
        btn.setFixedWidth(CommandButton.width() + MenuButtonSpace + TextWidth)
        btn.setFixedHeight(ButtonSize.height())
        CommandButton.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        Label_Text.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        ArrowButton.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        # return the new button
        btn.setObjectName("CustomWidget")
        return btn

    def CustomOptionMenu(Menu=None, actionList=None, parent=None):
        # If menu is none, define a new one
        if Menu is None:
            Menu = QMenu()
        # add all the actions from the action list
        for i in range(len(actionList)):
            action = actionList[i]
            if isinstance(action, QAction):
                Menu.addAction(action)
            if isinstance(action, list):
                # if it is a submenu, it is a list with two items
                # The first, is the default action with text
                # The second is the action with all the subactions, but without text or icon

                # Get the first action
                action_0 = action[0]
                # Get the second action
                action_1 = action[1]
                # Set the text and icon for the second action with those from the first action
                action_1.setText(action_0.text())
                action_1.setIcon(action_0.icon())
                # Add the second action
                Menu.addAction(action_1)

        # Set the stylesheet
        BackGroundColor = StyleMapping_Ribbon.ReturnStyleItem("Background_Color")
        BorderColor = StyleMapping_Ribbon.ReturnStyleItem("Border_Color")
        if Parameters_Ribbon.CUSTOM_COLORS_ENABLED:
            BorderColor = Parameters_Ribbon.COLOR_BORDERS
        if Parameters_Ribbon.BORDER_TRANSPARANT:
            BorderColor = StyleMapping_Ribbon.ReturnStyleItem(
                "Background_Color_Hover"
            )
        Menu.setStyleSheet("background-color: " + BackGroundColor + ";border: " + BorderColor + ";")

        # Define an custom enter event, to set "MenuEntered" to True on the ribbon and unfold the ribbon
        def enterEventCustom(event):
            if parent is not None:
                # Set the value in the parent for detecting that the menu is entered.
                # Needed for keeping the ribbon open while showing a dropdown menu
                parent.MenuEntered = True
                parent.UnfoldRibbon()

        Menu.enterEvent = lambda enterEvent: enterEventCustom(enterEvent)

        # Set MenuEntered to True. This keeps the ribbon visible
        def on_OptionButton_clicked():
            parent.MenuEntered = True

        Menu.aboutToShow.connect(on_OptionButton_clicked)

        # Set MenuEntered to False. This allows the ribbon to fold after leaving the menu and the ribbon.
        def SetToFoldRibbon():
            if parent is not None:
                # If the menu is hidden, set the value in the parent for detecting that the menu is entered to False.
                parent.MenuEntered = False
                pos = QCursor.pos()
                if parent.geometry().contains(pos) is False:
                    parent.FoldRibbon()

        Menu.aboutToHide.connect(SetToFoldRibbon)
        return Menu

    def EmptyButton():
        btn = QToolButton()
        btn.mouseMoveEvent = lambda mouseEvent: CustomControls.mouseMoveEvent(
            btn, mouseEvent
        )
        return btn

