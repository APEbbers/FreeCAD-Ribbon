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

# Script for creating the command for FreeCAD

# FreeCAD init script of the Work Features module
import FreeCAD as App
import FreeCADGui as Gui

# Define the translation
translate = App.Qt.translate


class RibbonApplicationMenu_Class:
    def GetResources(self):
        return {
            "Pixmap": "./Resources/icons/FreecadNew.svg",  # the name of a svg file available in the resources
            "Accel": "Alt+A",
            "MenuText": "Ribbon menu",
            "ToolTip": "Shows the ribbon menu",
        }

    def Activated(self):
        from PySide.QtWidgets import QDockWidget
        from FCBinding import ModernMenu

        # Get the main window of FreeCAD
        mw = Gui.getMainWindow()

        DockWidget = mw.findChildren(QDockWidget, "Ribbon")[0]
        Ribbon = DockWidget.findChildren(ModernMenu, "Ribbon")[0]
        Ribbon.applicationOptionButton().animateClick()
        return


class RibbonLayout_Class:
    def GetResources(self):
        return {
            "Pixmap": "./Resources/icons/FreecadNew.svg",
            "Accel": "Alt+L",
            "MenuText": "Ribbon Layout",
            "ToolTip": "Design the ribbon to your preference",
        }

    def Activated(self):
        from PySide.QtWidgets import QDockWidget
        from FCBinding import ModernMenu

        # Get the main window of FreeCAD
        mw = Gui.getMainWindow()

        DockWidget = mw.findChildren(QDockWidget, "Ribbon")[0]
        Ribbon = DockWidget.findChildren(ModernMenu, "Ribbon")[0]
        Ribbon.loadDesignMenu()
        return


class RibbonPreferences_Class:
    def GetResources(self):
        return {
            "Pixmap": "./Resources/icons/FreecadNew.svg",
            "Accel": "Alt+P",
            "MenuText": "Ribbon Preferences",
            "ToolTip": "Set preferences for the Ribbon UI",
        }

    def Activated(self):
        from PySide.QtWidgets import QDockWidget
        from FCBinding import ModernMenu

        # Get the main window of FreeCAD
        mw = Gui.getMainWindow()

        DockWidget = mw.findChildren(QDockWidget, "Ribbon")[0]
        Ribbon = DockWidget.findChildren(ModernMenu, "Ribbon")[0]
        Ribbon.loadSettingsMenu()
        return


class RibbonPin_Class:
    def GetResources(self):
        return {
            "Pixmap": "./Resources/icons/pin-icon-default.svg",
            "Accel": "Alt+T",
            "MenuText": "Pin button",
            "ToolTip": "Click to toggle the autohide function on or off",
        }

    def Activated(self):
        from PySide.QtWidgets import QDockWidget, QToolButton
        from FCBinding import ModernMenu

        # Get the main window of FreeCAD
        mw = Gui.getMainWindow()

        DockWidget = mw.findChildren(QDockWidget, "Ribbon")[0]
        Ribbon = DockWidget.findChildren(ModernMenu, "Ribbon")[0]
        RightToolbar = Ribbon.rightToolBar()
        PinButton = RightToolbar.findChildren(QToolButton, "Pin Ribbon")[0]
        PinButton.animateClick()
        return


class MenuBar_Class:
    def GetResources(self):
        return {
            "Pixmap": "./Resources/icons/FreecadNew.svg",
            "Accel": "Alt+M",
            "MenuText": "Toggle menubar",
            "ToolTip": "Click to show or hide the menubar",
        }

    def Activated(self):
        # from PySide.QtWidgets import QMenuBar, QToolButton

        # Get the main window of FreeCAD
        mw = Gui.getMainWindow()

        MenuBar = mw.menuBar()
        print(MenuBar.isVisible())
        if MenuBar.isVisible() is True:
            MenuBar.hide()
            print("Menubar hidden")
            return
        if MenuBar.isVisible() is False:
            MenuBar.show()
            print("Menubar shown")
            return
        # ToggleButton = mw.findChildren(QToolButton, "ToggleMenuBar")[0]
        # ToggleButton.animateClick()
        return


Gui.addCommand("Ribbon_Menu", RibbonApplicationMenu_Class())
Gui.addCommand("Ribbon_Layout", RibbonLayout_Class())
Gui.addCommand("Ribbon_Preferences", RibbonPreferences_Class())
Gui.addCommand("Ribbon_Pin", RibbonPin_Class())
# Gui.addCommand("Ribbon_Menubar", MenuBar_Class())
