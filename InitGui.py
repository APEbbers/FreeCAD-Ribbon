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
import os
import FreeCAD as App
import FreeCADGui as Gui
import FCBinding
import Standard_Functions_RIbbon as StandardFunctions

qtpy_present = True
pyqtribbon_present = True
keyboard_present = True

try:
    import qtpy
except ImportError:
    qtpy_present = False
try:
    import pyqtribbon
except ImportError:
    pyqtribbon_present = False


def QT_TRANSLATE_NOOP(context, text):
    return text


translate = App.Qt.translate

if qtpy_present is True:
    try:
        print(translate("FreeCAD Ribbon", "Activating Ribbon Bar..."))
        mw = Gui.getMainWindow()
        mw.workbenchActivated.connect(FCBinding.run)
    except Exception as e:
        print(e)

    Gui.addLanguagePath(os.path.join(os.path.dirname(FCBinding.__file__), "translations"))
    Gui.updateLocale()
if qtpy_present is False:
    message = translate(
        "FreeCAD Ribbon",
        "the qtpy package is missing. please , excecute the following steps:\n"
        + "1. Start 'FreeCADCmd.exe'.\n"
        + "2. type 'import pip' and press enter.\n"
        + "3. type pip.main(['install'] + ['qtpy']) and press enter\n"
        + "after that, qtpy should be installed. Now restart FreeCAD.",
    )
    StandardFunctions.Mbox(message, "FreeCAD-Ribbon", 0, "Warning")
if pyqtribbon_present is False:
    message = translate(
        "FreeCAD Ribbon",
        "The package 'pyqtribbon' is missing, a local version is used instead.\n"
        + "If you want or need to install the missing package, excecute the following steps:\n"
        + "1. Start 'FreeCADCmd.exe'.\n"
        + "2. type 'import pip' and press enter.\n"
        + "3. type pip.main(['install'] + ['qtpy']) and press enter\n"
        + "after that, qtpy should be installed. Now restart FreeCAD.",
    )
    print(message)
