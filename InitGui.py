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
import Parameters_Ribbon
import shutil


def QT_TRANSLATE_NOOP(context, text):
    return text


translate = App.Qt.translate

# check if there is a "RibbonStructure.json". if not create one
file = os.path.join(os.path.dirname(FCBinding.__file__), "RibbonStructure.json")
file_default = os.path.join(
    os.path.dirname(FCBinding.__file__), "RibbonStructure_default.json"
)
source = os.path.join(os.path.dirname(FCBinding.__file__), "CreateStructure.txt")
source_default = os.path.join(
    os.path.dirname(FCBinding.__file__), "CreateStructure.txt"
)

# check if file exits
fileExists = os.path.isfile(file)
# if not, copy and rename
if fileExists is False:
    shutil.copy(source, file)

# check if file exits
fileExists = os.path.isfile(file_default)
# if not, copy and rename
if fileExists is False:
    shutil.copy(source_default, file_default)

# remove the test workbench
Gui.removeWorkbench("TestWorkbench")

try:
    print(translate("FreeCAD Ribbon", "Activating Ribbon Bar..."))
    mw = Gui.getMainWindow()
    mw.workbenchActivated.connect(FCBinding.run)
except Exception as e:
    if Parameters_Ribbon.DEBUG_MODE is True:
        print(f"{e.with_traceback(e.__traceback__)}, 0")

Gui.addLanguagePath(os.path.join(os.path.dirname(FCBinding.__file__), "translations"))
Gui.updateLocale()
