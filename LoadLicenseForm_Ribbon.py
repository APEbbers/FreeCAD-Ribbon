# *************************************************************************
# *                                                                       *
# * Copyright (c) 2019-2024 Paul Ebbers                                   *
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
    QDialogButtonBox,
    QApplication,
    QPushButton,
    QDialog,
)
from PySide.QtGui import QIcon, QPixmap
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
import LicenseForm_ui as LicenseForm_ui

# Define the translation
translate = App.Qt.translate


class LoadDialog(LicenseForm_ui.Ui_Dialog):

    FormLoaded = False

    def __init__(self):
        # Makes "self.on_CreateBOM_clicked" listen to the changed control values instead initial values
        super(LoadDialog, self).__init__()

        # # this will create a Qt widget from our ui file
        self.form = Gui.PySideUic.loadUi(os.path.join(pathUI, "LicenseForm.ui"))

        # Make sure that the dialog stays on top
        # self.form.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)
        self.form.setWindowFlags(Qt.WindowType.Tool)
        self.form.setWindowModality(Qt.WindowModality.WindowModal)

        # Get the style from the main window and use it for this form
        mw = Gui.getMainWindow()
        palette = mw.palette()
        self.form.setPalette(palette)
        Style = mw.style()
        self.form.setStyle(Style)

        GitData = StandardFunctions.GetGitData()

        PackageXML = os.path.join(os.path.dirname(__file__), "package.xml")
        version = StandardFunctions.ReturnXML_Value(PackageXML, "version")
        Maintainer = StandardFunctions.ReturnXML_Value(PackageXML, "maintainer")
        CommitID = GitData[0]
        if CommitID is None:
            CommitID = "-"
        branch = GitData[1]
        if branch is None:
            branch = "-"

        # Add a logo
        pixmap = QPixmap(os.path.join(pathIcons, "FreecadNew.svg"))
        self.form.LogoHolder.setFixedSize(pixmap.height(), pixmap.width())
        self.form.LogoHolder.setPixmap(pixmap)

        if QLabel(self.form.LogoHolder).pixmap() is None:
            self.form.LogoHolder.setHidden(True)
            self.form.LogoHolder.setDisabled(True)

        # set the title text
        self.form.TitleText.setText("Ribbon UI")

        # Write here the introduction text and include the version
        self.form.Introduction.setText(
            translate(
                "FreeCAD Ribbon",
                f"""
        A customizable ribbon UI for FreeCAD.

        Developed by Paul Ebbers.
        Current maintainer: {Maintainer}

        Version information:
            Installed version: {version}
            Branch: {branch}
            CommitID: {CommitID}
        """,
            )
        )
        # Add the copybutton
        self.form.CopyVersionInfo.clicked.connect(
            lambda: self.on_CopyVersionInfo_Clicked(
                self,
                f"Installed version: {version}\nBranch: {branch}\nCommit ID: {CommitID}",
            ),
        )

        # Write the text for credits

        Contributers = GitData[2]
        if len(Contributers) > 0:
            text = translate("FreeCAD Ribbon", "Contributors:\n")
            for Contributor in Contributers:
                text = text + " - " + Contributor + "\n"

            self.form.ContributersText.setText(text)
        else:
            self.form.groupBox.setDisabled(True)
            self.form.groupBox.setHidden(True)

        # Read the license file from the add-on directory
        file_path = os.path.join(os.path.dirname(__file__), "LICENSE")
        with open(file_path, "r") as file:
            LICENSE = file.read()

        self.form.LicenseText.setText(LICENSE)

        # set only the ok button
        self.form.buttonBox.setStandardButtons(self.form.buttonBox.StandardButton.Ok)
        return

    @staticmethod
    def on_CopyVersionInfo_Clicked(self, Text):
        StandardFunctions.AddToClipboard(Text)
        print(Text)
        return


def main():
    # Get the form
    Dialog = LoadDialog().form
    # Show the form
    Dialog.show()

    return
