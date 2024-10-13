## FreeCAD Ribbon UI

An Ribbon UI for FreeCAD, based on the PyQtRibbon library (https://github.com/haiiliin/pyqtribbon).
This ribbon is based the work of Geolta (https://github.com/geolta/FreeCAD-Ribbon) and HakanSeven (https://github.com/HakanSeven12/Modern-UI) for the Modern-UI workbench.

![FreeCAD Ribbon UI](https://github.com/APEbbers/FreeCAD-Ribbon/blob/main/Resources/Images/Screenshot.png)

The FreeCAD ribbon provides the following functions and features:

* Replace the default toolbars with a ribbon based on the original toolbars
* The ribbon design is stored in a Json file for easy modification of the ribbon design.
* A Ribbon Design dialog is provided for easy customization. (The changes are stored in the Json file). With this dialog you can:
  * Include/exclude toolbars to be used as a panel in the ribbon
  * Include/exclude workbenches
  * Create your own panels based on one or more toolbars
  * Change the order of the panels
  * Change the order of the buttons
  * Customize button text
  * Set the button size to small, medium or large
* You can apply your own stylesheet
* Scripts are provided to help setup your own customized Ribbon
* And much more...

See the [wiki page](https://github.com/APEbbers/FreeCAD-Ribbon/wiki) for more details and on how to customize the Ribbon to your preference.

## Installation

There are three options for installing this addon:
### Via the Addon manager
Go to 'Tools/Addon-Manager' and search for 'FreeCAD-Ribbon'). Click on 'Install'.

### Custom Repository for Addon Manager

Go to `Edit/Preferences/Addon-Manager` and add the custom repository `https://github.com/APEbbers/FreeCAD-Ribbon.git` with the branch `main`. Now you can go to the Addon Manager (`Tools/Addon-Manager`) and install "FreeCAD Ribbon" (it can be that you have to update your local cache first). Now restart FreeCAD and you will see a ribbon interface :)

### Manual Installation

Download this repository, extract the folder and copy it to the `Mod` folder of FreeCAD, detailed information can be found at the [FreeCAD Wiki](https://wiki.freecad.org/Installing_more_workbenches). Now restart FreeCAD and you will see a ribbon interface :)

## Uninstallation

1. Remove the folder of this in the `Mod` folder of your FreeCAD installation
1. Restart FreeCAD.
1. When you restarted you don't see any toolbar.
1. Create a new macro (Macro menu -> macros...-> create macro)
1. Paste this code in to the new macro.

    ```python
    from PySide import QtCore, QtGui, QtWidgets
    mw = FreeCADGui.getMainWindow()
    mw.menuBar().show()

    WBList = FreeCADGui.listWorkbenches()
    for WB in WBList:
        FreeCADGui.activateWorkbench(WB)
        for tb in mw.findChildren(QtWidgets.QToolBar):
            tb.show()
    ```

1. Execute the macro
1. Restart FreeCAD.

## Discussion

Feel free to discuss this addon on the [FreeCAD Forum](https://forum.freecad.org/viewtopic.php?t=79235).

## Known Issues

- To retrieve all toolbars and command per workbench, all workbenches must be activated. Unfortunally, this results in a longer loading time for the Ribbon Design menu. (up to a few minutes)
* When the Assembly4 Workbench is installed, make sure that the internal assembly workbench is placed before the Assembly4 workbench. If not, the ribbon for the internal assembly will show the wrong panel named "Assembly".

## License

GPL v3.0 (see [LICENSE](LICENSE))
