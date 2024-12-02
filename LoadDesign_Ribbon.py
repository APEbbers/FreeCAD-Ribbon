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
import FreeCAD as App
import FreeCADGui as Gui
import os
from PySide.QtGui import QIcon, QPixmap, QAction
from PySide.QtWidgets import (
    QListWidgetItem,
    QTableWidgetItem,
    QListWidget,
    QTableWidget,
    QToolBar,
    QToolButton,
    QComboBox,
    QPushButton,
    QMenu,
    QWidget,
)
from PySide.QtCore import Qt, SIGNAL, Signal, QObject, QThread, QSize
import sys
import json
from datetime import datetime
import shutil
import Standard_Functions_RIbbon as StandardFunctions
from Standard_Functions_RIbbon import CommandInfoCorrections
import Parameters_Ribbon
import Serialize_Ribbon
import webbrowser
import time

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
import Design_ui as Design_ui

# Define the translation
translate = App.Qt.translate

# Get the main window of FreeCAD
mw = Gui.getMainWindow()


class LoadDialog(Design_ui.Ui_Form):

    ReproAdress: str = ""

    # Define list of the workbenches, toolbars and commands on class level
    List_Workbenches = []
    StringList_Toolbars = []
    List_WorkBenchToolBarItems = []
    List_Commands = []

    # Create lists for the several list in the json file.
    List_IgnoredToolbars = []
    List_IconOnly_Toolbars = []
    List_QuickAccessCommands = []
    List_IgnoredWorkbenches = []
    Dict_RibbonCommandPanel = {}
    Dict_CustomToolbars = {}

    ShowText_Small = False
    ShowText_Medium = False
    ShowText_Large = False

    List_IgnoredToolbars_internal = []

    # Create the lists for the deserialized icons
    List_CommandIcons = []
    List_WorkBenchIcons = []

    def __init__(self):
        # Makes "self.on_CreateBOM_clicked" listen to the changed control values instead initial values
        super(LoadDialog, self).__init__()

        # Get the main window from FreeCAD
        mw = Gui.getMainWindow()

        # # this will create a Qt widget from our ui file
        self.form = Gui.PySideUic.loadUi(os.path.join(pathUI, "Design.ui"))

        # Make sure that the dialog stays on top
        self.form.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)
        self.form.label_4.hide()
        self.form.MoveDownPanel_RD.hide()
        self.form.MoveUpPanel_RD.hide()
        self.form.PanelOrder_RD.hide()

        # Position the dialog in front of FreeCAD
        centerPoint = mw.geometry().center()
        Rectangle = self.form.frameGeometry()
        Rectangle.moveCenter(centerPoint)
        self.form.move(Rectangle.topLeft())

        # Set the window title
        self.form.setWindowTitle(translate("FreeCAD Ribbon", "Ribbon design"))

        # Get the style from the main window and use it for this form
        palette = mw.palette()
        self.form.setPalette(palette)
        Style = mw.style()
        self.form.setStyle(Style)

        # load the RibbonStructure.json
        self.ReadJson()

        # Check if there is a datafile. if not, ask the user to create one.
        DataFile = os.path.join(os.path.dirname(__file__), "RibbonDataFile.dat")
        if os.path.exists(DataFile) is False:
            Question = (
                translate("FreeCAD Ribbon", "The first time, a data file must be generated!")
                + "\n"
                + translate("FreeCAD Ribbon", "This can take a while! Do you want to proceed?")
            )
            Answer = StandardFunctions.Mbox(Question, "FreeCAD Ribbon", 1, "Question")
            if Answer == "yes":
                self.on_ReloadWB_clicked()

        # region - Load data------------------------------------------------------------------
        #
        Data = {}
        # read ribbon structure from JSON file
        with open(DataFile, "r") as file:
            Data.update(json.load(file))
        file.close()

        # get the system language
        FreeCAD_preferences = App.ParamGet("User parameter:BaseApp/Preferences/General")
        try:
            FCLanguage = FreeCAD_preferences.GetString("Language")
            # Check if the language in the data file machtes the system language
            IsSystemLanguage = True
            if FCLanguage != Data["language"]:
                IsSystemLanguage = False
            # If the languguage doesn't match, ask the user to update the data
            if IsSystemLanguage is False:
                Question = (
                    translate(
                        "FreeCAD Ribbon",
                        "The data was generated for a differernt language!",
                    )
                    + "\n"
                    + translate("FreeCAD Ribbon", "Do you want to update the data?")
                    + "\n"
                    + translate("FreeCAD Ribbon", "This can take a while!")
                )

                Answer = StandardFunctions.Mbox(Question, "FreeCAD Ribbon", 1, "Question")
                if Answer == "yes":
                    self.on_ReloadWB_clicked()
        except Exception:
            pass

        # Load the standard lists for Workbenches, toolbars and commands
        self.List_Workbenches = Data["List_Workbenches"]
        self.StringList_Toolbars = Data["StringList_Toolbars"]
        self.List_Commands = Data["List_Commands"]
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
        except Exception:
            pass

        # check if the list with workbenches is up-to-date
        missingWB = []
        for WorkBenchName in Gui.listWorkbenches():
            for j in range(len(self.List_Workbenches)):
                if WorkBenchName == self.List_Workbenches[j][0] or WorkBenchName == "NoneWorkbench":
                    break
                if j == len(self.List_Workbenches) - 1:
                    missingWB.append(WorkBenchName)
        if len(missingWB) > 0:
            ListWB = "  "
            for WB in missingWB:
                ListWB = ListWB + WB + "\n" + "  "
            Question = (
                translate(
                    "FreeCAD Ribbon",
                    "The following workbenches are installed after the last data update: ",
                )
                + "\n"
                + ListWB
                + "\n"
                + "\n"
                + translate("FreeCAD Ribbon", "Do you want to update the data?")
                + "\n"
                + translate("FreeCAD Ribbon", "This can take a while!")
            )
            Answer = StandardFunctions.Mbox(Question, "FreeCAD Ribbon", 1, "Question")
            if Answer == "yes":
                self.on_ReloadWB_clicked()
        # endregion

        # # Update the RibbonStructure.json
        # self.UpdateRibbonStructure()

        # region - Load all controls------------------------------------------------------------------
        #
        # laod all controls
        self.LoadControls()

        # -- Custom panel tab --
        self.form.CustomToolbarSelector_CP.addItem(translate("FreeCAD Ribbon", "New"))
        try:
            for WorkBenchName in self.Dict_CustomToolbars["customToolbars"]:
                WorkBenchTitle = ""
                for WorkBenchItem in self.List_Workbenches:
                    if WorkBenchItem[0] == WorkBenchName:
                        WorkBenchTitle = WorkBenchItem[2]
                for CustomPanelTitle in self.Dict_CustomToolbars["customToolbars"][WorkBenchName]:
                    if WorkBenchTitle != "":
                        self.form.CustomToolbarSelector_CP.addItem(f"{CustomPanelTitle}, {WorkBenchTitle}")
        except Exception:
            pass
        #
        # endregion-----------------------------------------------------------------------------------

        # region - connect controls with functions----------------------------------------------------
        #
        #
        # --- Reload function -------------------
        self.form.LoadWB.connect(self.form.LoadWB, SIGNAL("clicked()"), self.on_ReloadWB_clicked)

        # --- QuickCommandsTab ------------------
        #
        # Connect Add/Remove and move events to the buttons on the QuickAccess Tab
        self.form.Add_Command_QC.connect(self.form.Add_Command_QC, SIGNAL("clicked()"), self.on_AddCommand_QC_clicked)
        self.form.Remove_Command_QC.connect(
            self.form.Remove_Command_QC, SIGNAL("clicked()"), self.on_RemoveCommand_QC_clicked
        )
        self.form.MoveUp_Command_QC.connect(
            self.form.MoveUp_Command_QC, SIGNAL("clicked()"), self.on_MoveUpCommand_QC_clicked
        )
        self.form.MoveDown_Command_QC.connect(
            self.form.MoveDown_Command_QC,
            SIGNAL("clicked()"),
            self.on_MoveDownCommand_QC_clicked,
        )

        # Connect the filter for the quick commands on the quickcommands tab
        def FilterQuickCommands_QC():
            self.on_ListCategory_QC_TextChanged()

        # Connect the filter for the quick commands on the quickcommands tab
        self.form.ListCategory_QC.currentTextChanged.connect(FilterQuickCommands_QC)
        # Connect the searchbar for the quick commands on the quick commands tab
        self.form.SearchBar_QC.textChanged.connect(self.on_SearchBar_QC_TextChanged)

        #
        # --- ExcludePanelsTab ------------------
        #
        # Connect LoadToolbars with the dropdown PanelList_RD on the Ribbon design tab
        def FilterPanels_EP():
            self.on_ListCategory_EP_TextChanged()

        # Connect the filter for the toolbars on the toolbar tab
        self.form.ListCategory_EP.currentTextChanged.connect(FilterPanels_EP)
        # Connect the searchbar for the toolbars on the toolbar tab
        self.form.SearchBar_EP.textChanged.connect(self.on_SearchBar_EP_TextChanged)
        # Connect Add/Remove events to the buttons on the Toolbars Tab
        self.form.AddPanel_EP.connect(self.form.AddPanel_EP, SIGNAL("clicked()"), self.on_AddToolbar_EP_clicked)
        self.form.RemovePanel_EP.connect(
            self.form.RemovePanel_EP, SIGNAL("clicked()"), self.on_RemoveToolbar_EP_clicked
        )

        #
        # --- IncludeWorkbenchTab ------------------
        #
        # Connect Add/Remove events to the buttons on the Workbench Tab
        self.form.AddWorkbench_IW.connect(
            self.form.AddWorkbench_IW, SIGNAL("clicked()"), self.on_AddWorkbench_IW_clicked
        )
        self.form.RemoveWorkbench_IW.connect(
            self.form.RemoveWorkbench_IW,
            SIGNAL("clicked()"),
            self.on_RemoveWorkbench_IW_clicked,
        )

        #
        # --- CustomPanelsTab ------------------
        #
        # Connect move and events to the buttons on the Custom Panels Tab
        self.form.MoveUpPanelCommand_CP.connect(
            self.form.MoveUpPanelCommand_CP,
            SIGNAL("clicked()"),
            self.on_MoveUpPanelCommand_CP_clicked,
        )
        self.form.MoveDownPanelCommand_CP.connect(
            self.form.MoveDownPanelCommand_CP,
            SIGNAL("clicked()"),
            self.on_MoveDownPanelCommand_CP_clicked,
        )

        # Connect Add events to the buttons on the Custom Panels Tab for adding commands to the panel
        self.form.AddPanel_CP.connect(self.form.AddPanel_CP, SIGNAL("clicked()"), self.on_AddPanel_CP_clicked)

        self.form.AddCustomPanel_CP.connect(
            self.form.AddCustomPanel_CP,
            SIGNAL("clicked()"),
            self.on_AddCustomPanel_CP_clicked,
        )

        # Connect LoadWorkbenches with the dropdown WorkbenchList on the Ribbon design tab
        def LoadWorkbenches_CP():
            self.on_WorkbenchList_CP__activated()

        self.form.WorkbenchList_CP.activated.connect(LoadWorkbenches_CP)

        # Connect custom toolbar selector on the Custom Panels Tab
        def CustomToolbarSelect_CP():
            self.on_CustomToolbarSelector_CP_activated()

        self.form.CustomToolbarSelector_CP.activated.connect(CustomToolbarSelect_CP)

        self.form.RemovePanel_CP.connect(self.form.RemovePanel_CP, SIGNAL("clicked()"), self.on_RemovePanel_CP_clicked)

        #
        # --- RibbonDesignTab ------------------
        #
        # Connect LoadWorkbenches with the dropdown WorkbenchList on the Ribbon design tab
        def LoadWorkbenches_RD():
            self.on_WorkbenchList_RD__TextChanged()

        self.form.WorkbenchList_RD.currentTextChanged.connect(LoadWorkbenches_RD)

        # Connect LoadToolbars with the dropdown PanelList_RD on the Ribbon design tab
        def LoadPanels_RD():
            self.on_PanelList_RD__TextChanged()

        self.form.PanelList_RD.currentTextChanged.connect(LoadPanels_RD)

        # Connect the icon only checkbox
        self.form.IconOnly_RD.clicked.connect(self.on_IconOnly_RD_clicked)
        # Connect a click event on the tablewidgit on the Ribbon design tab
        self.form.CommandTable_RD.itemClicked.connect(self.on_TableCell_RD_clicked)
        # Connect a change event on the tablewidgit on the Ribbon design tab to change the button text.
        self.form.CommandTable_RD.itemChanged.connect(self.on_TableCell_RD_changed)

        # Connect move events to the buttons on the Ribbon design Tab
        self.form.MoveUp_RibbonCommand_RD.connect(
            self.form.MoveUp_RibbonCommand_RD,
            SIGNAL("clicked()"),
            self.on_MoveUpCommandTable_RD_clicked,
        )
        self.form.MoveDown_RibbonCommand_RD.connect(
            self.form.MoveDown_RibbonCommand_RD,
            SIGNAL("clicked()"),
            self.on_MoveDownCommandTable_RD_clicked,
        )
        self.form.MoveUpPanel_RD.connect(
            self.form.MoveUpPanel_RD,
            SIGNAL("clicked()"),
            self.on_MoveUpPanel_RD_clicked,
        )
        self.form.MoveDownPanel_RD.connect(
            self.form.MoveDownPanel_RD,
            SIGNAL("clicked()"),
            self.on_MoveDownPanel_RD_clicked,
        )
        self.form.PanelOrder_RD.indexesMoved.connect(self.on_PanelOrder_RD_changed)

        self.form.AddSeparator_RD.connect(
            self.form.AddSeparator_RD,
            SIGNAL("clicked()"),
            self.on_AddSeparator_RD_clicked,
        )

        self.form.RemoveSeparator_RD.connect(
            self.form.RemoveSeparator_RD,
            SIGNAL("clicked()"),
            self.on_RemoveSeparator_RD_clicked,
        )

        # --- Form controls ------------------
        #
        # Connect the button UpdateJson with the function on_UpdateJson_clicked
        def UpdateJson():
            self.on_UpdateJson_clicked(self)

        self.form.UpdateJson.connect(self.form.UpdateJson, SIGNAL("clicked()"), UpdateJson)

        # Connect the button Close with the function on_Close_clicked
        def Close():
            self.on_Close_clicked(self)

        self.form.Close.connect(self.form.Close, SIGNAL("clicked()"), Close)

        self.form.RestoreJson.connect(self.form.RestoreJson, SIGNAL("clicked()"), self.on_RestoreJson_clicked)
        self.form.ResetJson.connect(self.form.ResetJson, SIGNAL("clicked()"), self.on_ResetJson_clicked)

        # connect the change of the current tab event to a function to set the size per tab
        self.form.tabWidget.currentChanged.connect(self.on_tabBar_currentIndexChanged)

        # Connect the cancel button
        def Cancel():
            self.on_Cancel_clicked(self)

        self.form.Cancel.connect(self.form.Cancel, SIGNAL("clicked()"), Cancel)

        # Connect the help buttons
        def Help():
            self.on_Helpbutton_clicked(self)

        self.form.HelpButton.connect(self.form.HelpButton, SIGNAL("clicked()"), Help)

        # endregion

        # region - Modify controls--------------------------------------------------------------------
        #
        # -- TabWidget
        # Set the first tab activated
        self.form.tabWidget.setCurrentWidget(self.form.tabWidget.widget(0))
        # -- Ribbon design tab --
        # Settings for the table widget
        self.form.CommandTable_RD.setEnabled(True)
        self.form.CommandTable_RD.horizontalHeader().setVisible(True)
        self.form.CommandTable_RD.setColumnWidth(0, 300)
        self.form.CommandTable_RD.resizeColumnToContents(1)
        self.form.CommandTable_RD.resizeColumnToContents(2)
        self.form.CommandTable_RD.resizeColumnToContents(3)
        #
        self.form.label_4.hide()
        self.form.MoveDownPanel_RD.hide()
        self.form.MoveUpPanel_RD.hide()
        self.form.PanelOrder_RD.hide()

        # -- Form buttons --
        # Get the icon from the FreeCAD help
        helpMenu = mw.findChildren(QMenu, "&Help")[0]
        helpAction = helpMenu.actions()[0]
        helpIcon = helpAction.icon()

        if helpIcon is not None:
            self.form.HelpButton.setIcon(helpIcon)
        self.form.HelpButton.setMinimumHeight(self.form.Close.minimumHeight())

        # Disable and hide the restore button if the backup function is disabled
        if Parameters_Ribbon.ENABLE_BACKUP is False:
            self.form.RestoreJson.setDisabled(True)
            self.form.RestoreJson.setHidden(True)
        else:
            self.form.RestoreJson.setEnabled(True)
            self.form.RestoreJson.setVisible(True)

        # Set the icon and size for the refresh button
        self.form.LoadWB.setIcon(Gui.getIcon("view-refresh"))
        self.form.LoadWB.setIconSize(QSize(20, 20))
        # endregion

        # self.form.resizeEvent = lambda event: self.resizeEvent_custom(event)
        return

    def on_ReloadWB_clicked(self):
        # clear the lists first
        self.List_Workbenches.clear()
        self.StringList_Toolbars.clear()
        self.List_Commands.clear()

        # get the system language
        FreeCAD_preferences = App.ParamGet("User parameter:BaseApp/Preferences/General")
        FCLanguage = FreeCAD_preferences.GetString("Language")

        # --- Workbenches ----------------------------------------------------------------------------------------------
        #
        # Create a list of all workbenches with their icon
        self.List_Workbenches.clear()
        List_Workbenches = Gui.listWorkbenches().copy()
        for WorkBenchName in List_Workbenches:
            if str(WorkBenchName) != "" or WorkBenchName is not None:
                if str(WorkBenchName) != "NoneWorkbench":
                    Gui.activateWorkbench(WorkBenchName)
                    WorkBench = Gui.getWorkbench(WorkBenchName)
                    ToolbarItems: dict = WorkBench.getToolbarItems()

                    IconName = ""
                    IconName = str(Gui.getWorkbench(WorkBenchName).Icon)
                    WorkbenchTitle = Gui.getWorkbench(WorkBenchName).MenuText
                    self.List_Workbenches.append([str(WorkBenchName), IconName, WorkbenchTitle, ToolbarItems])

        # --- Toolbars ----------------------------------------------------------------------------------------------
        #
        # Store the current active workbench
        ActiveWB = Gui.activeWorkbench().name()
        # Go through the list of workbenches
        i = 0
        for WorkBench in self.List_Workbenches:
            wbToolbars = []
            if WorkBench[0] != "General" and WorkBench[0] != "" and WorkBench[0] is not None:
                Gui.activateWorkbench(WorkBench[0])
                wbToolbars = Gui.getWorkbench(WorkBench[0]).listToolbars()
                # Go through the toolbars
                for Toolbar in wbToolbars:
                    self.StringList_Toolbars.append([Toolbar, WorkBench[2], WorkBench[0]])

        # Add the custom toolbars
        CustomToolbars = self.List_ReturnCustomToolbars()
        for Customtoolbar in CustomToolbars:
            self.StringList_Toolbars.append(Customtoolbar)
        CustomToolbars = self.List_ReturnCustomToolbars_Global()
        for Customtoolbar in CustomToolbars:
            self.StringList_Toolbars.append(Customtoolbar)

        # --- Commands ----------------------------------------------------------------------------------------------
        #
        # Create a list of all commands with their icon
        self.List_Commands.clear()
        # Create a list of command names
        CommandNames = []
        for i in range(len(self.List_Workbenches)):
            Gui.activateWorkbench(self.List_Workbenches[i][0])
            WorkBench = Gui.getWorkbench(self.List_Workbenches[i][0])
            ToolbarItems = WorkBench.getToolbarItems()

            for key, value in list(ToolbarItems.items()):
                for j in range(len(value)):
                    Item = [value[j], self.List_Workbenches[i][0]]
                    CommandNames.append(Item)

        # Go through the list
        for CommandName in CommandNames:
            # get the command with this name
            command = Gui.Command.get(CommandName[0])
            WorkBenchName = CommandName[1]
            if command is not None:
                # get the icon for this command
                if CommandInfoCorrections(CommandName[0])["pixmap"] != "":
                    IconName = CommandInfoCorrections(CommandName[0])["pixmap"]
                else:
                    IconName = ""
                MenuName = CommandInfoCorrections(CommandName[0])["menuText"].replace("&", "").replace("...", "")
                self.List_Commands.append([CommandName[0], IconName, MenuName, WorkBenchName])
        # add also custom commands
        Toolbars = self.List_ReturnCustomToolbars()
        for Toolbar in Toolbars:
            WorkbenchTitle = Toolbar[1]
            for WorkBench in self.List_Workbenches:
                if WorkbenchTitle == WorkBench[2]:
                    WorkBenchName = WorkBench[0]
                    for CustomCommand in Toolbar[2]:
                        command = Gui.Command.get(CustomCommand)
                        if CommandInfoCorrections(CustomCommand)["pixmap"] != "":
                            IconName = CommandInfoCorrections(CustomCommand)["pixmap"]
                        else:
                            IconName = ""
                        MenuName = CommandInfoCorrections(CustomCommand)["menuText"].replace("&", "").replace("...", "")
                        self.List_Commands.append([CustomCommand, IconName, MenuName, WorkBenchName])
        Toolbars = self.List_ReturnCustomToolbars_Global()
        for Toolbar in Toolbars:
            for CustomCommand in Toolbar[2]:
                command = Gui.Command.get(CustomCommand)
                if CommandInfoCorrections(CustomCommand)["pixmap"] != "":
                    IconName = CommandInfoCorrections(CustomCommand)["pixmap"]
                else:
                    IconName = None
                MenuName = CommandInfoCorrections(CustomCommand)["menuText"].replace("&", "").replace("...", "")
                self.List_Commands.append([CustomCommand, IconName, MenuName, Toolbar[1]])
        if int(App.Version()[0]) > 0:
            command = Gui.Command.get("Std_Measure")
            if CommandInfoCorrections("Std_Measure")["pixmap"] != "":
                IconName = CommandInfoCorrections("Std_Measure")["pixmap"]
            else:
                IconName = ""
            MenuName = CommandInfoCorrections("Std_Measure")["menuText"].replace("&", "").replace("...", "")
            self.List_Commands.append(["Std_Measure", IconName, MenuName, "General"])

        # re-activate the workbench that was stored.
        Gui.activateWorkbench(ActiveWB)

        # --- Serialize Icons ------------------------------------------------------------------------------------------
        #
        WorkbenchIcon = []
        for WorkBenchItem in self.List_Workbenches:
            WorkBenchName = WorkBenchItem[0]
            Icon = Gui.getIcon(WorkBenchItem[1])
            if Icon is not None and Icon.isNull() is False:
                try:
                    SerializedIcon = Serialize_Ribbon.serializeIcon(Icon)

                    WorkbenchIcon.append([WorkBenchName, SerializedIcon])
                    # add the icons also to the deserialized list
                    self.List_WorkBenchIcons.append([WorkBenchName, Icon])
                except Exception as e:
                    if Parameters_Ribbon.DEBUG_MODE is True:
                        print(e)

        CommandIcons = []
        for CommandItem in self.List_Commands:
            CommandName = CommandItem[0]
            Icon = StandardFunctions.returnQiCons_Commands(CommandName, CommandItem[1])
            if Icon is not None and Icon.isNull() is False:
                try:
                    SerializedIcon = Serialize_Ribbon.serializeIcon(Icon)

                    CommandIcons.append([CommandName, SerializedIcon])
                    # add the icons also to the deserialized list
                    self.List_CommandIcons.append([CommandName, Icon])
                except Exception as e:
                    if Parameters_Ribbon.DEBUG_MODE is True:
                        print(e)

        # Write the lists to a data file
        #
        # clear the data file. If not exists, create it
        DataFile = os.path.join(os.path.dirname(__file__), "RibbonDataFile.dat")
        open(DataFile, "w").close()

        # Open de data file, load it as json and then close it again
        Data = {}
        # Update the data
        Data["Language"] = FCLanguage
        Data["List_Workbenches"] = self.List_Workbenches
        Data["StringList_Toolbars"] = self.StringList_Toolbars
        Data["List_Commands"] = self.List_Commands
        Data["WorkBench_Icons"] = WorkbenchIcon
        Data["Command_Icons"] = CommandIcons
        # Write to the data file
        DataFile = os.path.join(os.path.dirname(__file__), "RibbonDataFile.dat")
        with open(DataFile, "w") as outfile:
            json.dump(Data, outfile, indent=4)
        outfile.close()

        # If there is a RibbonStructure.json file, load it
        os.path.isfile(os.path.join(os.path.dirname(__file__), "RibbonStructure.json"))
        self.ReadJson()

        self.LoadControls()
        return

    # region - Control functions----------------------------------------------------------------------
    # Add all toolbars of the selected workbench to the toolbar list(QComboBox)
    #
    # region - QuickCommands tab
    def on_ListCategory_QC_TextChanged(self):
        self.form.CommandsAvailable_QC.clear()

        ShadowList = []  # List to add the commands and prevent duplicates
        IsInList = False

        for ToolbarCommand in self.List_Commands:
            CommandName = ToolbarCommand[0]
            workbenchName = ToolbarCommand[3]
            IsInList = ShadowList.__contains__(f"{CommandName}, {workbenchName}")

            if IsInList is False and workbenchName != "Global" and workbenchName != "General":
                # Get the translated menuname
                MenuName = StandardFunctions.CommandInfoCorrections(CommandName)["ActionText"]

                WorkbenchTitle = Gui.getWorkbench(workbenchName).MenuText
                if (
                    WorkbenchTitle == self.form.ListCategory_QC.currentText()
                    or self.form.ListCategory_QC.currentText() == translate("FreeCAD Ribbon", "All")
                ):
                    IsInlist = False
                    for i in range(self.form.CommandsAvailable_QC.count()):
                        CommandItem = self.form.CommandsAvailable_QC.item(i)
                        if CommandItem.text() == MenuName:
                            IsInlist = True

                    if IsInlist is False:
                        # Define a new ListWidgetItem.
                        textAddition = ""
                        Icon = QIcon()
                        for item in self.List_CommandIcons:
                            if item[0] == ToolbarCommand[0]:
                                Icon = item[1]
                        if Icon is None:
                            Icon = Gui.getIcon(ToolbarCommand[1])

                        ListWidgetItem = QListWidgetItem()
                        ListWidgetItem.setText(
                            (
                                StandardFunctions.CommandInfoCorrections(CommandName)["ActionText"]
                                + textAddition.replace("&", "")
                            )
                        )
                        ListWidgetItem.setData(Qt.ItemDataRole.UserRole, CommandName)
                        if Icon is not None:
                            ListWidgetItem.setIcon(Icon)
                        ListWidgetItem.setToolTip(ToolbarCommand[0])  # Use the tooltip to store the actual command.

                        # Add the ListWidgetItem to the correct ListWidget
                        if Icon is not None:
                            self.form.CommandsAvailable_QC.addItem(ListWidgetItem)
            ShadowList.append(f"{CommandName}, {workbenchName}")
        return

    def on_SearchBar_QC_TextChanged(self):
        self.form.CommandsAvailable_QC.clear()

        ShadowList = []  # List to add the commands and prevent duplicates
        IsInList = False

        for ToolbarCommand in self.List_Commands:
            CommandName = ToolbarCommand[0]
            workbenchName = ToolbarCommand[3]
            IsInList = ShadowList.__contains__(f"{CommandName}, {workbenchName}")

            if IsInList is False and workbenchName != "Global":
                # Command = Gui.Command.get(CommandName)
                MenuName = StandardFunctions.CommandInfoCorrections(CommandName)["ActionText"]

                if MenuName.lower().startswith(self.form.SearchBar_QC.text().lower()):
                    IsInlist = False
                    for i in range(self.form.CommandsAvailable_QC.count()):
                        CommandItem = self.form.CommandsAvailable_QC.item(i)
                        if CommandItem.text() == MenuName:
                            IsInlist = True

                    if IsInlist is False:
                        # Define a new ListWidgetItem.
                        textAddition = ""
                        Icon = QIcon()
                        for item in self.List_CommandIcons:
                            if item[0] == ToolbarCommand[0]:
                                Icon = item[1]
                        if Icon is None:
                            Icon = Gui.getIcon(ToolbarCommand[1])
                        ListWidgetItem = QListWidgetItem()
                        ListWidgetItem.setText(
                            (
                                StandardFunctions.CommandInfoCorrections(CommandName)["ActionText"]
                                + textAddition.replace("&", "")
                            )
                        )
                        ListWidgetItem.setData(Qt.ItemDataRole.UserRole, CommandName)
                        if Icon is not None:
                            ListWidgetItem.setIcon(Icon)
                        ListWidgetItem.setToolTip(CommandName)  # Use the tooltip to store the actual command.

                        # Add the ListWidgetItem to the correct ListWidget
                        if Icon is not None:
                            self.form.CommandsAvailable_QC.addItem(ListWidgetItem)
            ShadowList.append(f"{CommandName}, {workbenchName}")
        return

    def on_AddCommand_QC_clicked(self):
        self.AddItem(
            SourceWidget=self.form.CommandsAvailable_QC,
            DestinationWidget=self.form.CommandsSelected_QC,
        )

        # Enable the apply button
        if self.CheckChanges() is True:
            self.form.UpdateJson.setEnabled(True)

        return

    def on_RemoveCommand_QC_clicked(self):
        self.AddItem(
            SourceWidget=self.form.CommandsSelected_QC,
            DestinationWidget=self.form.CommandsAvailable_QC,
        )

        # Enable the apply button
        if self.CheckChanges() is True:
            self.form.UpdateJson.setEnabled(True)

        return

    def on_MoveUpCommand_QC_clicked(self):
        self.MoveItem(ListWidget=self.form.CommandsSelected_QC, Up=True)

        # Enable the apply button
        if self.CheckChanges() is True:
            self.form.UpdateJson.setEnabled(True)

        return

    def on_MoveDownCommand_QC_clicked(self):
        self.MoveItem(ListWidget=self.form.CommandsSelected_QC, Up=False)

        # Enable the apply button
        if self.CheckChanges() is True:
            self.form.UpdateJson.setEnabled(True)

        return

    # endregion

    # region - Exclude panels tab
    def on_ListCategory_EP_TextChanged(self):
        self.form.PanelsToExclude_EP.clear()

        for Toolbar in self.StringList_Toolbars:
            WorkbenchTitle = Toolbar[1]
            WorkbenchName = Toolbar[2]
            if (
                WorkbenchTitle == self.form.ListCategory_EP.currentText()
                or self.form.ListCategory_EP.currentText() == "All"
            ):
                IsInlist = False
                for i in range(self.form.PanelsToExclude_EP.count()):
                    ToolbarItem = self.form.PanelsToExclude_EP.item(i)
                    if ToolbarItem.text().replace("&", "") == StandardFunctions.TranslationsMapping(
                        WorkbenchName, Toolbar[0]
                    ).replace("&", ""):
                        IsInlist = True

                if IsInlist is False:
                    ListWidgetItem = QListWidgetItem()
                    ListWidgetItem.setText(StandardFunctions.TranslationsMapping(WorkbenchName, Toolbar[0])).replace(
                        "&", ""
                    )
                    ListWidgetItem.setData(Qt.ItemDataRole.UserRole, Toolbar)

                    # Add the ListWidgetItem to the correct ListWidget
                    self.form.PanelsToExclude_EP.addItem(ListWidgetItem)

    def on_SearchBar_EP_TextChanged(self):
        self.form.PanelsToExclude_EP.clear()

        for Toolbar in self.StringList_Toolbars:
            if Toolbar[0].lower().startswith(self.form.SearchBar_EP.text().lower()):
                WorkbenchName = Toolbar[2]
                ListWidgetItem = QListWidgetItem()
                ListWidgetItem.setText(StandardFunctions.TranslationsMapping(WorkbenchName, Toolbar[0])).replace(
                    "&", ""
                )
                ListWidgetItem.setData(Qt.ItemDataRole.UserRole, Toolbar)

                IsInlist = False
                for i in range(self.form.PanelsToExclude_EP.count()):
                    ToolbarItem = self.form.PanelsToExclude_EP.item(i)
                    if ToolbarItem.text() == StandardFunctions.TranslationsMapping(WorkbenchName, Toolbar[0]):
                        IsInlist = True

                if IsInlist is False:
                    # Add the ListWidgetItem to the correct ListWidget
                    self.form.PanelsToExclude_EP.addItem(ListWidgetItem)

    def on_AddToolbar_EP_clicked(self):
        self.AddItem(
            SourceWidget=self.form.PanelsToExclude_EP,
            DestinationWidget=self.form.PanelsExcluded_EP,
        )

        # Enable the apply button
        if self.CheckChanges() is True:
            self.form.UpdateJson.setEnabled(True)

        return

    def on_RemoveToolbar_EP_clicked(self):
        self.AddItem(
            SourceWidget=self.form.PanelsExcluded_EP,
            DestinationWidget=self.form.PanelsToExclude_EP,
        )

        # Enable the apply button
        if self.CheckChanges() is True:
            self.form.UpdateJson.setEnabled(True)

        return

    # endregion

    # region - Include workbench tab
    def on_AddWorkbench_IW_clicked(self):
        self.AddItem(
            SourceWidget=self.form.WorkbenchesAvailable_IW,
            DestinationWidget=self.form.WorkbenchesSelected_IW,
        )

        # Enable the apply button
        if self.CheckChanges() is True:
            self.form.UpdateJson.setEnabled(True)

        return

    def on_RemoveWorkbench_IW_clicked(self):
        self.AddItem(
            SourceWidget=self.form.WorkbenchesSelected_IW,
            DestinationWidget=self.form.WorkbenchesAvailable_IW,
        )

        # Enable the apply button
        if self.CheckChanges() is True:
            self.form.UpdateJson.setEnabled(True)

        return

    # endregion

    # region - Custom panels tab
    def on_WorkbenchList_CP__activated(self, setCustomToolbarSelector_CP: bool = False, CurrentText=""):
        # Set the workbench name.
        WorkBenchName = ""
        WorkBenchTitle = ""
        for WorkBench in self.List_Workbenches:
            if WorkBench[2] == self.form.WorkbenchList_CP.currentData():
                WorkBenchName = WorkBench[0]
                WorkBenchTitle = WorkBench[2]

        # Get the toolbars of the workbench
        wbToolbars = self.returnWorkBenchToolbars(WorkBenchName)
        # Get all the custom toolbars from the toolbar layout
        CustomToolbars = self.List_ReturnCustomToolbars()
        for CustomToolbar in CustomToolbars:
            if CustomToolbar[1] == WorkBenchTitle:
                wbToolbars.append(CustomToolbar[0])
        # Get the global custom toolbars
        CustomToolbars = self.Dict_ReturnCustomToolbars_Global()
        for CustomToolbar in CustomToolbars:
            wbToolbars.append(CustomToolbar)
        # Get the custom panels
        CustomPanel = self.List_AddCustomPanel_CPsToWorkbench(WorkBenchName=WorkBenchName)
        for CustomToolbar in CustomPanel:
            if CustomToolbar[1] == WorkBenchTitle:
                wbToolbars.append(CustomToolbar[0])

        # Get the workbench
        WorkBench = Gui.getWorkbench(WorkBenchName)

        # Clear the listwidget before filling it
        self.form.PanelAvailable_CP.clear()
        # Sort the toolbar list
        wbToolbars = self.SortedPanelList_RD(wbToolbars, WorkBenchName)

        # Go through the toolbars and check if they must be ignored.
        for Toolbar in wbToolbars:
            IsIgnored = False
            for IgnoredToolbar in self.List_IgnoredToolbars:
                if Toolbar == IgnoredToolbar:
                    IsIgnored = True

            # If the are not to be ignored, add them to the listwidget
            if IsIgnored is False and Toolbar != "":
                ListWidgetItem = QListWidgetItem()
                ListWidgetItem.setText(StandardFunctions.TranslationsMapping(WorkBenchName, Toolbar))
                ListWidgetItem.setData(Qt.ItemDataRole.UserRole, Toolbar)
                self.form.PanelAvailable_CP.addItem(ListWidgetItem)

                if setCustomToolbarSelector_CP is True:
                    self.form.CustomToolbarSelector_CP.setCurrentText("New")

                if CurrentText != "":
                    self.form.WorkbenchList_CP.setCurrentText(CurrentText)

            self.form.PanelSelected_CP.clear()
        return

    def on_MoveUpPanelCommand_CP_clicked(self):
        self.MoveItem(ListWidget=self.form.PanelSelected_CP, Up=True)

        # Enable the apply button
        if self.CheckChanges() is True:
            self.form.UpdateJson.setEnabled(True)

        return

    def on_MoveDownPanelCommand_CP_clicked(self):
        self.MoveItem(ListWidget=self.form.PanelSelected_CP, Up=False)

        # Enable the apply button
        if self.CheckChanges() is True:
            self.form.UpdateJson.setEnabled(True)

        return

    def on_AddPanel_CP_clicked(self):
        SelectedToolbars = self.form.PanelAvailable_CP.selectedItems()

        # Go through the list of workbenches
        for WorkBenchItem in self.List_Workbenches:
            # If the workbench title matches the selected workbench, continue
            if WorkBenchItem[2] == self.form.WorkbenchList_CP.currentData():
                WorkbenchName = WorkBenchItem[0]

                # Get the dict with the toolbars of this workbench
                ToolbarItems = self.returnToolbarCommands(WorkbenchName)
                # Get the custom toolbars from each installed workbench
                CustomCommands = self.Dict_ReturnCustomToolbars(WorkbenchName)
                ToolbarItems.update(CustomCommands)
                # Get the global custom toolbars
                CustomCommands = self.Dict_ReturnCustomToolbars_Global()
                ToolbarItems.update(CustomCommands)
                for key, value in list(ToolbarItems.items()):
                    # Go through the selected items, if they mach continue
                    for i in range(len(SelectedToolbars)):
                        toolbar = QListWidgetItem(SelectedToolbars[i]).data(Qt.ItemDataRole.UserRole)
                        if key == toolbar:
                            for j in range(len(value)):
                                CommandName = value[j]
                                for ToolbarCommand in self.List_Commands:
                                    if ToolbarCommand[0] == CommandName:
                                        # Get the command
                                        Command = Gui.Command.get(CommandName)
                                        if Command is not None:
                                            if Command is None:
                                                continue
                                            MenuName = ToolbarCommand[2].replace("&", "")

                                            # get the icon for this command if there isn't one, leave it None
                                            Icon = QIcon()
                                            for item in self.List_CommandIcons:
                                                if item[0] == ToolbarCommand[0]:
                                                    Icon = item[1]
                                            if Icon is None:
                                                Icon = Gui.getIcon(CommandInfoCorrections(CommandName)["pixmap"])
                                            action = Command.getAction()
                                            try:
                                                if len(action) > 1:
                                                    Icon = action[0].icon()
                                            except Exception:
                                                pass

                                            # Define a new ListWidgetItem.
                                            ListWidgetItem = QListWidgetItem()
                                            ListWidgetItem.setText(
                                                StandardFunctions.TranslationsMapping(WorkbenchName, MenuName)
                                            )
                                            if Icon is not None:
                                                ListWidgetItem.setIcon(Icon)
                                            ListWidgetItem.setData(
                                                Qt.ItemDataRole.UserRole, key
                                            )  # add here the toolbar name as hidden data

                                            IsInList = False
                                            for k in range(self.form.PanelSelected_CP.count()):
                                                if self.form.PanelSelected_CP.item(k).text() == ListWidgetItem.text():
                                                    IsInList = True

                                            if IsInList is False:
                                                self.form.PanelSelected_CP.addItem(ListWidgetItem)

        # Enable the apply button
        if self.CheckChanges() is True:
            self.form.UpdateJson.setEnabled(True)

        return

    def on_AddCustomPanel_CP_clicked(self):
        CustomPanelTitle = ""
        if self.form.PanelName_CP.text() != "":
            CustomPanelTitle = self.form.PanelName_CP.text()
        if self.form.PanelName_CP.text() == "":
            StandardFunctions.Mbox(
                translate("FreeCAD Ribbon", "Enter a name for your custom panel first!"),
                "",
                0,
                "Warning",
            )
            return

        # Go through the list of workbenches
        for WorkBenchItem in self.List_Workbenches:
            WorkBenchTitle = self.form.WorkbenchList_CP.currentData()
            # If the workbench title matches the selected workbench, continue
            if WorkBenchItem[2] == WorkBenchTitle and WorkBenchItem[2] != "":
                WorkBenchName = WorkBenchItem[0]

                # Create item that defines the custom toolbar
                Commands = []
                MenuName = ""
                for i in range(self.form.PanelSelected_CP.count()):
                    ListWidgetItem = self.form.PanelSelected_CP.item(i)
                    MenuName_ListWidgetItem = ListWidgetItem.text().replace("&", "").replace("...", "")
                    # if the translated menuname from the ListWidgetItem is equel to the MenuName from the command
                    # Add the commandName to the list commandslist for this custom panel
                    for CommandItem in self.List_Commands:
                        MenuName = CommandItem[2].replace("&", "").replace("...", "")
                        if MenuName == MenuName_ListWidgetItem:
                            CommandName = CommandItem[0]
                            Commands.append(CommandName)

                    # Get the original toolbar
                    OriginalToolbar = ListWidgetItem.data(Qt.ItemDataRole.UserRole)
                    # define the suffix
                    Suffix = "_custom"

                    # Create or modify the dict that will be entered
                    StandardFunctions.add_keys_nested_dict(
                        self.Dict_CustomToolbars,
                        [
                            "customToolbars",
                            WorkBenchName,
                            CustomPanelTitle + Suffix,
                            "commands",
                            MenuName,
                        ],
                    )

                    # Update the dict
                    self.Dict_CustomToolbars["customToolbars"][WorkBenchName][CustomPanelTitle + Suffix]["commands"][
                        MenuName
                    ] = OriginalToolbar

                # Check if the custom panel is selected in the Json file
                IsInList = False
                for j in range(self.form.CustomToolbarSelector_CP.count()):
                    CustomToolbar = self.form.CustomToolbarSelector_CP.itemText(i).split(", ")[0]
                    if CustomToolbar == f"{CustomPanelTitle}, {WorkBenchTitle}":
                        IsInList = True

                # If the custom panel is not in the json file, add it to the QComboBox
                if IsInList is False:
                    self.form.CustomToolbarSelector_CP.addItem(f"{CustomPanelTitle}, {WorkBenchTitle}")
                # Set the Custom panel as current text for the QComboBox
                self.form.CustomToolbarSelector_CP.setCurrentText(f"{CustomPanelTitle}, {WorkBenchTitle}")

                # Add the order of panels to the Json file
                ToolbarOrder = []
                for i2 in range(self.form.PanelOrder_RD.count()):
                    ToolbarOrder.append(self.form.PanelOrder_RD.item(i2).data(Qt.ItemDataRole.UserRole))
                StandardFunctions.add_keys_nested_dict(
                    self.Dict_RibbonCommandPanel,
                    ["workbenches", WorkBenchName, "toolbars", "order"],
                )
                self.Dict_RibbonCommandPanel["workbenches"][WorkBenchName]["toolbars"]["order"] = ToolbarOrder

        # Enable the apply button
        if self.CheckChanges() is True:
            self.form.UpdateJson.setEnabled(True)

        return

    def on_CustomToolbarSelector_CP_activated(self):
        self.form.PanelSelected_CP.clear()

        # If the selected item is "new", clear the list widgets and exit
        if self.form.CustomToolbarSelector_CP.currentText() == "New":
            self.form.PanelAvailable_CP.clear()
            self.form.PanelName_CP.clear()
            return

        # Get the current custom toolbar name
        CustomPanelTitle = ""
        WorkBenchTitle = ""
        if self.form.CustomToolbarSelector_CP.currentText() != "":
            CustomPanelTitle = self.form.CustomToolbarSelector_CP.currentText().split(", ")[0]
            WorkBenchTitle = self.form.CustomToolbarSelector_CP.currentText().split(", ")[1]

            # Set the workbench selector to the workbench to which this custom toolbar belongs
            self.form.WorkbenchList_CP.setCurrentText(WorkBenchTitle)
            self.on_WorkbenchList_CP__activated(False, WorkBenchTitle)

            ShadowList = []  # Create a shadow list. To check if items are already existing.
            WorkBenchName = ""
            for WorkBench in self.Dict_CustomToolbars["customToolbars"]:
                for CustomToolbar in self.Dict_CustomToolbars["customToolbars"][WorkBench]:
                    if CustomToolbar == CustomPanelTitle:
                        WorkBenchName = WorkBench

                        # Get the commands and their original toolbar
                        for key, value in list(
                            self.Dict_CustomToolbars["customToolbars"][WorkBenchName][CustomPanelTitle][
                                "commands"
                            ].items()
                        ):
                            for CommandItem in self.List_Commands:
                                # Check if the items is already there
                                IsInList = ShadowList.__contains__(CommandItem[0])
                                # if not, continue
                                if IsInList is False:
                                    if CommandItem[2] == key and CommandItem[3] == WorkBenchName:
                                        # Command = Gui.Command.get(CommandItem[0])
                                        MenuName = CommandItem[2].replace("&", "").replace("...", "")

                                        # Define a new ListWidgetItem.
                                        ListWidgetItem = QListWidgetItem()
                                        ListWidgetItem.setText(MenuName)
                                        ListWidgetItem.setData(Qt.ItemDataRole.UserRole, CommandItem)
                                        Icon = QIcon()
                                        for item in self.List_CommandIcons:
                                            if item[0] == CommandItem[0]:
                                                Icon = item[1]
                                        if Icon is None:
                                            Icon = Gui.getIcon(CommandItem[1])
                                        if Icon is not None:
                                            ListWidgetItem.setIcon(Icon)

                                        if ListWidgetItem.text() != "":
                                            self.form.PanelSelected_CP.addItem(ListWidgetItem)

                                        # Add the command to the shadow list
                                        ShadowList.append(CommandItem[0])

            # Enable the apply button
            if self.CheckChanges() is True:
                self.form.UpdateJson.setEnabled(True)
        else:
            return

        return

    def on_RemovePanel_CP_clicked(self):
        # Get the current custom toolbar name
        CustomPanelTitle = ""
        WorkBenchTitle = ""
        if self.form.CustomToolbarSelector_CP.currentText() != "":
            CustomPanelTitle = self.form.CustomToolbarSelector_CP.currentText().split(", ")[0]
            WorkBenchTitle = self.form.CustomToolbarSelector_CP.currentText().split(", ")[1]
        else:
            return

        WorkBenchName = ""
        for WorkBench in self.List_Workbenches:
            if WorkBench[2] == WorkBenchTitle:
                WorkBenchName = WorkBench[0]
                try:
                    for key, value in list(self.Dict_CustomToolbars["customToolbars"][WorkBenchName].items()):
                        if key == CustomPanelTitle:
                            # remove the custom toolbar from the combobox
                            for i in range(self.form.CustomToolbarSelector_CP.count()):
                                if self.form.CustomToolbarSelector_CP.itemText(i).split(", ")[0] == key:
                                    if (
                                        self.form.CustomToolbarSelector_CP.itemText(i).split(", ")[1] == WorkBenchTitle
                                        and self.form.CustomToolbarSelector_CP.itemText(i).split(", ")[1] != ""
                                    ):
                                        self.form.CustomToolbarSelector_CP.removeItem(i)
                                        self.form.CustomToolbarSelector_CP.setCurrentText(
                                            self.form.CustomToolbarSelector_CP.itemText(i - 1)
                                        )

                            orderList: list = self.Dict_RibbonCommandPanel["workbenches"][WorkBenchName]["toolbars"][
                                "order"
                            ]
                            if key in orderList:
                                orderList.remove(key)

                            # remove the custom toolbar also from the workbenches dict
                            del self.Dict_CustomToolbars["customToolbars"][WorkBenchName][key]
                            if key in self.Dict_RibbonCommandPanel["workbenches"][WorkBenchName]["toolbars"]:
                                del self.Dict_RibbonCommandPanel["workbenches"][WorkBenchName]["toolbars"][key]

                            # update the order list
                            self.Dict_RibbonCommandPanel["workbenches"][WorkBenchName]["order"] = orderList

                            # Enable the apply button
                            if self.CheckChanges() is True:
                                self.form.UpdateJson.setEnabled(True)

                            return
                except Exception as e:
                    raise (e)
        return

    # endregion

    # region - Ribbon design tab
    def on_tabBar_currentIndexChanged(self):
        # width_small: int = Parameters_Ribbon.Settings.GetIntSetting("TabWidth_small")
        # if width_small is None:
        width_small = 730
        # width_large: int = Parameters_Ribbon.Settings.GetIntSetting("TabWidth_large")
        # if width_large is None:
        width_large = 940

        if self.form.tabWidget.currentIndex() == 7:
            # Set the default size of the form
            Geometry = self.form.geometry()
            Geometry.setWidth(width_large)
            self.form.setGeometry(Geometry)

            self.form.label_4.show()
            self.form.MoveDownPanel_RD.show()
            self.form.MoveUpPanel_RD.show()
            self.form.PanelOrder_RD.show()
            self.form.setMinimumWidth(width_large)
            self.form.setMaximumWidth(width_large)
            self.form.setMaximumWidth(120000)
        else:
            self.form.label_4.hide()
            self.form.MoveDownPanel_RD.hide()
            self.form.MoveUpPanel_RD.hide()
            self.form.PanelOrder_RD.hide()
            # Set the default size of the form
            Geometry = self.form.geometry()
            Geometry.setWidth(width_small)
            self.form.setGeometry(Geometry)
            self.form.setMinimumWidth(width_small)
            self.form.setMaximumWidth(width_small)
            self.form.setMaximumWidth(120000)

    def on_WorkbenchList_RD__TextChanged(self):
        # Set the workbench name.
        WorkBenchName = ""
        WorkBenchTitle = ""
        for WorkBench in self.List_Workbenches:
            if WorkBench[2] == self.form.WorkbenchList_RD.currentData():
                WorkBenchName = WorkBench[0]
                WorkBenchTitle = WorkBench[2]

        # If there is no workbench, return
        if WorkBenchName == "":
            return

        # Get the toolbars of the workbench
        # wbToolbars: list = Gui.getWorkbench(WorkBenchName).listToolbars()
        wbToolbars = []
        wbToolbars = self.returnWorkBenchToolbars(WorkBenchName)
        # Get all the custom toolbars from the toolbar layout
        CustomToolbars = self.List_ReturnCustomToolbars()
        for CustomToolbar in CustomToolbars:
            if CustomToolbar[1] == WorkBenchTitle:
                wbToolbars.append(CustomToolbar[0])
        # Get the global custom toolbars
        CustomToolbars = self.Dict_ReturnCustomToolbars_Global()
        for CustomToolbar in CustomToolbars:
            wbToolbars.append(CustomToolbar)
        # Get the custom panels
        CustomPanel = self.List_AddCustomPanel_CPsToWorkbench(WorkBenchName=WorkBenchName)
        for CustomToolbar in CustomPanel:
            if CustomToolbar[1] == WorkBenchTitle:
                wbToolbars.append(CustomToolbar[0])

        # Clear the listwidget before filling it
        self.form.PanelList_RD.clear()
        self.form.PanelOrder_RD.clear()

        # Get the order from the json file
        wbToolbars = self.SortedPanelList_RD(wbToolbars, WorkBenchName)

        # Go through the toolbars and check if they must be ignored.
        for Toolbar in wbToolbars:
            IsIgnored = False
            for IgnoredToolbar in self.List_IgnoredToolbars:
                if Toolbar == IgnoredToolbar:
                    IsIgnored = True
            for IgnoredToolbar in self.List_IgnoredToolbars_internal:
                if Toolbar == IgnoredToolbar:
                    IsIgnored = True

            # If the are not to be ignored, add them to the listwidget
            if IsIgnored is False:
                if Toolbar != "":
                    self.form.PanelList_RD.addItem(
                        StandardFunctions.TranslationsMapping(WorkBenchName, Toolbar),
                        Toolbar,
                    )
                    # Define a new ListWidgetItem.
                    ListWidgetItem = QListWidgetItem()
                    ListWidgetItem.setText(StandardFunctions.TranslationsMapping(WorkBenchName, Toolbar))
                    ListWidgetItem.setData(Qt.ItemDataRole.UserRole, Toolbar)
                    self.form.PanelOrder_RD.addItem(ListWidgetItem)

        # Update the combobox PanelList_RD
        self.on_PanelList_RD__TextChanged
        return

    def on_PanelList_RD__TextChanged(self):
        if "workbenches" in self.Dict_RibbonCommandPanel:
            # Clear the table
            self.form.CommandTable_RD.setRowCount(0)

            # Create the row in the table
            # add a row to the table widget
            FirstItem = QTableWidgetItem()
            FirstItem.setText("All")
            self.form.CommandTable_RD.insertRow(self.form.CommandTable_RD.rowCount())

            # Get the last rownumber and set this row with the CommandTable_RDItem
            RowNumber = 0
            # update the data
            FirstItem.setData(Qt.ItemDataRole.UserRole, "All")

            # Add the first cell with the table widget
            self.form.CommandTable_RD.setItem(RowNumber, 0, FirstItem)

            # Create the second cell and set the checkstate according the checkstate as defined earlier
            Icon_small = QTableWidgetItem()
            Icon_small.setText("")
            Icon_small.setCheckState(Qt.CheckState.Unchecked)
            self.form.CommandTable_RD.setItem(RowNumber, 1, Icon_small)

            # Create the third cell and set the checkstate according the checkstate as defined earlier
            Icon_medium = QTableWidgetItem()
            Icon_medium.setText("")
            Icon_medium.setCheckState(Qt.CheckState.Unchecked)
            self.form.CommandTable_RD.setItem(RowNumber, 2, Icon_medium)

            # Create the last cell and set the checkstate according the checkstate as defined earlier
            Icon_large = QTableWidgetItem()
            Icon_large.setText("")
            Icon_large.setCheckState(Qt.CheckState.Unchecked)
            self.form.CommandTable_RD.setItem(RowNumber, 3, Icon_large)

            # # Add the first cell with the table widget
            # self.form.CommandTable_RD.setItem(RowNumber, 0, CommandTable_RDItem)

            ShadowList = []  # Create a shadow list. To check if items are already existing.

            # Get the correct workbench name
            WorkBenchName = ""
            for WorkBench in self.List_Workbenches:
                if WorkBench[2] == self.form.WorkbenchList_RD.currentData():
                    WorkBenchName = WorkBench[0]

            # Get the toolbar name
            Toolbar = self.form.PanelList_RD.currentData()
            # Copy the workbench Toolbars
            Toolbaritems = self.returnToolbarCommands(WorkBenchName)
            # Get the custom toolbars from each installed workbench
            CustomCommands = self.Dict_ReturnCustomToolbars(WorkBenchName)
            Toolbaritems.update(CustomCommands)
            # Get the custom toolbars from global
            CustomCommands = self.Dict_ReturnCustomToolbars_Global()
            Toolbaritems.update(CustomCommands)
            # Get the commands from
            CustomPanelCommands = self.Dict_AddCustomPanel_CPCommandsToWorkbench(WorkBenchName)
            Toolbaritems.update(CustomPanelCommands)

            # Get the commands in this toolbar
            ToolbarCommands = []
            for key in Toolbaritems:
                if key == Toolbar:
                    ToolbarCommands = Toolbaritems[key]

            # add separators to the command list.
            index = 0
            if WorkBenchName in self.Dict_RibbonCommandPanel["workbenches"]:
                if Toolbar != "" and Toolbar in self.Dict_RibbonCommandPanel["workbenches"][WorkBenchName]["toolbars"]:
                    if "order" in self.Dict_RibbonCommandPanel["workbenches"][WorkBenchName]["toolbars"][Toolbar]:
                        for j in range(
                            len(
                                self.Dict_RibbonCommandPanel["workbenches"][WorkBenchName]["toolbars"][Toolbar]["order"]
                            )
                        ):
                            if (
                                self.Dict_RibbonCommandPanel["workbenches"][WorkBenchName]["toolbars"][Toolbar][
                                    "order"
                                ][j]
                                .lower()
                                .__contains__("separator")
                            ):
                                ToolbarCommands.insert(
                                    j + index,
                                    self.Dict_RibbonCommandPanel["workbenches"][WorkBenchName]["toolbars"][Toolbar][
                                        "order"
                                    ][j],
                                )
                                index = index + 1

            # Sort the Toolbarcommands according the sorted list
            def SortCommands(item):
                try:
                    try:
                        if item.lower().__contains__("separator") is False:
                            MenuName = CommandInfoCorrections(item)["menuText"].replace("&", "").replace("...", "")
                            item = MenuName
                    except Exception:
                        pass
                    OrderList: list = self.Dict_RibbonCommandPanel["workbenches"][WorkBenchName]["toolbars"][Toolbar][
                        "order"
                    ]
                    position = OrderList.index(item)
                except Exception:
                    position = 999999

                return position

            ToolbarCommands.sort(key=SortCommands)

            # Go through the list of toolbar commands
            for ToolbarCommand in ToolbarCommands:
                if ToolbarCommand.__contains__("separator"):
                    # Create the row in the table
                    # add a row to the table widget
                    self.form.CommandTable_RD.insertRow(self.form.CommandTable_RD.rowCount())

                    # Define a table widget item
                    Separator = QTableWidgetItem()
                    Separator.setText("Separator")
                    Separator.setData(Qt.ItemDataRole.UserRole, "separator")

                    # Get the last rownumber and set this row with the CommandTable_RDItem
                    RowNumber = self.form.CommandTable_RD.rowCount() - 1
                    # update the data
                    Separator.setData(Qt.ItemDataRole.UserRole, f"{RowNumber}_separator_{WorkBenchName}")

                    # Add the first cell with the table widget
                    self.form.CommandTable_RD.setItem(RowNumber, 0, Separator)

                    # Create the second cell and set the checkstate according the checkstate as defined earlier
                    Icon_small = QTableWidgetItem()
                    Icon_small.setText("")
                    self.form.CommandTable_RD.setItem(RowNumber, 1, Icon_small)

                    # Create the third cell and set the checkstate according the checkstate as defined earlier
                    Icon_medium = QTableWidgetItem()
                    Icon_medium.setText("")
                    self.form.CommandTable_RD.setItem(RowNumber, 2, Icon_medium)

                    # Create the last cell and set the checkstate according the checkstate as defined earlier
                    Icon_large = QTableWidgetItem()
                    Icon_large.setText("")
                    self.form.CommandTable_RD.setItem(RowNumber, 3, Icon_large)

                    # Define the order based on the order in this table widget
                    Order = []
                    for j in range(self.form.CommandTable_RD.rowCount()):
                        Order.append(
                            QTableWidgetItem(self.form.CommandTable_RD.item(j, 0)).data(Qt.ItemDataRole.UserRole)
                        )

                    # Add or update the dict for the Ribbon command panel
                    StandardFunctions.add_keys_nested_dict(
                        self.Dict_RibbonCommandPanel,
                        ["workbenches", WorkBenchName, "toolbars", Toolbar, "order"],
                    )
                    self.Dict_RibbonCommandPanel["workbenches"][WorkBenchName]["toolbars"][Toolbar]["order"] = Order

                if not ToolbarCommand.__contains__("separator") and not ToolbarCommand.__contains__("All"):
                    # Get the command
                    CommandName = ToolbarCommand

                    # Check if the items is already there
                    IsInList = ShadowList.__contains__(f"{CommandName}, {WorkBenchName}")
                    # if not, continue
                    if IsInList is False and CommandName is not None:
                        # Get the untranslated text
                        MenuName = CommandInfoCorrections(CommandName)["menuText"].replace("&", "").replace("...", "")
                        if MenuName == "":
                            continue

                        textAddition = ""
                        IconName = ""
                        # get the icon for this command if there isn't one, leave it None
                        IconName = CommandInfoCorrections(CommandName)["pixmap"]
                        Icon = StandardFunctions.returnQiCons_Commands(CommandName, IconName)

                        # Set the default check states
                        checked_small = Qt.CheckState.Checked
                        checked_medium = Qt.CheckState.Unchecked
                        checked_large = Qt.CheckState.Unchecked
                        # set the default size
                        Size = "small"

                        # Go through the toolbars in the Json Ribbon list
                        MenuNameJson = ""
                        for j in range(len(self.List_Workbenches)):
                            if self.List_Workbenches[j][0] == WorkBenchName:
                                try:
                                    MenuNameJson = self.Dict_RibbonCommandPanel["workbenches"][WorkBenchName][
                                        "toolbars"
                                    ][Toolbar]["commands"][CommandName]["text"]
                                    Size = self.Dict_RibbonCommandPanel["workbenches"][WorkBenchName]["toolbars"][
                                        Toolbar
                                    ]["commands"][CommandName]["size"]

                                    if Size == "medium":
                                        checked_small = Qt.CheckState.Unchecked
                                        checked_medium = Qt.CheckState.Checked
                                        checked_large = Qt.CheckState.Unchecked
                                    if Size == "large":
                                        checked_small = Qt.CheckState.Unchecked
                                        checked_medium = Qt.CheckState.Unchecked
                                        checked_large = Qt.CheckState.Checked
                                    Icon_Json_Name = self.Dict_RibbonCommandPanel["workbenches"][WorkBenchName][
                                        "toolbars"
                                    ][Toolbar]["commands"][CommandName]["icon"]
                                    Icon = StandardFunctions.returnQiCons_Commands(CommandName, Icon_Json_Name)
                                except Exception:
                                    continue

                        MenuNameTabelWidgetItem = ""
                        if MenuNameJson != CommandInfoCorrections(ToolbarCommand)["menuText"].replace("&", "").replace(
                            "...", ""
                        ):
                            MenuNameTabelWidgetItem = MenuNameJson
                        else:
                            for CommandItem in self.List_Commands:
                                if CommandItem[0] == CommandName:
                                    MenuNameTabelWidgetItem = StandardFunctions.CommandInfoCorrections(CommandName)[
                                        "ActionText"
                                    ]

                        # Create the row in the table
                        # add a row to the table widget
                        self.form.CommandTable_RD.insertRow(self.form.CommandTable_RD.rowCount())

                        # Fill the table widget ----------------------------------------------------------------------------------
                        #
                        # Define a table widget item
                        CommandWidgetItem = QTableWidgetItem()
                        CommandWidgetItem.setText((MenuNameTabelWidgetItem + textAddition).replace("&", ""))
                        CommandWidgetItem.setData(
                            Qt.ItemDataRole.UserRole,
                            MenuName.replace("&", "").replace("...", ""),
                        )
                        CommandWidgetItem.setFlags(CommandWidgetItem.flags() | Qt.ItemFlag.ItemIsEditable)
                        if Icon is not None:
                            CommandWidgetItem.setIcon(Icon)
                        if Icon is None:
                            CommandWidgetItem.setFlags(CommandWidgetItem.flags() & ~Qt.ItemFlag.ItemIsEnabled)
                        # Get the last rownumber and set this row with the CommandTable_RDItem
                        RowNumber = self.form.CommandTable_RD.rowCount() - 1

                        # Add the first cell with the table widget
                        self.form.CommandTable_RD.setItem(RowNumber, 0, CommandWidgetItem)

                        # Create the second cell and set the checkstate according the checkstate as defined earlier
                        Icon_small = QTableWidgetItem()
                        Icon_small.setCheckState(checked_small)
                        self.form.CommandTable_RD.setItem(RowNumber, 1, Icon_small)

                        # Create the third cell and set the checkstate according the checkstate as defined earlier
                        Icon_medium = QTableWidgetItem()
                        Icon_medium.setCheckState(checked_medium)
                        self.form.CommandTable_RD.setItem(RowNumber, 2, Icon_medium)

                        # Create the last cell and set the checkstate according the checkstate as defined earlier
                        Icon_large = QTableWidgetItem()
                        Icon_large.setCheckState(checked_large)
                        self.form.CommandTable_RD.setItem(RowNumber, 3, Icon_large)

                        # Double check the workbench name
                        WorkbenchTitle = self.form.WorkbenchList_RD.currentData()
                        for item in self.List_Workbenches:
                            if item[2] == WorkbenchTitle:
                                WorkBenchName = item[0]

                        # Define the order based on the order in this table widget
                        Order = []
                        for j in range(self.form.CommandTable_RD.rowCount()):
                            Order.append(
                                QTableWidgetItem(self.form.CommandTable_RD.item(j, 0)).data(Qt.ItemDataRole.UserRole)
                            )

                        # Add or update the dict for the Ribbon command panel
                        StandardFunctions.add_keys_nested_dict(
                            self.Dict_RibbonCommandPanel,
                            ["workbenches", WorkBenchName, "toolbars", Toolbar, "order"],
                        )
                        StandardFunctions.add_keys_nested_dict(
                            self.Dict_RibbonCommandPanel,
                            [
                                "workbenches",
                                WorkBenchName,
                                "toolbars",
                                Toolbar,
                                "commands",
                                CommandName,
                            ],
                        )
                        self.Dict_RibbonCommandPanel["workbenches"][WorkBenchName]["toolbars"][Toolbar]["order"] = Order
                        self.Dict_RibbonCommandPanel["workbenches"][WorkBenchName]["toolbars"][Toolbar]["commands"][
                            CommandName
                        ] = {
                            "size": Size,
                            "text": MenuName,
                            "icon": IconName,
                        }

                        # Set the IconOnly_Toolbars control
                        IsInList = False
                        for item in self.List_IconOnly_Toolbars:
                            if item == Toolbar:
                                IsInList = True
                        if IsInList is True:
                            self.form.IconOnly_RD.setCheckState(Qt.CheckState.Checked)
                        else:
                            self.form.IconOnly_RD.setCheckState(Qt.CheckState.Unchecked)

                        # Add the command to the shadow list
                        ShadowList.append(f"{CommandName}, {WorkBenchName}")
        return

    def on_AddSeparator_RD_clicked(self):
        # Get the correct workbench name
        WorkBenchName = ""
        for WorkBench in self.List_Workbenches:
            if WorkBench[2] == self.form.WorkbenchList_RD.currentData():
                WorkBenchName = WorkBench[0]

        # Get the toolbar name
        Toolbar = self.form.PanelList_RD.currentData()

        # Define a table widget item
        CommandTable_RDItem = QTableWidgetItem()
        CommandTable_RDItem.setText("Separator")
        CommandTable_RDItem.setData(Qt.ItemDataRole.UserRole, "separator")

        # Get the last rownumber and set this row with the CommandTable_RDItem
        RowNumber = self.form.CommandTable_RD.rowCount()
        if len(self.form.CommandTable_RD.selectedItems()) > 0:
            RowNumber = self.form.CommandTable_RD.currentRow()
        # # update the data
        CommandTable_RDItem.setData(Qt.ItemDataRole.UserRole, f"{RowNumber}_separator_{WorkBenchName}")
        self.form.CommandTable_RD.insertRow(RowNumber)

        # Add the first cell with the table widget
        self.form.CommandTable_RD.setItem(RowNumber, 0, CommandTable_RDItem)

        # Create the second cell and set the checkstate according the checkstate as defined earlier
        Icon_small = QTableWidgetItem()
        Icon_small.setText("")
        self.form.CommandTable_RD.setItem(RowNumber, 1, Icon_small)

        # Create the third cell and set the checkstate according the checkstate as defined earlier
        Icon_medium = QTableWidgetItem()
        Icon_medium.setText("")
        self.form.CommandTable_RD.setItem(RowNumber, 2, Icon_medium)

        # Create the last cell and set the checkstate according the checkstate as defined earlier
        Icon_large = QTableWidgetItem()
        Icon_large.setText("")
        self.form.CommandTable_RD.setItem(RowNumber, 3, Icon_large)

        self.form.CommandTable_RD.selectRow(RowNumber)

        # Double check the workbench name
        WorkbenchTitle = self.form.WorkbenchList_RD.currentData()
        for item in self.List_Workbenches:
            if item[2] == WorkbenchTitle:
                WorkBenchName = item[0]

        # Define the order based on the order in this table widget
        Order = []
        for i in range(self.form.CommandTable_RD.rowCount()):
            Order.append(QTableWidgetItem(self.form.CommandTable_RD.item(i, 0)).data(Qt.ItemDataRole.UserRole))

        # Add or update the dict for the Ribbon command panel
        StandardFunctions.add_keys_nested_dict(
            self.Dict_RibbonCommandPanel,
            ["workbenches", WorkBenchName, "toolbars", Toolbar, "order"],
        )
        self.Dict_RibbonCommandPanel["workbenches"][WorkBenchName]["toolbars"][Toolbar]["order"] = Order
        return

    def on_RemoveSeparator_RD_clicked(self):
        self.Remove_TableItem(self.form.CommandTable_RD, "separator")

        # Enable the apply button
        if self.CheckChanges() is True:
            self.form.UpdateJson.setEnabled(True)

        return

    def on_IconOnly_RD_clicked(self):
        if self.form.IconOnly_RD.isChecked() is True:
            toolbar = self.form.PanelList_RD.currentData()

            isInList = False
            for item in self.List_IconOnly_Toolbars:
                if item == toolbar:
                    isInList = True

            if isInList is False:
                self.List_IconOnly_Toolbars.append(toolbar)

        if self.form.IconOnly_RD.isChecked() is False:
            toolbar = self.form.PanelList_RD.currentData()

            isInList = False
            for item in self.List_IconOnly_Toolbars:
                if item == toolbar:
                    isInList = True

            if isInList is True:
                self.List_IconOnly_Toolbars.remove(toolbar)

        # Enable the apply button
        if self.CheckChanges() is True:
            self.form.UpdateJson.setEnabled(True)

        return

    def on_TableCell_RD_changed(self, Item):
        text = Item.text()
        if text == "":
            Item.setText(Item.data(Qt.ItemDataRole.UserRole))

        # Update the data with the (text)changed
        self.UpdateData()
        # Update the order of the commands
        self.on_PanelOrder_RD_changed()

        # Enable the apply button
        if self.CheckChanges() is True:
            self.form.UpdateJson.setEnabled(True)

        return

    def on_TableCell_RD_clicked(self, Item):
        # Get the row and column of the clicked item (cell)
        row = Item.row()
        column = Item.column()
        if column == 0:
            return

        # Go through the cells in the first row. If checkstate is checked, uncheck the other cells in all other rows
        CheckState = self.form.CommandTable_RD.item(row, column).checkState()
        if row == 0:
            for i1 in range(1, self.form.CommandTable_RD.columnCount()):
                if CheckState == Qt.CheckState.Checked:
                    if i1 == column:
                        self.form.CommandTable_RD.item(0, i1).setCheckState(Qt.CheckState.Checked)
                    else:
                        self.form.CommandTable_RD.item(0, i1).setCheckState(Qt.CheckState.Unchecked)
                for i2 in range(1, self.form.CommandTable_RD.rowCount()):
                    if i1 == column:
                        self.form.CommandTable_RD.item(i2, i1).setCheckState(CheckState)
                    if i1 != column:
                        self.form.CommandTable_RD.item(i2, i1).setCheckState(Qt.CheckState.Unchecked)

        # else:
        # Get the checkedstate from the clicked cell
        CheckState = self.form.CommandTable_RD.item(row, column).checkState()
        # Go through the cells in the row. If checkstate is checked, uncheck the other cells in the row
        for i3 in range(1, self.form.CommandTable_RD.columnCount()):
            if CheckState == Qt.CheckState.Checked:
                if i3 == column:
                    self.form.CommandTable_RD.item(row, i3).setCheckState(Qt.CheckState.Checked)
                else:
                    self.form.CommandTable_RD.item(row, i3).setCheckState(Qt.CheckState.Unchecked)

        # Update the data
        self.UpdateData()
        # Update the order of the commands
        self.on_PanelOrder_RD_changed()

        # Enable the apply button
        if self.CheckChanges() is True:
            self.form.UpdateJson.setEnabled(True)

        return

    def on_MoveUpCommandTable_RD_clicked(self):
        self.MoveItem_CommandTable(self.form.CommandTable_RD, True)

        # Enable the apply button
        if self.CheckChanges() is True:
            self.form.UpdateJson.setEnabled(True)

        return

    def on_MoveDownCommandTable_RD_clicked(self):
        self.MoveItem_CommandTable(self.form.CommandTable_RD, False)

        # Enable the apply button
        if self.CheckChanges() is True:
            self.form.UpdateJson.setEnabled(True)

        return

    def on_MoveUpPanel_RD_clicked(self):
        self.MoveItem(self.form.PanelOrder_RD, True)
        self.on_PanelOrder_RD_changed()

        # Enable the apply button
        if self.CheckChanges() is True:
            self.form.UpdateJson.setEnabled(True)

        return

    def on_MoveDownPanel_RD_clicked(self):
        self.MoveItem(self.form.PanelOrder_RD, False)
        self.on_PanelOrder_RD_changed()

        # Enable the apply button
        if self.CheckChanges() is True:
            self.form.UpdateJson.setEnabled(True)

        return

    def on_PanelOrder_RD_changed(self):
        # Get the correct workbench name
        WorkBenchName = ""
        for WorkBench in self.List_Workbenches:
            if WorkBench[2] == self.form.WorkbenchList_RD.currentData()[2]:
                WorkBenchName = WorkBench[0]

        ToolbarOrder = []
        for i2 in range(self.form.PanelOrder_RD.count()):
            Toolbar = self.form.PanelOrder_RD.item(i2).data(Qt.ItemDataRole.UserRole)
            ToolbarOrder.append(Toolbar)
        StandardFunctions.add_keys_nested_dict(
            self.Dict_RibbonCommandPanel,
            [
                "workbenches",
                WorkBenchName,
                "toolbars",
                "order",
            ],
        )
        self.Dict_RibbonCommandPanel["workbenches"][WorkBenchName]["toolbars"]["order"] = ToolbarOrder

        return

    # endregion

    # region - Form buttons tab
    def on_RestoreJson_clicked(self):
        self.form.setWindowFlags(Qt.WindowType.WindowStaysOnBottomHint)
        # get the path for the Json file
        JsonPath = os.path.dirname(__file__)
        JsonFile = os.path.join(JsonPath, "RibbonStructure.json")

        BackupFiles = []
        # returns a list of names (with extension, without full path) of all files
        # in backup path
        for name in os.listdir(pathBackup):
            if os.path.isfile(os.path.join(pathBackup, name)):
                if name.lower().endswith("json"):
                    BackupFiles.append(name)

        if len(BackupFiles) > 0:
            SelectedFile = StandardFunctions.Mbox(
                translate("FreeCAD Ribbon", "Select a backup file"),
                "",
                21,
                "NoIcon",
                BackupFiles[0],
                BackupFiles,
            )
            BackupFile = os.path.join(pathBackup, SelectedFile)
            result = shutil.copy(BackupFile, JsonFile)
            StandardFunctions.Print(
                translate("FreeCAD Ribbon", "Ribbon bar set back to settings from: ") + f"{result}!",
                "Warning",
            )

            message = (
                translate("FreeCAD Ribbon", "Settings reset to ")
                + SelectedFile
                + "!\n"
                + translate(
                    "FreeCAD Ribbon",
                    "You must restart FreeCAD for changes to take effect.",
                )
            )
            answer = StandardFunctions.RestartDialog(message=message)
            if answer == "yes":
                StandardFunctions.restart_freecad()

        self.form.close()
        return

    def on_ResetJson_clicked(self):
        self.form.setWindowFlags(Qt.WindowType.WindowStaysOnBottomHint)
        # get the path for the Json file
        JsonPath = os.path.dirname(__file__)
        JsonFile = os.path.join(JsonPath, "RibbonStructure.json")

        BackupFile = os.path.join(JsonPath, "RibbonStructure_default.json")

        message = (
            translate("FreeCAD Ribbon", "Settings reset to default!")
            + "\n"
            + translate("FreeCAD Ribbon", "You must restart FreeCAD for changes to take effect.")
        )

        result = shutil.copy(BackupFile, JsonFile)
        StandardFunctions.Print(
            translate("FreeCAD Ribbon", "Ribbon bar reset from ") + f"{result}!",
            "Warning",
        )
        answer = StandardFunctions.RestartDialog(message=message)
        if answer == "yes":
            StandardFunctions.restart_freecad()

        self.form.close()
        return

    @staticmethod
    def on_UpdateJson_clicked(self):
        self.WriteJson()
        # Set the button disabled
        self.form.UpdateJson.setDisabled(True)
        return

    @staticmethod
    def on_Close_clicked(self):
        self.WriteJson()
        # Close the form
        self.form.close()

        # show the restart dialog
        result = StandardFunctions.RestartDialog(includeIcons=True)
        if result == "yes":
            StandardFunctions.restart_freecad()
        return

    @staticmethod
    def on_Cancel_clicked(self):
        # Close the form
        self.form.close()
        return

    @staticmethod
    def on_Helpbutton_clicked(self):
        if self.ReproAdress != "" or self.ReproAdress is not None:
            if not self.ReproAdress.endswith("/"):
                self.ReproAdress = self.ReproAdress + "/"

            AboutAdress = self.ReproAdress + "wiki"
            webbrowser.open(AboutAdress, new=2, autoraise=True)
        return

    # endregion

    # endregion---------------------------------------------------------------------------------------

    # region - Functions------------------------------------------------------------------------------
    def addWorkbenches(self):
        """Fill the Workbenches available, selected and workbench list"""
        self.form.WorkbenchList_RD.clear()
        self.form.WorkbenchesAvailable_IW.clear()
        self.form.WorkbenchesSelected_IW.clear()
        self.form.WorkbenchList_CP.clear()
        self.form.WorkbenchList_IS.clear()

        # Add "All" to the categoryListWidgets
        All_KeyWord = translate("FreeCAD Ribbon", "All")
        self.form.ListCategory_QC.addItem(All_KeyWord)
        self.form.ListCategory_EP.addItem(All_KeyWord)

        for workbench in self.List_Workbenches:
            WorkbenchName = workbench[0]
            WorkbenchTitle = workbench[2]
            # Default a workbench is selected
            # if in List_IgnoredWorkbenches, set IsSelected to false
            IsSelected = True
            for IgnoredWorkbench in self.List_IgnoredWorkbenches:
                if workbench[2] == IgnoredWorkbench:
                    IsSelected = False

            # Define a new ListWidgetItem.
            ListWidgetItem = QListWidgetItem()
            ListWidgetItem.setText(StandardFunctions.TranslationsMapping(WorkbenchName, WorkbenchTitle))
            ListWidgetItem.setData(Qt.ItemDataRole.UserRole, workbench)
            Icon = QIcon()
            for item in self.List_WorkBenchIcons:
                if item[0] == WorkbenchName:
                    Icon = item[1]
            if Icon is None:
                Icon = Gui.getIcon(workbench[1])

            if Icon is not None:
                ListWidgetItem.setIcon(Icon)

            # Add the ListWidgetItem to the correct ListWidget
            if IsSelected is False:
                self.form.WorkbenchesAvailable_IW.addItem(ListWidgetItem)
            if IsSelected is True:
                # Add the listwidgetItem to all workbench listwidgets
                self.form.WorkbenchList_IS.addItem(ListWidgetItem)
                self.form.WorkbenchesSelected_IW.addItem(ListWidgetItem)
                self.form.WorkbenchList_RD.addItem(
                    Icon,
                    StandardFunctions.TranslationsMapping(WorkbenchName, workbench[2]),
                    workbench[2],
                )
                # Add the ListWidgetItem also to the second WorkbenchList_RD.
                self.form.WorkbenchList_CP.addItem(
                    Icon,
                    StandardFunctions.TranslationsMapping(WorkbenchName, workbench[2]),
                    workbench[2],
                )  # Add the ListWidgetItem also to the second WorkbenchList_RD.
                self.form.WorkbenchList_NP.addItem(
                    Icon,
                    StandardFunctions.TranslationsMapping(WorkbenchName, workbench[2]),
                    workbench[2],
                )

            # Add the ListWidgetItem also to the categoryListWidgets
            self.form.ListCategory_QC.addItem(
                Icon,
                StandardFunctions.TranslationsMapping(WorkbenchName, workbench[2]),
                workbench[2],
            )
            self.form.ListCategory_EP.addItem(
                Icon,
                StandardFunctions.TranslationsMapping(WorkbenchName, workbench[2]),
                workbench[2],
            )
            self.form.ListCategory_NP.addItem(
                Icon,
                StandardFunctions.TranslationsMapping(WorkbenchName, workbench[2]),
                workbench[2],
            )
            self.form.ListCategory_DDB.addItem(
                Icon,
                StandardFunctions.TranslationsMapping(WorkbenchName, workbench[2]),
                workbench[2],
            )

        self.form.ListCategory_QC.setCurrentText(All_KeyWord)
        self.form.ListCategory_EP.setCurrentText(All_KeyWord)
        self.form.ListCategory_NP.setCurrentText(All_KeyWord)

        # Set the text in the combobox to the name of the active workbench
        self.form.WorkbenchList_RD.setCurrentText(
            StandardFunctions.TranslationsMapping(WorkbenchName, Gui.activeWorkbench().name())
        )
        self.form.WorkbenchList_CP.setCurrentText(
            StandardFunctions.TranslationsMapping(WorkbenchName, Gui.activeWorkbench().name())
        )

        return

    def ExcludedToolbars(self):
        self.form.PanelsToExclude_EP.clear()
        self.form.PanelsExcluded_EP.clear()

        for Toolbar in self.StringList_Toolbars:
            IsSelected = False
            for IgnoredToolbar in self.List_IgnoredToolbars:
                if Toolbar[0] == IgnoredToolbar:
                    IsSelected = True

            if Toolbar[0] != "":
                WorkbenchName = Toolbar[2]
                ListWidgetItem = QListWidgetItem()
                ListWidgetItem.setText(StandardFunctions.TranslationsMapping(WorkbenchName, Toolbar[0]))
                ListWidgetItem.setData(Qt.ItemDataRole.UserRole, Toolbar)
                if IsSelected is False:
                    IsInlist = False
                    for i in range(self.form.PanelsToExclude_EP.count()):
                        ToolbarItem = self.form.PanelsToExclude_EP.item(i)
                        if ToolbarItem.text() == StandardFunctions.TranslationsMapping(WorkbenchName, Toolbar[0]):
                            IsInlist = True

                    if IsInlist is False:
                        self.form.PanelsToExclude_EP.addItem(ListWidgetItem)
                if IsSelected is True:
                    IsInlist = False
                    for i in range(self.form.PanelsExcluded_EP.count()):
                        ToolbarItem = self.form.PanelsExcluded_EP.item(i)
                        if ToolbarItem.text() == StandardFunctions.TranslationsMapping(WorkbenchName, Toolbar[0]):
                            IsInlist = True

                    if IsInlist is False:
                        self.form.PanelsExcluded_EP.addItem(ListWidgetItem)
        return

    def QuickAccessCommands(self):
        """Fill the Quick Commands Available and Selected"""
        self.form.CommandsAvailable_QC.clear()
        self.form.CommandsSelected_QC.clear()

        ShadowList = []  # List to add the commands and prevent duplicates
        IsInList = False

        for ToolbarCommand in self.List_Commands:
            IsInList = ShadowList.__contains__(ToolbarCommand[0])

            if IsInList is False:
                CommandName = ToolbarCommand[0]
                # Command = Gui.Command.get(CommandName)
                MenuName = StandardFunctions.CommandInfoCorrections(CommandName)["ActionText"]
                workbenchName = ToolbarCommand[3]

                # Default a command is not selected
                IsSelected = False and workbenchName != "Global"
                for QuickCommand in self.List_QuickAccessCommands:
                    if ToolbarCommand[0] == QuickCommand:
                        IsSelected = True

                if MenuName != "":
                    # Define a new ListWidgetItem.
                    textAddition = ""
                    Icon = QIcon()
                    for item in self.List_CommandIcons:
                        if item[0] == ToolbarCommand[0]:
                            Icon = item[1]
                    if Icon is None:
                        IconName = ToolbarCommand[1]
                        Icon = StandardFunctions.returnQiCons_Commands(CommandName, IconName)

                    ListWidgetItem = QListWidgetItem()
                    ListWidgetItem.setText((MenuName + textAddition).replace("&", ""))
                    if Icon is not None:
                        ListWidgetItem.setIcon(Icon)
                    ListWidgetItem.setToolTip(CommandName)  # Use the tooltip to store the actual command.
                    ListWidgetItem.setData(Qt.ItemDataRole.UserRole, CommandName)

                    # Add the ListWidgetItem to the correct ListWidget
                    if Icon is not None:
                        if IsSelected is False:
                            IsInlist = False
                            for i in range(self.form.CommandsAvailable_QC.count()):
                                CommandItem = self.form.CommandsAvailable_QC.item(i)
                                if CommandItem.text() == MenuName:
                                    IsInlist = True

                            if IsInlist is False:
                                self.form.CommandsAvailable_QC.addItem(ListWidgetItem)
                        if IsSelected is True:
                            IsInlist = False
                            for i in range(self.form.CommandsSelected_QC.count()):
                                CommandItem = self.form.CommandsSelected_QC.item(i)
                                if CommandItem.text() == MenuName:
                                    IsInlist = True

                            if IsInlist is False:
                                self.form.CommandsSelected_QC.addItem(ListWidgetItem)
            ShadowList.append(ToolbarCommand[0])
        return

    def UpdateData(self):
        for i1 in range(1, self.form.CommandTable_RD.rowCount()):
            row = i1

            WorkbenchTitle = self.form.WorkbenchList_RD.currentText()
            WorkBenchName = ""
            try:
                for WorkbenchItem in self.List_Workbenches:
                    if WorkbenchItem[2] == WorkbenchTitle:
                        WorkBenchName = WorkbenchItem[0]

                        # get the name of the toolbar
                        Toolbar = self.form.PanelList_RD.currentData()
                        # create a empty size string
                        Size = "small"
                        # Define empty strings for the command name and icon name
                        CommandName = ""
                        IconName = ""
                        # # Get the command text from the first cell in the row
                        # MenuNameCommandTable_RDItem = (
                        #     self.form.CommandTable_RD.item(row, 0).text().replace("&", "").replace("...", "")
                        # )
                        # Get the menu name from the stored data
                        MenuName = self.form.CommandTable_RD.item(row, 0).data(Qt.ItemDataRole.UserRole)

                        # Go through the list with all available commands.
                        # If the commandText is in this list, get the command name.
                        for i3 in range(len(self.List_Commands)):
                            if MenuName == self.List_Commands[i3][2]:
                                if WorkBenchName == self.List_Commands[i3][3] or self.List_Commands[i3][3] == "Global":
                                    CommandName = self.List_Commands[i3][0]
                                    # Command = Gui.Command.get(CommandName)
                                    IconName = self.List_Commands[i3][1]

                                    # Go through the cells in the row. If checkstate is checked, uncheck the other cells in the row
                                    for i6 in range(1, self.form.CommandTable_RD.columnCount()):
                                        CheckState = self.form.CommandTable_RD.item(row, i6).checkState()
                                        if CheckState == Qt.CheckState.Checked:
                                            if i6 == 1:
                                                Size = "small"
                                            if i6 == 2:
                                                Size = "medium"
                                            if i6 == 3:
                                                Size = "large"

                                    Order = []
                                    for i7 in range(1, self.form.CommandTable_RD.rowCount()):
                                        Order.append(
                                            QTableWidgetItem(self.form.CommandTable_RD.item(i7, 0)).data(
                                                Qt.ItemDataRole.UserRole
                                            )
                                        )

                                    StandardFunctions.add_keys_nested_dict(
                                        self.Dict_RibbonCommandPanel,
                                        [
                                            "workbenches",
                                            WorkBenchName,
                                            "toolbars",
                                            Toolbar,
                                            "order",
                                        ],
                                    )
                                    StandardFunctions.add_keys_nested_dict(
                                        self.Dict_RibbonCommandPanel,
                                        [
                                            "workbenches",
                                            WorkBenchName,
                                            "toolbars",
                                            Toolbar,
                                            "commands",
                                            CommandName,
                                        ],
                                    )

                                    self.Dict_RibbonCommandPanel["workbenches"][WorkBenchName]["toolbars"][Toolbar][
                                        "order"
                                    ] = Order
                                    self.Dict_RibbonCommandPanel["workbenches"][WorkBenchName]["toolbars"][Toolbar][
                                        "commands"
                                    ][CommandName] = {
                                        "size": Size,
                                        "text": MenuName,
                                        "icon": IconName,
                                    }
            except Exception as e:
                if Parameters_Ribbon.DEBUG_MODE is True:
                    print(f"{CommandName}, {WorkBenchName} {e}")
                continue
        return

    def ReadJson(self):
        """Read the Json file and fill the lists and set settings"""
        # Open the JsonFile and load the data
        JsonFile = open(os.path.join(os.path.dirname(__file__), "RibbonStructure.json"))
        data = json.load(JsonFile)

        # Get all the ignored toolbars
        for IgnoredToolbar in data["ignoredToolbars"]:
            self.List_IgnoredToolbars.append(IgnoredToolbar)

        # Get all the icon only toolbars
        for IconOnly_Toolbar in data["iconOnlyToolbars"]:
            self.List_IconOnly_Toolbars.append(IconOnly_Toolbar)

        # Get all the quick access command
        for QuickAccessCommand in data["quickAccessCommands"]:
            self.List_QuickAccessCommands.append(QuickAccessCommand)

        # Get all the ignored workbenches
        for IgnoredWorkbench in data["ignoredWorkbenches"]:
            self.List_IgnoredWorkbenches.append(IgnoredWorkbench)

        # Get all the custom toolbars
        try:
            self.Dict_CustomToolbars["customToolbars"] = data["customToolbars"]
        except Exception:
            pass

        # Get the dict with the customized date for the buttons
        try:
            self.Dict_RibbonCommandPanel["workbenches"] = data["workbenches"]
        except Exception:
            pass

        JsonFile.close()
        return

    def WriteJson(self):
        # get the system language
        # Get the current stylesheet for FreeCAD
        FreeCAD_preferences = App.ParamGet("User parameter:BaseApp/Preferences/General")
        FCLanguage = FreeCAD_preferences.GetString("Language")

        # Create the internal lists
        List_IgnoredToolbars = []
        List_IconOnly_Toolbars = []
        List_QuickAccessCommands = []
        List_IgnoredWorkbenches = []

        # IgnoredToolbars
        ExcludedToolbars = self.ListWidgetItems(self.form.PanelsExcluded_EP)
        for i1 in range(len(ExcludedToolbars)):
            ListWidgetItem: QListWidgetItem = ExcludedToolbars[i1]
            Toolbar = ListWidgetItem.data(Qt.ItemDataRole.UserRole)
            IgnoredToolbar = Toolbar[0]
            List_IgnoredToolbars.append(IgnoredToolbar)

        # IconOnly_Toolbars
        for IconOnly_Toolbar in self.List_IconOnly_Toolbars:
            IsInlist = False
            for item in List_IconOnly_Toolbars:
                if item == IconOnly_Toolbar:
                    IsInlist = True
            if IsInlist is False:
                List_IconOnly_Toolbars.append(IconOnly_Toolbar)

        # QuickAccessCommands
        SelectedCommands = self.ListWidgetItems(self.form.CommandsSelected_QC)
        for i2 in range(len(SelectedCommands)):
            ListWidgetItem: QListWidgetItem = SelectedCommands[i2]
            QuickAccessCommand = CommandInfoCorrections(ListWidgetItem.data(Qt.ItemDataRole.UserRole))["name"]
            List_QuickAccessCommands.append(QuickAccessCommand)

        # IgnoredWorkbences
        AvailableWorkbenches = self.ListWidgetItems(self.form.WorkbenchesAvailable_IW)
        for i3 in range(len(AvailableWorkbenches)):
            ListWidgetItem: QListWidgetItem = AvailableWorkbenches[i3]
            IgnoredWorkbench = ListWidgetItem.data(Qt.ItemDataRole.UserRole)
            List_IgnoredWorkbenches.append(IgnoredWorkbench[2])

        # Create a resulting dict
        resultingDict = {}
        # add the various lists to the resulting dict.
        resultingDict["language"] = FCLanguage
        resultingDict["ignoredToolbars"] = List_IgnoredToolbars
        resultingDict["iconOnlyToolbars"] = List_IconOnly_Toolbars
        resultingDict["quickAccessCommands"] = List_QuickAccessCommands
        resultingDict["ignoredWorkbenches"] = List_IgnoredWorkbenches
        resultingDict.update(self.Dict_CustomToolbars)

        # RibbonTabs
        # Get the Ribbon dictionary
        resultingDict.update(self.Dict_RibbonCommandPanel)

        # get the path for the Json file
        JsonFile = Parameters_Ribbon.RIBBON_STRUCTURE_JSON

        # create a copy and rename it as a backup if enabled
        if Parameters_Ribbon.ENABLE_BACKUP is True:
            Suffix = datetime.now().strftime("%Y%m%d_%H%M%S")
            BackupName = f"RibbonStructure_{Suffix}.json"
            if os.path.exists(pathBackup) is False:
                os.makedirs(pathBackup)
            BackupFile = os.path.join(pathBackup, BackupName)
            shutil.copy(JsonFile, BackupFile)

        # Writing to sample.json
        with open(JsonFile, "w") as outfile:
            json.dump(resultingDict, outfile, indent=4)

        outfile.close()
        return

    def ListWidgetItems(self, ListWidget: QListWidget) -> list:
        items = []
        for x in range(ListWidget.count()):
            items.append(ListWidget.item(x))

        return items

    def AddItem(self, SourceWidget: QListWidget, DestinationWidget: QListWidget):
        """Move a list item widgtet from one list to another

        Args:
            SourceWidget (QListWidget): _description_
            DestinationWidget (QListWidget): _description_
        """
        Values = SourceWidget.selectedItems()

        # Go through the items
        for Value in Values:
            # Get the item text
            DestinationItem = QListWidgetItem(Value)

            # Add the item to the list with current items
            DestinationWidget.addItem(DestinationItem)

            # Go through the items on the list with items to add.
            for i in range(SourceWidget.count()):
                # Get the item
                SourceItem = SourceWidget.item(i)
                # If the item is not none and the item text is equal to itemText,
                # remove it from the columns to add list.
                if SourceItem is not None:
                    if SourceItem.text() == DestinationItem.text():
                        SourceWidget.takeItem(i)

        return

    def MoveItem(self, ListWidget: QListWidget, Up: bool = True):
        # Get the current row
        Row = ListWidget.currentRow()
        # remove the current row
        Item = ListWidget.takeItem(Row)
        # Add the just removed row, one row higher on the list
        if Up is True:
            ListWidget.insertItem(Row - 1, Item)
            # Set the moved row, to the current row
            ListWidget.setCurrentRow(Row - 1)
        if Up is False:
            ListWidget.insertItem(Row + 1, Item)
            # Set the moved row, to the current row
            ListWidget.setCurrentRow(Row + 1)

        return

    def MoveItem_CommandTable(self, CommandTable: QTableWidget, Up: bool = True):
        row = CommandTable.currentRow()
        column = CommandTable.currentColumn()
        if Up is False:
            if row < CommandTable.rowCount() - 1:
                CommandTable.insertRow(row + 2)
                for i in range(CommandTable.columnCount()):
                    item = CommandTable.takeItem(row, i)
                    CommandTable.setItem(row + 2, i, item)
                    CommandTable.setCurrentCell(row + 2, column)
                CommandTable.removeRow(row)

        if Up is True:
            if row > 0:
                CommandTable.insertRow(row - 1)
                for i in range(CommandTable.columnCount()):
                    item = CommandTable.takeItem(row + 1, i)
                    CommandTable.setItem(row - 1, i, item)
                    CommandTable.setCurrentCell(row - 1, column)
                CommandTable.removeRow(row + 1)

        self.UpdateData()
        return

    def Remove_TableItem(self, CommandTable: QTableWidget, filter: str = ""):
        row = CommandTable.currentRow()
        if filter != "":
            if CommandTable.item(row, 0).text().lower() == "separator":
                CommandTable.removeRow(row)
        else:
            CommandTable.removeRow(row)

        # Get the correct workbench name
        WorkBenchName = ""
        for WorkBench in self.List_Workbenches:
            if WorkBench[2] == self.form.WorkbenchList_RD.currentData():
                WorkBenchName = WorkBench[0]

        # Get the toolbar name
        Toolbar = self.form.PanelList_RD.currentData()

        # Define the order based on the order in this table widget
        Order = []
        for i in range(CommandTable.rowCount()):
            Order.append(QTableWidgetItem(CommandTable.item(i, 0)).data(Qt.ItemDataRole.UserRole))

        # Add or update the dict for the Ribbon command panel
        StandardFunctions.add_keys_nested_dict(
            self.Dict_RibbonCommandPanel,
            ["workbenches", WorkBenchName, "toolbars", Toolbar, "order"],
        )
        self.Dict_RibbonCommandPanel["workbenches"][WorkBenchName]["toolbars"][Toolbar]["order"] = Order

        return

    def List_ReturnCustomToolbars(self):
        """
        Returns custom toolbars as a list.
        each item is a list with:
        [
            Name,
            Workbench Title,
            List of commands
        ]
        """
        # Get the main window of FreeCAD
        mw = Gui.getMainWindow()
        Toolbars = []

        List_Workbenches = Gui.listWorkbenches().copy()
        for WorkBenchName in List_Workbenches:
            WorkbenchTitle = Gui.getWorkbench(WorkBenchName).MenuText
            if str(WorkBenchName) != "" or WorkBenchName is not None:
                if str(WorkBenchName) != "NoneWorkbench":
                    # Get the custom toolbars for this workbench
                    CustomToolbars: list = App.ParamGet(
                        "User parameter:BaseApp/Workbench/" + WorkBenchName + "/Toolbar"
                    ).GetGroups()

                    for Group in CustomToolbars:
                        Parameter = App.ParamGet(
                            "User parameter:BaseApp/Workbench/" + WorkBenchName + "/Toolbar/" + Group
                        )
                        Name = Parameter.GetString("Name")

                        ListCommands = []
                        try:
                            # get list of all buttons in toolbar
                            TB = mw.findChildren(QToolBar, Name)
                            allButtons: list = TB[0].findChildren(QToolButton)
                            for button in allButtons:
                                if button.text() == "":
                                    continue

                                action = button.defaultAction()
                                if action is not None:
                                    Command = action.objectName()
                                    ListCommands.append(Command)

                            Toolbars.append([Name, WorkbenchTitle, ListCommands])
                        except Exception:
                            continue

        return Toolbars

    def List_ReturnCustomToolbars_Global(self):
        """
        Returns custom toolbars as a list.
        each item is a list with:
        [
            Name,
            Workbench Title,
            List of commands
        ]
        """
        # Get the main window of FreeCAD
        mw = Gui.getMainWindow()
        Toolbars = []

        # Get the custom toolbars for this workbench
        CustomToolbars: list = App.ParamGet("User parameter:BaseApp/Workbench/Global/Toolbar").GetGroups()

        for Group in CustomToolbars:
            Parameter = App.ParamGet("User parameter:BaseApp/Workbench/Global/Toolbar/" + Group)
            Name = Parameter.GetString("Name")

            ListCommands = []
            # get list of all buttons in toolbar
            try:
                TB = mw.findChildren(QToolBar, Name)
                allButtons: list = TB[0].findChildren(QToolButton)
                for button in allButtons:
                    if button.text() == "":
                        continue

                    action = button.defaultAction()
                    if action is not None:
                        Command = action.objectName()
                        ListCommands.append(Command)

                Toolbars.append([Name, "Global", ListCommands])
            except Exception:
                continue

        return Toolbars

    def Dict_ReturnCustomToolbars(self, WorkBenchName):
        """_summary_

        Args:
            WorkBenchName (string): the internal name of the workbench

        Returns:
            dict: a dict with the toolbar name as key and a list of commandnames as value
        """
        # Get the main window of FreeCAD
        mw = Gui.getMainWindow()
        Toolbars = {}

        if str(WorkBenchName) != "" or WorkBenchName is not None:
            if str(WorkBenchName) != "NoneWorkbench":
                # Get the custom toolbars for this workbench
                CustomToolbars: list = App.ParamGet(
                    "User parameter:BaseApp/Workbench/" + WorkBenchName + "/Toolbar"
                ).GetGroups()

                for Group in CustomToolbars:
                    Parameter = App.ParamGet("User parameter:BaseApp/Workbench/" + WorkBenchName + "/Toolbar/" + Group)
                    Name = Parameter.GetString("Name")

                    if Name != "":
                        ListCommands = []
                        # get list of all buttons in toolbar
                        try:
                            TB = mw.findChildren(QToolBar, Name)
                            allButtons: list = TB[0].findChildren(QToolButton)
                            for button in allButtons:
                                if button.text() == "":
                                    continue
                                action = button.defaultAction()
                                Command = action.objectName()
                                ListCommands.append(Command)

                                Toolbars[Name] = ListCommands
                        except Exception:
                            continue

        return Toolbars

    def Dict_ReturnCustomToolbars_Global(self):
        """_summary_
        Returns:
            dict: a dict with the toolbar name as key and a list of commandnames as value
        """
        # Get the main window of FreeCAD
        mw = Gui.getMainWindow()
        Toolbars = {}

        # Get the custom toolbars for this workbench
        CustomToolbars: list = App.ParamGet("User parameter:BaseApp/Workbench/Global/Toolbar").GetGroups()

        for Group in CustomToolbars:
            Parameter = App.ParamGet("User parameter:BaseApp/Workbench/Global/Toolbar/" + Group)
            Name = Parameter.GetString("Name")

            IsIgnored = False
            for ToolBar in self.List_IgnoredToolbars:
                if ToolBar == Name:
                    IsIgnored = True

            if Name != "" and IsIgnored is False:
                ListCommands = []
                # get list of all buttons in toolbar
                TB = mw.findChildren(QToolBar, Name)
                allButtons: list = TB[0].findChildren(QToolButton)
                for button in allButtons:
                    if button.text() == "":
                        continue
                    action = button.defaultAction()
                    Command = action.objectName()
                    ListCommands.append(Command)
                    Toolbars[Name] = ListCommands

        return Toolbars

    def List_AddCustomPanel_CPsToWorkbench(self, WorkBenchName):
        Toolbars = []

        if str(WorkBenchName) != "" or WorkBenchName is not None:
            if str(WorkBenchName) != "NoneWorkbench":
                try:
                    for CustomToolbar in self.Dict_CustomToolbars["customToolbars"][WorkBenchName]:
                        if len(self.Dict_CustomToolbars["customToolbars"][WorkBenchName]) > 0:
                            ListCommands = []
                            Commands = self.Dict_CustomToolbars["customToolbars"][WorkBenchName][CustomToolbar][
                                "commands"
                            ]

                            WorkbenchTitle = Gui.getWorkbench(WorkBenchName).MenuText

                            for key, value in list(Commands.items()):
                                for i in range(len(self.List_Commands)):
                                    if self.List_Commands[i][2] == key and self.List_Commands[i][3] == WorkBenchName:
                                        Command = self.List_Commands[i][0]
                                        ListCommands.append(Command)
                                    if self.List_Commands[i][2] == key and self.List_Commands[i][3] == "Global":
                                        Command = self.List_Commands[i][0]
                                        ListCommands.append(Command)

                                if self.List_IgnoredToolbars_internal.__contains__(value) is False:
                                    self.List_IgnoredToolbars_internal.append(f"{value}")

                            Toolbars.append([CustomToolbar, WorkbenchTitle, ListCommands])
                except Exception:
                    pass

        return Toolbars

    def Dict_AddCustomPanel_CPCommandsToWorkbench(self, WorkBenchName):
        Toolbars = {}

        try:
            for CustomToolbar in self.Dict_CustomToolbars["customToolbars"][WorkBenchName]:
                ListCommands = []
                Commands = self.Dict_CustomToolbars["customToolbars"][WorkBenchName][CustomToolbar]["commands"]

                for key, value in list(Commands.items()):
                    for i in range(len(self.List_Commands)):
                        if self.List_Commands[i][2] == key:
                            if self.List_Commands[i][3] == WorkBenchName or self.List_Commands[i][3] == "Global":
                                Command = self.List_Commands[i][0]
                                ListCommands.append(Command)

                        if self.List_IgnoredToolbars_internal.__contains__(value) is False:
                            self.List_IgnoredToolbars_internal.append(f"{value}")

                    Toolbars[CustomToolbar] = ListCommands
        except Exception:
            pass

        return Toolbars

    def CheckChanges(self):
        # Open the JsonFile and load the data
        JsonFile = open(os.path.join(os.path.dirname(__file__), "RibbonStructure.json"))
        data = json.load(JsonFile)

        IsChanged = False

        if data["ignoredToolbars"].sort() == self.List_IgnoredToolbars.sort():
            IsChanged = True
        if data["iconOnlyToolbars"].sort() == self.List_IconOnly_Toolbars.sort():
            IsChanged = True
        if data["quickAccessCommands"].sort() == self.List_QuickAccessCommands.sort():
            IsChanged = True
        if data["ignoredWorkbenches"].sort() == self.List_IgnoredWorkbenches.sort():
            IsChanged = True
        if data["customToolbars"] == self.Dict_CustomToolbars:
            IsChanged = True
        if data["workbenches"] == self.Dict_RibbonCommandPanel:
            IsChanged = True

        JsonFile.close()
        return IsChanged

    def SortedPanelList_RD(self, PanelList_RD: list, WorkBenchName):
        JsonOrderList = []
        try:
            if len(self.Dict_RibbonCommandPanel["workbenches"][WorkBenchName]["toolbars"]["order"]) > 0:
                JsonOrderList = self.Dict_RibbonCommandPanel["workbenches"][WorkBenchName]["toolbars"]["order"]
        except Exception:
            JsonOrderList = PanelList_RD

        def SortList(toolbar):
            if toolbar == "":
                return -1

            position = None
            try:
                position = JsonOrderList.index(toolbar)
            except ValueError:
                position = 999999
            return position

        PanelList_RD.sort(key=SortList)

        return PanelList_RD

    def LoadControls(self):
        # Clear all listWidgets
        self.form.WorkbenchList_RD.clear()
        self.form.WorkbenchesAvailable_IW.clear()
        self.form.WorkbenchesSelected_IW.clear()
        self.form.PanelsToExclude_EP.clear()
        self.form.PanelsExcluded_EP.clear()
        self.form.CommandsAvailable_QC.clear()
        self.form.CommandsSelected_QC.clear()
        self.form.PanelAvailable_CP.clear()
        self.form.PanelSelected_CP.clear()
        self.form.PanelOrder_RD.clear()

        # -- Ribbon design tab --
        # Add all workbenches to the ListItem Widget. In this case a dropdown list.
        self.addWorkbenches()
        # Add all toolbars of the selected workbench to the toolbar list(dropdown)
        self.on_WorkbenchList_RD__TextChanged()
        self.on_WorkbenchList_CP__activated(False)

        # load the commands in the table.
        self.on_PanelList_RD__TextChanged()

        # -- Excluded toolbars --
        self.ExcludedToolbars()

        # -- Quick access toolbar tab --
        # Add all commands to the listbox for the quick access toolbar
        self.QuickAccessCommands()

        # -- Custom panel tab --
        self.form.CustomToolbarSelector_CP.addItem(translate("FreeCAD Ribbon", "New"))
        try:
            for WorkBenchName in self.Dict_CustomToolbars["customToolbars"]:
                WorkBenchTitle = ""
                for WorkBenchItem in self.List_Workbenches:
                    if WorkBenchItem[0] == WorkBenchName:
                        WorkBenchTitle = WorkBenchItem[2]
                for CustomPanelTitle in self.Dict_CustomToolbars["customToolbars"][WorkBenchName]:
                    if WorkBenchTitle != "":
                        self.form.CustomToolbarSelector_CP.addItem(f"{CustomPanelTitle}, {WorkBenchTitle}")
        except Exception:
            pass

    def returnWorkBenchToolbars(self, WorkBenchName):
        wbToolbars = []
        try:
            for WorkBench in self.StringList_Toolbars:
                if WorkBench[2] == WorkBenchName:
                    wbToolbars.append(WorkBench[0])
        except Exception:
            Gui.activateWorkbench(WorkBenchName)
            wbToolbars: list = Gui.getWorkbench(WorkBenchName).listToolbars()
        return wbToolbars

    def returnToolbarCommands(self, WorkBenchName):
        try:
            for item in self.List_Workbenches:
                if item[0] == WorkBenchName:
                    return item[3]
        except Exception:
            Gui.activateWorkbench(WorkBenchName)
            Toolbars = Gui.getWorkbench(WorkBenchName).getToolbarItems()
            return Toolbars

    # def UpdateRibbonStructure(self):
    #     for WorkbenchItem in self.List_Workbenches:
    #         WorkBenchName = WorkbenchItem[0]
    #         ToolbarItems = WorkbenchItem[3]

    #         # Write the keys if they don't exist
    #         StandardFunctions.add_keys_nested_dict(
    #             self.Dict_RibbonCommandPanel, ["workbenches", WorkBenchName, "toolbars", "order"]
    #         )
    #         for Toolbar, Commands in ToolbarItems.items():
    #             # Set the toolbar order
    #             ToolbarOrder = self.Dict_RibbonCommandPanel["workbenches"][WorkBenchName]["toolbars"]["order"]
    #             if type(ToolbarOrder) is not list:
    #                 ToolbarOrder = []
    #             OrderedToolbar = ""
    #             IsInList = False
    #             for OrderedToolbar in ToolbarOrder:
    #                 if OrderedToolbar == Toolbar or Toolbar == "":
    #                     IsInList = True
    #             if IsInList is False:
    #                 ToolbarOrder.append(Toolbar)
    #             self.Dict_RibbonCommandPanel["workbenches"][WorkBenchName]["toolbars"]["order"] = ToolbarOrder

    #             # Write the keys if they don't exist
    #             StandardFunctions.add_keys_nested_dict(
    #                 self.Dict_RibbonCommandPanel,
    #                 ["workbenches", WorkBenchName, "toolbars", Toolbar, "order"],
    #             )
    #             for CommandName in Commands:
    #                 StandardFunctions.add_keys_nested_dict(
    #                     self.Dict_RibbonCommandPanel,
    #                     ["workbenches", WorkBenchName, "toolbars", Toolbar, "commands", CommandName],
    #                 )

    #                 # Set or update the command order
    #                 CommandOrder = self.Dict_RibbonCommandPanel["workbenches"][WorkBenchName]["toolbars"][Toolbar][
    #                     "order"
    #                 ]
    #                 if type(CommandOrder) is not list:
    #                     CommandOrder = []
    #                 IsInList = False
    #                 OrderedCommand = ""
    #                 for OrderedCommand in CommandOrder:
    #                     if (
    #                         OrderedCommand == CommandName
    #                         or OrderedCommand == ""
    #                         or str(OrderedCommand).__contains__("separator")
    #                     ):
    #                         IsInList = True
    #                 if IsInList is False:
    #                     CommandOrder.append(StandardFunctions.CommandInfoCorrections(CommandName)["ActionText"])
    #                 self.Dict_RibbonCommandPanel["workbenches"][WorkBenchName]["toolbars"][Toolbar][
    #                     "order"
    #                 ] = OrderedCommand

    #                 # Get the size. If size is "", set size to "small"
    #                 Size = ""
    #                 try:
    #                     Size = self.Dict_RibbonCommandPanel["workbenches"][WorkBenchName]["toolbars"][Toolbar][
    #                         "commands"
    #                     ][CommandName]["size"]
    #                 except Exception:
    #                     pass
    #                 if Size == "":
    #                     Size = "small"

    #                 # Get the Menutext. If empty, get the MenuText from FreeCAD
    #                 MenuText = ""
    #                 try:
    #                     MenuText = self.Dict_RibbonCommandPanel["workbenches"][WorkBenchName]["toolbars"][Toolbar][
    #                         "commands"
    #                     ][CommandName]["text"]
    #                 except Exception:
    #                     pass
    #                 if MenuText == "":
    #                     MenuText = StandardFunctions.CommandInfoCorrections(CommandName)["ActionText"]

    #                 # Get the IconNmae. If empty, get the IconNmae from FreeCAD
    #                 IconName = ""
    #                 try:
    #                     IconName = self.Dict_RibbonCommandPanel["workbenches"][WorkBenchName]["toolbars"][Toolbar][
    #                         "commands"
    #                     ][CommandName]["icon"]
    #                 except Exception:
    #                     pass
    #                 if IconName == "":
    #                     IconName = StandardFunctions.CommandInfoCorrections(CommandName)["pixmap"]

    #                 # Write the entries
    #                 self.Dict_RibbonCommandPanel["workbenches"][WorkBenchName]["toolbars"][Toolbar]["commands"][
    #                     CommandName
    #                 ] = {
    #                     "size": Size,
    #                     "text": MenuText,
    #                     "icon": IconName,
    #                 }
    #     return


def main():
    # Get the form
    Dialog = LoadDialog().form
    # Show the form
    Dialog.show()

    return
