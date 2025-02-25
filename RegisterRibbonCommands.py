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


# FreeCAD init script of the Work Features module
import FreeCAD as App
import FreeCADGui as Gui

# Define the translation
translate = App.Qt.translate


class RibbonApplicationMenu_Class:
    def GetResources(self):
        return {
            "Pixmap": "FreecadNew.svg",  # the name of a svg file available in the resources
            "Accel": "Alt+A",
            "MenuText": "Ribbon menu",
            "ToolTip": "Shows the ribbon menu",
        }

    def Activated(self):
        from FCBinding import ModernMenu
        from pyqtribbon_local.ribbonbar import RibbonApplicationButton

        Command = ModernMenu.applicationOptionButton().animateClick()

        return


Gui.addCommand("Ribbon_Menu", RibbonApplicationMenu_Class())
