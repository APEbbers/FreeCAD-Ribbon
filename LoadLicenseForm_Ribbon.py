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

import Standard_Functions_Ribbon as StandardFunctions
import Parameters_Ribbon
from Parameters_Ribbon import Parameters

# Get the resources
ConfigDirectory = Parameters.CONFIG_DIR
pathIcons = Parameters.ICON_LOCATION
pathStylSheets = Parameters.STYLESHEET_LOCATION
pathUI = Parameters.UI_LOCATION
pathScripts = os.path.join(ConfigDirectory, "Scripts")
pathPackages = os.path.join(os.path.dirname(__file__), "Resources", "packages")
pathBackup = Parameters.BACKUP_LOCATION
sys.path.append(ConfigDirectory)
sys.path.append(pathIcons)
sys.path.append(pathStylSheets)
sys.path.append(pathUI)
sys.path.append(pathPackages)
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

        # Get the git info
        PackageXML = os.path.join(os.path.dirname(__file__), "package.xml")
        version = StandardFunctions.ReturnXML_Value(PackageXML, "version")
        Maintainer = StandardFunctions.ReturnXML_Value(PackageXML, "maintainer")
        branch = "main"
        CommitID = ""
        with open(os.path.join(os.path.dirname(__file__), "Resources", "GitInfo", "version_main"), "r") as fd:
            line = fd.readlines()[0]
            CommitID = line[:10]
        
        if version.endswith("dev"):
            branch = "Develop"
            with open(os.path.join(os.path.dirname(__file__), "Resources", "GitInfo", "version_Develop"), "r") as fd:
                line = fd.readlines()[0]
                CommitID = line[:10]

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

        # Write the text for credits if present 
        if os.path.exists(os.path.join(os.path.dirname(__file__), "Resources", "GitInfo", "contributors.txt")):
            lines = []
            with open(os.path.join(os.path.dirname(__file__), "Resources", "GitInfo", "contributors.txt"), "r") as fd:
                    lines = fd.readlines()
                
            text = translate("FreeCAD Ribbon", "Contributors:\n")                
            for line in lines:
                if "pre-commit" in line or "Email" in line:
                    continue
                # Filter the lines
                addition = line.split()[0]
                addition = addition.split("\t")[0]
                if "@" in addition and "noreply" in addition:
                    addition = addition.split("@")[0]
                if "+" in addition:
                    addition = addition.split("+")[1]
                text = text + " - " + addition + "\n"
            # Set the text
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
        
        self.form.CopyVersionInfo.setText(translate("FreeCAD Ribbon", "Copied!"))
        print(Text)
        return


def main():
    # Get the form
    Dialog = LoadDialog().form
    # Show the form
    Dialog.show()

    return
