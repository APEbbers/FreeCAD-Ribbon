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

from PySide.QtCore import Qt, SIGNAL, Signal, QObject, QThread, QSize, QEvent, QEventLoop
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
    QListWidget,
    QListWidgetItem,
    QLineEdit,
)
from PySide.QtGui import QIcon, QPixmap, QDragEnterEvent, QDragLeaveEvent
import sys
import json
from datetime import datetime, timedelta

import Standard_Functions_Ribbon as StandardFunctions
from Standard_Functions_Ribbon import CommandInfoCorrections
import Parameters_Ribbon
from Parameters_Ribbon import Parameters
import Serialize_Ribbon
import CacheFunctions
import FCBinding
from CustomWidgets import QuickAccessToolButton, CustomControls
import StyleMapping_Ribbon

import pyqtribbon_local as pyqtribbon
from pyqtribbon_local.ribbonbar import RibbonMenu, RibbonTitleWidget, RibbonApplicationButton
from pyqtribbon_local.panel import RibbonPanel, RibbonPanelItemWidget, RibbonPanelTitle
from pyqtribbon_local.toolbutton import RibbonToolButton, RibbonButtonStyle
from pyqtribbon_local.separator import RibbonSeparator
from pyqtribbon_local.category import RibbonCategory, RibbonCategoryLayoutButton, RibbonNormalCategory, RibbonContextCategory

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
import AddCommands_ui as AddCommands_ui

# Define the translation
translate = App.Qt.translate

 # Get the main window from FreeCAD
mw = Gui.getMainWindow()

class LoadDialog(AddCommands_ui.Ui_Form):    
    # Create a list for the commands
    List_Commands = []
    # Create a dict for the dropdownbuttons and newPanels
    Dict_DropDownButtons = {}
    Dict_NewPanels = {}
    # Create the lists for the deserialized icons
    List_CommandIcons = []
    List_WorkBenchIcons = []
    
    buttonRemove = Signal()
    
    # Create a signal to emit the closeEvent to FCBinding
    closeSignal = Signal()
            
    def __init__(self):
        super(LoadDialog, self).__init__()
        
        # Set the wait cursor
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        QApplication.processEvents(QEventLoop.ProcessEventsFlag.AllEvents)

        # # this will create a Qt widget from our ui file
        self.form = Gui.PySideUic.loadUi(os.path.join(pathUI, "AddCommands.ui"))
        # Set its title
        self.form.setWindowTitle(translate("FreeCAD Ribbon", "Add or remove buttons"))
        self.form.setAcceptDrops(True)
        
        # Install an event filter to catch events from the main window and act on it.
        self.form.installEventFilter(EventInspector(self.form))
        
        # set all widgets on the form to not accepting drops
        self.form.CommandsAvailable_NP.setAcceptDrops(False)
        self.form.SearchBar_NP.setAcceptDrops(False)
        
        # Get the address of the repository address
        PackageXML = os.path.join(os.path.dirname(__file__), "package.xml")
        self.ReproAdress = StandardFunctions.ReturnXML_Value(
            PackageXML, "url", "type", "repository"
        )
        
        # load the RibbonStructure.json
        self.ReadJson()

        # Make sure that the dialog stays on top
        self.form.raise_()
        self.form.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)
        self.form.setFocus(Qt.FocusReason.PopupFocusReason)

        # Position the dialog in front of FreeCAD
        centerPoint = mw.geometry().center()
        Rectangle = self.form.frameGeometry()
        Rectangle.moveCenter(centerPoint)
        self.form.move(Rectangle.topLeft())
        
        # Check if there is a datafile. if not, ask the user to create one.
        DataFile = os.path.join(ConfigDirectory, "RibbonDataFile.dat")
        if os.path.exists(DataFile) is False:
            Question = translate(
                "FreeCAD Ribbon",
                "The first time, a data file must be generated!\n"
                "This can take a while! Do you want to proceed?",
            )
            Answer = StandardFunctions.Mbox(Question, "FreeCAD Ribbon", 1, "Question")
            if Answer == "yes":
                CacheFunctions.CreateCache()
        
        # region - Load data------------------------------------------------------------------
        #
        Data = {}
        # read ribbon structure from JSON file
        with open(DataFile, "r") as file:
            Data.update(json.load(file))
        file.close()

        DataUpdateNeeded = False
        try:
            FileVersion = Data["dataVersion"]
            if FileVersion != CacheFunctions.DataFileVersion:
                DataUpdateNeeded = True
        except Exception:
            DataUpdateNeeded = True
        if DataUpdateNeeded is True:
            Question = translate(
                "FreeCAD Ribbon",
                "The current data file is based on an older format!\n"
                "It is important to update the data!\n"
                "Do you want to proceed?\n"
                "This can take a while!",
            )

            Answer = StandardFunctions.Mbox(Question, "FreeCAD Ribbon", 1, "Question")
            if Answer == "yes":
                CacheFunctions.CreateCache()

        # get the system language
        FreeCAD_preferences = App.ParamGet("User parameter:BaseApp/Preferences/General")
        try:
            FCLanguage = FreeCAD_preferences.GetString("Language")
            # Check if the language in the data file machtes the system language
            IsSystemLanguage = True
            if FCLanguage != Data["Language"]:
                IsSystemLanguage = False
            # If the languguage doesn't match, ask the user to update the data
            if IsSystemLanguage is False:
                Question = translate(
                    "FreeCAD Ribbon",
                    "The data was generated for a differernt language!\n"
                    "Do you want to update the data?\n"
                    "This can take a while!",
                )

                Answer = StandardFunctions.Mbox(
                    Question, "FreeCAD Ribbon", 1, "Question"
                )
                if Answer == "yes":
                    CacheFunctions.CreateCache(resetTexts=True)
        except Exception:
            pass

        # Load the standard lists for Workbenches, toolbars and commands
        self.List_Workbenches = Data["List_Workbenches"]
        self.StringList_Toolbars = Data["StringList_Toolbars"]
        self.List_Commands = Data["List_Commands"]

        # test if List_Commands is correct
        i = 5
        if len(self.List_Commands) > 0:
            for item in self.List_Commands:
                if len(item) < 5:
                    i = len(item)
                    break
        if i < 5:
            Question = translate(
                "FreeCAD Ribbon",
                "It seems that the data file is not up-to-date.\n"
                "Do you want to update the data?\n"
                "This can take a while!",
            )
            Answer = StandardFunctions.Mbox(Question, "FreeCAD Ribbon", 1, "Question")
            if Answer == "yes":
                CacheFunctions.CreateCache()

        # Load the lists for the deserialized icons
        try:
            for IconItem in Data["WorkBench_Icons"]:
                Icon: QIcon = Serialize_Ribbon.deserializeIcon(IconItem[1])
                item = [IconItem[0], Icon]
                self.List_WorkBenchIcons.append(item)
            # Load the lists for the deserialized icons
            for IconItem in Data["Command_Icons"]:
                Icon: QIcon = Serialize_Ribbon.deserializeIcon(IconItem[1])
                item = [IconItem[0], Icon]
                self.List_CommandIcons.append(item)
        except Exception as e:
            StandardFunctions.Print(f"{e.with_traceback(e.__traceback__)}", "Warning")
            pass

        # check if the list with workbenches is up-to-date
        missingWB = []
        for WorkBenchName in Gui.listWorkbenches():
            for j in range(len(self.List_Workbenches)):
                if (
                    WorkBenchName == self.List_Workbenches[j][0]
                    or WorkBenchName == "NoneWorkbench"
                ):
                    break
                if j == len(self.List_Workbenches) - 1:
                    missingWB.append(WorkBenchName)
        if len(missingWB) > 0:
            ListWB = "  "
            for WB in missingWB:
                ListWB = ListWB + WB + "\n" + "  "
            Question = translate(
                "FreeCAD Ribbon",
                "The following workbenches were installed after the last data update: \n"
                "{}\n\n"
                "Do you want to update the data?\n"
                "This can take a while!",
            ).format(ListWB)
            Answer = StandardFunctions.Mbox(Question, "FreeCAD Ribbon", 1, "Question")
            if Answer == "yes":
                CacheFunctions.CreateCache()

        # Add dropdownbuttons to the list of commands
        try:
            for DropDownCommand, Commands in self.Dict_DropDownButtons[
                "dropdownButtons"
            ].items():
                if isinstance(Commands, list):
                    CommandName = Commands[0][0]
                    IconName = ""
                    for CommandItem in self.List_Commands:
                        if CommandItem[0] == CommandName:
                            IconName = StandardFunctions.CommandInfoCorrections(
                                CommandItem[1]
                            )["pixmap"]
                    self.List_Commands.append(
                        [
                            DropDownCommand,
                            IconName,
                            DropDownCommand.split("_")[0],
                            "General",
                            DropDownCommand.split("_")[0],
                        ]
                    )
                else:
                    del self.Dict_DropDownButtons["dropdownButtons"]
                    StandardFunctions.Print(
                        "dropdownbuttons have wrong format. Please create them again!",
                        "Warning",
                    )
        except Exception as e:
            if Parameters.DEBUG_MODE is True:
                StandardFunctions.Print(
                    f"{e.with_traceback(e.__traceback__)}", "Warning"
                )
            pass

        # add commands from newpanels to the list of commands
        try:
            for NewPanelWorkBench in self.Dict_NewPanels["newPanels"]:
                for NewPanel in self.Dict_NewPanels["newPanels"][NewPanelWorkBench]:
                    for NewPanelCommand in self.Dict_NewPanels["newPanels"][
                        NewPanelWorkBench
                    ][NewPanel]:
                        # get the icon for this command
                        if CommandInfoCorrections(NewPanelCommand[0])["pixmap"] != "":
                            IconName = CommandInfoCorrections(NewPanelCommand[0])[
                                "pixmap"
                            ]
                        else:
                            IconName = ""
                        MenuName = CommandInfoCorrections(NewPanelCommand[0])[
                            "menuText"
                        ].replace("&", "")
                        MenuNameTranslated = CommandInfoCorrections(NewPanelCommand[0])[
                            "ActionText"
                        ].replace("&", "")
                        self.List_Commands.append(
                            [
                                NewPanelCommand[0],
                                IconName,
                                MenuName,
                                NewPanelWorkBench,
                                MenuNameTranslated,
                            ]
                        )
        except Exception:
            pass
        # endregion

        # Add the workbenches
        self.addWorkbenches()
        
        # Load the commands
        self.LoadCommands()
        
        # Connect the filter for the quick commands on the quickcommands tab
        def FilterWorkbench_NP():
            self.on_ListCategory_NP_TextChanged()

        # Connect the filter for the quick commands on the quickcommands tab
        self.form.ListCategory_NP.currentTextChanged.connect(FilterWorkbench_NP)
        # Connect the searchbar for the quick commands on the quick commands tab
        self.form.SearchBar_NP.textChanged.connect(
            self.on_SearchBar_NP_TextChanged
        )
        
        # Connect the "CreateNewPanel" button
        self.form.CreateNewPanel.clicked.connect(self.on_CreateNewPanel_clicked)
        
        # Connect the reload button
        self.form.LoadWB.connect(
            self.form.LoadWB, SIGNAL("clicked()"), self.on_ReloadWB_clicked
        )
        # Set the icon and size for the refresh button
        self.form.LoadWB.heightForWidth(1)
        self.form.LoadWB.setIcon(Gui.getIcon("view-refresh"))
        self.form.LoadWB.setIconSize(QSize(20, 20))
        # Create the a message to indicate when the last time the data was (re)created.
        TimeStamp = Parameters_Ribbon.Settings.GetStringSetting("ReloadTimeStamp")
        date_format = "%B %d, %Y, %H:%M:%S"
        lastDate = datetime.strptime(TimeStamp, date_format)
        deltaDate: timedelta = datetime.now()-lastDate
        deltaDict = StandardFunctions.TimeDeltaToDict(deltaDate)
        # Get the separate values
        delta_days = deltaDict['days']
        delta_hours = deltaDict['hours']
        delta_minutes= deltaDict['minutes']
        # Set the message        
        if TimeStamp == "" or TimeStamp is None:
            TimeStamp = "-"
        self.form.TimeStamp_Reloaded.setText(
            translate("FreeCAD Ribbon", f"Last reloaded on: {TimeStamp}. This is {delta_days} days, {delta_hours} hour(s) and {delta_minutes} minutes ago.")
        )
        
        # Connect the OK and Cancel buttons
        self.form.cancelButton.clicked.connect(self.on_Cancel_Clicked)
        self.form.okButton.clicked.connect(self.on_Ok_Clicked)

        # Restore the cursor
        QApplication.restoreOverrideCursor()
        return        
        
    def addWorkbenches(self):
        ShadowList = []  # List to add the commands and prevent duplicates

        # Fill the Workbenches available, selected and workbench list
        self.form.ListCategory_NP.clear()
        # self.form.ListCategory_DDB.clear()

        # Add "All" to the categoryListWidgets
        All_KeyWord = translate("FreeCAD Ribbon", "All")
        self.form.ListCategory_NP.addItem(All_KeyWord, "All")
        # self.form.ListCategory_DDB.addItem(All_KeyWord, "All")
        
        # Add "Standard" to the list for the panels
        Standard_KeyWord = translate("FreeCAD Ribbon", "Standard")
        self.form.ListCategory_NP.addItem(Gui.getIcon("freecad"), Standard_KeyWord)
        # self.form.ListCategory_DDB.addItem(Gui.getIcon("freecad"), Standard_KeyWord)

        self.List_Workbenches.sort()

        WorkbenchName =""
        for workbench in self.List_Workbenches:
            WorkbenchName = workbench[0]
            WorkbenchTitle = workbench[2]

            if [WorkbenchName, WorkbenchTitle] not in ShadowList:
                 # Get the translate worbench title
                if len(workbench) == 5:
                    WorkbenchTitle = workbench[4]
                else:
                    WorkbenchTitle = workbench[2]

                # Define a new ListWidgetItem.
                Icon = QIcon()
                for item in self.List_WorkBenchIcons:
                    if item[0] == WorkbenchName:
                        Icon = item[1]
                if Icon is None:
                    Icon = Gui.getIcon(workbench[1])

                # Add the ListWidgetItem also to the categoryListWidgets
                self.form.ListCategory_NP.addItem(
                    Icon,
                    WorkbenchTitle,
                    workbench,
                )
                # self.form.ListCategory_DDB.addItem(
                #     Icon,
                #     WorkbenchTitle,
                #     workbench,
                # )

            ShadowList.append([WorkbenchName, WorkbenchTitle])

        self.form.ListCategory_NP.setCurrentText(All_KeyWord)
        # self.form.ListCategory_DDB.setCurrentText(All_KeyWord)

        return    
    
    
    def LoadCommands(self):
        """Fill the Quick Commands Available and Selected"""
        self.form.CommandsAvailable_NP.clear()
        # self.form.CommandList_DDB.clear()

        ShadowList = []  # List to add the commands and prevent duplicates

        for CommandItem in self.List_Commands:
            CommandName = CommandItem[0]
            MenuNameTranslated = CommandItem[2].replace("&", "")  # Not translated
            if len(CommandItem) == 5:
                MenuNameTranslated = CommandItem[4].replace("&", "")  # Translated
            # Remove numbers from dropdown child commands
            if MenuNameTranslated.split(" ")[0].isdigit() is True:
                MenuNameTranslated = MenuNameTranslated.split(" ")[1]
            # Remove any suffix frp, the menuname
            if CommandName.endswith("_ddb"):
                MenuNameTranslated = CommandName.replace("_ddb", "")

            if MenuNameTranslated != "":
                if CommandName not in ShadowList:
                    Icon = QIcon()
                    FreeCAD_Icons = os.path.abspath(os.path.join(os.path.dirname(__file__), "Resources", "FreeCAD Icons"))
                    for root, dirs, files in os.walk(FreeCAD_Icons):
                        for fileName in files:
                            if CommandName.lower() in fileName.lower() or (fileName.lower().split(".")[0] in CommandName.lower()):
                                Icon = QIcon()
                                Icon.addPixmap(QPixmap(os.path.join(root, fileName)))
                    if Icon.isNull():
                        for item in self.List_CommandIcons:
                            if item[0] == CommandName:
                                Icon = item[1]
                            if (
                                str(CommandName).endswith("_ddb")
                                and "dropdownButtons" in self.Dict_DropDownButtons
                            ):
                                for (
                                    DropDownCommand,
                                    Commands,
                                ) in self.Dict_DropDownButtons["dropdownButtons"].items():
                                    if Commands[0][0] == item[0]:
                                        Icon = item[1]
                    if Icon.isNull():
                        IconName = StandardFunctions.CommandInfoCorrections(CommandName)["pixmap"]
                        Icon = StandardFunctions.returnQiCons_Commands(CommandName, IconName)
                        if (
                            str(CommandName).endswith("_ddb")
                            and "dropdownButtons" in self.Dict_DropDownButtons
                        ):
                            for (
                                DropDownCommand,
                                Commands,
                            ) in self.Dict_DropDownButtons["dropdownButtons"].items():
                                if Commands[0][0] == CommandName:
                                    IconName = CommandItem[1]
                                    Icon = StandardFunctions.returnQiCons_Commands(
                                        CommandName, IconName
                                    )

                    Text = MenuNameTranslated
                    ListWidgetItem = QListWidgetItem()
                    ListWidgetItem.setText(Text)
                    ListWidgetItem.setData(Qt.ItemDataRole.UserRole, CommandName)
                    
                    # Check if there is an Icon. if not add a replacement
                    if CommandName != "Std_OnlineHelp":
                        result = StandardFunctions.CompareIcons(QIcon, Icon)
                        if result is True:
                            Icon = Gui.getIcon("preferences-workbenches")
                            ListWidgetItem.setIcon(Icon)
                    
                    if Icon is not None and Icon.isNull() is False:
                        ListWidgetItem.setIcon(Icon)
                        ListWidgetItem.setToolTip(
                            CommandName
                        )  # Use the tooltip to store the actual command.

                        # Add the ListWidgetItem to the correct ListWidget
                        #
                        # HasIcon = True
                        # if StandardFunctions.CommandInfoCorrections(CommandName)["pixmap"] != "":
                        #     HasIcon = True
                        # if len(CommandName.split(",")) > 1:
                        #     HasIcon = True
                        # if Icon is not None and Icon.isNull() is False and HasIcon:
                        # Add clones of the listWidgetItem to the other listwidgets
                        self.form.CommandsAvailable_NP.addItem(ListWidgetItem)
                        # self.form.CommandsAvailable_DDB.addItem(ListWidgetItem.clone())

                        # # If there are any dropdown buttons in the json file, add them to the dropdown list
                        # if (
                        #     str(CommandName).endswith("_ddb")
                        #     and "dropdownButtons" in self.Dict_DropDownButtons
                        # ):
                        #     self.form.CommandList_DDB.addItem(
                        #         CommandName.replace("_ddb", "")
                        #     )

                        ShadowList.append(CommandName)

        # # Add a "new" item to the dropdown list
        # self.form.CommandList_DDB.addItem(translate("FreeCAD Ribbon", "New"), "new")
        # self.form.CommandList_DDB.setCurrentText(translate("FreeCAD Ribbon", "New"))
        return

    # region - Add commands
    def on_ListCategory_NP_TextChanged(self):
        self.FilterCommands_ListCategory(
            self.form.CommandsAvailable_NP,
            self.form.ListCategory_NP,
            self.form.SearchBar_NP,
        )
        return


    def on_SearchBar_NP_TextChanged(self):
        self.FilterCommands_SearchBar(
            self.form.CommandsAvailable_NP,
            self.form.SearchBar_NP,
            self.form.ListCategory_NP,
        )
        return


    def FilterCommands_SearchBar(
        self,
        ListWidget_Commands: QListWidget,
        SearchBar: QLineEdit,
        ListWidget_WorkBenches: QListWidget,
    ):
        # Get the text in the searchbar as lower case. (This makes it not sensitive for Upper or lower cases)
        SearchbarText = SearchBar.text().lower()

        # Clear the listwidget
        ListWidget_Commands.clear()

        ShadowList = []  # List to add the commands and prevent duplicates
        for ToolbarCommand in self.List_Commands:
            CommandName = ToolbarCommand[0]
            workbenchName = ToolbarCommand[3]
            MenuNameTranslated = ToolbarCommand[2].replace("&", "")  # Not translated
            if len(ToolbarCommand) == 5:
                MenuNameTranslated = ToolbarCommand[4].replace("&", "")  # Translated
            # Remove numbers from dropdown child commands
            if MenuNameTranslated.split(" ")[0].isdigit() is True:
                MenuNameTranslated = MenuNameTranslated.split(" ")[1]
            # Remove any suffix frp, the menuname
            if CommandName.endswith("_ddb"):
                MenuNameTranslated = CommandName.replace("_ddb", "")

            if MenuNameTranslated != "":
                if (
                    SearchbarText != ""
                    and MenuNameTranslated.lower().startswith(SearchbarText)
                ) or SearchbarText == "":                    
                    if CommandName not in ShadowList:
                        try:
                            if (
                                workbenchName != "Global"
                                and workbenchName != "General"
                                and workbenchName != "Standard"
                                and workbenchName != "All"
                                and workbenchName != ""
                            ):
                                WorkbenchTitle = Gui.getWorkbench(
                                    workbenchName
                                ).MenuText
                            else:
                                WorkbenchTitle = workbenchName
                        except Exception:
                            return
                        try:
                            if (
                                ListWidget_WorkBenches is not None and
                                WorkbenchTitle
                                == ListWidget_WorkBenches.currentData(
                                    Qt.ItemDataRole.UserRole
                                )[2]
                                or ListWidget_WorkBenches.currentText() == "All"
                            ):
                                # Define a new ListWidgetItem.
                                Icon = QIcon()
                                FreeCAD_Icons = os.path.abspath(os.path.join(os.path.dirname(__file__), "Resources", "FreeCAD Icons"))
                                for root, dirs, files in os.walk(FreeCAD_Icons):
                                    for fileName in files:
                                        if CommandName.lower() in fileName.lower() or (fileName.lower().split(".")[0] in CommandName.lower()):
                                            Icon = QIcon()
                                            Icon.addPixmap(QPixmap(os.path.join(root, fileName)))
                                if Icon.isNull():
                                    for item in self.List_CommandIcons:
                                        if item[0] == CommandName:
                                            Icon = item[1]
                                        if (
                                            str(CommandName).endswith("_ddb")
                                            and "dropdownButtons" in self.Dict_DropDownButtons
                                        ):
                                            for (
                                                DropDownCommand,
                                                Commands,
                                            ) in self.Dict_DropDownButtons[
                                                "dropdownButtons"
                                            ].items():
                                                if Commands[0][0] == item[0]:
                                                    Icon = item[1]
                                if Icon.isNull():
                                    IconName = StandardFunctions.CommandInfoCorrections(
                                        CommandName
                                    )["pixmap"]
                                    Icon = StandardFunctions.returnQiCons_Commands(CommandName, IconName)
                                    if (
                                        str(CommandName).endswith("_ddb")
                                        and "dropdownButtons" in self.Dict_DropDownButtons
                                    ):
                                        for (
                                            DropDownCommand,
                                            Commands,
                                        ) in self.Dict_DropDownButtons[
                                            "dropdownButtons"
                                        ].items():
                                            if Commands[0][0] == CommandName:
                                                IconName = ToolbarCommand[1]
                                                Icon = StandardFunctions.returnQiCons_Commands(
                                                    CommandName, IconName
                                    )

                                # Define a new ListWidgetItem.
                                ListWidgetItem = QListWidgetItem()
                                ListWidgetItem.setText(MenuNameTranslated)
                                ListWidgetItem.setData(
                                    Qt.ItemDataRole.UserRole, CommandName
                                )
                                
                                # Check if there is an Icon. if not add a replacement
                                if CommandName != "Std_OnlineHelp":
                                    result = StandardFunctions.CompareIcons(QIcon, Icon)
                                    if result is True:
                                        Icon = Gui.getIcon("preferences-workbenches")
                                        ListWidgetItem.setIcon(Icon)

                                        if Icon is not None and Icon.isNull() is False:
                                            ListWidgetItem.setIcon(Icon)
                                            ListWidgetItem.setToolTip(
                                                CommandName
                                            )

                                    ListWidget_Commands.addItem(ListWidgetItem)
                                    # Add the commandName to the shadowList
                                    ShadowList.append(CommandName)
                                    
                                if Icon.isNull() or Icon is None:
                                    if Parameters.DEBUG_MODE is True:
                                        StandardFunctions.Print(
                                            f"{CommandName} has no icon!", "Warning"
                                        )
                                    
                        except Exception:
                            continue            

        return


    def FilterCommands_ListCategory(
        self,
        ListWidget_Commands: QListWidget,
        ListWidget_WorkBenches: QListWidget,
        SearchBar: QLineEdit,
    ):
        if (
            ListWidget_WorkBenches.currentData(Qt.ItemDataRole.UserRole) is None
            and ListWidget_WorkBenches.currentText() != "All"
            and ListWidget_WorkBenches.currentText() != "Standard"
        ):
            return

        # Get the text in the searchbar as lower case. (This makes it not sensitive for Upper or lower cases)
        SearchbarText = SearchBar.text().lower()

        # Clear the listwidget
        ListWidget_Commands.clear()

        ShadowList = []  # List to add the commands and prevent duplicates
        for ToolbarCommand in self.List_Commands:
            CommandName = ToolbarCommand[0]
            workbenchName = ToolbarCommand[3]
            MenuNameTranslated = ToolbarCommand[2].replace("&", "")  # Not transleted!
            if len(ToolbarCommand) == 5:
                MenuNameTranslated = ToolbarCommand[4].replace("&", "")  # Translated
            # Remove numbers from dropdown child commands
            if MenuNameTranslated.split(" ")[0].isdigit() is True:
                MenuNameTranslated = MenuNameTranslated.split(" ")[1]
            # Remove any suffix frp, the menuname
            if CommandName.endswith("_ddb"):
                MenuNameTranslated = CommandName.replace("_ddb", "")

            if MenuNameTranslated != "":
                if (
                    SearchbarText != ""
                    and MenuNameTranslated.lower().startswith(SearchbarText)
                ) or SearchbarText == "":
                    if (
                        ListWidget_WorkBenches.currentData(Qt.ItemDataRole.UserRole)
                        != "All"
                    ):
                        if (
                            CommandName not in ShadowList
                            and workbenchName != "Global"
                            and workbenchName != "General"
                            and workbenchName != "Standard"
                            and workbenchName != ""
                        ):
                            try:
                                WorkbenchTitle = Gui.getWorkbench(
                                    workbenchName
                                ).MenuText
                            except Exception:
                                return
                            if (
                                ListWidget_WorkBenches.currentData(
                                    Qt.ItemDataRole.UserRole
                                ) is not None and
                                WorkbenchTitle
                                == ListWidget_WorkBenches.currentData(
                                    Qt.ItemDataRole.UserRole
                                )[2]
                            ):
                                # Define a new ListWidgetItem.
                                Icon = QIcon()
                                FreeCAD_Icons = os.path.abspath(os.path.join(os.path.dirname(__file__), "Resources", "FreeCAD Icons"))
                                for root, dirs, files in os.walk(FreeCAD_Icons):
                                    for fileName in files:
                                        if CommandName.lower() in fileName.lower() or (fileName.lower().split(".")[0] in CommandName.lower()):
                                            Icon = QIcon()
                                            Icon.addPixmap(QPixmap(os.path.join(root, fileName)))
                                if Icon.isNull():
                                    for item in self.List_CommandIcons:
                                        if item[0] == CommandName:
                                            Icon = item[1]
                                        if (
                                            str(CommandName).endswith("_ddb")
                                            and "dropdownButtons" in self.Dict_DropDownButtons
                                        ):
                                            for (
                                                DropDownCommand,
                                                Commands,
                                            ) in self.Dict_DropDownButtons[
                                                "dropdownButtons"
                                            ].items():
                                                if Commands[0][0] == item[0]:
                                                    Icon = item[1]
                                if Icon.isNull():
                                    IconName = StandardFunctions.CommandInfoCorrections(
                                        CommandName
                                    )["pixmap"]
                                    Icon = StandardFunctions.returnQiCons_Commands(CommandName, IconName)
                                    if (
                                        str(CommandName).endswith("_ddb")
                                        and "dropdownButtons" in self.Dict_DropDownButtons
                                    ):
                                        for (
                                            DropDownCommand,
                                            Commands,
                                        ) in self.Dict_DropDownButtons[
                                            "dropdownButtons"
                                        ].items():
                                            if Commands[0][0] == CommandName:
                                                IconName = ToolbarCommand[1]
                                                Icon = StandardFunctions.returnQiCons_Commands(
                                                    CommandName, IconName
                                    )

                                Text = MenuNameTranslated
                                ListWidgetItem = QListWidgetItem()
                                ListWidgetItem.setText(Text)
                                ListWidgetItem.setData(
                                    Qt.ItemDataRole.UserRole, CommandName
                                )
                                
                                # Check if there is an Icon. if not add a replacement
                                if CommandName != "Std_OnlineHelp":
                                    result = StandardFunctions.CompareIcons(QIcon, Icon)
                                    if result is True:
                                        Icon = Gui.getIcon("preferences-workbenches")
                                        ListWidgetItem.setIcon(Icon)

                                if Icon is not None and Icon.isNull() is False:
                                    ListWidgetItem.setIcon(Icon)
                                    ListWidgetItem.setToolTip(
                                        CommandName
                                    )  # Use the tooltip to store the actual command.

                                    # Add the ListWidgetItem to the correct ListWidget
                                    ListWidget_Commands.addItem(ListWidgetItem)

                                    # Add the commandname to the shadow list
                                    ShadowList.append(CommandName)
                    if (
                        workbenchName == "Standard" and
                        ListWidget_WorkBenches.currentText() == "Standard"
                    ):                        
                        # Define a commandname for the icon
                        Icon = QIcon()
                        FreeCAD_Icons = os.path.abspath(os.path.join(os.path.dirname(__file__), "Resources", "FreeCAD Icons"))
                        for root, dirs, files in os.walk(FreeCAD_Icons):
                            for fileName in files:
                                if CommandName.lower() in fileName.lower() or (fileName.lower().split(".")[0] in CommandName.lower()):
                                    Icon = QIcon()
                                    Icon.addPixmap(QPixmap(os.path.join(root, fileName)))
                        if Icon.isNull():
                            for item in self.List_CommandIcons:
                                if item[0] == CommandName:
                                    Icon = item[1]
                                if (
                                    str(CommandName).endswith("_ddb")
                                    and "dropdownButtons" in self.Dict_DropDownButtons
                                ):
                                    for (
                                        DropDownCommand,
                                        Commands,
                                    ) in self.Dict_DropDownButtons[
                                        "dropdownButtons"
                                    ].items():
                                        if Commands[0][0] == item[0]:
                                            Icon = item[1]
                        if Icon.isNull():
                            IconName = StandardFunctions.CommandInfoCorrections(
                                CommandName
                            )["pixmap"]
                            Icon = StandardFunctions.returnQiCons_Commands(CommandName, IconName)
                            if (
                                str(CommandName).endswith("_ddb")
                                and "dropdownButtons" in self.Dict_DropDownButtons
                            ):
                                for (
                                    DropDownCommand,
                                    Commands,
                                ) in self.Dict_DropDownButtons[
                                    "dropdownButtons"
                                ].items():
                                    if Commands[0][0] == CommandName:
                                        IconName = ToolbarCommand[1]
                                        Icon = StandardFunctions.returnQiCons_Commands(
                                            CommandName, IconName
                            )
                                                
                        Text = MenuNameTranslated
                        ListWidgetItem = QListWidgetItem()
                        ListWidgetItem.setText(Text)
                        ListWidgetItem.setData(
                            Qt.ItemDataRole.UserRole, CommandName
                        )
                        if Icon is not None:
                            ListWidgetItem.setIcon(Icon)
                        ListWidgetItem.setToolTip(
                            CommandName
                        )  # Use the tooltip to store the actual command.

                        # Check if there is an Icon. if not add a replacement
                        if CommandName != "Std_OnlineHelp":
                            result = StandardFunctions.CompareIcons(QIcon, Icon)
                            if result is True:
                                Icon = Gui.getIcon("preferences-workbenches")
                                ListWidgetItem.setIcon(Icon)
                        
                        if Icon is not None and Icon.isNull() is False:
                            ListWidget_Commands.addItem(ListWidgetItem)
                            ShadowList.append(CommandName)

                    if (
                        ListWidget_WorkBenches.currentData(Qt.ItemDataRole.UserRole)
                        == "All"
                    ):
                        # Define a new ListWidgetItem.
                        Icon = QIcon()
                        FreeCAD_Icons = os.path.abspath(os.path.join(os.path.dirname(__file__), "Resources", "FreeCAD Icons"))
                        for root, dirs, files in os.walk(FreeCAD_Icons):
                            for fileName in files:
                                if CommandName.lower() in fileName.lower() or (fileName.lower().split(".")[0] in CommandName.lower()):
                                    Icon = QIcon()
                                    Icon.addPixmap(QPixmap(os.path.join(root, fileName)))
                        if Icon.isNull():
                            for item in self.List_CommandIcons:
                                if item[0] == CommandName:
                                    Icon = item[1]
                                if (
                                    str(CommandName).endswith("_ddb")
                                    and "dropdownButtons" in self.Dict_DropDownButtons
                                ):
                                    for (
                                        DropDownCommand,
                                        Commands,
                                    ) in self.Dict_DropDownButtons[
                                        "dropdownButtons"
                                    ].items():
                                        if Commands[0][0] == item[0]:
                                            Icon = item[1]
                        if Icon.isNull():
                            IconName = StandardFunctions.CommandInfoCorrections(
                                CommandName
                            )["pixmap"]
                            Icon = StandardFunctions.returnQiCons_Commands(CommandName, IconName)
                            if (
                                str(CommandName).endswith("_ddb")
                                and "dropdownButtons" in self.Dict_DropDownButtons
                            ):
                                for (
                                    DropDownCommand,
                                    Commands,
                                ) in self.Dict_DropDownButtons[
                                    "dropdownButtons"
                                ].items():
                                    if Commands[0][0] == CommandName:
                                        IconName = ToolbarCommand[1]
                                        Icon = StandardFunctions.returnQiCons_Commands(
                                            CommandName, IconName
                            )

                        Text = MenuNameTranslated
                        ListWidgetItem = QListWidgetItem()
                        ListWidgetItem.setText(Text)
                        ListWidgetItem.setData(
                            Qt.ItemDataRole.UserRole, CommandName
                        )
                        
                        # Check if there is an Icon. if not add a replacement
                        if CommandName != "Std_OnlineHelp":
                            result = StandardFunctions.CompareIcons(QIcon, Icon)
                            if result is True:
                                Icon = Gui.getIcon("preferences-workbenches")
                                ListWidgetItem.setIcon(Icon)
                        
                        if Icon is not None and Icon.isNull() is False:
                            ListWidgetItem.setIcon(Icon)
                            ListWidgetItem.setToolTip(
                                CommandName
                            )  # Use the tooltip to store the actual command.

                            # Add the ListWidgetItem to the correct ListWidget
                            ListWidget_Commands.addItem(ListWidgetItem)                                
                            ShadowList.append(CommandName)
        return

    def on_CreateNewPanel_clicked(self):
        if self.form.PanelTitle.text() != "":
            RibbonBar: FCBinding.ModernMenu = mw.findChild(FCBinding.ModernMenu, "Ribbon")
            RibbonBar.CreateNewPanel(self.form.PanelTitle.text())
        return
    # endregion
    
    # region - Form controls
    def on_Cancel_Clicked(self):
        RibbonBar: FCBinding.ModernMenu = mw.findChild(FCBinding.ModernMenu, "Ribbon")        
        RibbonBar.on_Cancel_Clicked()
        
    def on_Ok_Clicked(self):
        RibbonBar: FCBinding.ModernMenu = mw.findChild(FCBinding.ModernMenu, "Ribbon")        
        RibbonBar.on_Ok_Clicked()
        
    def on_ReloadWB_clicked(self, resetTexts=False, RestartFreeCAD=False):
        # minimize the dialog
        self.form.hide()
        
        # Create the data file
        CacheFunctions.CreateCache(resetTexts=resetTexts)

        # if RestartFreeCAD is False:
        #     # Show the dialog again
        #     self.closeSignal.emit()
        if RestartFreeCAD is True:
            result = StandardFunctions.RestartDialog(includeIcons=True)
            if result == "yes":
                StandardFunctions.restart_freecad()
            # else:
            #     self.closeSignal.emit()
        # show the dialog
        self.form.show()
        return
    # endregion
    
    def ReadJson(self, Section="All", JsonFile=""):
        # Open the JsonFile and load the data
        try:
            if JsonFile != "":
                JsonFile = open(JsonFile)
            else:
                JsonFile = open(Parameters.RIBBON_STRUCTURE_JSON)
        except Exception:
            JsonFile = open(Parameters.RIBBON_STRUCTURE_JSON)
        data = json.load(JsonFile)

        # # Get all the ignored toolbars
        # if Section == "ignoredToolbars" or Section == "All":
        #     for IgnoredToolbar in data["ignoredToolbars"]:
        #         self.List_IgnoredToolbars.append(IgnoredToolbar)

        # # Get all the icon only toolbars
        # if Section == "iconOnlyToolbars" or Section == "All":
        #     for IconOnly_Toolbar in data["iconOnlyToolbars"]:
        #         self.List_IconOnly_Toolbars.append(IconOnly_Toolbar)

        # # Get all the quick access command
        # if Section == "quickAccessCommands" or Section == "All":
        #     for QuickAccessCommand in data["quickAccessCommands"]:
        #         self.List_QuickAccessCommands.append(QuickAccessCommand)

        # # Get all the ignored workbenches
        # if Section == "ignoredWorkbenches" or Section == "All":
        #     for IgnoredWorkbench in data["ignoredWorkbenches"]:
        #         self.List_IgnoredWorkbenches.append(IgnoredWorkbench)

        # # Get all the custom toolbars
        # if Section == "customToolbars" or Section == "All":
        #     try:
        #         self.Dict_CustomToolbars["customToolbars"] = data["customToolbars"]
        #     except Exception:
        #         pass

        # Get all the dropdown buttons
        if Section == "dropdownButtons" or Section == "All":
            try:
                self.Dict_DropDownButtons["dropdownButtons"] = data["dropdownButtons"]
            except Exception:
                pass

        # Get all the new toolbars
        if Section == "newPanels" or Section == "All":
            try:
                self.Dict_NewPanels["newPanels"] = data["newPanels"]
            except Exception:
                pass

        # # Get the dict with the customized date for the buttons
        # if Section == "workbenches" or Section == "All":
        #     try:
        #         self.Dict_RibbonCommandPanel["workbenches"] = data["workbenches"]
        #     except Exception:
        #         pass

        JsonFile.close()
        return
    
def main():
    # Get the form
    Dialog = LoadDialog().form
    # Show the form
    Dialog.show()

class EventInspector(QObject):
    dragEntered = False
    widget = None
    pos = None
    
    def __init__(self, parent):
        super(EventInspector, self).__init__(parent)

    def eventFilter(self, obj, event: QEvent):
        if self.dragEntered is True and QApplication.mouseButtons().value == 0:
            count = 0
            parent = None
            panel = None
            if self.widget is not None:
                parent = self.widget.parent()
                while (count < 10):
                    if type(parent) is RibbonPanel:
                        panel = parent
                        break
                    # if type(parent) is CustomControls:
                    #     self.widget = parent
                        # break
                    else:
                        if parent is not None:
                            parent = parent.parent()
                    count = count + 1
                   
            # Get the mainwindow, the ribbon and the title
            mw = Gui.getMainWindow()
            RibbonBar: FCBinding.ModernMenu = mw.findChild(FCBinding.ModernMenu, "Ribbon")
            if type(self.widget) is not QuickAccessToolButton:
                if panel is not None:
                    RibbonBar.RemoveButtonFromPanel(panel, self.widget)                    
            if type(self.widget) is QuickAccessToolButton:
                RibbonBar.RemoveButtonFromQuickAccess(self.widget, self.pos)
            self.dragEntered = False
            # return True
        # # Show the mainwindow after the application is activated
        if event.type() == QEvent.Type.DragEnter:
            self.dragEntered = True
            self.widget = event.source()
            # self.widget = self.widget.parent()
            self.pos= event.source().pos()
            event.accept()
        if event.type() == QEvent.Type.DragLeave:
            if self.widget is not None:
                self.widget = None
                self.pos = None
                self.dragEntered = False
        return False
  