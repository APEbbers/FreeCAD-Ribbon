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

from PySide.QtCore import Qt, SIGNAL
from PySide.QtWidgets import (
    QTabWidget,
    QSlider,
    QSpinBox,
    QCheckBox,
    QComboBox,
    QLabel,
    QTabWidget,
    QSizePolicy,
)
import sys

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
    Backup = Parameters_Ribbon.ENABLE_BACKUP
    BackupLocation = pathBackup
    StyleSheet = Parameters_Ribbon.STYLESHEET
    ShowText_Small = Parameters_Ribbon.SHOW_ICON_TEXT_SMALL
    ShowText_Medium = Parameters_Ribbon.SHOW_ICON_TEXT_MEDIUM
    ShowText_Large = Parameters_Ribbon.SHOW_ICON_TEXT_LARGE
    DebugMode = Parameters_Ribbon.DEBUG_MODE
    ShowOnHover = Parameters_Ribbon.SHOW_ON_HOVER
    UseToolsPanel = Parameters_Ribbon.USE_TOOLSPANEL

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
        self.form.tabWidget.removeTab(2)

        # Remove tabbar click settings for the time being
        self.form.label_15.setHidden(True)
        self.form.label_15.setDisabled(True)
        self.form.ScrollClicks_TabBar.setHidden(True)
        self.form.ScrollClicks_TabBar.setDisabled(True)

        # load all settings
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
        self.form.MaxPanelColumn.setValue(Parameters_Ribbon.MAX_COLUMN_PANELS)
        if Parameters_Ribbon.DEBUG_MODE is True:
            self.form.DebugMode.setCheckState(Qt.CheckState.Checked)
        else:
            self.form.DebugMode.setCheckState(Qt.CheckState.Unchecked)

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

        self.form.PreferedViewPanel.setCurrentIndex(Parameters_Ribbon.PREFERRED_VIEW)

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
        # Connect the preferred panel settings
        self.form.PreferedViewPanel.currentIndexChanged.connect(self.on_PreferedViewPanel_currentIndexChanged)
        # Connect the EnableTools checkbox:
        self.form.EnableToolsPanel.clicked.connect(self.on_EnableToolsPanelt_clicked)
        # endregion

        # Set the minimum and maximum settings for the iconsizes
        self.form.IconSize_Small.setMinimum(5)
        self.form.IconSize_Medium.setMinimum(5)
        self.form.IconSize_Large.setMinimum(5)
        self.form.IconSize_ApplicationButton.setMinimum(5)
        self.form.IconSize_QuickAccessButton.setMinimum(5)
        self.form.IconSize_rightToolbarButton.setMinimum(5)
        self.form.TabbarHeight.setMinimum(5)

        # Set the first tab active
        self.form.tabWidget.setCurrentIndex(0)

        return

    # region - Control functions----------------------------------------------------------------------

    def on_EnableBackup_clicked(self):
        if self.form.EnableBackup.isChecked() is True:
            Parameters_Ribbon.ENABLE_BACKUP = True
            self.Backup = True
        if self.form.EnableBackup.isChecked() is False:
            Parameters_Ribbon.ENABLE_BACKUP = False
            self.Backup = False

        self.settingChanged = True
        return

    def on_BackUpLocation_clicked(self):
        BackupFolder = ""
        BackupFolder = StandardFunctions.GetFolder(parent=None, DefaultPath=Parameters_Ribbon.BACKUP_LOCATION)
        if BackupFolder != "":
            self.pathBackup = BackupFolder
            self.form.label_4.setText(BackupFolder)
            Parameters_Ribbon.BACKUP_LOCATION = BackupFolder
            self.BackupLocation = BackupFolder
            self.settingChanged = True
        return

    def on_TabbarStyle_currentIndexChanged(self):
        # Parameters_Ribbon.TABBAR_STYLE = self.form.TabbarStyle.currentIndex()
        self.settingChanged = True
        return

    def on_IconSize_Small_TextChanged(self):
        # Parameters_Ribbon.ICON_SIZE_SMALL = int(self.form.IconSize_Small.text())
        self.settingChanged = True
        return

    def on_IconSize_Medium_TextChanged(self):
        # Parameters_Ribbon.ICON_SIZE_MEDIUM = int(self.form.IconSize_Medium.text())
        self.settingChanged = True
        return

    def on_IconSize_Large_TextChanged(self):
        # Parameters_Ribbon.ICON_SIZE_LARGE = int(self.form.IconSize_Large.text())
        self.settingChanged = True
        return

    def on_IconSize_ApplicationButton_TextChanged(self):
        # Parameters_Ribbon.APP_ICON_SIZE = int(self.form.IconSize_ApplicationButton.text())
        self.settingChanged = True
        return

    def on_IconSize_QuickAccessButton_TextChanged(self):
        # Parameters_Ribbon.QUICK_ICON_SIZE = int(self.form.IconSize_QuickAccessButton.text())
        self.settingChanged = True
        return

    def on_IconSize_rightToolbarButton_TextChanged(self):
        # Parameters_Ribbon.RIGHT_ICON_SIZE = int(self.form.IconSize_rightToolbarButton.text())
        self.settingChanged = True
        return

    def on_TabbarHeight_TextChanged(self):
        # Parameters_Ribbon.TABBAR_SIZE = int(self.form.TabbarHeight.text())
        self.settingChanged = True
        return

    def on_MaxPanelColumn_TextChanged(self):
        # Parameters_Ribbon.MAX_COLUMN_PANELS = int(self.form.MaxPanelColumn.text())
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
            # Parameters_Ribbon.STYLESHEET = StyleSheet
            self.StyleSheet = StyleSheet
            self.settingChanged = True
        return

    def on_ShowTextSmall_clicked(self):
        if self.form.ShowText_Small.isChecked() is True:
            # Parameters_Ribbon.SHOW_ICON_TEXT_SMALL = True
            self.ShowText_Small = True
        if self.form.ShowText_Small.isChecked() is False:
            # Parameters_Ribbon.SHOW_ICON_TEXT_SMALL = False
            self.ShowText_Small = False
        self.settingChanged = True
        return

    def on_ShowTextMedium_clicked(self):
        if self.form.ShowText_Medium.isChecked() is True:
            # Parameters_Ribbon.SHOW_ICON_TEXT_MEDIUM = True
            self.ShowText_Medium = True
        if self.form.ShowText_Medium.isChecked() is False:
            # Parameters_Ribbon.SHOW_ICON_TEXT_MEDIUM = False
            self.ShowText_Medium = False
        self.settingChanged = True
        return

    def on_ShowTextLarge_clicked(self):
        if self.form.ShowText_Large.isChecked() is True:
            # Parameters_Ribbon.SHOW_ICON_TEXT_LARGE = True
            self.ShowText_Large = True
        if self.form.ShowText_Large.isChecked() is False:
            # Parameters_Ribbon.SHOW_ICON_TEXT_LARGE = False
            self.ShowText_Large = False
        self.settingChanged = True
        return

    def on_DebugMode_clicked(self):
        if self.form.DebugMode.isChecked() is True:
            # Parameters_Ribbon.DEBUG_MODE = True
            self.DebugMode = True
        if self.form.DebugMode.isChecked() is False:
            # Parameters_Ribbon.DEBUG_MODE = False
            self.DebugMode = False
        self.settingChanged = True
        return

    def on_EnableEnterEvent_clicked(self):
        if self.form.EnableEnterEvent.isChecked() is True:
            # Parameters_Ribbon.SHOW_ON_HOVER = True
            self.ShowOnHover = True
        if self.form.EnableEnterEvent.isChecked() is False:
            # Parameters_Ribbon.SHOW_ON_HOVER = False
            self.ShowOnHover = False
        self.settingChanged = True

    def on_ScrollSpeed_TabBar_valueCHanged(self):
        # Parameters_Ribbon.TABBAR_SCROLLSPEED = self.form.ScrollSpeed_TabBar.value()
        self.settingChanged = True

    def on_ScrollSpeed_Ribbon_valueCHanged(self):
        # Parameters_Ribbon.RIBBON_SCROLLSPEED = self.form.ScrollSpeed_Ribbon.value()
        self.settingChanged = True

    def on_ScrollClicks_TabBar_valueCHanged(self):
        # Parameters_Ribbon.TABBAR_CLICKSPEED = self.form.ScrollClicks_TabBar.value()
        self.settingChanged = True

    def on_ScrollClicks_Ribbon_valueCHanged(self):
        # Parameters_Ribbon.RIBBON_CLICKSPEED = self.form.ScrollClicks_Ribbon.value()
        self.settingChanged = True

    def on_PreferedViewPanel_currentIndexChanged(self):
        # Parameters_Ribbon.PREFERRED_VIEW = self.form.PreferedViewPanel.currentIndex()
        self.settingChanged = True
        return

    def on_EnableToolsPanelt_clicked(self):
        if self.form.EnableToolsPanel.isChecked() is True:
            # Parameters_Ribbon.USE_TOOLSPANEL = True
            self.UseToolsPanel = True
        if self.form.EnableToolsPanel.isChecked() is False:
            # Parameters_Ribbon.SHOW_ICON_TEXT_LARGE = False
            self.UseToolsPanel = False
        self.settingChanged = True
        return

    @staticmethod
    def on_Cancel_clicked(self):
        # Set the size of the window to the previous state
        Parameters_Ribbon.Settings.SetIntSetting("SettingsDialog_Height", self.form.height())
        Parameters_Ribbon.Settings.SetIntSetting("SettingsDialog_Width", self.form.width())
        # Close the form
        self.form.close()
        return

    @staticmethod
    def on_Close_clicked(self):
        # Save backup settings
        Parameters_Ribbon.Settings.SetBoolSetting("BackupEnabled", self.Backup)
        Parameters_Ribbon.Settings.SetStringSetting("BackupFolder", self.BackupLocation)
        # Save tabBar style
        Parameters_Ribbon.Settings.SetIntSetting("TabBar_Style", self.form.TabbarStyle.currentIndex())
        # Save icon sizes
        Parameters_Ribbon.Settings.SetIntSetting("IconSize_Small", int(self.form.IconSize_Small.text()))
        Parameters_Ribbon.Settings.SetIntSetting("IconSize_Medium", int(self.form.IconSize_Medium.text()))
        Parameters_Ribbon.Settings.SetIntSetting("IconSize_Large", int(self.form.IconSize_Large.text()))
        Parameters_Ribbon.Settings.SetStringSetting("Stylesheet", self.StyleSheet)
        Parameters_Ribbon.Settings.SetIntSetting(
            "ApplicationButtonSize", int(self.form.IconSize_ApplicationButton.text())
        )
        Parameters_Ribbon.Settings.SetIntSetting(
            "QuickAccessButtonSize", int(self.form.IconSize_QuickAccessButton.text())
        )
        Parameters_Ribbon.Settings.SetIntSetting("TabBarSize", int(self.form.TabbarHeight.text()))
        Parameters_Ribbon.Settings.SetIntSetting(
            "RightToolbarButtonSize", int(self.form.IconSize_rightToolbarButton.text())
        )
        # Save text settings
        Parameters_Ribbon.Settings.SetBoolSetting("ShowIconText_Small", self.ShowText_Small)
        Parameters_Ribbon.Settings.SetBoolSetting("ShowIconText_Medium", self.ShowText_Medium)
        Parameters_Ribbon.Settings.SetBoolSetting("ShowIconText_Large", self.ShowText_Large)
        # Save No of columns
        Parameters_Ribbon.Settings.SetIntSetting("MaxColumnsPerPanel", int(self.form.MaxPanelColumn.text()))
        Parameters_Ribbon.Settings.SetBoolSetting("DebugMode", self.DebugMode)
        Parameters_Ribbon.Settings.SetBoolSetting("ShowOnHover", self.ShowOnHover)
        # Save behavior settings
        Parameters_Ribbon.Settings.SetIntSetting("TabBar_Scroll", self.form.ScrollSpeed_TabBar.value())
        Parameters_Ribbon.Settings.SetIntSetting("Ribbon_Scroll", self.form.ScrollSpeed_Ribbon.value())
        Parameters_Ribbon.Settings.SetIntSetting("TabBar_Click", self.form.ScrollClicks_TabBar.value())
        Parameters_Ribbon.Settings.SetIntSetting("Ribbon_Click", self.form.ScrollClicks_Ribbon.value())
        # Save the preferred toolbars
        Parameters_Ribbon.Settings.SetIntSetting("Preferred_view", self.form.PreferedViewPanel.currentIndex())

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
        # it is FreeCAD 1.0 disable this option.
        if int(App.Version()[0]) > 0:
            self.form.EnableEnterEvent.setDisabled(True)
            self.form.EnableEnterEvent.setHidden(True)

        self.form.ScrollSpeed_TabBar.setValue(DefaultSettings["TabBar_Scroll"])
        self.form.ScrollSpeed_Ribbon.setValue(DefaultSettings["Ribbon_Scroll"])
        self.form.ScrollClicks_TabBar.setValue(DefaultSettings["TabBar_Click"])
        self.form.ScrollClicks_Ribbon.setValue(DefaultSettings["Ribbon_Click"])

        self.form.PreferedViewPanel.setCurrentIndex(DefaultSettings["Preferred_view"])

        self.settingChanged = True

        return

    # endregion---------------------------------------------------------------------------------------


def main():
    # Get the form
    Dialog = LoadDialog().form
    # Show the form
    Dialog.show()

    return
