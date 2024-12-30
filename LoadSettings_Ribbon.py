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
import os

from PySide.QtCore import Qt, SIGNAL, QSize
from PySide.QtWidgets import (
    QTabWidget,
    QSlider,
    QSpinBox,
    QCheckBox,
    QComboBox,
    QLabel,
    QTabWidget,
    QSizePolicy,
    QPushButton,
    QLineEdit.
)
from PySide.QtGui import QIcon, QPixmap, QColor

import sys
import StyleMapping
import Standard_Functions_RIbbon as StandardFunctions
import Parameters_Ribbon
from Parameters_Ribbon import DefaultSettings

# Get the resources
pathIcons = Parameters_Ribbon.ICON_LOCATION
pathStylSheets = Parameters_Ribbon.STYLESHEET_LOCATION
pathUI = Parameters_Ribbon.UI_LOCATION
pathBackup = Parameters_Ribbon.BACKUP_LOCATION
sys.path.append(pathIcons)
sys.path.append(pathStylSheets)
sys.path.append(pathUI)
sys.path.append(pathBackup)

# import graphical created Ui. (With QtDesigner or QtCreator)
import Settings_ui as Settings_ui

# Define the translation
translate = App.Qt.translate


class LoadDialog(Settings_ui.Ui_Settings):
    # Store the current values before change
    OriginalValues = {
        "BackupEnabled": Parameters_Ribbon.ENABLE_BACKUP,
        "BackupFolder": Parameters_Ribbon.BACKUP_LOCATION,
        "TabBar_Style": Parameters_Ribbon.TABBAR_STYLE,
        "IconSize_Small": Parameters_Ribbon.ICON_SIZE_SMALL,
        "IconSize_Medium": Parameters_Ribbon.ICON_SIZE_MEDIUM,
        "IconSize_Large": Parameters_Ribbon.ICON_SIZE_LARGE,
        "ApplicationButtonSize": Parameters_Ribbon.APP_ICON_SIZE,
        "QuickAccessButtonSize": Parameters_Ribbon.QUICK_ICON_SIZE,
        "RightToolbarButtonSize": Parameters_Ribbon.RIGHT_ICON_SIZE,
        "TabBarSize": Parameters_Ribbon.TABBAR_SIZE,
        "Stylesheet": Parameters_Ribbon.STYLESHEET,
        "ShowIconText_Small": Parameters_Ribbon.SHOW_ICON_TEXT_SMALL,
        "ShowIconText_Medium": Parameters_Ribbon.SHOW_ICON_TEXT_MEDIUM,
        "ShowIconText_Large": Parameters_Ribbon.SHOW_ICON_TEXT_LARGE,
        "MaxColumnsPerPanel": Parameters_Ribbon.MAX_COLUMN_PANELS,
        "DebugMode": Parameters_Ribbon.DEBUG_MODE,
        "ShowOnHover": Parameters_Ribbon.SHOW_ON_HOVER,
        "TabBar_Scroll": Parameters_Ribbon.TABBAR_SCROLLSPEED,
        "Ribbon_Scroll": Parameters_Ribbon.RIBBON_SCROLLSPEED,
        "TabBar_Click": Parameters_Ribbon.TABBAR_CLICKSPEED,
        "Ribbon_Click": Parameters_Ribbon.RIBBON_CLICKSPEED,
        "Preferred_view": Parameters_Ribbon.PREFERRED_VIEW,
        "UseToolsPanel": Parameters_Ribbon.USE_TOOLSPANEL,
        "WrapText_Large": Parameters_Ribbon.WRAPTEXT_LARGE,
        "WrapText_Medium": Parameters_Ribbon.WRAPTEXT_LARGE,
        "UseFCOverlay": Parameters_Ribbon.USE_FC_OVERLAY,
        "UseButtonBackGround": Parameters_Ribbon.BUTTON_BACKGROUND_ENABLED,
        "CustomIcons": Parameters_Ribbon.CUSTOM_ICONS_ENABLED,
        "CustomColors": Parameters_Ribbon.CUSTOM_COLORS_ENABLED,
        "BorderTransparant": Parameters_Ribbon.BORDER_TRANSPARANT,
        "Color_Borders": Parameters_Ribbon.COLOR_BORDERS,
        # "Color_Background": Parameters_Ribbon.COLOR_BACKGROUND,
        "Color_Background_Hover": Parameters_Ribbon.COLOR_BACKGROUND_HOVER,
        "Color_Background_App": Parameters_Ribbon.COLOR_APPLICATION_BUTTON_BACKGROUND,
        "Shortcut_Application": Parameters_Ribbon.SHORTCUT_APPLICATION,
    }

    # Store the current values before change
    ValuesToUpdate = {
        "BackupEnabled": Parameters_Ribbon.ENABLE_BACKUP,
        "BackupFolder": Parameters_Ribbon.BACKUP_LOCATION,
        "TabBar_Style": Parameters_Ribbon.TABBAR_STYLE,
        "IconSize_Small": Parameters_Ribbon.ICON_SIZE_SMALL,
        "IconSize_Medium": Parameters_Ribbon.ICON_SIZE_MEDIUM,
        "IconSize_Large": Parameters_Ribbon.ICON_SIZE_LARGE,
        "ApplicationButtonSize": Parameters_Ribbon.APP_ICON_SIZE,
        "QuickAccessButtonSize": Parameters_Ribbon.QUICK_ICON_SIZE,
        "RightToolbarButtonSize": Parameters_Ribbon.RIGHT_ICON_SIZE,
        "TabBarSize": Parameters_Ribbon.TABBAR_SIZE,
        "Stylesheet": Parameters_Ribbon.STYLESHEET,
        "ShowIconText_Small": Parameters_Ribbon.SHOW_ICON_TEXT_SMALL,
        "ShowIconText_Medium": Parameters_Ribbon.SHOW_ICON_TEXT_MEDIUM,
        "ShowIconText_Large": Parameters_Ribbon.SHOW_ICON_TEXT_LARGE,
        "MaxColumnsPerPanel": Parameters_Ribbon.MAX_COLUMN_PANELS,
        "DebugMode": Parameters_Ribbon.DEBUG_MODE,
        "ShowOnHover": Parameters_Ribbon.SHOW_ON_HOVER,
        "TabBar_Scroll": Parameters_Ribbon.TABBAR_SCROLLSPEED,
        "Ribbon_Scroll": Parameters_Ribbon.RIBBON_SCROLLSPEED,
        "TabBar_Click": Parameters_Ribbon.TABBAR_CLICKSPEED,
        "Ribbon_Click": Parameters_Ribbon.RIBBON_CLICKSPEED,
        "Preferred_view": Parameters_Ribbon.PREFERRED_VIEW,
        "UseToolsPanel": Parameters_Ribbon.USE_TOOLSPANEL,
        "WrapText_Medium": Parameters_Ribbon.WRAPTEXT_LARGE,
        "WrapText_Large": Parameters_Ribbon.WRAPTEXT_LARGE,
        "UseFCOverlay": Parameters_Ribbon.USE_FC_OVERLAY,
        "UseButtonBackGround": Parameters_Ribbon.BUTTON_BACKGROUND_ENABLED,
        "CustomIcons": Parameters_Ribbon.CUSTOM_ICONS_ENABLED,
        "CustomColors": Parameters_Ribbon.CUSTOM_COLORS_ENABLED,
        "BorderTransparant": Parameters_Ribbon.BORDER_TRANSPARANT,
        "Color_Borders": Parameters_Ribbon.COLOR_BORDERS,
        # "Color_Background": Parameters_Ribbon.COLOR_BACKGROUND,
        "Color_Background_Hover": Parameters_Ribbon.COLOR_BACKGROUND_HOVER,
        "Color_Background_App": Parameters_Ribbon.COLOR_APPLICATION_BUTTON_BACKGROUND,
        "Shortcut_Application": Parameters_Ribbon.SHORTCUT_APPLICATION,
    }

    settingChanged = False

    def __init__(self):
        # Makes "self.on_CreateBOM_clicked" listen to the changed control values instead initial values
        super(LoadDialog, self).__init__()

        # # this will create a Qt widget from our ui file
        self.form = Gui.PySideUic.loadUi(os.path.join(pathUI, "Settings.ui"))

        # Make sure that the dialog stays on top
        self.form.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)

        # Get the style from the main window and use it for this form
        mw = Gui.getMainWindow()
        palette = mw.palette()
        self.form.setPalette(palette)
        Style = mw.style()
        self.form.setStyle(Style)

        # Set the size of the window to the previous state
        #
        # Get the previous values
        LayoutDialog_Height = Parameters_Ribbon.Settings.GetIntSetting("SettingsDialog_Height")
        if LayoutDialog_Height == 0 or LayoutDialog_Height is None:
            LayoutDialog_Height = 730
        LayoutDialog_Width = Parameters_Ribbon.Settings.GetIntSetting("SettingsDialog_Width")
        if LayoutDialog_Width == 0 or LayoutDialog_Height is None:
            LayoutDialog_Width = 800
        # set a fixed size to force the form in to shape
        self.form.setFixedSize(LayoutDialog_Width, LayoutDialog_Height)
        # Set the size policy to fixed
        self.form.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        # Set a minimum and maximum size
        self.form.setMinimumSize(600, 600)
        self.form.setMaximumSize(120000, 120000)
        # change the sizepolicy to preferred, to allow stretching
        self.form.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)

        # Disable custom Colors and Icons for the time being
        # self.form.tabWidget.removeTab(2)

        # Remove tabbar click settings for the time being
        self.form.label_15.setHidden(True)
        self.form.label_15.setDisabled(True)
        self.form.ScrollClicks_TabBar.setHidden(True)
        self.form.ScrollClicks_TabBar.setDisabled(True)

        # load all settings
        #
        # General
        self.form.EnableBackup.setChecked(Parameters_Ribbon.ENABLE_BACKUP)
        self.form.label_4.setText(Parameters_Ribbon.BACKUP_LOCATION)
        self.form.TabbarStyle.setCurrentIndex(Parameters_Ribbon.TABBAR_STYLE)
        self.form.IconSize_Small.setValue(Parameters_Ribbon.ICON_SIZE_SMALL)
        self.form.IconSize_Medium.setValue(Parameters_Ribbon.ICON_SIZE_MEDIUM)
        self.form.IconSize_Large.setValue(Parameters_Ribbon.ICON_SIZE_LARGE)
        self.form.IconSize_ApplicationButton.setValue(Parameters_Ribbon.APP_ICON_SIZE)
        self.form.IconSize_QuickAccessButton.setValue(Parameters_Ribbon.QUICK_ICON_SIZE)
        self.form.IconSize_rightToolbarButton.setValue(Parameters_Ribbon.RIGHT_ICON_SIZE)
        self.form.TabbarHeight.setValue(Parameters_Ribbon.TABBAR_SIZE)
        self.form.label_7.setText(Parameters_Ribbon.STYLESHEET)
        if Parameters_Ribbon.SHOW_ICON_TEXT_SMALL is True:
            self.form.ShowText_Small.setCheckState(Qt.CheckState.Checked)
        else:
            self.form.ShowText_Small.setCheckState(Qt.CheckState.Unchecked)

        if Parameters_Ribbon.SHOW_ICON_TEXT_MEDIUM is True:
            self.form.ShowText_Medium.setCheckState(Qt.CheckState.Checked)
        else:
            self.form.ShowText_Medium.setCheckState(Qt.CheckState.Unchecked)

        if Parameters_Ribbon.SHOW_ICON_TEXT_LARGE is True:
            self.form.ShowText_Large.setCheckState(Qt.CheckState.Checked)
        else:
            self.form.ShowText_Large.setCheckState(Qt.CheckState.Unchecked)

        if Parameters_Ribbon.WRAPTEXT_MEDIUM is True:
            self.form.EnableWrap_Medium.setCheckState(Qt.CheckState.Checked)
        else:
            self.form.EnableWrap_Medium.setCheckState(Qt.CheckState.Unchecked)

        if Parameters_Ribbon.WRAPTEXT_LARGE is True:
            self.form.EnableWrap_Large.setCheckState(Qt.CheckState.Checked)
        else:
            self.form.EnableWrap_Large.setCheckState(Qt.CheckState.Unchecked)

        self.form.MaxPanelColumn.setValue(Parameters_Ribbon.MAX_COLUMN_PANELS)
        if Parameters_Ribbon.DEBUG_MODE is True:
            self.form.DebugMode.setCheckState(Qt.CheckState.Checked)
        else:
            self.form.DebugMode.setCheckState(Qt.CheckState.Unchecked)

        # Navigation settings
        if Parameters_Ribbon.SHOW_ON_HOVER is True:
            self.form.EnableEnterEvent.setCheckState(Qt.CheckState.Checked)
        else:
            self.form.EnableEnterEvent.setCheckState(Qt.CheckState.Unchecked)
        # it is FreeCAD 1.0 disable this option.
        if int(App.Version()[0]) > 0:
            self.form.EnableEnterEvent.setDisabled(True)
            self.form.EnableEnterEvent.setHidden(True)

        self.form.ScrollSpeed_TabBar.setValue(Parameters_Ribbon.TABBAR_SCROLLSPEED)
        self.form.ScrollSpeed_Ribbon.setValue(Parameters_Ribbon.RIBBON_SCROLLSPEED)
        self.form.ScrollClicks_TabBar.setValue(Parameters_Ribbon.TABBAR_CLICKSPEED)
        self.form.ScrollClicks_Ribbon.setValue(Parameters_Ribbon.RIBBON_CLICKSPEED)
        self.form.ModifierKeyApp.setCurrentText(Parameters_Ribbon.SHORTCUT_APPLICATION.split("+")[0])
        self.form.ModifierKeyApp.setItemData(
            self.form.ModifierKeyApp.currentIndex(),
            Parameters_Ribbon.SHORTCUT_APPLICATION.split("+")[0],
            Qt.ItemDataRole.UserRole,
        )
        self.form.AppShortCut.setText(Parameters_Ribbon.SHORTCUT_APPLICATION.split("+")[1])
        self.form.ShortcutTaken_1.setHidden(True)

        # Miscellaneous
        self.form.PreferedViewPanel.setCurrentIndex(Parameters_Ribbon.PREFERRED_VIEW)
        if Parameters_Ribbon.USE_TOOLSPANEL is True:
            self.form.EnableToolsPanel.setCheckState(Qt.CheckState.Checked)
        else:
            self.form.EnableToolsPanel.setCheckState(Qt.CheckState.Unchecked)

        if Parameters_Ribbon.USE_FC_OVERLAY is True:
            self.form.FCOverlayEnabled.setCheckState(Qt.CheckState.Checked)
        else:
            self.form.FCOverlayEnabled.setCheckState(Qt.CheckState.Unchecked)

        if Parameters_Ribbon.BUTTON_BACKGROUND_ENABLED is True:
            self.form.UseButtonBackGround.setCheckState(Qt.CheckState.Checked)
        else:
            self.form.UseButtonBackGround.setCheckState(Qt.CheckState.Unchecked)

        # Set the color and icon buttons
        if Parameters_Ribbon.CUSTOM_ICONS_ENABLED is True:
            self.form.CustomIcons.setCheckState(Qt.CheckState.Checked)
        else:
            self.form.CustomIcons.setCheckState(Qt.CheckState.Unchecked)

        self.form.Tab_Scroll_Left.setIcon(StyleMapping.ReturnStyleItem("ScrollLeftButton_Tab", True))
        self.form.Tab_Scroll_Left.setIconSize(
            QSize(self.form.Tab_Scroll_Left.width() - 6, self.form.Tab_Scroll_Left.height() - 6)
        )

        self.form.Tab_Scroll_Right.setIcon(StyleMapping.ReturnStyleItem("ScrollRightButton_Tab", True))
        self.form.Tab_Scroll_Right.setIconSize(
            QSize(self.form.Tab_Scroll_Right.width() - 6, self.form.Tab_Scroll_Right.height() - 6)
        )

        self.form.Ribbon_Scroll_Left.setIcon(StyleMapping.ReturnStyleItem("ScrollLeftButton_Category", True))
        self.form.Ribbon_Scroll_Left.setIconSize(
            QSize(self.form.Ribbon_Scroll_Left.width() - 6, self.form.Ribbon_Scroll_Left.height() - 6)
        )

        self.form.Ribbon_Scroll_Right.setIcon(StyleMapping.ReturnStyleItem("ScrollRightButton_Category", True))
        self.form.Ribbon_Scroll_Right.setIconSize(
            QSize(self.form.Ribbon_Scroll_Right.width() - 6, self.form.Ribbon_Scroll_Right.height() - 6)
        )

        self.form.MoreCommands.setIcon(StyleMapping.ReturnStyleItem("OptionButton", True))
        self.form.MoreCommands.setIconSize(
            QSize(self.form.MoreCommands.width() - 6, self.form.MoreCommands.height() - 6)
        )

        self.form.pinButton_open.setIcon(StyleMapping.ReturnStyleItem("PinButton_open", True))
        self.form.pinButton_open.setIconSize(
            QSize(self.form.pinButton_open.width() - 6, self.form.pinButton_open.height() - 6)
        )

        self.form.pinButton_closed.setIcon(StyleMapping.ReturnStyleItem("PinButton_closed", True))
        self.form.pinButton_closed.setIconSize(
            QSize(self.form.pinButton_closed.width() - 6, self.form.pinButton_closed.height() - 6)
        )

        if Parameters_Ribbon.CUSTOM_COLORS_ENABLED is True:
            self.form.CustomColors.setCheckState(Qt.CheckState.Checked)
        else:
            self.form.CustomColors.setCheckState(Qt.CheckState.Unchecked)

        if Parameters_Ribbon.BORDER_TRANSPARANT is True:
            self.form.BorderTransparant.setCheckState(Qt.CheckState.Checked)
        else:
            self.form.BorderTransparant.setCheckState(Qt.CheckState.Unchecked)

        self.form.Color_Borders.setProperty("color", QColor(Parameters_Ribbon.COLOR_BORDERS))
        # self.form.Color_Background.setProperty("color", QColor(Parameters_Ribbon.COLOR_BACKGROUND))
        self.form.Color_Background_Hover.setProperty("color", QColor(Parameters_Ribbon.COLOR_BACKGROUND_HOVER))
        self.form.Color_Background_App.setProperty(
            "color", QColor(Parameters_Ribbon.COLOR_APPLICATION_BUTTON_BACKGROUND)
        )

        # region - connect controls with functions----------------------------------------------------
        #
        # Connect Backup
        self.form.EnableBackup.clicked.connect(self.on_EnableBackup_clicked)
        self.form.BackUpLocation.clicked.connect(self.on_BackUpLocation_clicked)
        # Connect the tabbar style
        self.form.TabbarStyle.currentIndexChanged.connect(self.on_TabbarStyle_currentIndexChanged)
        # Connect icon sizes
        self.form.IconSize_Small.textChanged.connect(self.on_IconSize_Small_TextChanged)
        self.form.IconSize_Medium.textChanged.connect(self.on_IconSize_Medium_TextChanged)
        self.form.IconSize_Large.textChanged.connect(self.on_IconSize_Large_TextChanged)
        self.form.IconSize_ApplicationButton.textChanged.connect(self.on_IconSize_ApplicationButton_TextChanged)
        self.form.IconSize_QuickAccessButton.textChanged.connect(self.on_IconSize_QuickAccessButton_TextChanged)
        self.form.IconSize_rightToolbarButton.textChanged.connect(self.on_IconSize_rightToolbarButton_TextChanged)
        self.form.TabbarHeight.textChanged.connect(self.on_TabbarHeight_TextChanged)
        # Connect stylesheet
        self.form.StyleSheetLocation.clicked.connect(self.on_StyleSheetLocation_clicked)
        # Connect icon texts
        self.form.ShowText_Small.clicked.connect(self.on_ShowTextSmall_clicked)
        self.form.ShowText_Medium.clicked.connect(self.on_ShowTextMedium_clicked)
        self.form.ShowText_Large.clicked.connect(self.on_ShowTextLarge_clicked)
        self.form.EnableWrap_Medium.clicked.connect(self.on_EnableWrap_Medium_clicked)
        self.form.EnableWrap_Large.clicked.connect(self.on_EnableWrap_Large_clicked)
        # Connect column width
        self.form.MaxPanelColumn.textChanged.connect(self.on_MaxPanelColumn_TextChanged)
        # Connect debug mode
        self.form.DebugMode.clicked.connect(self.on_DebugMode_clicked)

        # Connect the cancel button
        def Cancel():
            self.on_Cancel_clicked(self)

        self.form.Cancel.connect(self.form.Cancel, SIGNAL("clicked()"), Cancel)

        # Connect the button GenerateJsonExit with the function on_GenerateJsonExit_clicked
        def GenerateJsonExit():
            self.on_Close_clicked(self)

        self.form.GenerateJsonExit.connect(self.form.GenerateJsonExit, SIGNAL("clicked()"), GenerateJsonExit)

        # Connect the reset button
        def Reset():
            self.on_Reset_clicked(self)

        self.form.Reset.connect(self.form.Reset, SIGNAL("clicked()"), Reset)

        # Connect the behavior settings
        self.form.EnableEnterEvent.clicked.connect(self.on_EnableEnterEvent_clicked)
        self.form.ScrollSpeed_TabBar.valueChanged.connect(self.on_ScrollSpeed_TabBar_valueCHanged)
        self.form.ScrollSpeed_Ribbon.valueChanged.connect(self.on_ScrollSpeed_Ribbon_valueCHanged)
        self.form.ScrollClicks_TabBar.textChanged.connect(self.on_ScrollClicks_TabBar_valueCHanged)
        self.form.ScrollClicks_Ribbon.textChanged.connect(self.on_ScrollClicks_Ribbon_valueCHanged)
        self.form.ApplyShortcutApp.clicked.connect(
            self.form.ApplyShortcutApp, SIGNAL("clicked()"), self.on_ApplyShortcutApp_clicked
        )
        QLineEdit(self.form.AppShortCut).textChanged.connect(self.on_AppShortCut_textChanged)
        # Connect the preferred panel settings
        self.form.PreferedViewPanel.currentIndexChanged.connect(self.on_PreferedViewPanel_currentIndexChanged)
        # Connect the EnableTools checkbox:
        self.form.EnableToolsPanel.clicked.connect(self.on_EnableToolsPanel_clicked)
        # Connect the overlay setting:
        self.form.FCOverlayEnabled.clicked.connect(self.on_FCOverlayEnabled_clicked)
        self.form.UseButtonBackGround.clicked.connect(self.on_UseButtonBackGround_clicked)
        # endregion

        # Set the minimum and maximum settings for the iconsizes
        self.form.IconSize_Small.setMinimum(5)
        self.form.IconSize_Medium.setMinimum(5)
        self.form.IconSize_Large.setMinimum(5)
        self.form.IconSize_ApplicationButton.setMinimum(5)
        self.form.IconSize_QuickAccessButton.setMinimum(5)
        self.form.IconSize_rightToolbarButton.setMinimum(5)
        self.form.TabbarHeight.setMinimum(5)

        # Connect the controls for custom icons and colors
        self.form.CustomIcons.clicked.connect(self.on_CustomIcons_clicked)

        #
        def TabScrollLeft():
            self.on_Tab_Scroll_Left_clicked()

        self.form.Tab_Scroll_Left.connect(self.form.Tab_Scroll_Left, SIGNAL("clicked()"), TabScrollLeft)

        #
        def TabScrollRight():
            self.on_Tab_Scroll_Right_clicked()

        self.form.Tab_Scroll_Right.connect(self.form.Tab_Scroll_Right, SIGNAL("clicked()"), TabScrollRight)

        #
        def CategoryScrollLeft():
            self.on_Ribbon_Scroll_Left_clicked()

        self.form.Ribbon_Scroll_Left.connect(self.form.Ribbon_Scroll_Left, SIGNAL("clicked()"), CategoryScrollLeft)

        #
        def CategoryScrollRight():
            self.on_Ribbon_Scroll_Right_clicked()

        self.form.Ribbon_Scroll_Right.connect(self.form.Ribbon_Scroll_Right, SIGNAL("clicked()"), CategoryScrollRight)

        #
        def MoreCommands():
            self.on_MoreCommands_clicked()

        self.form.MoreCommands.connect(self.form.MoreCommands, SIGNAL("clicked()"), MoreCommands)

        #
        def PinButtonOpen():
            self.on_pinButton_open_clicked()

        self.form.pinButton_open.connect(self.form.pinButton_open, SIGNAL("clicked()"), PinButtonOpen)

        #
        def PinButtonClosed():
            self.on_pinButton_closed_clicked()

        self.form.pinButton_closed.connect(self.form.pinButton_closed, SIGNAL("clicked()"), PinButtonClosed)
        self.form.CustomColors.clicked.connect(self.on_CustomColors_clicked)
        self.form.BorderTransparant.clicked.connect(self.on_BorderTransparant_clicked)
        self.form.Color_Borders.clicked.connect(self.on_Color_Borders_clicked)
        # self.form.Color_Background.clicked.connect(self.on_Color_Background_clicked)
        self.form.Color_Background_Hover.clicked.connect(self.on_Color_Background_Hover_clicked)
        self.form.Color_Background_App.clicked.connect(self.on_Color_Background_App_clicked)

        # Set the first tab active
        self.form.tabWidget.setCurrentIndex(0)

        return

    # region - Control functions----------------------------------------------------------------------

    def on_EnableBackup_clicked(self):
        if self.form.EnableBackup.isChecked() is True:
            self.ValuesToUpdate["BackupEnabled"] = True
            self.Backup = True
        if self.form.EnableBackup.isChecked() is False:
            self.ValuesToUpdate["BackupEnabled"] = False
            self.Backup = False

        self.settingChanged = True
        return

    def on_BackUpLocation_clicked(self):
        BackupFolder = ""
        BackupFolder = StandardFunctions.GetFolder(parent=None, DefaultPath=Parameters_Ribbon.BACKUP_LOCATION)
        if BackupFolder != "":
            self.pathBackup = BackupFolder
            self.form.label_4.setText(BackupFolder)
            self.ValuesToUpdate["BackupFolder"] = BackupFolder
            self.settingChanged = True
        return

    def on_TabbarStyle_currentIndexChanged(self):
        self.ValuesToUpdate["TabBar_Style"] = self.form.TabbarStyle.currentIndex()
        self.settingChanged = True
        return

    def on_IconSize_Small_TextChanged(self):
        self.ValuesToUpdate["IconSize_Small"] = int(self.form.IconSize_Small.text())
        self.settingChanged = True
        return

    def on_IconSize_Medium_TextChanged(self):
        self.ValuesToUpdate["IconSize_Medium"] = int(self.form.IconSize_Medium.text())
        self.settingChanged = True
        return

    def on_IconSize_Large_TextChanged(self):
        self.ValuesToUpdate["IconSize_Large"] = int(self.form.IconSize_Large.text())
        self.settingChanged = True
        return

    def on_IconSize_ApplicationButton_TextChanged(self):
        self.ValuesToUpdate["ApplicationButtonSize"] = int(self.form.IconSize_ApplicationButton.text())
        self.settingChanged = True
        return

    def on_IconSize_QuickAccessButton_TextChanged(self):
        self.ValuesToUpdate["QuickAccessButtonSize"] = int(self.form.IconSize_QuickAccessButton.text())
        self.settingChanged = True
        return

    def on_IconSize_rightToolbarButton_TextChanged(self):
        self.ValuesToUpdate["RightToolbarButtonSize"] = int(self.form.IconSize_rightToolbarButton.text())
        self.settingChanged = True
        return

    def on_TabbarHeight_TextChanged(self):
        self.ValuesToUpdate["TabBarSize"] = int(self.form.TabbarHeight.text())
        self.settingChanged = True
        return

    def on_MaxPanelColumn_TextChanged(self):
        self.ValuesToUpdate["MaxColumnsPerPanel"] = int(self.form.MaxPanelColumn.text())
        self.settingChanged = True

    def on_StyleSheetLocation_clicked(self):
        StyleSheet = ""
        StyleSheet = StandardFunctions.GetFileDialog(
            Filter="Stylesheet (*.qss)",
            parent=None,
            DefaultPath=os.path.dirname(Parameters_Ribbon.STYLESHEET),
            SaveAs=False,
        )
        if StyleSheet != "":
            self.form.label_7.setText(StyleSheet)
            self.ValuesToUpdate["Stylesheet"] = StyleSheet
            self.settingChanged = True
        return

    def on_ShowTextSmall_clicked(self):
        if self.form.ShowText_Small.isChecked() is True:
            self.ValuesToUpdate["ShowIconText_Small"] = True
        if self.form.ShowText_Small.isChecked() is False:
            self.ValuesToUpdate["ShowIconText_Small"] = False
        self.settingChanged = True
        return

    def on_ShowTextMedium_clicked(self):
        if self.form.ShowText_Medium.isChecked() is True:
            self.ValuesToUpdate["ShowIconText_Medium"] = True
        if self.form.ShowText_Medium.isChecked() is False:
            self.ValuesToUpdate["ShowIconText_Medium"] = False
        self.settingChanged = True
        return

    def on_ShowTextLarge_clicked(self):
        if self.form.ShowText_Large.isChecked() is True:
            self.ValuesToUpdate["ShowIconText_Large"] = True
        if self.form.ShowText_Large.isChecked() is False:
            self.ValuesToUpdate["ShowIconText_Large"] = False
        self.settingChanged = True
        return

    def on_EnableWrap_Medium_clicked(self):
        if self.form.EnableWrap_Medium.isChecked() is True:
            self.ValuesToUpdate["WrapText_Medium"] = True
        if self.form.EnableWrap_Medium.isChecked() is False:
            self.ValuesToUpdate["WrapText_Medium"] = False
        self.settingChanged = True
        return

    def on_EnableWrap_Large_clicked(self):
        if self.form.EnableWrap_Large.isChecked() is True:
            self.ValuesToUpdate["WrapText_Large"] = True
        if self.form.EnableWrap_Large.isChecked() is False:
            self.ValuesToUpdate["WrapText_Large"] = False
        self.settingChanged = True
        return

    def on_DebugMode_clicked(self):
        if self.form.DebugMode.isChecked() is True:
            self.ValuesToUpdate["DebugMode"] = True
        if self.form.DebugMode.isChecked() is False:
            self.ValuesToUpdate["DebugMode"] = False
        self.settingChanged = True
        return

    def on_EnableEnterEvent_clicked(self):
        if self.form.EnableEnterEvent.isChecked() is True:
            self.ValuesToUpdate["ShowOnHover"] = True
        if self.form.EnableEnterEvent.isChecked() is False:
            self.ValuesToUpdate["ShowOnHover"] = False
        self.settingChanged = True

    def on_ScrollSpeed_TabBar_valueCHanged(self):
        self.ValuesToUpdate["TabBar_Scroll"] = self.form.ScrollSpeed_TabBar.value()
        self.settingChanged = True

    def on_ScrollSpeed_Ribbon_valueCHanged(self):
        self.ValuesToUpdate["Ribbon_Scroll"] = self.form.ScrollSpeed_Ribbon.value()
        self.settingChanged = True

    def on_ScrollClicks_TabBar_valueCHanged(self):
        self.ValuesToUpdate["TabBar_Click"] = self.form.ScrollClicks_TabBar.value()
        self.settingChanged = True

    def on_ScrollClicks_Ribbon_valueCHanged(self):
        self.ValuesToUpdate["Ribbon_Click"] = self.form.ScrollClicks_Ribbon.value()
        self.settingChanged = True

    def on_PreferedViewPanel_currentIndexChanged(self):
        self.ValuesToUpdate["Preferred_view"] = self.form.PreferedViewPanel.currentIndex()
        self.settingChanged = True
        return

    def on_EnableToolsPanel_clicked(self):
        if self.form.EnableToolsPanel.isChecked() is True:
            self.ValuesToUpdate["UseToolsPanel"] = True
        if self.form.EnableToolsPanel.isChecked() is False:
            self.ValuesToUpdate["UseToolsPanel"] = False
        self.settingChanged = True
        return

    def on_FCOverlayEnabled_clicked(self):
        if self.form.FCOverlayEnabled.isChecked() is True:
            self.ValuesToUpdate["UseFCOverlay"] = True
        if self.form.FCOverlayEnabled.isChecked() is False:
            self.ValuesToUpdate["UseFCOverlay"] = False
        self.settingChanged = True
        return

    def on_UseButtonBackGround_clicked(self):
        if self.form.UseButtonBackGround.isChecked() is True:
            self.ValuesToUpdate["UseButtonBackGround"] = True
        if self.form.UseButtonBackGround.isChecked() is False:
            self.ValuesToUpdate["UseButtonBackGround"] = False
        self.settingChanged = True
        return

    def on_CustomIcons_clicked(self):
        if self.form.CustomIcons.isChecked() is True:
            self.ValuesToUpdate["CustomIcons"] = True
        if self.form.CustomIcons.isChecked() is False:
            self.ValuesToUpdate["CustomIcons"] = False
        self.settingChanged = True
        return

    # region - Color and icon buttons
    def on_Tab_Scroll_Left_clicked(self):
        # Define th edefault path
        DefaultPath = os.path.dirname(Parameters_Ribbon.SCROLL_LEFT_BUTTON_TAB)
        if DefaultSettings != "":
            DefaultPath = Parameters_Ribbon.ICON_LOCATION
        # Get the file with a dialog
        File = StandardFunctions.GetFileDialog(
            Filter="Pictures (*.png *.svg)",
            parent=None,
            DefaultPath=DefaultPath,
            SaveAs=False,
        )
        # if File is not nothing, set the icon in settings and on the button
        if File is not None and File != "" and os.path.isfile(File):
            Parameters_Ribbon.Settings.SetStringSetting("ScrollLeftButton_Tab", File)
            self.form.Tab_Scroll_Left.setIcon(QIcon(QPixmap(File)))
            self.form.Tab_Scroll_Left.setIconSize(
                QSize(self.form.Tab_Scroll_Left.width() - 6, self.form.Tab_Scroll_Left.height() - 6)
            )
            self.settingChanged = True
        return

    def on_Tab_Scroll_Right_clicked(self):
        # Define th edefault path
        DefaultPath = os.path.dirname(Parameters_Ribbon.SCROLL_RIGHT_BUTTON_TAB)
        if DefaultSettings != "":
            DefaultPath = Parameters_Ribbon.ICON_LOCATION
        # Get the file with a dialog
        File = StandardFunctions.GetFileDialog(
            Filter="Pictures (*.png *.svg)",
            parent=None,
            DefaultPath=DefaultPath,
            SaveAs=False,
        )
        # if File is not nothing, set the icon in settings and on the button
        if File is not None and File != "" and os.path.isfile(File):
            Parameters_Ribbon.Settings.SetStringSetting("ScrollRightButton_Tab", File)
            self.form.Tab_Scroll_Right.setIcon(QIcon(QPixmap(File)))
            self.form.Tab_Scroll_Right.setIconSize(
                QSize(self.form.Tab_Scroll_Right.width() - 6, self.form.Tab_Scroll_Right.height() - 6)
            )
            self.settingChanged = True
        return

    def on_Ribbon_Scroll_Left_clicked(self):
        # Define th edefault path
        DefaultPath = os.path.dirname(Parameters_Ribbon.SCROLL_LEFT_BUTTON_CATEGORY)
        if DefaultSettings != "":
            DefaultPath = Parameters_Ribbon.ICON_LOCATION
        # Get the file with a dialog
        File = StandardFunctions.GetFileDialog(
            Filter="Pictures (*.png *.svg)",
            parent=None,
            DefaultPath=DefaultPath,
            SaveAs=False,
        )
        # if File is not nothing, set the icon in settings and on the button
        if File is not None and File != "" and os.path.isfile(File):
            Parameters_Ribbon.Settings.SetStringSetting("ScrollLeftButton_Category", File)
            self.form.Ribbon_Scroll_Left.setIcon(QIcon(QPixmap(File)))
            self.form.Ribbon_Scroll_Left.setIconSize(
                QSize(self.form.Ribbon_Scroll_Left.width() - 6, self.form.Ribbon_Scroll_Left.height() - 6)
            )
            self.settingChanged = True
        return

    def on_Ribbon_Scroll_Right_clicked(self):
        # Define th edefault path
        DefaultPath = os.path.dirname(Parameters_Ribbon.SCROLL_RIGHT_BUTTON_CATEGORY)
        if DefaultSettings != "":
            DefaultPath = Parameters_Ribbon.ICON_LOCATION
        # Get the file with a dialog
        File = StandardFunctions.GetFileDialog(
            Filter="Pictures (*.png *.svg)",
            parent=None,
            DefaultPath=DefaultPath,
            SaveAs=False,
        )
        # if File is not nothing, set the icon in settings and on the button
        if File is not None and File != "" and os.path.isfile(File):
            Parameters_Ribbon.Settings.SetStringSetting("ScrollRightButton_Category", File)
            self.form.Ribbon_Scroll_Right.setIcon(QIcon(QPixmap(File)))
            self.form.Ribbon_Scroll_Right.setIconSize(
                QSize(self.form.Ribbon_Scroll_Right.width() - 6, self.form.Ribbon_Scroll_Right.height() - 6)
            )
            self.settingChanged = True
        return

    def on_MoreCommands_clicked(self):
        # Define th edefault path
        DefaultPath = os.path.dirname(Parameters_Ribbon.OPTION_BUTTON)
        if DefaultSettings != "":
            DefaultPath = Parameters_Ribbon.ICON_LOCATION
        # Get the file with a dialog
        File = StandardFunctions.GetFileDialog(
            Filter="Pictures (*.png *.svg)",
            parent=None,
            DefaultPath=DefaultPath,
            SaveAs=False,
        )
        # if File is not nothing, set the icon in settings and on the button
        if File is not None and File != "" and os.path.isfile(File):
            Parameters_Ribbon.Settings.SetStringSetting("OptionButton", File)
            self.form.MoreCommands.setIcon(QIcon(QPixmap(File)))
            self.form.MoreCommands.setIconSize(
                QSize(self.form.MoreCommands.width() - 6, self.form.MoreCommands.height() - 6)
            )
            self.settingChanged = True
        return

    def on_pinButton_open_clicked(self):
        # Define th edefault path
        DefaultPath = os.path.dirname(Parameters_Ribbon.PIN_BUTTON_OPEN)
        if DefaultSettings != "":
            DefaultPath = Parameters_Ribbon.ICON_LOCATION
        # Get the file with a dialog
        File = StandardFunctions.GetFileDialog(
            Filter="Pictures (*.png *.svg)",
            parent=None,
            DefaultPath=DefaultPath,
            SaveAs=False,
        )
        # if File is not nothing, set the icon in settings and on the button
        if File is not None and File != "" and os.path.isfile(File):
            Parameters_Ribbon.Settings.SetStringSetting("PinButton_open", File)
            self.form.pinButton_open.setIcon(QIcon(QPixmap(File)))
            self.form.pinButton_open.setIconSize(
                QSize(self.form.pinButton_open.width() - 6, self.form.pinButton_open.height() - 6)
            )
            self.settingChanged = True
        return

    def on_pinButton_closed_clicked(self):
        # Define th edefault path
        DefaultPath = os.path.dirname(Parameters_Ribbon.PIN_BUTTON_CLOSED)
        if DefaultSettings != "":
            DefaultPath = Parameters_Ribbon.ICON_LOCATION
        # Get the file with a dialog
        File = StandardFunctions.GetFileDialog(
            Filter="Pictures (*.png *.svg)",
            parent=None,
            DefaultPath=DefaultPath,
            SaveAs=False,
        )
        # if File is not nothing, set the icon in settings and on the button
        if File is not None and File != "" and os.path.isfile(File):
            Parameters_Ribbon.Settings.SetStringSetting("PinButton_closed", File)
            self.form.pinButton_closed.setIcon(QIcon(QPixmap(File)))
            self.form.pinButton_closed.setIconSize(
                QSize(self.form.pinButton_closed.width() - 6, self.form.pinButton_closed.height() - 6)
            )
            self.settingChanged = True
        return

    def on_CustomColors_clicked(self):
        if self.form.CustomColors.isChecked() is True:
            self.ValuesToUpdate["CustomColors"] = True
        if self.form.CustomColors.isChecked() is False:
            self.ValuesToUpdate["CustomColors"] = False
        self.settingChanged = True
        return

    def on_Color_Borders_clicked(self):
        Color = QColor(self.form.Color_Borders.property("color")).toTuple()  # RGBA tupple
        HexColor = StandardFunctions.ColorConvertor(Color, Color[3] / 255, True, False)
        self.ValuesToUpdate["Color_Borders"] = HexColor
        self.settingChanged = True
        return

    def on_BorderTransparant_clicked(self):
        if self.form.BorderTransparant.isChecked() is True:
            self.ValuesToUpdate["BorderTransparant"] = True
        if self.form.BorderTransparant.isChecked() is False:
            self.ValuesToUpdate["BorderTransparant"] = False
        self.settingChanged = True

    # def on_Color_Background_clicked(self):
    #     Color = QColor(self.form.Color_Background.property("color")).toTuple()  # RGBA tupple
    #     HexColor = StandardFunctions.ColorConvertor(Color, Color[3] / 255, True, False)
    #     self.ValuesToUpdate["Color_Background"] = HexColor
    #     self.settingChanged = True
    #     return

    def on_Color_Background_Hover_clicked(self):
        Color = QColor(self.form.Color_Background_Hover.property("color")).toTuple()  # RGBA tupple
        HexColor = StandardFunctions.ColorConvertor(Color, Color[3] / 255, True, False)
        self.ValuesToUpdate["Color_Background_Hover"] = HexColor
        self.settingChanged = True
        return

    def on_Color_Background_App_clicked(self):
        Color = QColor(self.form.Color_Background_App.property("color")).toTuple()  # RGBA tupple
        HexColor = StandardFunctions.ColorConvertor(Color, Color[3] / 255, True, False)
        self.ValuesToUpdate["Color_Background_App"] = HexColor
        self.settingChanged = True
        return

    def on_ApplyShortcutApp_clicked(self):
        shortCut = f"{self.form.ModifierKeyApp.currentData(Qt.ItemDataRole.UserRole)}+{self.form.AppShortCut.text()}"
        if StandardFunctions.ShortCutTaken(shortCut) is True:
            self.form.ShortcutTaken_1.setVisible(True)
        else:
            self.form.ShortcutTaken_1.setHidden(True)
            self.ValuesToUpdate["Shortcut_Application"] = shortCut
        self.settingChanged = True
        return

    def on_AppShortCut_textChanged(self):
        test = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        if self.form.AppShortCut.text() not in test:
            self.form.AppShortCut.clear()

    # endregion

    @staticmethod
    def on_Cancel_clicked(self):
        # Save backup settings
        Parameters_Ribbon.Settings.SetBoolSetting("BackupEnabled", self.OriginalValues["BackupEnabled"])
        Parameters_Ribbon.Settings.SetStringSetting("BackupFolder", self.OriginalValues["BackupFolder"])
        # Save tabBar style
        Parameters_Ribbon.Settings.SetIntSetting("TabBar_Style", self.OriginalValues["TabBar_Style"])
        # Save icon sizes
        Parameters_Ribbon.Settings.SetIntSetting("IconSize_Small", int(self.OriginalValues["IconSize_Small"]))
        Parameters_Ribbon.Settings.SetIntSetting("IconSize_Medium", int(self.OriginalValues["IconSize_Medium"]))
        Parameters_Ribbon.Settings.SetIntSetting("IconSize_Large", int(self.OriginalValues["IconSize_Large"]))
        Parameters_Ribbon.Settings.SetStringSetting("Stylesheet", self.OriginalValues["Stylesheet"])
        Parameters_Ribbon.Settings.SetIntSetting(
            "ApplicationButtonSize", int(self.OriginalValues["ApplicationButtonSize"])
        )
        Parameters_Ribbon.Settings.SetIntSetting(
            "QuickAccessButtonSize", int(self.OriginalValues["QuickAccessButtonSize"])
        )
        Parameters_Ribbon.Settings.SetIntSetting("TabBarSize", int(self.OriginalValues["TabBarSize"]))
        Parameters_Ribbon.Settings.SetIntSetting(
            "RightToolbarButtonSize", int(self.OriginalValues["RightToolbarButtonSize"])
        )
        # Save text settings
        Parameters_Ribbon.Settings.SetBoolSetting("ShowIconText_Small", self.OriginalValues["ShowIconText_Small"])
        Parameters_Ribbon.Settings.SetBoolSetting("ShowIconText_Medium", self.OriginalValues["ShowIconText_Medium"])
        Parameters_Ribbon.Settings.SetBoolSetting("ShowIconText_Large", self.OriginalValues["ShowIconText_Large"])
        Parameters_Ribbon.Settings.SetBoolSetting("WrapText_Medium", self.OriginalValues["WrapText_Medium"])
        Parameters_Ribbon.Settings.SetBoolSetting("WrapText_Large", self.OriginalValues["WrapText_Large"])
        # Save No of columns
        Parameters_Ribbon.Settings.SetIntSetting("MaxColumnsPerPanel", int(self.OriginalValues["MaxColumnsPerPanel"]))
        Parameters_Ribbon.Settings.SetBoolSetting("DebugMode", self.OriginalValues["DebugMode"])
        Parameters_Ribbon.Settings.SetBoolSetting("ShowOnHover", self.OriginalValues["ShowOnHover"])
        # Save behavior settings
        Parameters_Ribbon.Settings.SetIntSetting("TabBar_Scroll", self.OriginalValues["TabBar_Scroll"])
        Parameters_Ribbon.Settings.SetIntSetting("Ribbon_Scroll", self.OriginalValues["Ribbon_Scroll"])
        Parameters_Ribbon.Settings.SetIntSetting("TabBar_Click", self.OriginalValues["TabBar_Click"])
        Parameters_Ribbon.Settings.SetIntSetting("Ribbon_Click", self.OriginalValues["Ribbon_Click"])
        # Save the preferred toolbars
        Parameters_Ribbon.Settings.SetIntSetting("Preferred_view", self.OriginalValues["Preferred_view"])
        # Set the use of the tools panel
        Parameters_Ribbon.Settings.SetBoolSetting("UseToolsPanel", self.OriginalValues["UseToolsPanel"])
        # Set the use of FreeCAD's overlay function
        Parameters_Ribbon.Settings.SetBoolSetting("UseFCOverlay", self.OriginalValues["UseFCOverlay"])
        Parameters_Ribbon.Settings.SetBoolSetting("UseButtonBackGround", self.OriginalValues["UseButtonBackGround"])
        # Set the use of custom icons
        Parameters_Ribbon.Settings.SetBoolSetting("CustomIcons", self.OriginalValues["CustomIcons"])
        # Set the use of custom colors
        Parameters_Ribbon.Settings.SetBoolSetting("CustomColors", self.OriginalValues["CustomColors"])
        Parameters_Ribbon.Settings.SetBoolSetting("BorderTransparant", self.OriginalValues["BorderTransparant"])
        Parameters_Ribbon.Settings.SetStringSetting("Color_Borders", self.OriginalValues["Color_Borders"])
        # Parameters_Ribbon.Settings.SetStringSetting("Color_Background", self.OriginalValues["Color_Background"])
        Parameters_Ribbon.Settings.SetStringSetting(
            "Color_Background_Hover", self.OriginalValues["Color_Background_Hover"]
        )
        Parameters_Ribbon.Settings.SetStringSetting("Color_Background_App", self.OriginalValues["Color_Background_App"])

        # Set the size of the window to the previous state
        Parameters_Ribbon.Settings.SetIntSetting("SettingsDialog_Height", self.form.height())
        Parameters_Ribbon.Settings.SetIntSetting("SettingsDialog_Width", self.form.width())

        # Close the form
        self.form.close()
        return

    @staticmethod
    def on_Close_clicked(self):
        # Save backup settings
        Parameters_Ribbon.Settings.SetBoolSetting("BackupEnabled", self.ValuesToUpdate["BackupEnabled"])
        Parameters_Ribbon.Settings.SetStringSetting("BackupFolder", self.ValuesToUpdate["BackupFolder"])
        # Save tabBar style
        Parameters_Ribbon.Settings.SetIntSetting("TabBar_Style", self.ValuesToUpdate["TabBar_Style"])
        # Save icon sizes
        Parameters_Ribbon.Settings.SetIntSetting("IconSize_Small", int(self.ValuesToUpdate["IconSize_Small"]))
        Parameters_Ribbon.Settings.SetIntSetting("IconSize_Medium", int(self.ValuesToUpdate["IconSize_Medium"]))
        Parameters_Ribbon.Settings.SetIntSetting("IconSize_Large", int(self.ValuesToUpdate["IconSize_Large"]))
        Parameters_Ribbon.Settings.SetStringSetting("Stylesheet", self.ValuesToUpdate["Stylesheet"])
        Parameters_Ribbon.Settings.SetIntSetting(
            "ApplicationButtonSize", int(self.ValuesToUpdate["ApplicationButtonSize"])
        )
        Parameters_Ribbon.Settings.SetIntSetting(
            "QuickAccessButtonSize", int(self.ValuesToUpdate["QuickAccessButtonSize"])
        )
        Parameters_Ribbon.Settings.SetIntSetting("TabBarSize", int(self.ValuesToUpdate["TabBarSize"]))
        Parameters_Ribbon.Settings.SetIntSetting(
            "RightToolbarButtonSize", int(self.ValuesToUpdate["RightToolbarButtonSize"])
        )
        # Save text settings
        Parameters_Ribbon.Settings.SetBoolSetting("ShowIconText_Small", self.ValuesToUpdate["ShowIconText_Small"])
        Parameters_Ribbon.Settings.SetBoolSetting("ShowIconText_Medium", self.ValuesToUpdate["ShowIconText_Medium"])
        Parameters_Ribbon.Settings.SetBoolSetting("ShowIconText_Large", self.ValuesToUpdate["ShowIconText_Large"])
        Parameters_Ribbon.Settings.SetBoolSetting("WrapText_Medium", self.ValuesToUpdate["WrapText_Medium"])
        Parameters_Ribbon.Settings.SetBoolSetting("WrapText_Large", self.ValuesToUpdate["WrapText_Large"])
        # Save No of columns
        Parameters_Ribbon.Settings.SetIntSetting("MaxColumnsPerPanel", int(self.ValuesToUpdate["MaxColumnsPerPanel"]))
        Parameters_Ribbon.Settings.SetBoolSetting("DebugMode", self.ValuesToUpdate["DebugMode"])
        Parameters_Ribbon.Settings.SetBoolSetting("ShowOnHover", self.ValuesToUpdate["ShowOnHover"])
        # Save behavior settings
        Parameters_Ribbon.Settings.SetIntSetting("TabBar_Scroll", self.ValuesToUpdate["TabBar_Scroll"])
        Parameters_Ribbon.Settings.SetIntSetting("Ribbon_Scroll", self.ValuesToUpdate["Ribbon_Scroll"])
        Parameters_Ribbon.Settings.SetIntSetting("TabBar_Click", self.ValuesToUpdate["TabBar_Click"])
        Parameters_Ribbon.Settings.SetIntSetting("Ribbon_Click", self.ValuesToUpdate["Ribbon_Click"])
        # Save the preferred toolbars
        Parameters_Ribbon.Settings.SetIntSetting("Preferred_view", self.ValuesToUpdate["Preferred_view"])
        # Set the use of the tools panel
        Parameters_Ribbon.Settings.SetBoolSetting("UseToolsPanel", self.ValuesToUpdate["UseToolsPanel"])
        # Set the use of FreeCAD's overlay function
        Parameters_Ribbon.Settings.SetBoolSetting("UseFCOverlay", self.ValuesToUpdate["UseFCOverlay"])
        Parameters_Ribbon.Settings.SetBoolSetting("UseButtonBackGround", self.ValuesToUpdate["UseButtonBackGround"])
        # Set the use of custom icons
        Parameters_Ribbon.Settings.SetBoolSetting("CustomIcons", self.ValuesToUpdate["CustomIcons"])
        # Set the use of custom colors
        Parameters_Ribbon.Settings.SetBoolSetting("CustomColors", self.ValuesToUpdate["CustomColors"])
        Parameters_Ribbon.Settings.SetBoolSetting("BorderTransparant", self.ValuesToUpdate["BorderTransparant"])
        Parameters_Ribbon.Settings.SetStringSetting("Color_Borders", self.ValuesToUpdate["Color_Borders"])
        # Parameters_Ribbon.Settings.SetStringSetting("Color_Background", self.ValuesToUpdate["Color_Background"])
        Parameters_Ribbon.Settings.SetStringSetting(
            "Color_Background_Hover", self.ValuesToUpdate["Color_Background_Hover"]
        )
        Parameters_Ribbon.Settings.SetStringSetting("Color_Background_App", self.ValuesToUpdate["Color_Background_App"])

        # Set the size of the window to the previous state
        Parameters_Ribbon.Settings.SetIntSetting("SettingsDialog_Height", self.form.height())
        Parameters_Ribbon.Settings.SetIntSetting("SettingsDialog_Width", self.form.width())

        # Close the form
        self.form.close()
        # show the restart dialog
        if self.settingChanged is True:
            result = StandardFunctions.RestartDialog(includeIcons=True)
            if result == "yes":
                StandardFunctions.restart_freecad()
            if result == "no":
                App.saveParameter()
        return

    @staticmethod
    def on_Reset_clicked(self):
        # load all settings
        self.form.EnableBackup.setChecked(DefaultSettings["BackupEnabled"])
        self.form.label_4.setText(DefaultSettings["BackupFolder"])
        self.form.TabbarStyle.setCurrentIndex(DefaultSettings["TabBar_Style"])
        self.form.IconSize_Small.setValue(DefaultSettings["IconSize_Small"])
        self.form.IconSize_Medium.setValue(DefaultSettings["IconSize_Medium"])
        self.form.IconSize_Large.setValue(DefaultSettings["IconSize_Large"])
        self.form.IconSize_ApplicationButton.setValue(DefaultSettings["ApplicationButtonSize"])
        self.form.IconSize_QuickAccessButton.setValue(DefaultSettings["QuickAccessButtonSize"])
        self.form.IconSize_rightToolbarButton.setValue(DefaultSettings["RightToolbarButtonSize"])
        self.form.TabbarHeight.setValue(DefaultSettings["TabBarSize"])
        self.form.label_7.setText(DefaultSettings["Stylesheet"])
        if DefaultSettings["ShowIconText_Small"] is True:
            self.form.ShowText_Small.setCheckState(Qt.CheckState.Checked)
        else:
            self.form.ShowText_Small.setCheckState(Qt.CheckState.Unchecked)
        if DefaultSettings["ShowIconText_Medium"] is True:
            self.form.ShowText_Medium.setCheckState(Qt.CheckState.Checked)
        else:
            self.form.ShowText_Medium.setCheckState(Qt.CheckState.Unchecked)
        if DefaultSettings["ShowIconText_Large"] is True:
            self.form.ShowText_Large.setCheckState(Qt.CheckState.Checked)
        else:
            self.form.ShowText_Large.setCheckState(Qt.CheckState.Unchecked)
        self.form.MaxPanelColumn.setValue(DefaultSettings["MaxColumnsPerPanel"])
        if DefaultSettings["DebugMode"] is True:
            self.form.DebugMode.setCheckState(Qt.CheckState.Checked)
        else:
            self.form.DebugMode.setCheckState(Qt.CheckState.Unchecked)

        if DefaultSettings["ShowOnHover"] is True:
            self.form.EnableEnterEvent.setCheckState(Qt.CheckState.Checked)
        else:
            self.form.EnableEnterEvent.setCheckState(Qt.CheckState.Unchecked)
        # if it is FreeCAD 1.0 disable this option.
        if int(App.Version()[0]) > 0:
            self.form.EnableEnterEvent.setDisabled(True)
            self.form.EnableEnterEvent.setHidden(True)

        self.form.ScrollSpeed_TabBar.setValue(DefaultSettings["TabBar_Scroll"])
        self.form.ScrollSpeed_Ribbon.setValue(DefaultSettings["Ribbon_Scroll"])
        self.form.ScrollClicks_TabBar.setValue(DefaultSettings["TabBar_Click"])
        self.form.ScrollClicks_Ribbon.setValue(DefaultSettings["Ribbon_Click"])

        self.form.PreferedViewPanel.setCurrentIndex(DefaultSettings["Preferred_view"])
        if DefaultSettings["UseToolsPanel"] is True:
            self.form.FCOverlayEnabled.setCheckState(Qt.CheckState.Checked)
        else:
            self.form.FCOverlayEnabled.setCheckState(Qt.CheckState.Unchecked)
        self.settingChanged = True

        # Set the color and icon buttons
        self.form.CustomIcons.setCheckState(Qt.CheckState.Unchecked)

        self.form.Tab_Scroll_Left.setIcon(StyleMapping.ReturnStyleItem("ScrollLeftButton_Tab", False))
        self.form.Tab_Scroll_Left.setIconSize(
            QSize(self.form.Tab_Scroll_Left.width() - 6, self.form.Tab_Scroll_Left.height() - 6)
        )

        self.form.Tab_Scroll_Right.setIcon(StyleMapping.ReturnStyleItem("ScrollRightButton_Tab", False))
        self.form.Tab_Scroll_Right.setIconSize(
            QSize(self.form.Tab_Scroll_Right.width() - 6, self.form.Tab_Scroll_Right.height() - 6)
        )

        self.form.Ribbon_Scroll_Left.setIcon(StyleMapping.ReturnStyleItem("ScrollLeftButton_Category", False))
        self.form.Ribbon_Scroll_Left.setIconSize(
            QSize(self.form.Ribbon_Scroll_Left.width() - 6, self.form.Ribbon_Scroll_Left.height() - 6)
        )

        self.form.Ribbon_Scroll_Right.setIcon(StyleMapping.ReturnStyleItem("ScrollRightButton_Category", False))
        self.form.Ribbon_Scroll_Right.setIconSize(
            QSize(self.form.Ribbon_Scroll_Right.width() - 6, self.form.Ribbon_Scroll_Right.height() - 6)
        )

        self.form.MoreCommands.setIcon(StyleMapping.ReturnStyleItem("OptionButton", False))
        self.form.MoreCommands.setIconSize(
            QSize(self.form.MoreCommands.width() - 6, self.form.MoreCommands.height() - 6)
        )

        self.form.pinButton_open.setIcon(StyleMapping.ReturnStyleItem("PinButton_open", False))
        self.form.pinButton_open.setIconSize(
            QSize(self.form.pinButton_open.width() - 6, self.form.pinButton_open.height() - 6)
        )

        self.form.pinButton_closed.setIcon(StyleMapping.ReturnStyleItem("PinButton_closed", False))
        self.form.pinButton_closed.setIconSize(
            QSize(self.form.pinButton_closed.width() - 6, self.form.pinButton_closed.height() - 6)
        )

        self.form.Color_Borders.setProperty("color", QColor(StyleMapping.ReturnStyleItem("Color_Borders")))
        # self.form.Color_Background.setProperty("color", QColor(StyleMapping.ReturnStyleItem("Color_Background")))
        self.form.Color_Background_Hover.setProperty(
            "color", QColor(StyleMapping.ReturnStyleItem("Color_Background_Hover"))
        )
        self.form.Color_Background_App.setProperty(
            "color", QColor(StyleMapping.ReturnStyleItem("Color_Background_App"))
        )
        return

    # endregion---------------------------------------------------------------------------------------


def main():
    # Get the form
    Dialog = LoadDialog().form
    # Show the form
    Dialog.show()

    return
