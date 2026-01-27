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

from PySide6.QtCore import Qt, SIGNAL, Signal, QObject, QThread, QSize, QEvent
from PySide6.QtWidgets import (
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
from PySide6.QtGui import QIcon, QPixmap
import sys
import json

import Standard_Functions_Ribbon as StandardFunctions
from Standard_Functions_Ribbon import CommandInfoCorrections
import Parameters_Ribbon
import Serialize_Ribbon
import CacheFunctions

# Get the resources
ConfigDirectory = Parameters_Ribbon.CONFIG_DIR
pathIcons = Parameters_Ribbon.ICON_LOCATION
pathStylSheets = Parameters_Ribbon.STYLESHEET_LOCATION
pathUI = Parameters_Ribbon.UI_LOCATION
pathScripts = os.path.join(ConfigDirectory, "Scripts")
pathPackages = os.path.join(os.path.dirname(__file__), "Resources", "packages")
pathBackup = Parameters_Ribbon.BACKUP_LOCATION
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


class LoadDialog(AddCommands_ui.Ui_Form):
    # Create a list for the commands
    List_Commands = []
    # Create a dict for the dropdownbuttons and newPanels
    Dict_DropDownButtons = {}
    Dict_NewPanels = {}
    # Create the lists for the deserialized icons
    List_CommandIcons = []
    List_WorkBenchIcons = []
            
    def __init__(self):

        # Makes "self.on_CreateBOM_clicked" listen to the changed control values instead initial values
        super(LoadDialog, self).__init__()

        # Get the main window from FreeCAD
        mw = Gui.getMainWindow()

        # # this will create a Qt widget from our ui file
        self.form = Gui.PySideUic.loadUi(os.path.join(pathUI, "AddCommands.ui"))
        
        # Install an event filter to catch events from the main window and act on it.
        self.form.installEventFilter(EventInspector(self.form))

        # Get the address of the repository address
        PackageXML = os.path.join(os.path.dirname(__file__), "package.xml")
        self.ReproAdress = StandardFunctions.ReturnXML_Value(
            PackageXML, "url", "type", "repository"
        )

        # Make sure that the dialog stays on top
        self.form.raise_()
        self.form.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)
        # self.form.setWindowFlags(Qt.WindowType.Tool)
        # self.form.setWindowModality(Qt.WindowModality.WindowModal)

        # Position the dialog in front of FreeCAD
        centerPoint = mw.geometry().center()
        Rectangle = self.form.frameGeometry()
        Rectangle.moveCenter(centerPoint)
        self.form.move(Rectangle.topLeft())
        
        # Add drag event to listwidget
        self.form.CommandsAvailable_NP.dragEnterEvent =  lambda e: self.dragEnterEvent_ListWidget(e, self.form.CommandsAvailable_NP)
        self.form.CommandsAvailable_NP.dragMoveEvent =  lambda e: self.dragMoveEvent_ListWidget(e, self.form.CommandsAvailable_NP)
        
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
            if Parameters_Ribbon.DEBUG_MODE is True:
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
    
    
    def dragEnterEvent_ListWidget(self, event, ListWidget):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            super(ListWidget, self).dragEnterEvent(event)

    def dragMoveEvent_ListWidget(self, event, ListWidget):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.DropAction.CopyAction)
            event.accept()
        else:
            super(ListWidget, self).dragMoveEvent(event)
        
        
    def addWorkbenches(self):
        ShadowList = []  # List to add the commands and prevent duplicates

        # Fill the Workbenches available, selected and workbench list
        self.form.ListCategory_NP.clear()
        # self.form.ListCategory_DDB.clear()

        # Add "All" to the categoryListWidgets
        All_KeyWord = translate("FreeCAD Ribbon", "All")
        self.form.ListCategory_NP.addItem(All_KeyWord, "All")
        # self.form.ListCategory_DDB.addItem(All_KeyWord, "All")

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
            if CommandName.endswith("_ddb"):
                MenuNameTranslated = CommandName.replace("_ddb", "")

            if MenuNameTranslated != "":
                if f"{MenuNameTranslated}" not in ShadowList:
                    Icon = None
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
                    if Icon is None:
                        IconName = StandardFunctions.CommandInfoCorrections(
                            CommandName
                        )["pixmap"]
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
                    if Icon is not None:
                        ListWidgetItem.setIcon(Icon)
                        ListWidgetItem.setToolTip(
                            CommandName
                        )  # Use the tooltip to store the actual command.

                    # Add the ListWidgetItem to the correct ListWidget
                    #
                    # Default a command is not selected
                    if Icon is not None:
                        # Add clones of the listWidgetItem to the other listwidgets
                        self.form.CommandsAvailable_NP.addItem(ListWidgetItem.clone())
                        # self.form.CommandsAvailable_DDB.addItem(ListWidgetItem.clone())

                    # # If there are any dropdown buttons in the json file, add them to the dropdown list
                    # if (
                    #     str(CommandName).endswith("_ddb")
                    #     and "dropdownButtons" in self.Dict_DropDownButtons
                    # ):
                    #     self.form.CommandList_DDB.addItem(
                    #         CommandName.replace("_ddb", "")
                    #     )

            ShadowList.append(f"{MenuNameTranslated}")

        # # Add a "new" item to the dropdown list
        # self.form.CommandList_DDB.addItem(translate("FreeCAD Ribbon", "New"), "new")
        # self.form.CommandList_DDB.setCurrentText(translate("FreeCAD Ribbon", "New"))
        return


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
        ListWidget: QListWidget,
        SearchBar: QLineEdit,
        ListWidget_WorkBenches: QListWidget,
    ):
        # Get the text in the searchbar as lower case. (This makes it not sensitive for Upper or lower cases)
        SearchbarText = SearchBar.text().lower()

        # Clear the listwidget
        ListWidget.clear()

        ShadowList = []  # List to add the commands and prevent duplicates
        for ToolbarCommand in self.List_Commands:
            CommandName = ToolbarCommand[0]
            workbenchName = ToolbarCommand[3]
            MenuNameTranslated = ToolbarCommand[2].replace("&", "")  # Not translated
            if len(ToolbarCommand) == 5:
                MenuNameTranslated = ToolbarCommand[4].replace("&", "")  # Translated
            if CommandName.endswith("_ddb"):
                MenuNameTranslated = CommandName.replace("_ddb", "")

            if MenuNameTranslated != "":
                if (
                    SearchbarText != ""
                    and MenuNameTranslated.lower().startswith(SearchbarText)
                ) or SearchbarText == "":
                    if f"{MenuNameTranslated}" not in ShadowList:
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
                                # Get an icon
                                # Define a commandname for the icon
                                CommandName_Icon = CommandName
                                # If the command is a dropdown button, get the icon from the first command in the dropdown list
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
                                        if DropDownCommand == CommandName:
                                            CommandName_Icon = Commands[0][0]
                                # Get the icon name
                                IconName = StandardFunctions.CommandInfoCorrections(
                                    CommandName_Icon
                                )["pixmap"]
                                # get the icon for this command if there isn't one, leave it None
                                Icon = StandardFunctions.returnQiCons_Commands(
                                    CommandName_Icon, IconName
                                )
                                # If the icon is still None, get the icon from the iconlist
                                if Icon is None or (Icon is not None and Icon.isNull()):
                                    for item in self.List_CommandIcons:
                                        if item[0] == CommandName_Icon:
                                            Icon = item[1]
                                            break

                                # Define a new ListWidgetItem.
                                ListWidgetItem = QListWidgetItem()
                                ListWidgetItem.setText(MenuNameTranslated)
                                ListWidgetItem.setData(
                                    Qt.ItemDataRole.UserRole, CommandName
                                )
                                if Icon is not None:
                                    ListWidgetItem.setIcon(Icon)
                                    ListWidgetItem.setToolTip(
                                        CommandName
                                    )

                                    ListWidget.addItem(ListWidgetItem)
                                if Icon is None:
                                    if Parameters_Ribbon.DEBUG_MODE is True:
                                        StandardFunctions.Print(
                                            f"{CommandName} has no icon!", "Warning"
                                        )
                        except Exception:
                            continue
            ShadowList.append(f"{MenuNameTranslated}")

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
                            f"{MenuNameTranslated}" not in ShadowList
                            and workbenchName != "Global"
                            and workbenchName != "General"
                            and workbenchName != "Standard"
                            and workbenchName != "Standard"
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
                                # Get an icon
                                # Define a commandname for the icon
                                CommandName_Icon = CommandName
                                # If the command is a dropdown button, get the icon from the first command in the dropdown list
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
                                        if DropDownCommand == CommandName:
                                            CommandName_Icon = Commands[0][0]
                                # Get the icon name
                                IconName = StandardFunctions.CommandInfoCorrections(
                                    CommandName_Icon
                                )["pixmap"]
                                # get the icon for this command if there isn't one, leave it None
                                Icon = StandardFunctions.returnQiCons_Commands(
                                    CommandName_Icon, IconName
                                )
                                # If the icon is still None, get the icon from the iconlist
                                if Icon is None or (Icon is not None and Icon.isNull()):
                                    for item in self.List_CommandIcons:
                                        if item[0] == CommandName_Icon:
                                            Icon = item[1]
                                            break

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

                                # Add the ListWidgetItem to the correct ListWidget
                                if Icon is not None:
                                    ListWidget_Commands.addItem(ListWidgetItem)

                        ShadowList.append(f"{MenuNameTranslated}")
                    if (
                        f"{MenuNameTranslated}" not in ShadowList
                        and workbenchName == "Standard"
                    ):
                        WorkbenchTitle = workbenchName
                        if (
                            WorkbenchTitle
                            == ListWidget_WorkBenches.currentData(
                                Qt.ItemDataRole.UserRole
                            )[2]
                        ):
                            IsInlist = False
                            for i in range(ListWidget_Commands.count()):
                                CommandItem = ListWidget_Commands.item(i)
                                if (
                                    CommandItem.data(Qt.ItemDataRole.UserRole)
                                    == CommandName
                                ):
                                    IsInlist = True

                                if IsInlist is False:
                                    # Define a commandname for the icon
                                    CommandName_Icon = CommandName
                                    Icon = StandardFunctions.returnQiCons_Commands(
                                        CommandName_Icon
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

                                    # Add the ListWidgetItem to the correct ListWidget
                                    if Icon is not None:
                                        ListWidget_Commands.addItem(ListWidgetItem)

                    if (
                        ListWidget_WorkBenches.currentData(Qt.ItemDataRole.UserRole)
                        == "All"
                    ):
                        IsInlist = False
                        for i in range(ListWidget_Commands.count()):
                            CommandItem = ListWidget_Commands.item(i)
                            # if CommandItem.data(Qt.ItemDataRole.UserRole) == CommandName:
                            #     IsInlist = True
                            if CommandItem.text() == MenuNameTranslated:
                                IsInlist = True

                        if IsInlist is False:
                            # Define a new ListWidgetItem.
                            Icon = None
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
                            if Icon is None:
                                IconName = StandardFunctions.CommandInfoCorrections(
                                    CommandName
                                )["pixmap"]
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

                                # Add the ListWidgetItem to the correct ListWidget
                                ListWidget_Commands.addItem(ListWidgetItem)
        return


class EventInspector(QObject):
    form = None

    def __init__(self, parent):
        self.form = parent
        super(EventInspector, self).__init__(parent)

    def eventFilter(self, obj, event):
        import FCBinding

        # Show the mainwindow after the application is activated
        if event.type() == QEvent.Type.Close:
            # self.closeSignal.emit()
            mw = Gui.getMainWindow()
            RibbonBar: FCBinding.ModernMenu = mw.findChild(
                FCBinding.ModernMenu, "Ribbon"
            )
            self.EnableRibbonToolbarsAndMenus(RibbonBar=RibbonBar)
            return False

        if event.type() == QEvent.Type.WindowStateChange:
            # self.closeSignal.emit()
            mw = Gui.getMainWindow()
            if self.form.windowState() == Qt.WindowState.WindowMinimized:
                RibbonBar: FCBinding.ModernMenu = mw.findChild(
                    FCBinding.ModernMenu, "Ribbon"
                )
                self.EnableRibbonToolbarsAndMenus(RibbonBar=RibbonBar)
            else:
                RibbonBar: FCBinding.ModernMenu = mw.findChild(
                    FCBinding.ModernMenu, "Ribbon"
                )
                self.DisableRibbonToolbarsAndMenus(RibbonBar=RibbonBar)
            return False

        return False

    def EnableRibbonToolbarsAndMenus(self, RibbonBar):
        RibbonBar.rightToolBar().setEnabled(True)
        RibbonBar.quickAccessToolBar().setEnabled(True)
        RibbonBar.applicationOptionButton().setEnabled(True)
        RibbonBar.DesignMenuLoaded = False
        Gui.updateGui()
        return

    def DisableRibbonToolbarsAndMenus(self, RibbonBar):
        RibbonBar.rightToolBar().setDisabled(True)
        RibbonBar.quickAccessToolBar().setDisabled(True)
        RibbonBar.applicationOptionButton().setDisabled(True)
        RibbonBar.DesignMenuLoaded = True
        Gui.updateGui()
        return

def main():
    # Get the form
    Dialog = LoadDialog().form
    # Show the form
    Dialog.show()
