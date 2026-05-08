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
    QToolBar,
    QToolButton,
    QDockWidget,
    QSizePolicy,
    QGridLayout,
    QHBoxLayout,
)
from PySide.QtGui import QIcon, QPixmap, QDragEnterEvent, QDragLeaveEvent, QDropEvent
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
import webbrowser

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
    ReproAdress: str = "" 
    # Create a list for the commands
    List_Commands = []
    # Create a dict for the dropdownbuttons and newPanels
    Dict_DropDownButtons = {}
    Dict_NewPanels = {}
    # Create the lists for the deserialized icons
    List_CommandIcons = []
    List_WorkBenchIcons = []
    
    # Create lists for the several list in the json file.
    List_IgnoredToolbars = []
    List_IconOnly_Toolbars = []
    List_QuickAccessCommands = []
    List_IgnoredWorkbenches = []
    Dict_RibbonCommandPanel = {}
    Dict_CustomToolbars = {}
    Dict_DropDownButtons = {}
    Dict_NewPanels = {}

    # Create a variable to state if the dialog is closed or not
    DialogClosed = False
    
    # Create a dict for the workbench
    workBenchDict = {}
    
    # Create varables for the current workbench title and name
    CurrentWorkBenchTitle = None
    CurrentWorkBenchName = None
    
    # Create a tomporary list for newly added dropdown buttons
    newDDBList = []
            
    def __init__(self, workBenchDict):
        super(LoadDialog, self).__init__()
        
        self.workBenchDict = workBenchDict

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
            for DropDownCommand, Commands in self.workBenchDict["dropdownButtons"].items():
                if isinstance(Commands, list):
                    CommandName = Commands[0][0]
                    IconName = ""
                    for CommandItem in self.List_Commands:
                        if CommandItem[0] == CommandName:
                            IconName = StandardFunctions.CommandInfoCorrections(CommandItem[1])["pixmap"]
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
                    del self.workBenchDict["dropdownButtons"]
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

        # endregion

        # Add the workbenches
        self.addWorkbenches()
        
        # Load the commands
        self.LoadCommands()
        
        # Add all toolbar to the listboxes for the panels
        self.LoadPanels()
        
        # Connect the filter for the quick commands on the quickcommands tab
        def FilterWorkbench_NP():
            self.on_ListCategory_NP_TextChanged()

        #
        # --- AddCOmmandsTab ------------------
        #
        # Connect the filter for the quick commands on the quickcommands tab
        self.form.ListCategory_NP.currentTextChanged.connect(FilterWorkbench_NP)
        # Connect the searchbar for the quick commands on the quick commands tab
        self.form.SearchBar_NP.textChanged.connect(
            self.on_SearchBar_NP_TextChanged
        )
        
        # Connect the "CreateNewPanel" button
        self.form.CreateNewPanel.clicked.connect(self.on_CreateNewPanel_clicked)        
        
        #
        # --- CombinePanelsTab ------------------
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
        self.form.AddPanel_CP.connect(
            self.form.AddPanel_CP, SIGNAL("clicked()"), self.on_AddPanel_CP_clicked
        )

        self.form.AddCustomPanel_CP.connect(
            self.form.AddCustomPanel_CP,
            SIGNAL("clicked()"),
            self.on_AddCustomPanel_CP_clicked,
        )

        # Connect custom toolbar selector on the Custom Panels Tab
        def CommandList_CP():
            self.on_CustomToolbarSelector_CP_activated()

        self.form.CustomToolbarSelector_CP.activated.connect(CommandList_CP)

        self.form.RemovePanel_CP.connect(
            self.form.RemovePanel_CP,
            SIGNAL("clicked()"),
            self.on_RemovePanel_CP_clicked,
        )
        
        self.form.WorkbenchList_CP.setHidden(True)
        self.form.label_7.setHidden(True)
        
        #
        # --- CreateDropDownButtonTab ----------------
        #
        # Connect the Create dropdown button
        self.form.CreateControl_DDB.connect(
            self.form.CreateControl_DDB,
            SIGNAL("clicked()"),
            self.on_CreateControl_DDB_clicked,
        )

        # Connect  dropdownselector on the create dropdown button Tab
        def CommandList_DDB():
            self.on_CommandList_DDB_activated()

        self.form.CommandList_DDB.activated.connect(CommandList_DDB)

        # Connect the remove dropdown button
        self.form.RemoveControl_DDB.connect(
            self.form.RemoveControl_DDB,
            SIGNAL("clicked()"),
            self.on_RemoveControl_DDB_clicked,
        )

        # Connect Add/Remove and move events to the buttons on the QuickAccess Tab
        self.form.AddCommand_DDB.connect(
            self.form.AddCommand_DDB,
            SIGNAL("clicked()"),
            self.on_AddCommand_DDB_clicked,
        )
        self.form.RemoveCommand_DDB.connect(
            self.form.RemoveCommand_DDB,
            SIGNAL("clicked()"),
            self.on_RemoveCommand_DDB_clicked,
        )
        self.form.MoveUpCommand_DDB.connect(
            self.form.MoveUpCommand_DDB,
            SIGNAL("clicked()"),
            self.on_MoveUpCommand_DDB_clicked,
        )
        self.form.MoveDownCommand_DDB.connect(
            self.form.MoveDownCommand_DDB,
            SIGNAL("clicked()"),
            self.on_MoveDownCommand_DDB_clicked,
        )

        # Connect the filter for the quick commands on the quickcommands tab
        def FilterWorkbench_DDB():
            self.on_ListCategory_DDB_TextChanged()

        # Connect the filter for the quick commands on the quickcommands tab
        self.form.ListCategory_DDB.currentTextChanged.connect(FilterWorkbench_DDB)
        # Connect the searchbar for the quick commands on the quick commands tab
        self.form.SearchBar_DDB.textChanged.connect(
            self.on_SearchBar_DDB_TextChanged
        )
        
        # --- Form controls ------------------
        #
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
        self.form.cancelButton_2.clicked.connect(self.on_Cancel_Clicked)
        self.form.okButton_2.clicked.connect(self.on_Ok_Clicked)
        
        # Connect the helpbutton
        self.form.HelpButton.setIcon(Gui.getIcon("help-browser"))
        self.form.HelpButton.clicked.connect(self.on_Helpbutton_clicked)
        
        # Set the correct workbench active and connect it with the tab change
        RibbonBar: FCBinding.ModernMenu = mw.findChild(FCBinding.ModernMenu, "Ribbon")
        RibbonBar.TabChanged.connect(self.setWB)
        self.setWB()
        
        # Hide the correct ok and cancel button when the form is docked or not
        if Parameters.DOCKED_DIALOGS is True:
            self.form.okButton.setHidden(True)
            self.form.cancelButton.setHidden(True)
        else:
            self.form.DockedButtonFrame.setHidden(True)
        
        # Set the first tab active
        self.form.tabWidget.setCurrentIndex(0)

        # Restore the cursor
        QApplication.restoreOverrideCursor()
        return        
        
    def addWorkbenches(self):
        ShadowList = []  # List to add the commands and prevent duplicates

        # Fill the Workbenches available, selected and workbench list
        self.form.ListCategory_NP.clear()
        self.form.ListCategory_DDB.clear()

        # Add "All" to the categoryListWidgets
        All_KeyWord = translate("FreeCAD Ribbon", "All")
        self.form.ListCategory_NP.addItem(All_KeyWord, "All", [All_KeyWord, "All", "All"])
        self.form.ListCategory_DDB.addItem(All_KeyWord, "All", [All_KeyWord, "All", "All"])
        
        # Add "Standard" to the list for the panels
        Standard_KeyWord = translate("FreeCAD Ribbon", "Standard")
        self.form.ListCategory_NP.addItem(Gui.getIcon("freecad"), Standard_KeyWord, [Standard_KeyWord, "Standard", "Standard"])
        self.form.ListCategory_DDB.addItem(Gui.getIcon("freecad"), Standard_KeyWord)

        self.List_Workbenches.sort()

        WorkbenchName =""
        for workbench in self.List_Workbenches:
            WorkbenchName = workbench[0]
            WorkbenchTitle = workbench[2]
            
            if WorkbenchTitle in self.List_IgnoredWorkbenches:
                continue

            if [WorkbenchName, WorkbenchTitle] not in ShadowList:
                 # Get the translate worbench title
                if len(workbench) == 5:
                    WorkbenchTitle = workbench[4]
                else:
                    WorkbenchTitle = workbench[2]

                # Define a new ListWidgetItem.
                Icon = QIcon()
                Icon = Gui.getIcon(workbench[1])
                if Icon.isNull() or Icon is None:
                    for item in self.List_WorkBenchIcons:
                        if item[0] == WorkbenchName:
                            Icon = item[1]       

                # Add the ListWidgetItem also to the categoryListWidgets
                self.form.ListCategory_NP.addItem(
                    Icon,
                    WorkbenchTitle,
                    workbench,
                )
                self.form.ListCategory_DDB.addItem(
                    Icon,
                    WorkbenchTitle,
                    workbench,
                )

            ShadowList.append([WorkbenchName, WorkbenchTitle])

        self.form.ListCategory_NP.setCurrentText(All_KeyWord)
        self.form.ListCategory_DDB.setCurrentText(All_KeyWord)

        return    
       
    def LoadCommands(self):
        """Fill the Quick Commands Available and Selected"""
        self.form.CommandsAvailable_NP.clear()
        self.form.CommandList_DDB.clear()
        self.form.CommandsAvailable_DDB.clear()
        self.form.NewControl_DDB.clear()

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
                            if CommandName in fileName:
                                Icon = QIcon()
                                Icon.addPixmap(QPixmap(os.path.join(root, fileName)))
                    if Icon.isNull():
                        for item in self.List_CommandIcons:
                            if item[0] == CommandName:
                                Icon = item[1]
                                if (str(CommandName).endswith("_ddb") and "dropdownButtons" in self.workBenchDict):
                                    for (DropDownCommand, Commands) in self.workBenchDict["dropdownButtons"].items():
                                        if Commands[0][0] == item[0]:
                                            Icon = item[1]
                    if Icon.isNull():                        
                        if (str(CommandName).endswith("_ddb") and "dropdownButtons" in self.workBenchDict):
                            for (DropDownCommand, Commands) in self.workBenchDict["dropdownButtons"].items():
                                if DropDownCommand == CommandName:
                                    IconName = CommandItem[1]
                                    Icon = StandardFunctions.returnQiCons_Commands(Commands[0][0], IconName)
                        else:
                            IconName = StandardFunctions.CommandInfoCorrections(CommandName)["pixmap"]
                            Icon = StandardFunctions.returnQiCons_Commands(CommandName, IconName)

                    Text = MenuNameTranslated
                    ListWidgetItem = QListWidgetItem()
                    ListWidgetItem.setText(Text)
                    ListWidgetItem.setData(Qt.ItemDataRole.UserRole, CommandName)
                    
                    # Check if there is an Icon. if not add a replacement
                    if Icon.pixmap(64,64).toImage().bytesPerLine() < 256:
                        # Icon = Gui.getIcon("preferences-workbenches")
                        # ListWidgetItem.setIcon(Icon)
                        continue
                    
                    if Icon is not None and Icon.isNull() is False:
                        ListWidgetItem.setIcon(Icon)
                        ListWidgetItem.setToolTip(
                            CommandName
                        )  # Use the tooltip to store the actual command.

                        # Add the ListWidgetItem to the correct ListWidget
                        self.form.CommandsAvailable_NP.addItem(ListWidgetItem)
                        # Add clones of the listWidgetItem to the other listwidgets
                        self.form.CommandsAvailable_DDB.addItem(ListWidgetItem.clone())

                    # If there are any dropdown buttons in the json file, add them to the dropdown list
                    if (str(CommandName).endswith("_ddb") and "dropdownButtons" in self.workBenchDict):
                        self.form.CommandList_DDB.addItem(CommandName.replace("_ddb", ""))

                    ShadowList.append(CommandName)

        # Add a "new" item to the dropdown list
        self.form.CommandList_DDB.addItem(translate("FreeCAD Ribbon", "New"), "new")
        self.form.CommandList_DDB.setCurrentText(translate("FreeCAD Ribbon", "New"))
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

    def on_CreateNewPanel_clicked(self):
        if self.form.PanelTitle.text() != "":
            RibbonBar: FCBinding.ModernMenu = mw.findChild(FCBinding.ModernMenu, "Ribbon")
            RibbonBar.CreateNewPanel(self.form.PanelTitle.text())
        return
    # endregion---------------------------------------------------------------------------------------
    
    # region - Combine panels tab
    def setWB(self):
        # Get the ribbon, the current wb title and name
        RibbonBar: FCBinding.ModernMenu = mw.findChild(FCBinding.ModernMenu, "Ribbon")
        self.CurrentWorkBenchTitle = RibbonBar.currentCategory().title()
        self.CurrentWorkBenchName = RibbonBar.currentCategory().objectName()
        # Activate the correct workbench in this dialog (ComboBox is hidden)
        self.on_WorkbenchList_CP__activated()
        
        return
    
    def on_WorkbenchList_CP__activated(
        self, setCustomToolbarSelector_CP: bool = False, CurrentText=""
    ):
        # Set the workbench name.
        WorkBenchName = self.CurrentWorkBenchName
        WorkBenchTitle = self.CurrentWorkBenchTitle

        # If there is no workbench, return
        if WorkBenchName == "":
            return

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
        if "customToolbars" in self.workBenchDict:
            CustomPanel = self.List_ReturnCustomPanel(
                self.workBenchDict["customToolbars"], WorkBenchName=WorkBenchName
            )
            for CustomToolbar in CustomPanel:
                if CustomToolbar[1] == WorkBenchTitle or CustomToolbar[1] == "Global":
                    wbToolbars.append(CustomToolbar[0])
        # Get the new panels per workbench
        if "newPanels" in self.workBenchDict:
            NewPanels = self.List_ReturnNewPanel(
                self.workBenchDict["newPanels"], WorkBenchName=WorkBenchName, PanelDict="newPanels"
            )
            for Newpanel in NewPanels:
                if Newpanel[1] == WorkBenchTitle:
                    wbToolbars.append(Newpanel[0])
            # Get the new panels globally
            NewPanels = self.List_ReturnNewPanel(
                self.workBenchDict["newPanels"], WorkBenchName="Global", PanelDict="newPanels"
            )
            for Newpanel in NewPanels:
                if Newpanel[1] == "Global":
                    wbToolbars.append(Newpanel[0])                       

        # Clear the listwidget before filling it
        self.form.PanelAvailable_CP.clear()
        # Sort the toolbar list
        wbToolbars = self.SortedPanelList(wbToolbars, WorkBenchName)

        # Go through the toolbars and check if they must be ignored.
        shadowList = []
        for Toolbar in wbToolbars:
            if Toolbar in shadowList:
                continue
            IsIgnored = False
            if "ignoredToolbars" in self.workBenchDict:
                for IgnoredToolbar in self.workBenchDict["ignoredToolbars"]:
                    if Toolbar.lower() == IgnoredToolbar.lower():
                        IsIgnored = True

                # If the are not to be ignored, add them to the listwidget
                if IsIgnored is False and Toolbar != "":
                    ToolbarTransLated = Toolbar
                    # Get the translated toolbar name
                    for ToolBarItem in self.StringList_Toolbars:
                        if ToolBarItem[0] == Toolbar:
                            if len(ToolBarItem) == 4:
                                ToolbarTransLated = ToolBarItem[3]
                            else:
                                ToolbarTransLated = ToolBarItem[0]
                    # If it is a custom toolbar, remove the suffix
                    ToolbarTransLated = ToolbarTransLated.replace("_custom", "").replace(
                        "_newPanel", ""
                    )

                    ListWidgetItem = QListWidgetItem()
                    ListWidgetItem.setText(ToolbarTransLated.replace("&", ""))
                    ListWidgetItem.setData(Qt.ItemDataRole.UserRole, Toolbar)
                    self.form.PanelAvailable_CP.addItem(ListWidgetItem)
                    
                    # Add the toolbar to the shadow list to prevent from being added more than once.
                    shadowList.append(Toolbar)

                    if setCustomToolbarSelector_CP is True:
                        self.form.CustomToolbarSelector_CP.setCurrentText(
                            translate("FreeCAD Ribbon", "New")
                        )
                        self.form.CustomToolbarSelector_CP.setItemData(
                            0, "new", Qt.ItemDataRole.UserRole
                        )

                    # Get the ribbonbar
                    RibbonBar: FCBinding.ModernMenu = mw.findChild(FCBinding.ModernMenu, "Ribbon")
                    # Activate all buttons
                    RibbonBar.activateButtons()

            self.form.PanelSelected_CP.clear()       
        return

    def on_MoveUpPanelCommand_CP_clicked(self):
        self.MoveItem(ListWidget=self.form.PanelSelected_CP, Up=True)

        # # Enable the apply button
        # if self.CheckChanges() is True:
        #     self.form.UpdateJson.setEnabled(True)

        return

    def on_MoveDownPanelCommand_CP_clicked(self):
        self.MoveItem(ListWidget=self.form.PanelSelected_CP, Up=False)

        # # Enable the apply button
        # if self.CheckChanges() is True:
        #     self.form.UpdateJson.setEnabled(True)

        return

    def on_AddPanel_CP_clicked(self):
        SelectedToolbars = self.form.PanelAvailable_CP.selectedItems()

        # Set the workbench name.
        WorkbenchName = self.CurrentWorkBenchName

        # Get the dict with the toolbars of this workbench
        ToolbarItems = self.returnToolbarCommands(WorkbenchName)
        # Get the custom toolbars from each installed workbench
        CustomCommands = self.Dict_ReturnCustomToolbars(WorkbenchName)
        ToolbarItems.update(CustomCommands)
        # Get the global custom toolbars
        CustomCommands = self.Dict_ReturnCustomToolbars_Global()
        ToolbarItems.update(CustomCommands)
        # Get the new panels from each installed workbench
        NewPanelCommands = self.Dict_ReturnNewPanel(self.workBenchDict, WorkbenchName)
        ToolbarItems.update(NewPanelCommands)
        # Get the global new panels
        NewPanelCommands = self.Dict_ReturnNewPanel(self.workBenchDict)
        ToolbarItems.update(NewPanelCommands)
        
        for key, value in list(ToolbarItems.items()):
            # Go through the selected items, if they mach continue
            for i in range(len(SelectedToolbars)):
                toolbar = SelectedToolbars[i].data(Qt.ItemDataRole.UserRole)
                if key == toolbar:
                    for j in range(len(value)):
                        CommandName = value[j]
                        for ToolbarCommand in self.List_Commands:
                            if ToolbarCommand[0] == CommandName or ToolbarCommand[2] == CommandName:
                                # Get the command
                                MenuName = ToolbarCommand[4].replace("&", "")

                                # get the icon for this command if there isn't one, leave it None
                                Icon = QIcon()
                                for item in self.List_CommandIcons:
                                    if item[0] == ToolbarCommand[0]:
                                        Icon = item[1]
                                if Icon is None:
                                    Command = Gui.Command.get(CommandName)
                                    if Command is not None:
                                        Icon = Gui.getIcon(
                                            CommandInfoCorrections(CommandName)[
                                                "pixmap"
                                            ]
                                        )
                                        action = Command.getAction()
                                        try:
                                            if len(action) > 1:
                                                Icon = action[0].icon()
                                        except Exception:
                                            pass

                                # Define a new ListWidgetItem.
                                ListWidgetItem = QListWidgetItem()
                                ListWidgetItem.setText(
                                    StandardFunctions.TranslationsMapping(
                                        WorkbenchName, MenuName
                                    )
                                )
                                if Icon is not None:
                                    ListWidgetItem.setIcon(Icon)
                                ListWidgetItem.setData(
                                    Qt.ItemDataRole.UserRole, [key, CommandName]
                                )  # add here the toolbar name as hidden data

                                IsInList = False
                                for k in range(self.form.PanelSelected_CP.count()):
                                    if (
                                        self.form.PanelSelected_CP.item(k).text()
                                        == ListWidgetItem.text()
                                    ):
                                        IsInList = True

                                if IsInList is False:
                                    self.form.PanelSelected_CP.addItem(ListWidgetItem)

        # # Enable the apply button
        # if self.CheckChanges() is True:
        #     self.form.UpdateJson.setEnabled(True)

        return

    def on_AddCustomPanel_CP_clicked(self):        
        # define the suffix
        Suffix = "_custom"
        CustomPanelTitle = ""
        if self.form.PanelName_CP.text() != "":
            CustomPanelTitle = self.form.PanelName_CP.text()
        if self.form.PanelName_CP.text() == "":
            StandardFunctions.Mbox(
                translate("FreeCAD Ribbon", "Enter a name for your panel first!"),
                "",
                0,
                "Warning",
            )
            return

        if self.form.PanelSelected_CP.count() == 0:
            self.form.hide()
            StandardFunctions.Mbox(
                translate("FreeCAD Ribbon", "Add at least one panel first!"),
                "",
                0,
                "Warning",
            )
            self.form.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)
            self.form.show()
            return

        WorkBenchName = self.CurrentWorkBenchName
        WorkBenchTitle = self.CurrentWorkBenchTitle
        # Create item that defines the custom toolbar
        MenuName = ""
        for i in range(self.form.PanelSelected_CP.count()):
            ListWidgetItem = self.form.PanelSelected_CP.item(i)
            # if the translated menuname from the ListWidgetItem is equel to the MenuName from the command
            # Add the commandName to the list commandslist for this custom panel
            for CommandItem in self.List_Commands:
                if CommandItem[0] == ListWidgetItem.data(Qt.ItemDataRole.UserRole)[1]:
                    MenuName = CommandItem[2].replace("&", "")
                    # For FC 1.1.0, use commandnames instead of menu names
                    if StandardFunctions.checkFreeCADVersion(
                            Parameters.FreeCAD_Version["mainVersion"],
                            Parameters.FreeCAD_Version["subVersion"],
                            Parameters.FreeCAD_Version["patchVersion"],
                            Parameters.FreeCAD_Version["gitVersion"],
                        ) is True:
                        MenuName = CommandItem[0]

                    # Get the original toolbar
                    OriginalToolbar = ListWidgetItem.data(Qt.ItemDataRole.UserRole)[0]

                    # Create or modify the dict that will be entered
                    StandardFunctions.add_keys_nested_dict(
                        self.workBenchDict,
                        [
                            "customToolbars",
                            WorkBenchName,
                            CustomPanelTitle + Suffix,
                            "commands",
                            MenuName,
                        ],
                    )

                    # Update the dict
                    self.workBenchDict["customToolbars"][WorkBenchName][
                        CustomPanelTitle + Suffix
                    ]["commands"][MenuName] = OriginalToolbar

        # Check if the custom panel is selected in the Json file
        IsInList = False
        for j in range(self.form.CustomToolbarSelector_CP.count()):
            CustomToolbar = self.form.CustomToolbarSelector_CP.itemText(j)
            if CustomToolbar == f"{CustomPanelTitle}, {WorkBenchTitle}":
                IsInList = True

        # If the custom panel is not in the json file, add it to the QComboBox
        if IsInList is False:
            self.form.CustomToolbarSelector_CP.addItem(
                f"{CustomPanelTitle}, {WorkBenchTitle}"
            )

            # Set the Custom panel as current text for the QComboBox
            self.form.CustomToolbarSelector_CP.setCurrentText(
                f"{CustomPanelTitle}, {WorkBenchTitle}"
            )

            # Add the order of panels to the Json file
            StandardFunctions.add_keys_nested_dict(
                self.workBenchDict,
                ["workbenches", WorkBenchName, "toolbars", "order"],
            )
            ToolbarOrder = self.workBenchDict["workbenches"][WorkBenchName]["toolbars"][
                "order"
            ]
            ToolbarOrder.append(CustomPanelTitle + Suffix)

        # Get the ribbon
        RibbonBar: FCBinding.ModernMenu = mw.findChild(FCBinding.ModernMenu, "Ribbon")
        # Update the workBenchDict in the Ribbon
        RibbonBar.workBenchDict.update(self.workBenchDict)
        # Create the new panel in the ribbon
        newPanel = RibbonBar.CreatePanel(
            workbenchName=WorkBenchName,
            panelName=CustomPanelTitle + Suffix,
            addPanel=True,
            dict=self.workBenchDict,
            ignoreColumnLimit=True,
            showEnableControl=True,
            ActivateButtons=True
            )
        # Add the newPanel to the list of longPanels
        RibbonBar.longPanels.append(newPanel)
        # Remove the original panels
        panelsToRemove = []
        for key, value in self.workBenchDict["customToolbars"][WorkBenchName][CustomPanelTitle + Suffix]["commands"].items():
            for title, objPanel in RibbonBar.currentCategory().panels().items():
                if objPanel.objectName() == value:
                    # hide the enable checkboxes and hide the panel if it is unchecked
                    titleLayout = objPanel._titleLayout
                    EnableControl = titleLayout.itemAt(0).widget()
                    if EnableControl is not None:
                        EnableControl.setCheckState(Qt.CheckState.Unchecked) 
                        panelsToRemove.append(objPanel)
                        # Hide the panel
                        objPanel.hide()
                        # Write the state to the structure
                        StandardFunctions.add_keys_nested_dict(self.workBenchDict, ["workbenches", WorkBenchName, "toolbars", objPanel.objectName(), "Enabled"])
                        self.workBenchDict["workbenches"][WorkBenchName]["toolbars"][objPanel.objectName()]["Enabled"] = False
                        # Update the workBenchDict in the Ribbon
                        RibbonBar.workBenchDict.update(self.workBenchDict)
        
        # Remove the panels also from the current category. Othewise the will showup on clicking Ok
        for panel in panelsToRemove:
            # RibbonBar.currentCategory().removeWidget(panel)
            panel.hide()
            RibbonBar.ReplacedPanels.append(panel)
        return

    def on_CustomToolbarSelector_CP_activated(self):
        self.form.PanelSelected_CP.clear()

        # If the selected item is "new", clear the list widgets and exit
        if (
            self.form.CustomToolbarSelector_CP.currentData(Qt.ItemDataRole.UserRole)
            == "new"
        ):
            self.form.PanelAvailable_CP.clear()
            self.form.PanelName_CP.clear()
            self.on_WorkbenchList_CP__activated()
            return

        # Get the current custom toolbar name
        CustomPanelTitle = ""
        WorkBenchTitle = ""
        RibbonBar: FCBinding.ModernMenu = mw.findChild(FCBinding.ModernMenu, "Ribbon")
        if self.form.CustomToolbarSelector_CP.currentText() != "":
            CustomPanelTitle = (
                self.form.CustomToolbarSelector_CP.currentText().split(", ")[0]
                + "_custom"
            )
            WorkBenchTitle = self.form.CustomToolbarSelector_CP.currentText().split(", ")[1]
            category = RibbonBar.categories()[WorkBenchTitle]
            if category is not None:
                RibbonBar.setCurrentCategory(category)
                self.setWB()
            
            ShadowList = (
                []
            )  # Create a shadow list. To check if items are already existing.
            WorkBenchName = ""
            for WorkBench in self.Dict_CustomToolbars["customToolbars"]:
                for CustomToolbar in self.Dict_CustomToolbars["customToolbars"][
                    WorkBench
                ]:
                    if CustomToolbar == CustomPanelTitle:
                        WorkBenchName = WorkBench

                        # Get the commands and their original toolbar
                        for key, value in list(
                            self.Dict_CustomToolbars["customToolbars"][WorkBenchName][
                                CustomPanelTitle
                            ]["commands"].items()
                        ):
                            for CommandItem in self.List_Commands:
                                # Check if the items is already there
                                # if not, continue
                                if not CommandItem[0] in ShadowList:
                                    MenuName_Command = CommandItem[0]
                                    if (
                                        MenuName_Command == key
                                        and CommandItem[3] == WorkBenchName
                                    ):
                                        MenuName = (
                                            CommandItem[4]
                                            .replace("&", "")
                                            .replace("_custom", "")
                                        )

                                        # Define a new ListWidgetItem.
                                        ListWidgetItem = QListWidgetItem()
                                        ListWidgetItem.setText(MenuName)
                                        ListWidgetItem.setData(
                                            Qt.ItemDataRole.UserRole, [value,CommandItem[0]]
                                        )
                                        Icon = QIcon()
                                        for item in self.List_CommandIcons:
                                            if item[0] == CommandItem[0]:
                                                Icon = item[1]
                                        if Icon is None:
                                            Icon = Gui.getIcon(CommandItem[1])
                                        if Icon is not None:
                                            ListWidgetItem.setIcon(Icon)

                                        if ListWidgetItem.text() != "":
                                            self.form.PanelSelected_CP.addItem(
                                                ListWidgetItem
                                            )

                                        # Add the command to the shadow list
                                        ShadowList.append(CommandItem[0])

            self.form.PanelName_CP.setText(CustomPanelTitle.split("_")[0])
        else:
            return

        return

    def on_RemovePanel_CP_clicked(self):
        # Get the current custom toolbar name
        CustomPanelTitle = ""
        WorkBenchTitle = ""
        if (
            self.form.CustomToolbarSelector_CP.currentText() != ""
            or self.form.CustomToolbarSelector_CP.currentText() != "New"
        ):
            CustomPanelTitle = (
                self.form.CustomToolbarSelector_CP.currentText().split(", ")[0]
                + "_custom"
            )
            WorkBenchTitle = self.form.CustomToolbarSelector_CP.currentText().split(
                ", "
            )[1]
        else:
            return

        WorkBenchName = ""
        RibbonBar: FCBinding.ModernMenu = mw.findChild(FCBinding.ModernMenu, "Ribbon")
        for WorkBench in self.List_Workbenches:
            if WorkBench[2] == WorkBenchTitle:
                WorkBenchName = WorkBench[0]
                try:
                    for panel, commands in list(self.workBenchDict["customToolbars"][WorkBenchName].items()):
                        if panel == CustomPanelTitle:
                            # Get the order list
                            orderList: list = self.workBenchDict["workbenches"][WorkBenchName]["toolbars"]["order"]
                            
                            ListPanels = []
                            for command, toolbar in self.workBenchDict["customToolbars"][WorkBenchName][panel]["commands"].items():
                                if toolbar not in ListPanels:
                                    ListPanels.append(toolbar)

                            # Add the original panels
                            for toolbar in ListPanels:
                                TB = mw.findChildren(QToolBar, toolbar)
                                if TB is not None:
                                    # Create the panel based on the toolbars
                                    newPanel = RibbonBar.CreatePanel(workbenchName=WorkBenchName, panelName=toolbar, addPanel=False, dict=self.workBenchDict, showEnableControl=True, ActivateButtons=True)                                                                        
                                    # show the enable checkboxes  
                                    titleLayout: QHBoxLayout = newPanel._titleLayout
                                    EnableControl = titleLayout.itemAt(0).widget()
                                    if EnableControl is not None:
                                        EnableControl.setVisible(True)
                                        EnableControl.setChecked(True)
                                    # Add the original panel to the orderList
                                    if toolbar not in orderList:
                                        orderList.append(toolbar)
                                    # Add the panel
                                    index = orderList.index(toolbar)
                                    RibbonBar.currentCategory().insertWidget(newPanel, index)
                                    # Update the dict of the currentCategory with the new panel
                                    RibbonBar.currentCategory()._panels[newPanel.objectName()] = newPanel                                  
                            
                            # Remove the custom panel
                            #
                            # Close the panel first before removing
                            panelToRemove = RibbonBar.currentCategory().panels()[panel]                            
                            panelToRemove.close()
                            # Remove it
                            RibbonBar.currentCategory().removePanel(panel)
                                                                          
                            # remove the custom toolbar from the combobox
                            for i in range(self.form.CustomToolbarSelector_CP.count()):
                                if (self.form.CustomToolbarSelector_CP.itemText(i).split(", ")[0] == panel):
                                    if (self.form.CustomToolbarSelector_CP.itemText(i).split(", ")[1] == WorkBenchTitle and self.form.CustomToolbarSelector_CP.itemText(i).split(", ")[1] != ""):
                                        self.form.CustomToolbarSelector_CP.removeItem(i)
                                        self.form.CustomToolbarSelector_CP.setCurrentText(self.form.CustomToolbarSelector_CP.itemText(i - 1))

                            # Remove the custom panel from the order list
                            if panel in orderList:
                                orderList.remove(panel)

                            # remove the custom toolbar also from the workbenches dict
                            del self.workBenchDict["customToolbars"][WorkBenchName][panel]
                            if (panel in self.workBenchDict["workbenches"][WorkBenchName]["toolbars"]):
                                del self.workBenchDict["workbenches"][WorkBenchName]["toolbars"][panel]

                            # update the order list
                            if panel in self.workBenchDict["workbenches"][WorkBenchName]:
                                self.workBenchDict["workbenches"][WorkBenchName][panel]["order"] = orderList

                            # Set the current text to new
                            self.form.CustomToolbarSelector_CP.setCurrentText("New")

                            if (
                                self.form.CustomToolbarSelector_CP.currentText()
                                == "New"
                            ):
                                self.form.PanelSelected_CP.clear()
                                self.form.PanelName_CP.clear()

                            return
                except Exception as e:
                    if Parameters.DEBUG_MODE is True:
                        raise (e)
                    raise (e)
        return
    # endregion---------------------------------------------------------------------------------------
    
    # region - Create dropdown buttons tab
    def on_CreateControl_DDB_clicked(self):
        DropDownButton = []
        DropDownName = ""
        Suffix = ""
        if self.form.ControlName_DDB.text() != "":
            DropDownName = self.form.ControlName_DDB.text()
        if self.form.ControlName_DDB.text() == "":
            StandardFunctions.Mbox(
                translate(
                    "FreeCAD Ribbon", "Enter a name for your dropdown button first!"
                ),
                "",
                0,
                "Warning",
            )
            return
        IsInlist = False
        # If the dropdownbutton is already created, just return
        for Button in self.newDDBList:
            if DropDownName == Button:
                return

        # Add all commands for the new dropdown button in a list
        for i in range(self.form.NewControl_DDB.count()):
            ListWidgetItem = self.form.NewControl_DDB.item(i)

            for CommandItem in self.List_Commands:
                if CommandItem[0] == ListWidgetItem.data(Qt.ItemDataRole.UserRole):
                    CommandName = CommandItem[0]
                    WorkBenchName = CommandItem[3]
                    IsInlist = False
                    for item in DropDownButton:
                        if item[0] == CommandName:
                            IsInlist = True
                    if IsInlist is False:
                        DropDownButton.append([CommandName, WorkBenchName])

            # Create or modify the dict that will be entered
            Suffix = "_ddb"
            StandardFunctions.add_keys_nested_dict(self.workBenchDict["dropdownButtons"], [DropDownName + Suffix], endEmpty=True)

        # Update the dict
        self.workBenchDict["dropdownButtons"][DropDownName + Suffix] = DropDownButton

        # Add the dropdown button to the command list widgets
        FirstCommand = DropDownButton[0][0]
        Icon = QIcon()
        IconName = ""
        FreeCAD_Icons = os.path.abspath(os.path.join(os.path.dirname(__file__), "Resources", "FreeCAD Icons"))
        for root, dirs, files in os.walk(FreeCAD_Icons):
            for fileName in files:
                if FirstCommand in fileName:
                    Icon = QIcon()
                    Icon.addPixmap(QPixmap(os.path.join(root, fileName)))
        if Icon.isNull():
            for item in self.List_CommandIcons:
                if item[0] == FirstCommand:
                    Icon = item[1]
        if Icon.isNull():            
            IconName = FirstCommand
            Icon = StandardFunctions.returnQiCons_Commands(FirstCommand, IconName)
                            
        ListWidgetItem = QListWidgetItem()
        ListWidgetItem.setText(DropDownName)
        ListWidgetItem.setData(Qt.ItemDataRole.UserRole, DropDownName + Suffix)
        if Icon is not None:
            ListWidgetItem.setIcon(Icon)
            # Add the ListWidgetItem to the several listWidgets
            self.form.CommandsAvailable_NP.addItem(ListWidgetItem)
            self.form.CommandsAvailable_DDB.addItem(ListWidgetItem.clone())

            # Add the command to the list of commands
            self.List_Commands.append([DropDownName + Suffix, IconName, DropDownName, "General", DropDownName])

            # Add the drop down buttoon to the combobox
            self.form.CommandList_DDB.addItem(DropDownName)
            # make sure that no command is selected by default
            # to prevent accidental removal
            self.form.CommandList_DDB.setCurrentText("")
            # Add the command to the temporary list
            self.newDDBList.append(DropDownName)

        RibbonBar: FCBinding.ModernMenu = mw.findChild(FCBinding.ModernMenu, "Ribbon")
        RibbonBar.workBenchDict["dropdownButtons"] = self.workBenchDict["dropdownButtons"]
        return

    def on_CommandList_DDB_activated(self):
        self.form.NewControl_DDB.clear()
        DropDownControl = self.form.CommandList_DDB.currentText() + "_ddb"

        if self.form.CommandList_DDB.currentData(Qt.ItemDataRole.UserRole) == "new":
            self.form.NewControl_DDB.clear()
            return

        # if the dropdown text is not empty, continue
        if DropDownControl != "" and "dropdownButtons" in self.workBenchDict:
            # Go through the dropdown buttons.
            for DropDownButton, Commands in list(
                self.workBenchDict["dropdownButtons"].items()
            ):
                # If the DropDownButton is equal to the text in the combobox, go through its commands
                if DropDownButton == DropDownControl:
                    for CommandName in Commands:
                        for i in range(self.form.CommandsAvailable_DDB.count()):
                            ListWidgetItem = self.form.CommandsAvailable_DDB.item(i)

                            # If the command is equal to one in the commandsavaialble listwidget,
                            # Move it to the listwidget for the dropdown button.
                            if (
                                ListWidgetItem.data(Qt.ItemDataRole.UserRole)
                                == CommandName[0]
                            ):
                                self.form.NewControl_DDB.addItem(ListWidgetItem.clone())
                                self.form.CommandsAvailable_DDB.removeItemWidget(
                                    ListWidgetItem
                                )
                                # load the text as well
                                self.form.ControlName_DDB.setText(
                                    DropDownControl.split("_")[0]
                                )

        return

    def on_RemoveControl_DDB_clicked(self):
        DropDownControl = self.form.CommandList_DDB.currentText() + "_ddb"

        if DropDownControl != "" and "dropdownButtons" in self.workBenchDict:
            for DropDownButton, Commands in list(
                self.workBenchDict["dropdownButtons"].items()
            ):
                if DropDownButton == DropDownControl:
                    # remove the custom toolbar also from the workbenches dict
                    del self.workBenchDict["dropdownButtons"][DropDownButton]

                    # remove the command from the quickaccess toolbar
                    newList = []
                    for item in self.workBenchDict["quickAccessCommands"]:
                        if item != DropDownControl:
                            newList.append(item)
                    self.workBenchDict["quickAccessCommands"] = newList

                    # remove the control from the combobox
                    for i in range(self.form.CommandList_DDB.count()):
                        if (
                            self.form.CommandList_DDB.itemText(i) + "_ddb"
                            == DropDownControl
                        ):
                            self.form.CommandList_DDB.removeItem(i)

                    # Set the current text to new
                    self.form.CommandList_DDB.setCurrentText("New")

                    if self.form.CommandList_DDB.currentText() == "New":
                        self.form.NewControl_DDB.clear()
                        self.form.ControlName_DDB.clear()

            # # Enable the apply button
            # if self.CheckChanges() is True:
            #     self.form.UpdateJson.setEnabled(True)

        return

    def on_ListCategory_DDB_TextChanged(self):
        self.FilterCommands_ListCategory(
            self.form.CommandsAvailable_DDB,
            self.form.ListCategory_DDB,
            self.form.SearchBar_DDB,
        )
        return

    def on_SearchBar_DDB_TextChanged(self):
        self.FilterCommands_SearchBar(
            self.form.CommandsAvailable_DDB,
            self.form.SearchBar_DDB,
            self.form.ListCategory_DDB,
        )
        return

    def on_AddCommand_DDB_clicked(self):
        Filter = [self.form.CommandList_DDB.currentText() + "_ddb"]
        self.AddItem(
            SourceWidget=self.form.CommandsAvailable_DDB,
            DestinationWidget=self.form.NewControl_DDB,
            ExcludedItems=Filter,
        )

        # # Enable the apply button
        # if self.CheckChanges() is True:
        #     self.form.UpdateJson.setEnabled(True)

        return

    def on_RemoveCommand_DDB_clicked(self):
        self.AddItem(
            SourceWidget=self.form.NewControl_DDB,
            DestinationWidget=self.form.CommandsAvailable_DDB,
        )

        # # Enable the apply button
        # if self.CheckChanges() is True:
        #     self.form.UpdateJson.setEnabled(True)

        return

    def on_MoveUpCommand_DDB_clicked(self):
        self.MoveItem(ListWidget=self.form.NewControl_DDB, Up=True)

        # # Enable the apply button
        # if self.CheckChanges() is True:
        #     self.form.UpdateJson.setEnabled(True)

        return

    def on_MoveDownCommand_DDB_clicked(self):
        self.MoveItem(ListWidget=self.form.NewControl_DDB, Up=False)

        # # Enable the apply button
        # if self.CheckChanges() is True:
        #     self.form.UpdateJson.setEnabled(True)

        return

    # endregion---------------------------------------------------------------------------------------
    
    # region - Form controls
    def on_Cancel_Clicked(self):
        if self.DialogClosed is False:
            RibbonBar: FCBinding.ModernMenu = mw.findChild(FCBinding.ModernMenu, "Ribbon")        
            for category in RibbonBar.CustomizedCategories:
                RibbonBar.setCurrentCategory(category)
                RibbonBar.on_Cancel_Clicked()
            RibbonBar.CustomizedCategories.clear()
        return
        
    def on_Ok_Clicked(self):
        self.DialogClosed = True
        if self.DialogClosed is True:
            RibbonBar: FCBinding.ModernMenu = mw.findChild(FCBinding.ModernMenu, "Ribbon")       
            for category in RibbonBar.CustomizedCategories:
                RibbonBar.setCurrentCategory(category) 
                RibbonBar.on_Ok_Clicked()
            RibbonBar.CustomizedCategories.clear()
            # self.DialogClosed = False
        return
    
    def on_Helpbutton_clicked(self):
        if self.ReproAdress != "" or self.ReproAdress is not None:
            if not self.ReproAdress.endswith("/"):
                self.ReproAdress = self.ReproAdress + "/"

            Adress = self.ReproAdress + "wiki"
            webbrowser.open(Adress, new=2, autoraise=True)
        return
        
    def on_ReloadWB_clicked(self, resetTexts=False, RestartFreeCAD=False):
        # minimize the dialog
        DockWidget = mw.findChild(QDockWidget, "RibbonLayout")
        if DockWidget is None:
            self.form.hide()
        
        # Create the data file
        CacheFunctions.CreateCache()

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
        if DockWidget is None:
            self.form.show()
        return
    # endregion
    
    # region - Helper functions
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
                                        if CommandName in fileName:
                                            Icon = QIcon()
                                            Icon.addPixmap(QPixmap(os.path.join(root, fileName)))
                                if Icon.isNull():
                                    if (str(CommandName).endswith("_ddb") and "dropdownButtons" in self.workBenchDict):
                                        for (DropDownCommand, Commands) in self.workBenchDict["dropdownButtons"].items():
                                            if DropDownCommand == CommandName:
                                                for item in self.List_CommandIcons:
                                                    if item[0] == Commands[0][0]:
                                                        Icon = item[1]
                                    else:
                                        for item in self.List_CommandIcons:
                                            if item[0] == CommandName:
                                                Icon = item[1]
                                if Icon.isNull():                                    
                                    if (str(CommandName).endswith("_ddb") and "dropdownButtons" in self.workBenchDict):
                                        for (DropDownCommand, Commands) in self.workBenchDict["dropdownButtons"].items():
                                            if DropDownCommand == CommandName:
                                                IconName = ToolbarCommand[1]
                                                Icon = StandardFunctions.returnQiCons_Commands(Commands[0][0], IconName)
                                    else:
                                        IconName = StandardFunctions.CommandInfoCorrections(CommandName)["pixmap"]
                                        Icon = StandardFunctions.returnQiCons_Commands(CommandName, IconName)

                                # Define a new ListWidgetItem.
                                ListWidgetItem = QListWidgetItem()
                                ListWidgetItem.setText(MenuNameTranslated)
                                ListWidgetItem.setData(
                                    Qt.ItemDataRole.UserRole, CommandName
                                )
                                
                                # Check if there is an Icon. if not add a replacement
                                if Icon.pixmap(64,64).toImage().bytesPerLine() < 256:
                                    # Icon = Gui.getIcon("preferences-workbenches")
                                    # ListWidgetItem.setIcon(Icon)
                                    continue

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
                                    
                        except Exception as e:
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
                                        if CommandName in fileName:
                                            Icon = QIcon()
                                            Icon.addPixmap(QPixmap(os.path.join(root, fileName)))
                                if Icon.isNull():
                                    if (str(CommandName).endswith("_ddb") and "dropdownButtons" in self.workBenchDict):
                                        for (DropDownCommand, Commands) in self.workBenchDict["dropdownButtons"].items():
                                            if DropDownCommand == CommandName:
                                                for item in self.List_CommandIcons:
                                                    if item[0] == Commands[0][0]:
                                                        Icon = item[1]
                                    else:
                                        for item in self.List_CommandIcons:
                                            if item[0] == CommandName:
                                                Icon = item[1]
                                if Icon.isNull():
                                    if (str(CommandName).endswith("_ddb") and "dropdownButtons" in self.workBenchDict):
                                        for (DropDownCommand, Commands) in self.workBenchDict["dropdownButtons"].items():
                                            if DropDownCommand == CommandName:
                                                IconName = ToolbarCommand[1]
                                                Icon = StandardFunctions.returnQiCons_Commands(Commands[0][0], IconName)
                                    else:
                                        IconName = StandardFunctions.CommandInfoCorrections(CommandName)["pixmap"]
                                        Icon = StandardFunctions.returnQiCons_Commands(CommandName, IconName)

                                Text = MenuNameTranslated
                                ListWidgetItem = QListWidgetItem()
                                ListWidgetItem.setText(Text)
                                ListWidgetItem.setData(
                                    Qt.ItemDataRole.UserRole, CommandName
                                )
                                
                                # Check if there is an Icon. if not add a replacement
                                if Icon.pixmap(64,64).toImage().bytesPerLine() < 256:
                                    # Icon = Gui.getIcon("preferences-workbenches")
                                    # ListWidgetItem.setIcon(Icon)
                                    continue

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
                                if CommandName in fileName:
                                    Icon = QIcon()
                                    Icon.addPixmap(QPixmap(os.path.join(root, fileName)))
                        if Icon.isNull():
                            if (str(CommandName).endswith("_ddb") and "dropdownButtons" in self.workBenchDict):
                                for (DropDownCommand, Commands) in self.workBenchDict["dropdownButtons"].items():
                                    if DropDownCommand == CommandName:
                                        for item in self.List_CommandIcons:
                                            if item[0] == Commands[0][0]:
                                                Icon = item[1]
                            else:
                                for item in self.List_CommandIcons:
                                    if item[0] == CommandName:
                                        Icon = item[1]
                        if Icon.isNull():
                            if (str(CommandName).endswith("_ddb") and "dropdownButtons" in self.workBenchDict):
                                for (DropDownCommand, Commands) in self.workBenchDict["dropdownButtons"].items():
                                    if DropDownCommand == CommandName:
                                        IconName = ToolbarCommand[1]
                                        Icon = StandardFunctions.returnQiCons_Commands(Commands[0][0], IconName)
                            else:
                                IconName = StandardFunctions.CommandInfoCorrections(CommandName)["pixmap"]
                                Icon = StandardFunctions.returnQiCons_Commands(CommandName, IconName)
                                                
                        Text = MenuNameTranslated
                        ListWidgetItem = QListWidgetItem()
                        ListWidgetItem.setText(Text)
                        ListWidgetItem.setData(Qt.ItemDataRole.UserRole, CommandName)
                        if Icon is not None:
                            ListWidgetItem.setIcon(Icon)
                        ListWidgetItem.setToolTip(
                            CommandName
                        )  # Use the tooltip to store the actual command.

                        # Check if there is an Icon. if not add a replacement
                        if Icon.pixmap(64,64).toImage().bytesPerLine() < 256:
                            # Icon = Gui.getIcon("preferences-workbenches")
                            # ListWidgetItem.setIcon(Icon)
                            continue
                        
                        if Icon is not None and Icon.isNull() is False:
                            ListWidget_Commands.addItem(ListWidgetItem)
                            ShadowList.append(CommandName)

                    if (ListWidget_WorkBenches.currentData(Qt.ItemDataRole.UserRole) == "All"):
                        # Define a new ListWidgetItem.
                        Icon = QIcon()
                        FreeCAD_Icons = os.path.abspath(os.path.join(os.path.dirname(__file__), "Resources", "FreeCAD Icons"))
                        for root, dirs, files in os.walk(FreeCAD_Icons):
                            for fileName in files:
                                if CommandName in fileName:
                                    Icon = QIcon()
                                    Icon.addPixmap(QPixmap(os.path.join(root, fileName)))
                        if Icon.isNull():
                            if Icon.isNull():
                                if (str(CommandName).endswith("_ddb") and "dropdownButtons" in self.workBenchDict):
                                    for (DropDownCommand, Commands) in self.workBenchDict["dropdownButtons"].items():
                                        if DropDownCommand == CommandName:
                                            for item in self.List_CommandIcons:
                                                if item[0] == Commands[0][0]:
                                                    Icon = item[1]
                                else:
                                    for item in self.List_CommandIcons:
                                        if item[0] == CommandName:
                                            Icon = item[1]
                        if Icon.isNull():
                            if (str(CommandName).endswith("_ddb") and "dropdownButtons" in self.workBenchDict):
                                for (DropDownCommand, Commands) in self.workBenchDict["dropdownButtons"].items():
                                    if DropDownCommand == CommandName:
                                        IconName = ToolbarCommand[1]
                                        Icon = StandardFunctions.returnQiCons_Commands(Commands[0][0], IconName)
                            else:
                                IconName = StandardFunctions.CommandInfoCorrections(CommandName)["pixmap"]
                                Icon = StandardFunctions.returnQiCons_Commands(CommandName, IconName)

                        Text = MenuNameTranslated
                        ListWidgetItem = QListWidgetItem()
                        ListWidgetItem.setText(Text)
                        ListWidgetItem.setData(
                            Qt.ItemDataRole.UserRole, CommandName
                        )
                        
                        # Check if there is an Icon. if not add a replacement
                        if Icon.pixmap(64,64).toImage().bytesPerLine() < 256:
                            # Icon = Gui.getIcon("preferences-workbenches")
                            # ListWidgetItem.setIcon(Icon)
                            continue
                        
                        if Icon is not None and Icon.isNull() is False:
                            ListWidgetItem.setIcon(Icon)
                            ListWidgetItem.setToolTip(
                                CommandName
                            )  # Use the tooltip to store the actual command.

                            # Add the ListWidgetItem to the correct ListWidget
                            ListWidget_Commands.addItem(ListWidgetItem)                                
                            ShadowList.append(CommandName)
        return
    
    def returnWorkBenchToolbars(self, WorkBenchName):
        wbToolbars = []
        try:
            for ToolbarItem in self.StringList_Toolbars:
                if ToolbarItem[2] == WorkBenchName:
                    wbToolbars.append(ToolbarItem[0])
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

    def returnDropDownCommands(self, command):
        Commands = []
        if command is not None:
            if len(command.getAction()) > 1:
                for i in range(len(command.getAction()) - 1):
                    action = command.getAction()[i]
                    if action is not None and (
                        action.icon() is not None and not action.icon().isNull()
                    ):
                        Commands.append(
                            [
                                f"{command.getInfo()['name']}, {i}",
                                "actionIcon",
                                action.text(),
                                action.text(),
                            ]
                        )
        return Commands
    
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
                            "User parameter:BaseApp/Workbench/"
                            + WorkBenchName
                            + "/Toolbar/"
                            + Group
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

                            Toolbars.append([Name, WorkbenchTitle, ListCommands, Name])
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
        CustomToolbars: list = App.ParamGet(
            "User parameter:BaseApp/Workbench/Global/Toolbar"
        ).GetGroups()

        for Group in CustomToolbars:
            Parameter = App.ParamGet(
                "User parameter:BaseApp/Workbench/Global/Toolbar/" + Group
            )
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

                Toolbars.append([Name, "Global", ListCommands, Name])
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
                    Parameter = App.ParamGet(
                        "User parameter:BaseApp/Workbench/"
                        + WorkBenchName
                        + "/Toolbar/"
                        + Group
                    )
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
        CustomToolbars: list = App.ParamGet(
            "User parameter:BaseApp/Workbench/Global/Toolbar"
        ).GetGroups()

        for Group in CustomToolbars:
            Parameter = App.ParamGet(
                "User parameter:BaseApp/Workbench/Global/Toolbar/" + Group
            )
            Name = Parameter.GetString("Name")

            IsIgnored = False
            # for ToolBar in self.List_IgnoredToolbars:
            #     if ToolBar == Name:
            #         IsIgnored = True

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
    
    def Dict_ReturnNewPanel(self, DictPanels: dict, WorkBenchName="Global", PanelDict="newPanels"):
        Toolbars = {}

        try:
            for NewPanel in DictPanels[PanelDict][WorkBenchName]:
                ListCommands = []
                Commands = DictPanels[PanelDict][WorkBenchName][NewPanel]

                for commandName in Commands:
                    ListCommands.append(commandName[0])
                Toolbars[NewPanel] = ListCommands

            for NewPanel in DictPanels[PanelDict]["Global"]:
                ListCommands = []
                Commands = DictPanels[PanelDict][WorkBenchName][NewPanel]

                for commandName in Commands:
                    ListCommands.append(commandName[0])
                Toolbars[NewPanel] = ListCommands
        except Exception:
            pass
        return Toolbars
    
    def List_ReturnCustomPanel(self, DictPanels: dict, WorkBenchName="Global", PanelDict="customToolbars"):
        Toolbars = []

        if str(WorkBenchName) != "" or WorkBenchName is not None:
            if str(WorkBenchName) != "NoneWorkbench":
                try:
                    for CustomToolbar in DictPanels[PanelDict][WorkBenchName]:
                        if len(DictPanels[PanelDict][WorkBenchName]) > 0:
                            ListCommands = []
                            Commands = DictPanels[PanelDict][WorkBenchName][
                                CustomToolbar
                            ]["commands"]

                            WorkbenchTitle = Gui.getWorkbench(WorkBenchName).MenuText
                            if WorkBenchName == "Global":
                                WorkbenchTitle = "Global"

                            for key, value in list(Commands.items()):
                                for i in range(len(self.List_Commands)):
                                    if (
                                        self.List_Commands[i][0] == key
                                        and self.List_Commands[i][3] == WorkBenchName
                                    ):
                                        Command = self.List_Commands[i][0]
                                        ListCommands.append(Command)
                                    if (
                                        self.List_Commands[i][0] == key
                                        and self.List_Commands[i][3] == "Global"
                                    ):
                                        Command = self.List_Commands[i][0]
                                        ListCommands.append(Command)

                                if value not in self.List_IgnoredToolbars_internal:
                                    self.List_IgnoredToolbars_internal.append(
                                        f"{value}"
                                    )

                            Toolbars.append(
                                [
                                    CustomToolbar,
                                    WorkbenchTitle,
                                    ListCommands,
                                    CustomToolbar,
                                ]
                            )
                except Exception:
                    pass

        return Toolbars

    def List_ReturnNewPanel(self, DictPanels: dict, WorkBenchName="Global", PanelDict="newPanels"):
        Toolbars = []

        if WorkBenchName != "" or WorkBenchName is not None:
            if WorkBenchName != "NoneWorkbench":
                try:
                    for NewPanel in DictPanels[PanelDict][WorkBenchName]:
                        ListCommands = DictPanels[PanelDict][WorkBenchName][NewPanel]
                        if WorkBenchName == "Global":
                            WorkbenchTitle = WorkBenchName
                        else:
                            WorkbenchTitle = Gui.getWorkbench(WorkBenchName).MenuText

                        Toolbars.append(
                            [NewPanel, WorkbenchTitle, ListCommands, NewPanel]
                        )
                except Exception:
                    pass
        return Toolbars

    def ListWidgetItems(self, ListWidget: QListWidget) -> list:
        items = []
        for x in range(ListWidget.count()):
            items.append(ListWidget.item(x))

        return items

    def AddItem(
        self,
        SourceWidget: QListWidget,
        DestinationWidget: QListWidget,
        ExcludedItems=[],
        CheckIfInList=True,
    ):
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

            IsInList = False
            if CheckIfInList is True:
                for i in range(DestinationWidget.count()):
                    item = DestinationWidget.item(i)
                    if item.data(Qt.ItemDataRole.UserRole) == DestinationItem.data(
                        Qt.ItemDataRole.UserRole
                    ):
                        IsInList = True

            IsExcluded = False
            for ExcludedItem in ExcludedItems:
                if ExcludedItem == DestinationItem.data(Qt.ItemDataRole.UserRole):
                    IsExcluded = True

            # Add the item to the list with current items
            if IsInList is False and IsExcluded is False:
                DestinationWidget.addItem(DestinationItem)

                # Go through the items on the list with items to add.
                for i in range(SourceWidget.count()):
                    # Get the item
                    SourceItem = SourceWidget.item(i)
                    # If the item is not none and the item text is equal to itemText,
                    # remove it from the columns to add list.
                    if SourceItem is not None:
                        if SourceItem.data(
                            Qt.ItemDataRole.UserRole
                        ) == DestinationItem.data(Qt.ItemDataRole.UserRole):
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

    def CheckChanges(self):
        # Open the JsonFile and load the data
        JsonFile = open(os.path.join(ConfigDirectory, "RibbonStructure.json"))
        data = json.load(JsonFile)

        IsChanged = False
        if "ignoredToolbars" in data:
            if data["ignoredToolbars"] != self.List_IgnoredToolbars:
                IsChanged = True
                print("ignoredToolbars")
        if "iconOnlyToolbars" in data:
            if data["iconOnlyToolbars"] != self.List_IconOnly_Toolbars:
                IsChanged = True
                print("iconOnlyToolbars")
        if "quickAccessCommands" in data:
            if (
                data["quickAccessCommands"]
                != self.List_QuickAccessCommands
            ):
                IsChanged = True
                print("quickAccessCommands")
        if "ignoredWorkbenches" in data:
            if data["ignoredWorkbenches"] != self.List_IgnoredWorkbenches:
                IsChanged = True
                print("ignoredWorkbenches")
        if "customToolbars" in data:
            if data["customToolbars"] != self.Dict_CustomToolbars["customToolbars"]:
                IsChanged = True
        if "dropdownButtons" in data:
            if data["dropdownButtons"] != self.workBenchDict["dropdownButtons"]:
                IsChanged = True
        if "newPanels" in data:
            if data["newPanels"] != self.Dict_NewPanels["newPanels"]:
                IsChanged = True
        if "workbenches" in data:
            if data["workbenches"] != self.Dict_RibbonCommandPanel["workbenches"]:
                IsChanged = True

        JsonFile.close()
        self.IsChanged = IsChanged
        return IsChanged

    def SortedPanelList(self, PanelList_RD: list, WorkBenchName):
        JsonOrderList = []
        try:
            if (len(self.Dict_RibbonCommandPanel["workbenches"][WorkBenchName]["toolbars"]["order"]) > 0):
                JsonOrderList = self.Dict_RibbonCommandPanel["workbenches"][WorkBenchName]["toolbars"]["order"]
        except Exception:
            JsonOrderList = PanelList_RD

        def SortList(toolbar):
            if toolbar == "":
                return -1

            position = None
            try:
                position = JsonOrderList.index(toolbar) + 1
            except ValueError:
                position = 999999
                if toolbar.endswith("_custom") or toolbar.endswith("_newPanel"):
                    if Parameters.DEFAULT_PANEL_POSITION_CUSTOM == "Right":
                        position = 999999
                    else:
                        position = 0
            return position

        PanelList_RD.sort(key=SortList)

        return PanelList_RD
    
    def LoadPanels(self):
        self.form.CustomToolbarSelector_CP.clear()

        # -- Custom panel tab --
        self.form.CustomToolbarSelector_CP.addItem(
            translate("FreeCAD Ribbon", "New"), "new"
        )
        try:
            for WorkBenchName in self.Dict_CustomToolbars["customToolbars"]:
                WorkBenchTitle = ""
                for WorkBenchItem in self.List_Workbenches:
                    if WorkBenchItem[0] == WorkBenchName:
                        WorkBenchTitle = WorkBenchItem[2]
                for CustomPanelTitle in self.Dict_CustomToolbars["customToolbars"][
                    WorkBenchName
                ]:
                    if WorkBenchTitle != "":
                        self.form.CustomToolbarSelector_CP.addItem(
                            f'{CustomPanelTitle.replace("_custom", "")}, {WorkBenchTitle}'
                        )
        except Exception as e:
            if Parameters.DEBUG_MODE is True:
                StandardFunctions.Print(
                    f"{e.with_traceback(e.__traceback__)}", "Warning"
                )
            pass
        return
    
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

        # Get all the ignored toolbars
        if Section == "ignoredToolbars" or Section == "All":
            for IgnoredToolbar in data["ignoredToolbars"]:
                self.List_IgnoredToolbars.append(IgnoredToolbar)

        # Get all the icon only toolbars
        if Section == "iconOnlyToolbars" or Section == "All":
            for IconOnly_Toolbar in data["iconOnlyToolbars"]:
                self.List_IconOnly_Toolbars.append(IconOnly_Toolbar)

        # Get all the quick access command
        if Section == "quickAccessCommands" or Section == "All":
            for QuickAccessCommand in data["quickAccessCommands"]:
                self.List_QuickAccessCommands.append(QuickAccessCommand)

        # Get all the ignored workbenches
        if Section == "ignoredWorkbenches" or Section == "All":
            for IgnoredWorkbench in data["ignoredWorkbenches"]:
                self.List_IgnoredWorkbenches.append(IgnoredWorkbench)

        # Get all the custom toolbars
        if Section == "customToolbars" or Section == "All":
            try:
                self.Dict_CustomToolbars["customToolbars"] = data["customToolbars"]
            except Exception:
                pass

        # Get all the dropdown buttons
        if Section == "dropdownButtons" or Section == "All":
            try:
                self.workBenchDict["dropdownButtons"] = data["dropdownButtons"]
            except Exception:
                pass

        # Get all the new toolbars
        if Section == "newPanels" or Section == "All":
            try:
                self.Dict_NewPanels["newPanels"] = data["newPanels"]
            except Exception:
                pass

        # Get the dict with the customized date for the buttons
        if Section == "workbenches" or Section == "All":
            try:
                self.Dict_RibbonCommandPanel["workbenches"] = data["workbenches"]
            except Exception:
                pass

        JsonFile.close()
        return    
    
    # endregion
    
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
            if type(self.widget) is not QuickAccessToolButton and type(self.widget) is not RibbonPanel:
                if panel is not None:
                    # Set the wait cursor
                    QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
                    QApplication.processEvents(QEventLoop.ProcessEventsFlag.AllEvents)
                    # Remove the button from the panel
                    RibbonBar.RemoveButtonFromPanel(panel, self.widget)
                    self.dragEntered = False
                    # Restore the cursor
                    QApplication.restoreOverrideCursor()
                    event.accept()
                    return True              
            if type(self.widget) is QuickAccessToolButton:
                # Set the wait cursor
                QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
                QApplication.processEvents(QEventLoop.ProcessEventsFlag.AllEvents)
                # Remove the button from the panel
                RibbonBar.RemoveButtonFromQuickAccess(self.widget, self.pos)
                # Restore the cursor
                QApplication.restoreOverrideCursor()
                self.dragEntered = False
                event.accept()
                return True
            if type(self.widget) is RibbonPanel:
                RibbonBar.RemovePanelFromDict(self.widget)
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
            event.accept()
        if event.type() == QEvent.Type.Close:
            mw = Gui.getMainWindow()
            RibbonBar: FCBinding.ModernMenu = mw.findChild(FCBinding.ModernMenu, "Ribbon")
            DockWidget = mw.findChild(QDockWidget, "RibbonLayout")
            if DockWidget is None:   
                if LoadDialog.DialogClosed is False:        
                    try:          
                        RibbonBar.on_Cancel_Clicked()
                        LoadDialog.DialogClosed = True
                    except Exception:
                        pass
                return True
            # # Set the size of the central wiget back
            # mw.centralWidget().setFixedWidth(RibbonBar.CentralWidgetWidth)
            # mw.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        return False
  