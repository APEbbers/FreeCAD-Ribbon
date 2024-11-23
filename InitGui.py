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
from PySide.QtCore import Signal, QObject
import sys


def QT_TRANSLATE_NOOP(context, text):
    return text


translate = App.Qt.translate

# check if there is a "RibbonStructure.json". if not create one
file = os.path.join(os.path.dirname(FCBinding.__file__), "RibbonStructure.json")
file_default = os.path.join(os.path.dirname(FCBinding.__file__), "RibbonStructure_default.json")
source = os.path.join(os.path.dirname(FCBinding.__file__), "CreateStructure.txt")
source_default = os.path.join(os.path.dirname(FCBinding.__file__), "CreateStructure.txt")

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

try:
    print(translate("FreeCAD Ribbon", "Activating Ribbon Bar..."))
    mw = Gui.getMainWindow()
    mw.workbenchActivated.connect(FCBinding.run)
except Exception as e:
    if Parameters_Ribbon.DEBUG_MODE is True:
        print(f"{e.with_traceback(e.__traceback__)}, 0")

Gui.addLanguagePath(os.path.join(os.path.dirname(FCBinding.__file__), "translations"))
Gui.updateLocale()


# region - Exception handler--------------------------------------------------------------
#
#
# https://pyqribbon.readthedocs.io/en/stable/apidoc/pyqtribbon.logger.html
# https: // timlehr.com/2018/01/python-exception-hooks-with-qt-message-box/index.html
class UncaughtHook(QObject):
    _exception_caught = Signal(object)

    def __init__(self, *args, **kwargs):
        super(UncaughtHook, self).__init__(*args, **kwargs)

        # this registers the exception_hook() function as hook with the Python interpreter
        sys.excepthook = self.exception_hook

        # connect signal to execute the message box function always on main thread
        # self._exception_caught.connect(show_exception_box)

    def exception_hook(self, exc_type, exc_value, exc_traceback):
        """Function handling uncaught exceptions.
        It is triggered each time an uncaught exception occurs.
        """
        if issubclass(exc_type, KeyboardInterrupt):
            # ignore keyboard interrupt to support console applications
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
        else:
            # ----------Suppressed original handling---------------------------------------
            exc_info = (exc_type, exc_value, exc_traceback)
            # log_msg = '\n'.join([''.join(traceback.format_tb(exc_traceback)),
            #                      '{0}: {1}'.format(exc_type.__name__, exc_value)])
            # log.critical("Uncaught exception:\n {0}".format(log_msg), exc_info=exc_info)

            # trigger message box show
            # self._exception_caught.emit(log_msg)

            App.Console.PrintWarning(
                "RibbonUI: There was an error. This is probally caused by an incompatible FreeCAD plugin!"
            )
            App.Console.PrintWarning(exc_info)
        return


# create a global instance of our exception class to register the hook
qt_exception_hook = UncaughtHook()
#
#
# endregion=========================================================================================
