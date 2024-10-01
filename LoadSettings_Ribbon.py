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
import sys

import Standard_Functions_RIbbon as StandardFunctions
import Parameters_Ribbon

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


class LoadDialog(Settings_ui.Ui_Form):
    Backup = Parameters_Ribbon.ENABLE_BACKUP
    BackupLocation = pathBackup
    StyleSheet = Parameters_Ribbon.STYLESHEET
    ShowText_Small = Parameters_Ribbon.SHOW_ICON_TEXT_SMALL
    ShowText_Medium = Parameters_Ribbon.SHOW_ICON_TEXT_MEDIUM
    ShowText_Large = Parameters_Ribbon.SHOW_ICON_TEXT_LARGE

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

        # load all settings
        self.form.EnableBackup.setChecked(Parameters_Ribbon.ENABLE_BACKUP)
        self.form.label_4.setText(Parameters_Ribbon.BACKUP_LOCATION)
        self.form.IconSize_Small.setValue(Parameters_Ribbon.ICON_SIZE_SMALL)
        self.form.IconSize_Medium.setValue(Parameters_Ribbon.ICON_SIZE_MEDIUM)
        # self.form.IconSize_Large.setValue(Parameters_Ribbon.ICON_SIZE_LARGE)
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

        # region - connect controls with functions----------------------------------------------------
        #
        self.form.EnableBackup.clicked.connect(self.on_EnableBackup_clicked)
        self.form.BackUpLocation.clicked.connect(self.on_BackUpLocation_clicked)
        self.form.IconSize_Small.textChanged.connect(self.on_IconSize_Small_TextChanged)
        self.form.IconSize_Medium.textChanged.connect(self.on_IconSize_Medium_TextChanged)
        self.form.StyleSheetLocation.clicked.connect(self.on_StyleSheetLocation_clicked)

        self.form.ShowText_Small.clicked.connect(self.on_ShowTextSmall_clicked)
        self.form.ShowText_Medium.clicked.connect(self.on_ShowTextMedium_clicked)
        self.form.ShowText_Large.clicked.connect(self.on_ShowTextLarge_clicked)

        self.form.MaxPanelColumn.textChanged.connect(self.on_MaxPanelColumn_TextChanged)

        # Connect the cancel button
        def Cancel():
            self.on_Cancel_clicked(self)

        self.form.Cancel.connect(self.form.Cancel, SIGNAL("clicked()"), Cancel)

        # Connect the button GenerateJsonExit with the function on_GenerateJsonExit_clicked
        def GenerateJsonExit():
            self.on_Close_clicked(self)

        self.form.GenerateJsonExit.connect(self.form.GenerateJsonExit, SIGNAL("clicked()"), GenerateJsonExit)
        # endregion

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

    def on_IconSize_Small_TextChanged(self):
        Parameters_Ribbon.ICON_SIZE_SMALL = int(self.form.IconSize_Small.text())
        self.settingChanged = True
        return

    def on_IconSize_Medium_TextChanged(self):
        Parameters_Ribbon.ICON_SIZE_MEDIUM = int(self.form.IconSize_Medium.text())
        self.settingChanged = True
        return

    def on_MaxPanelColumn_TextChanged(self):
        Parameters_Ribbon.MAX_COLUMN_PANELS = int(self.form.MaxPanelColumn.text())
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
            Parameters_Ribbon.STYLESHEET = StyleSheet
            self.StyleSheet = StyleSheet
            self.settingChanged = True
        return

    def on_ShowTextSmall_clicked(self):
        if self.form.ShowText_Small.isChecked() is True:
            Parameters_Ribbon.SHOW_ICON_TEXT_SMALL = True
            self.ShowText_Small = True
        if self.form.ShowText_Small.isChecked() is False:
            Parameters_Ribbon.SHOW_ICON_TEXT_SMALL = False
            self.ShowText_Small = False
        self.settingChanged = True
        return

    def on_ShowTextMedium_clicked(self):
        if self.form.ShowText_Medium.isChecked() is True:
            Parameters_Ribbon.SHOW_ICON_TEXT_MEDIUM = True
            self.ShowText_Medium = True
        if self.form.ShowText_Medium.isChecked() is False:
            Parameters_Ribbon.SHOW_ICON_TEXT_MEDIUM = False
            self.ShowText_Medium = False
        self.settingChanged = True
        return

    def on_ShowTextLarge_clicked(self):
        if self.form.ShowText_Large.isChecked() is True:
            Parameters_Ribbon.SHOW_ICON_TEXT_LARGE = True
            self.ShowText_Large = True
        if self.form.ShowText_Large.isChecked() is False:
            Parameters_Ribbon.SHOW_ICON_TEXT_LARGE = False
            self.ShowText_Large = False
        self.settingChanged = True
        return

    @staticmethod
    def on_Cancel_clicked(self):
        # Close the form
        self.form.close()
        return

    @staticmethod
    def on_Close_clicked(self):
        Parameters_Ribbon.Settings.SetBoolSetting("BackupEnabled", self.Backup)
        Parameters_Ribbon.Settings.SetStringSetting("BackupFolder", self.BackupLocation)
        Parameters_Ribbon.Settings.SetIntSetting("IconSize_Small", int(self.form.IconSize_Small.text()))
        Parameters_Ribbon.Settings.SetIntSetting("IconSize_Medium", int(self.form.IconSize_Medium.text()))
        Parameters_Ribbon.Settings.SetStringSetting("Stylesheet", self.StyleSheet)
        Parameters_Ribbon.Settings.SetBoolSetting("ShowIconText_Small", self.ShowText_Small)
        Parameters_Ribbon.Settings.SetBoolSetting("ShowIconText_Medium", self.ShowText_Medium)
        Parameters_Ribbon.Settings.SetBoolSetting("ShowIconText_Large", self.ShowText_Large)
        Parameters_Ribbon.Settings.SetIntSetting("MaxColumnsPerPanel", int(self.form.MaxPanelColumn.text()))

        # Close the form
        self.form.close()
        # show the restart dialog
        if self.settingChanged is True:
            result = StandardFunctions.RestartDialog()
            if result == "yes":
                StandardFunctions.restart_freecad()
        return

    # endregion---------------------------------------------------------------------------------------


def main():
    # Get the form
    Dialog = LoadDialog().form
    # Show the form
    Dialog.show()

    return
