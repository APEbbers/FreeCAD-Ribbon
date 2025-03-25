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

from PySide.QtGui import (
    QIcon,
    QAction,
    QFontMetrics,
    QFont,
    QFontDatabase,
    QTextOption,
    QCursor,
    QPalette,
    QEnterEvent,
    QDrag,
    QPixmap,
)
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
    QWidget,
)
from PySide.QtCore import Qt, QSize, QRect, QMargins, QEvent, QObject, QMimeData

import os
import sys
import Parameters_Ribbon
import Standard_Functions_RIbbon as StandardFunctions
import StyleMapping_Ribbon

# from CustomWidgets import myMenu as QMenu

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


class CustomControls(QToolButton):
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
        btn = QToolButton()
        CommandButton = QToolButton()
        ArrowButton = QToolButton()
        Layout = QVBoxLayout()
        Label_Text = QTextEdit()

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
        # Set the buttonSize
        CommandButton.setFixedSize(ButtonSize)
        CommandButtonHeight = ButtonSize.height()
        # Set the icon and its size
        CommandButton.setIcon(Icon)
        CommandButton.setIconSize(IconSize.expandedTo(CommandButton.size()))
        # Set the content margins to zero
        CommandButton.setContentsMargins(0, 0, 0, 0)
        # Add a actions if there is only one
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

        # if showText is False:
        if MenuButtonSpace < 10:
            MenuButtonSpace = 10

        # If text must not be show, set the text to an empty string
        # Still create a label to set up the button properly
        if showText is True and Text != "":
            # Create a label with the correct properties
            # Label_Text = QTextEdit()
            Label_Text.setReadOnly(True)
            Label_Text.setFrameShape(QFrame.Shape.NoFrame)
            Label_Text.setFrameShadow(QFrame.Shadow.Plain)
            Label_Text.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)
            Label_Text.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
            Label_Text.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
            Label_Text.document().setDocumentMargin(0)
            Label_Text.viewport().setCursor(Qt.CursorShape.ArrowCursor)
            Label_Text.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            # Set the font
            Font = QFont()
            Font.setPixelSize(FontSize)
            Label_Text.setFont(Font)
            # change the menubutton space because text is included in the click area
            MenuButtonSpace = 10
            # Determine the height of a single row
            SingleHeight = QFontMetrics(Font).boundingRect(Text).height() + 3
            Label_Text.setMinimumHeight(SingleHeight * 1)
            Label_Text.setMaximumHeight(SingleHeight * MaxNumberOfLines)
            # Set the width of the label based on the size of the button
            Label_Text.setFixedWidth(ButtonSize.width())

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
                Label_Text.setWordWrapMode(QTextOption.WrapMode.NoWrap)
                Label_Text.setText(Text)
                # Set the maximum number of lines to 1
                MaxNumberOfLines = 1
                # Set the proper alignment
                Label_Text.setAlignment(TextAlignment)
                # Lower the height when there is a menu
                if Menu is not None and len(Menu.actions()) > 1:
                    Label_Text.setFixedHeight(SingleHeight)
                else:
                    Label_Text.setFixedHeight(SingleHeight + Space)

            # If wordwrap is enabled, set the text and height accordingly
            if setWordWrap is True:
                # Set the wrap mode
                Label_Text.setWordWrapMode(QTextOption.WrapMode.WordWrap)
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
                maxLength = maxLength + 3

                # Get the first text line
                line1 = StandardFunctions.ReturnWrappedText(Text, maxLength, MaxNumberOfLines, True)[0]
                # Set the alignment
                Label_Text.setAlignment(TextAlignment)
                # Add the line
                Label_Text.append(line1)
                # get the text width
                TextWidth = FontMetrics.horizontalAdvance(line1, -1)
                # Set the correct height. Avoid a too big difference in icon sizes by only decreasing the height when there is a menu.
                if Menu is not None and len(Menu.actions()) > 1:
                    Label_Text.setFixedHeight(SingleHeight)
                else:
                    Label_Text.setFixedHeight((SingleHeight * MaxNumberOfLines) - Space)
                # Try to get the second line if there is one
                try:
                    line2 = StandardFunctions.ReturnWrappedText(Text, maxLength, MaxNumberOfLines, True)[1]
                    # Set the alignment
                    Label_Text.setAlignment(TextAlignment)
                    # Add the line
                    Label_Text.append(line2)
                    # Set the correct height
                    Label_Text.setFixedHeight((SingleHeight * MaxNumberOfLines) - Space)
                    # Update the text width if neccesary
                    if FontMetrics.horizontalAdvance(line2, -1) > TextWidth:
                        TextWidth = TextWidth = FontMetrics.horizontalAdvance(line2, -1)
                except Exception:
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

            # Add the label to the area where the user can invoke the menu
            if showText is True:
                # Create custom events
                #
                # Peform a menu click when clicked on the label
                def mouseClickevent(event):
                    ArrowButton.animateClick()

                Label_Text.mousePressEvent = lambda mouseClick: mouseClickevent(mouseClick)
                ArrowButton.mousePressEvent = lambda mouseClick: mouseClickevent(mouseClick)

                # Change the background color for commandbutton and label on hovering (CSS)
                def enterEventCustom(event):
                    BorderColor = StyleMapping_Ribbon.ReturnStyleItem("Border_Color")
                    if Parameters_Ribbon.CUSTOM_COLORS_ENABLED:
                        BorderColor = Parameters_Ribbon.COLOR_BORDERS
                    if Parameters_Ribbon.BORDER_TRANSPARANT:
                        BorderColor = StyleMapping_Ribbon.ReturnStyleItem("Background_Color_Hover")
                    StyleSheet_Addition_Arrow = (
                        "QToolButton, QTextEdit {background-color: "
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
                        + """QToolButton::menu-indicator {
                                subcontrol-origin: padding;
                                subcontrol-position: center top;
                            }"""
                    )
                    StyleSheet_Addition_Label = (
                        "QToolButton, QTextEdit {background-color: "
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
                        "QToolButton, QTextEdit {background-color: "
                        + StyleMapping_Ribbon.ReturnStyleItem("Background_Color")
                        + ";border: none"
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

            if showText is False:
                # Change the background color for commandbutton and label on hovering (CSS)
                def enterEventCustom_2(event):
                    BorderColor = StyleMapping_Ribbon.ReturnStyleItem("Border_Color")
                    if Parameters_Ribbon.CUSTOM_COLORS_ENABLED:
                        BorderColor = Parameters_Ribbon.COLOR_BORDERS
                    if Parameters_Ribbon.BORDER_TRANSPARANT:
                        BorderColor = StyleMapping_Ribbon.ReturnStyleItem("Background_Color_Hover")
                    StyleSheet_Addition_Arrow = (
                        "QToolButton, QTextEdit {background-color: "
                        + StyleMapping_Ribbon.ReturnStyleItem("Background_Color_Hover")
                        + ";border: 0.5px solid"
                        + BorderColor
                        + ";border-radius: 2px"
                        + ";margin: 0px"
                        + ";spacing: 0px"
                        + ";}"
                        + """QToolButton::menu-indicator {
                                subcontrol-origin: padding;
                                subcontrol-position: center top;
                            }"""
                    )
                    StyleSheet_Addition_Button = (
                        "QToolButton, QTextEdit {background-color: "
                        + StyleMapping_Ribbon.ReturnStyleItem("Background_Color")
                        + ";border: none"
                        + ";}"
                    )
                    btn.setStyleSheet(StyleSheet_Addition_Button)
                    if ArrowButton.underMouse():
                        ArrowButton.setStyleSheet(StyleSheet_Addition_Arrow)
                    if Label_Text.underMouse():
                        ArrowButton.setStyleSheet(StyleSheet_Addition_Arrow)

                    if parent is not None:
                        # Set the value in the parent for detecting that the menu is entered to True.
                        # Needed for keeping the ribbon open while showing a dropdown menu
                        parent.MenuEntered = True

                Label_Text.enterEvent = lambda enterEvent: enterEventCustom_2(enterEvent)
                ArrowButton.enterEvent = lambda enterEvent: enterEventCustom_2(enterEvent)

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
            if showText is True:
                # Create custom events
                #
                # Peform a menu click when clicked on the label
                def mouseClickevent(event):
                    CommandButton.animateClick()

                Label_Text.mousePressEvent = lambda mouseClick: mouseClickevent(mouseClick)

                # Change the background color for commandbutton and label on hovering (CSS)
                def enterEventCustom(event):
                    BorderColor = StyleMapping_Ribbon.ReturnStyleItem("Border_Color")
                    if Parameters_Ribbon.CUSTOM_COLORS_ENABLED:
                        BorderColor = Parameters_Ribbon.COLOR_BORDERS
                    if Parameters_Ribbon.BORDER_TRANSPARANT:
                        BorderColor = StyleMapping_Ribbon.ReturnStyleItem("Background_Color_Hover")
                    StyleSheet_Addition_Label = (
                        "QToolButton, QTextEdit {background-color: "
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
                        "QToolButton, QTextEdit {background-color: "
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
                        "QToolButton, QTextEdit {background-color: "
                        + StyleMapping_Ribbon.ReturnStyleItem("Background_Color")
                        + ";border: none"
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
                CommandButton.enterEvent = lambda enterEvent: enterEventCustom(enterEvent)

            if showText is False:
                # Change the background color for commandbutton and label on hovering (CSS)
                def enterEventCustom_2(event):
                    BorderColor = StyleMapping_Ribbon.ReturnStyleItem("Border_Color")
                    if Parameters_Ribbon.CUSTOM_COLORS_ENABLED:
                        BorderColor = Parameters_Ribbon.COLOR_BORDERS
                    if Parameters_Ribbon.BORDER_TRANSPARANT:
                        BorderColor = StyleMapping_Ribbon.ReturnStyleItem("Background_Color_Hover")
                    StyleSheet_Addition_Command = (
                        "QToolButton, QTextEdit {background-color: "
                        + StyleMapping_Ribbon.ReturnStyleItem("Background_Color_Hover")
                        + ";border: 0.5px solid"
                        + BorderColor
                        + ";border-radius: 2px"
                        + ";margin: 0px"
                        + ";spacing: 0px"
                        + ";}"
                    )
                    StyleSheet_Addition_Button = (
                        "QToolButton, QTextEdit {background-color: "
                        + StyleMapping_Ribbon.ReturnStyleItem("Background_Color")
                        + ";border: none"
                        + ";}"
                    )
                    btn.setStyleSheet(StyleSheet_Addition_Button)
                    if CommandButton.underMouse():
                        CommandButton.setStyleSheet(StyleSheet_Addition_Command)
                    if Label_Text.underMouse():
                        CommandButton.setStyleSheet(StyleSheet_Addition_Command)

                Label_Text.enterEvent = lambda enterEvent: enterEventCustom_2(enterEvent)
                CommandButton.enterEvent = lambda enterEvent: enterEventCustom_2(enterEvent)

            # restore the stylesheets on leaving
            def leaveEventCustom(event):
                StyleSheet = StyleMapping_Ribbon.ReturnStyleSheet(
                    control="toolbutton",
                    radius="2px",
                )
                StyleSheet_Addition = (
                    "QToolButton, QToolButton:hover, QTextEdit, QTextEdit:hover {background-color: "
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

        btn.mouseMoveEvent = lambda mouseEvent: CustomControls.mouseMoveEvent(btn, mouseEvent)

        # Set the spacing to zero. If not, the CSS styling will show gaps
        Layout.setSpacing(0)
        # Add the layout to the button
        btn.setLayout(Layout)

        # Set the stylesheet
        StyleSheet = StyleMapping_Ribbon.ReturnStyleSheet(control="toolbutton", radius="2px")
        StyleSheet_Addition_Label = (
            "QToolButton, QTextEdit {background-color: "
            + StyleMapping_Ribbon.ReturnStyleItem("Background_Color")
            + ";border: 0.5px solid"
            + StyleMapping_Ribbon.ReturnStyleItem("Background_Color")
            + ";border-top: 0px solid"
            + StyleMapping_Ribbon.ReturnStyleItem("Background_Color")
            + ";border-radius: 2px"
            + ";margin: 0px"
            + ";spacing: 0px"
            + ";}"
        )
        StyleSheet_Addition_Command = (
            "QToolButton, QTextEdit {background-color: "
            + StyleMapping_Ribbon.ReturnStyleItem("Background_Color")
            + ";border: 0.5px solid"
            + StyleMapping_Ribbon.ReturnStyleItem("Background_Color")
            + ";border-bottom: 0px solid"
            + StyleMapping_Ribbon.ReturnStyleItem("Background_Color")
            + ";border-radius: 2px"
            + ";margin: 0px"
            + ";spacing: 0px"
            + ";}"
        )
        StyleSheet_Addition_Button = (
            "QToolButton, QTextEdit {background-color: "
            + StyleMapping_Ribbon.ReturnStyleItem("Background_Color")
            + ";border: none"
            + ";}"
        )
        StyleSheet_Addition_Arrow = (
            "QToolButton, QTextEdit {background-color: "
            + StyleMapping_Ribbon.ReturnStyleItem("Background_Color")
            + ";border: 0.5px solid"
            + StyleMapping_Ribbon.ReturnStyleItem("Background_Color")
            + ";border-top: 0px solid"
            + StyleMapping_Ribbon.ReturnStyleItem("Background_Color")
            + ";border-radius: 2px"
            + ";margin: 0px"
            + ";spacing: 0px"
            + ";}"
            + """QToolButton::menu-indicator {
                    subcontrol-origin: padding;
                    subcontrol-position: center top;
                }"""
        )
        CommandButton.setStyleSheet(StyleSheet_Addition_Command + StyleSheet)
        ArrowButton.setStyleSheet(StyleSheet_Addition_Arrow + StyleSheet)
        Label_Text.setStyleSheet(StyleSheet_Addition_Label + StyleSheet)
        btn.setStyleSheet(StyleSheet_Addition_Button + StyleSheet)

        # Set the final sizes
        width = ButtonSize.width()
        if TextWidth > 0 and TextWidth < CommandButtonHeight + Space:
            width = CommandButtonHeight + Space
        if TextWidth > 0 and TextWidth > CommandButtonHeight + Space:
            width = TextWidth + Space
        Label_Text.setFixedWidth(width)
        ArrowButton.setFixedWidth(width)
        CommandButton.setFixedSize(QSize(width, CommandButtonHeight))
        btn.setFixedSize(QSize(width, ButtonSize.height()))

        # Return the button
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
        btn = QToolButton()
        CommandButton = QToolButton()
        ArrowButton = QToolButton()
        Layout = QHBoxLayout()
        Label_Text = QTextEdit()
        # Set the default stylesheet
        StyleSheet_Addition_Button = (
            "QToolButton, QToolButton:hover {background-color: "
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
        CommandButton.setFixedSize(ButtonSize)
        # Set the icon and its size
        CommandButton.setIcon(Icon)
        CommandButton.setIconSize(IconSize)
        # Set the content margins to zero
        CommandButton.setContentsMargins(0, 0, 0, 0)
        # Add a actions if there is only one
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

        # if showText is False:
        if MenuButtonSpace < 12:
            MenuButtonSpace = 12

        # If text must be shown wrapped, add a layout with label
        if showText is True and Text != "":
            # Create a label
            # Label_Text = QTextEdit()
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
            Label_Text.setFixedHeight(CommandButton.height())
            # Set the font
            Font = QFont()
            Font.setPixelSize(FontSize)
            Label_Text.setFont(Font)
            FontMetrics = QFontMetrics(Font)
            if setWordWrap is True:
                Label_Text.setWordWrapMode(QTextOption.WrapMode.WordWrap)
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
                line1 = StandardFunctions.ReturnWrappedText(Text, maxLength, MaxNumberOfLines, True)[0]
                # Add the line with a space to avoid te need to set spacing. (Spacing breaks the hover background)
                Label_Text.append(" " + line1)
                # Try to get the second line if there is one
                try:
                    line2 = StandardFunctions.ReturnWrappedText(Text, maxLength, MaxNumberOfLines, True)[1]
                    # Add the line with a space to avoid te need to set spacing. (Spacing breaks the hover background)
                    Label_Text.append(" " + line2)
                    if FontMetrics.tightBoundingRect(line1).width() > FontMetrics.tightBoundingRect(line2).width():
                        # Update a parameter for the width
                        TextWidth = FontMetrics.tightBoundingRect(line1).width()
                    else:
                        # Update a parameter for the width
                        TextWidth = FontMetrics.tightBoundingRect(line2).width()
                except Exception:
                    # Correct the margin to set the arrow vertical center (bug in Qt)
                    marginCorrection = (CommandButton.height() - FontMetrics.boundingRect(Text).height()) / 2
                    Label_Text.setViewportMargins(0, marginCorrection, 0, 0)
                    # Update a parameter for the width
                    TextWidth = FontMetrics.tightBoundingRect(line1).width()

                # Adjust the size
                Label_Text.setMaximumWidth(TextWidth + space)
                # Update a parameter for the width
                TextWidth = TextWidth + space

                # If the text is higher than the commandbutton, switch to no wrap
                if (FontMetrics.boundingRect(line1).height() * MaxNumberOfLines) > ButtonSize.height():
                    setWordWrap = False
                    # reset the values
                    TextWidth = 0
                    Label_Text.setMaximumWidth(2000)  # set to a extra large value to avoid clipping
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
                Label_Text.setWordWrapMode(QTextOption.WrapMode.NoWrap)
                # Add the line with a space to avoid te need to set spacing. (Spacing breaks the hover background)
                Label_Text.setText(" " + Text)
                # Update the size
                Label_Text.adjustSize()
                Label_Text.setFixedHeight(CommandButton.height())
                # Correct the margin to set the arrow vertical center (bug in Qt)
                marginCorrection = (CommandButton.height() - FontMetrics.boundingRect(Text).height()) / 2
                Label_Text.setViewportMargins(0, marginCorrection, 0, 0)
                # Update the width parameter
                TextWidth = FontMetrics.boundingRect(Text).width() + space
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
            ArrowButton.setFixedHeight(CommandButton.height())
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
            if showText is True:
                # Create custom events
                #
                # Peform a menu click when clicked on the label
                def mouseClickevent(event):
                    ArrowButton.animateClick()

                Label_Text.mousePressEvent = lambda mouseClick: mouseClickevent(mouseClick)
                ArrowButton.mousePressEvent = lambda mouseClick: mouseClickevent(mouseClick)

                # Change the background color for commandbutton and label on hovering (CSS)
                def enterEventCustom(event):
                    BorderColor = StyleMapping_Ribbon.ReturnStyleItem("Border_Color")
                    if Parameters_Ribbon.CUSTOM_COLORS_ENABLED:
                        BorderColor = Parameters_Ribbon.COLOR_BORDERS
                    if Parameters_Ribbon.BORDER_TRANSPARANT:
                        BorderColor = StyleMapping_Ribbon.ReturnStyleItem("Background_Color_Hover")
                    StyleSheet_Addition_Label = (
                        "QToolButton, QTextEdit { "
                        + "background-color: "
                        + StyleMapping_Ribbon.ReturnStyleItem("Background_Color_Hover")
                        + ";border: 0.5px solid"
                        + BorderColor
                        + ";border-right: 0px solid"
                        + StyleMapping_Ribbon.ReturnStyleItem("Background_Color_Hover")
                        + ";border-top-left-radius: 2px;border-bottom-left-radius: 2px;"
                        + "border-top-right-radius: 0px;border-bottom-right-radius: 0px"
                        + ";margin: 0px"
                        + ";spacing: 0px"
                        + ";}"
                    )
                    StyleSheet_Addition_Arrow = (
                        "QToolButton, QTextEdit { "
                        + "background-color: "
                        + StyleMapping_Ribbon.ReturnStyleItem("Background_Color_Hover")
                        + ";border: 0.5px solid"
                        + BorderColor
                        + ";border-left: 0px solid"
                        + StyleMapping_Ribbon.ReturnStyleItem("Background_Color_Hover")
                        + ";border-top-left-radius: 0px;border-bottom-left-radius: 0px;"
                        + "border-top-right-radius: 2px;border-bottom-right-radius: 2px"
                        + ";margin: 0px"
                        + ";spacing: 0px"
                        + ";}"
                    )
                    StyleSheet_Addition_Button = (
                        "QToolButton:hover {background-color: "
                        + StyleMapping_Ribbon.ReturnStyleItem("Background_Color")
                        + ";border: none"
                        + ";}"
                    )
                    btn.setStyleSheet(StyleSheet_Addition_Button)
                    if ArrowButton.underMouse():
                        ArrowButton.setStyleSheet(StyleSheet_Addition_Arrow)
                        Label_Text.setStyleSheet(StyleSheet_Addition_Label)
                    if Label_Text.underMouse():
                        ArrowButton.setStyleSheet(StyleSheet_Addition_Arrow)
                        Label_Text.setStyleSheet(StyleSheet_Addition_Label)

                    if parent is not None:
                        # Set the value in the parent for detecting that the menu is entered.
                        # Needed for keeping the ribbon open while showing a dropdown menu
                        parent.MenuEntered = True

                Label_Text.enterEvent = lambda enterEvent: enterEventCustom(enterEvent)
                ArrowButton.enterEvent = lambda enterEvent: enterEventCustom(enterEvent)

            if showText is False:
                # Change the background color for commandbutton and label on hovering (CSS)
                def enterEventCustom_2(event):
                    BorderColor = StyleMapping_Ribbon.ReturnStyleItem("Border_Color")
                    if Parameters_Ribbon.CUSTOM_COLORS_ENABLED:
                        BorderColor = Parameters_Ribbon.COLOR_BORDERS
                    if Parameters_Ribbon.BORDER_TRANSPARANT:
                        BorderColor = StyleMapping_Ribbon.ReturnStyleItem("Background_Color_Hover")
                    StyleSheet_Addition_Arrow = (
                        "QToolButton, QTextEdit { "
                        + "background-color: "
                        + StyleMapping_Ribbon.ReturnStyleItem("Background_Color_Hover")
                        + ";border: 0.5px solid"
                        + BorderColor
                        + ";border-radius: 2px"
                        + ";margin: 0px"
                        + ";spacing: 0px"
                        + ";}"
                    )
                    StyleSheet_Addition_Button = (
                        "QToolButton:hover {background-color: "
                        + StyleMapping_Ribbon.ReturnStyleItem("Background_Color")
                        + ";border: none"
                        + ";}"
                    )
                    btn.setStyleSheet(StyleSheet_Addition_Button)
                    if ArrowButton.underMouse():
                        ArrowButton.setStyleSheet(StyleSheet_Addition_Arrow)
                    if Label_Text.underMouse():
                        ArrowButton.setStyleSheet(StyleSheet_Addition_Arrow)

                    if parent is not None:
                        # Set the value in the parent for detecting that the menu is entered.
                        # Needed for keeping the ribbon open while showing a dropdown menu
                        parent.MenuEntered = True

                Label_Text.enterEvent = lambda enterEvent: enterEventCustom_2(enterEvent)
                ArrowButton.enterEvent = lambda enterEvent: enterEventCustom_2(enterEvent)

            # restore the stylesheets on leaving
            def leaveEventCustom(event):
                StyleSheet = StyleMapping_Ribbon.ReturnStyleSheet(
                    control="toolbutton",
                    radius="2px",
                )
                StyleSheet_Addition = (
                    "QToolButton, QToolButton:hover, QTextEdit, QTextEdit:hover {background-color: "
                    + StyleMapping_Ribbon.ReturnStyleItem("Background_Color")
                    + ";border: none"
                    + ";}"
                )
                Label_Text.setStyleSheet(StyleSheet + StyleSheet_Addition)
                ArrowButton.setStyleSheet(StyleSheet + StyleSheet_Addition)

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
            # Add the label to the area where the user can invoke the menu
            if showText is True:
                # Create custom events
                #
                # Peform a menu click when clicked on the label
                def mouseClickevent(event):
                    CommandButton.animateClick()

                Label_Text.mousePressEvent = lambda mouseClick: mouseClickevent(mouseClick)
                ArrowButton.mousePressEvent = lambda mouseClick: mouseClickevent(mouseClick)

                # Change the background color for commandbutton and label on hovering (CSS)
                def enterEventCustom(event):
                    BorderColor = StyleMapping_Ribbon.ReturnStyleItem("Border_Color")
                    if Parameters_Ribbon.CUSTOM_COLORS_ENABLED:
                        BorderColor = Parameters_Ribbon.COLOR_BORDERS
                    if Parameters_Ribbon.BORDER_TRANSPARANT:
                        BorderColor = StyleMapping_Ribbon.ReturnStyleItem("Background_Color_Hover")
                    StyleSheet_Addition_Label = (
                        "QToolButton, QTextEdit { "
                        + "background-color: "
                        + StyleMapping_Ribbon.ReturnStyleItem("Background_Color_Hover")
                        + ";border: 0.5px solid"
                        + BorderColor
                        + ";border-left: 0px solid"
                        + StyleMapping_Ribbon.ReturnStyleItem("Background_Color_Hover")
                        + ";border-top-left-radius: 0px;border-bottom-left-radius: 0px;"
                        + "border-top-right-radius: 2px;border-bottom-right-radius: 2px"
                        + ";margin: 0px"
                        + ";spacing: 0px"
                        + ";}"
                    )
                    StyleSheet_Addition_Command = (
                        "QToolButton, QTextEdit { "
                        + "background-color: "
                        + StyleMapping_Ribbon.ReturnStyleItem("Background_Color_Hover")
                        + ";border: 0.5px solid"
                        + BorderColor
                        + ";border-right: 0px solid"
                        + StyleMapping_Ribbon.ReturnStyleItem("Background_Color_Hover")
                        + ";border-top-left-radius: 2px;border-bottom-left-radius: 2px;"
                        + "border-top-right-radius: 0px;border-bottom-right-radius: 0px"
                        + ";margin: 0px"
                        + ";spacing: 0px"
                        + ";}"
                    )
                    StyleSheet_Addition_Button = (
                        "QToolButton, QToolButton:hover {background-color: "
                        + StyleMapping_Ribbon.ReturnStyleItem("Background_Color")
                        + ";border: none"
                        + ";}"
                    )
                    btn.setStyleSheet(StyleSheet_Addition_Button)
                    if CommandButton.underMouse():
                        CommandButton.setStyleSheet(StyleSheet_Addition_Command)
                        Label_Text.setStyleSheet(StyleSheet_Addition_Label)
                    if Label_Text.underMouse():
                        CommandButton.setStyleSheet(StyleSheet_Addition_Command)
                        Label_Text.setStyleSheet(StyleSheet_Addition_Label)

                Label_Text.enterEvent = lambda enterEvent: enterEventCustom(enterEvent)
                CommandButton.enterEvent = lambda enterEvent: enterEventCustom(enterEvent)

            if showText is False:
                # Change the background color for commandbutton and label on hovering (CSS)
                def enterEventCustom_2(event):
                    BorderColor = StyleMapping_Ribbon.ReturnStyleItem("Border_Color")
                    if Parameters_Ribbon.CUSTOM_COLORS_ENABLED:
                        BorderColor = Parameters_Ribbon.COLOR_BORDERS
                    if Parameters_Ribbon.BORDER_TRANSPARANT:
                        BorderColor = StyleMapping_Ribbon.ReturnStyleItem("Background_Color_Hover")
                    StyleSheet_Addition_Command = (
                        "QToolButton, QTextEdit { "
                        + "background-color: "
                        + StyleMapping_Ribbon.ReturnStyleItem("Background_Color_Hover")
                        + ";border: 0.5px solid"
                        + BorderColor
                        + ";border-radius: 2px"
                        + ";margin: 0px"
                        + ";spacing: 0px"
                        + ";}"
                    )
                    StyleSheet_Addition_Button = (
                        "QToolButton, QToolButton:hover {background-color: "
                        + StyleMapping_Ribbon.ReturnStyleItem("Background_Color")
                        + ";border: none"
                        + ";}"
                    )
                    btn.setStyleSheet(StyleSheet_Addition_Button)
                    if CommandButton.underMouse():
                        CommandButton.setStyleSheet(StyleSheet_Addition_Command)
                    if Label_Text.underMouse():
                        CommandButton.setStyleSheet(StyleSheet_Addition_Command)

                Label_Text.enterEvent = lambda enterEvent: enterEventCustom_2(enterEvent)
                CommandButton.enterEvent = lambda enterEvent: enterEventCustom_2(enterEvent)

            # restore the stylesheets on leaving
            def leaveEventCustom(event):
                StyleSheet = StyleMapping_Ribbon.ReturnStyleSheet(
                    control="toolbutton",
                    radius="2px",
                )
                StyleSheet_Addition = (
                    "QToolButton, QToolButton:hover, QTextEdit, QTextEdit:hover {background-color: "
                    + StyleMapping_Ribbon.ReturnStyleItem("Background_Color")
                    + ";border: none"
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

        btn.mouseMoveEvent = lambda mouseEvent: CustomControls.mouseMoveEvent(btn, mouseEvent)

        # Set the minimum height for the button
        CommandButton.setMinimumHeight(ButtonSize.height())
        # Set spacing to zero (highlight background will have gaps otherwise)
        Layout.setSpacing(0)

        # Add the layout
        btn.setLayout(Layout)
        # Set the stylesheet for the controls
        StyleSheet = StyleMapping_Ribbon.ReturnStyleSheet(control="toolbutton")
        StyleSheet_Addition_Label = (
            "QToolButton, QTextEdit { "
            + "background-color: "
            + StyleMapping_Ribbon.ReturnStyleItem("Background_Color")
            + ";border: 0.5px solid"
            + StyleMapping_Ribbon.ReturnStyleItem("Background_Color")
            + ";border-left: 0px solid"
            + StyleMapping_Ribbon.ReturnStyleItem("Background_Color")
            + ";border-radius: 2px"
            + ";margin: 0px"
            + ";spacing: 0px"
            + ";}"
        )
        StyleSheet_Addition_Command = (
            "QToolButton, QTextEdit { "
            + "background-color: "
            + StyleMapping_Ribbon.ReturnStyleItem("Background_Color")
            + ";border: 0.5px solid"
            + StyleMapping_Ribbon.ReturnStyleItem("Background_Color")
            + ";border-right: 0px solid"
            + StyleMapping_Ribbon.ReturnStyleItem("Background_Color")
            + ";border-radius: 2px"
            + ";margin: 0px"
            + ";spacing: 0px"
            + ";}"
        )
        StyleSheet_Addition_Arrow = (
            "QToolButton, QTextEdit { "
            + "background-color: "
            + StyleMapping_Ribbon.ReturnStyleItem("Background_Color")
            + ";border: 0.5px solid"
            + StyleMapping_Ribbon.ReturnStyleItem("Background_Color")
            + ";border-left: 0px solid"
            + StyleMapping_Ribbon.ReturnStyleItem("Background_Color")
            + ";border-radius: 2px"
            + ";margin: 0px"
            + ";spacing: 0px"
            + ";}"
        )
        StyleSheet_Addition_button = (
            "QToolButton, QToolButton:hover, QTextEdit, QTextEdit:hover {background-color: "
            + StyleMapping_Ribbon.ReturnStyleItem("Background_Color")
            + ";border: 0px solid"
            + StyleMapping_Ribbon.ReturnStyleItem("Background_Color")
            + ";}"
        )
        CommandButton.setStyleSheet(StyleSheet_Addition_Command + StyleSheet)
        ArrowButton.setStyleSheet(StyleSheet_Addition_Arrow + StyleSheet)
        Label_Text.setStyleSheet(StyleSheet_Addition_Label + StyleSheet)
        btn.setStyleSheet(StyleSheet_Addition_button + StyleSheet)

        # Set the correct dimensions
        btn.setFixedWidth(CommandButton.width() + MenuButtonSpace + TextWidth)
        btn.setFixedHeight(CommandButton.height())

        # return the new button
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
        hexColor = StyleMapping_Ribbon.ReturnStyleItem("Background_Color")
        Menu.setStyleSheet("background-color: " + hexColor)

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
        btn.mouseMoveEvent = lambda mouseEvent: CustomControls.mouseMoveEvent(btn, mouseEvent)


class DragTargetIndicator(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setContentsMargins(3, 3, 3, 3)
        self.setStyleSheet(
            StyleMapping_Ribbon.ReturnStyleSheet(
                control="dragindicator", HoverColor=Parameters_Ribbon.COLOR_BACKGROUND_HOVER
            )
        )
