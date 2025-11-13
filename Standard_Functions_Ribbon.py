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

from xml.etree.ElementTree import Element, ElementTree

from requests import Request
import FreeCAD as App
import FreeCADGui as Gui
import math

# Define the translation
translate = App.Qt.translate

mw = Gui.getMainWindow()


def Mbox(
    text,
    title="",
    style=0,
    IconType="Information",
    default="",
    stringList="[,]",
):
    """
    Message Styles:\n
    0 : OK                          (text, title, style)\n
    1 : Yes | No                    (text, title, style)\n
    2 : Ok | Cancel                 (text, title, style)\n
    20 : Inputbox                   (text, title, style, default)\n
    21 : Inputbox with dropdown     (text, title, style, default, stringlist)\n
    Icontype:                       string: NoIcon, Question, Warning, Critical. Default Information\n
    30 : OK (Non blocking)          (text, title, style)\n
    """
    from PySide.QtWidgets import QMessageBox, QInputDialog
    from PySide.QtCore import Qt
    from PySide import QtWidgets

    Icon = QMessageBox.Icon.Information
    if IconType == "NoIcon":
        Icon = QMessageBox.Icon.NoIcon
    if IconType == "Question":
        Icon = QMessageBox.Icon.Question
    if IconType == "Warning":
        Icon = QMessageBox.Icon.Warning
    if IconType == "Critical":
        Icon = QMessageBox.Icon.Critical

    if style == 0:
        # Set the messagebox
        msgBox = QMessageBox()
        msgBox.setIcon(Icon)
        msgBox.setText(text)
        msgBox.setWindowTitle(title)

        reply = msgBox.exec()
        if reply == QMessageBox.StandardButton.Ok:
            return "ok"
    if style == 1:
        # Set the messagebox
        msgBox = QMessageBox()
        msgBox.setIcon(Icon)
        msgBox.setText(text)
        msgBox.setWindowTitle(title)
        # Set the buttons and default button
        msgBox.setStandardButtons(
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        msgBox.setDefaultButton(QMessageBox.StandardButton.No)

        reply = msgBox.exec_()
        if reply == QMessageBox.StandardButton.Yes:
            return "yes"
        if reply == QMessageBox.StandardButton.No:
            return "no"
    if style == 2:
        # Set the messagebox
        msgBox = QMessageBox()
        msgBox.setIcon(Icon)
        msgBox.setText(text)
        msgBox.setWindowTitle(title)
        # Set the buttons and default button
        msgBox.setStandardButtons(
            QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel
        )
        msgBox.setDefaultButton(QMessageBox.StandardButton.Ok)

        reply = msgBox.exec_()
        if reply == QMessageBox.StandardButton.Ok:
            return "ok"
        if reply == QMessageBox.StandardButton.Cancel:
            return "cancel"
    if style == 20:
        Dialog = QInputDialog()
        reply = Dialog.getText(
            None,
            title,
            text,
            text=default,
        )
        if reply[1]:
            # user clicked OK
            replyText = reply[0]
        else:
            # user clicked Cancel
            replyText = reply[0]  # which will be "" if they clicked Cancel
        return str(replyText)
    if style == 21:
        Dialog = QInputDialog()
        reply = Dialog.getItem(
            None,
            title,
            text,
            stringList,
            0,
            True,
        )
        if reply[1]:
            # user clicked OK
            replyText = reply[0]
        else:
            # user clicked Cancel
            replyText = reply[0]  # which will be "" if they clicked Cancel
        return str(replyText)
    if style == 30:
        # Set the messagebox
        msgBox = QMessageBox(mw)
        msgBox.setIcon(Icon)
        msgBox.setText(text)
        msgBox.setWindowTitle(title)
        msgBox.setWindowModality(Qt.WindowModality.NonModal)
        msgBox.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Dialog)

        reply = msgBox.show()
        return


def RestartDialog(message="", includeIcons=False):
    """_summary_
        shows a restart dialog
    Returns:
        string: returns 'yes' if restart now is clicked.
        otherwise returns 'no'
    """
    from PySide.QtWidgets import QMessageBox

    # Save the preferences before restarting
    App.saveParameter()

    # Set the message
    if message == "":
        message = translate(
            "FreeCAD Ribbon",
            "You must restart FreeCAD for changes to take effect.",
        )

    # Set the messagebox
    msgBox = QMessageBox()
    msgBox.setIcon(QMessageBox.Icon.Warning)
    msgBox.setText(message)
    msgBox.setWindowTitle("FreeCAD Ribbon")
    # Set the buttons and default button
    msgBox.setStandardButtons(
        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
    )
    msgBox.setDefaultButton(QMessageBox.StandardButton.No)
    msgBox.button(QMessageBox.StandardButton.Yes).setText(
        translate("FreeCAD Ribbon", "Restart now")
    )
    msgBox.button(QMessageBox.StandardButton.No).setText(
        translate("FreeCAD Ribbon", "Restart later")
    )
    if includeIcons is True:
        msgBox.button(QMessageBox.StandardButton.No).setIcon(
            Gui.getIcon("edit_Cancel.svg")
        )
        msgBox.button(QMessageBox.StandardButton.Yes).setIcon(
            Gui.getIcon("edit_OK.svg")
        )

    reply = msgBox.exec_()
    if reply == QMessageBox.StandardButton.Yes:
        return "yes"
    if reply == QMessageBox.StandardButton.No:
        return "no"


def restart_freecad():
    from PySide import QtWidgets, QtCore

    """Shuts down and restarts FreeCAD"""

    args = QtWidgets.QApplication.arguments()[1:]
    if Gui.getMainWindow().close():
        QtCore.QProcess.startDetached(
            QtWidgets.QApplication.applicationFilePath(), args
        )

    return


def SaveDialog(files, OverWrite: bool = True):
    """
    files must be like:\n
    files = [\n
        ('All Files', '*.*'),\n
        ('Python Files', '*.py'),\n
        ('Text Document', '*.txt')\n
    ]\n
    \n
    OverWrite:\n
    If True, file will be overwritten\n
    If False, only the path+filename will be returned\n
    """
    import tkinter as tk
    from tkinter.filedialog import asksaveasfile
    from tkinter.filedialog import askopenfilename

    # Create the window
    root = tk.Tk()
    # Hide the window
    root.withdraw()

    if OverWrite is True:
        file = asksaveasfile(filetypes=files, defaultextension=files)
        if file is not None:
            return file.name
    if OverWrite is False:
        file = askopenfilename(filetypes=files, defaultextension=files)
        if file is not None:
            return file

def OpenDirectory(path):
    import webbrowser
    import platform
    import subprocess
    import os
    
    try:
        if os.path.exists(path) is False:
            return False
        
        if platform.system().lower() == "darwin":
                subprocess.run(['open', path])
        elif platform.system().lower() == "Windows":
            os.startfile(path)
        else:
            # Linux: try xdg-open, then sensible-browser as fallback 
            try: 
                subprocess.run(['xdg-open', path], check=True) 
            except Exception: 
                subprocess.run(['gio', 'open', path], check=False)          
        return True
    except Exception:
        return False

def GetLetterFromNumber(number: int, UCase: bool = True):
    """Number to Excel-style column name, e.g., 1 = A, 26 = Z, 27 = AA, 703 = AAA."""
    Letter = ""
    while number > 0:
        number, r = divmod(number - 1, 26)
        Letter = chr(r + ord("A")) + Letter
    return Letter


def GetNumberFromLetter(Letter):
    """Excel-style column name to number, e.g., A = 1, Z = 26, AA = 27, AAA = 703."""
    number = 0
    for c in Letter:
        number = number * 26 + 1 + ord(c) - ord("A")
    return number


def ColorConvertor(ColorRGB: [], Alpha: float = 1, Hex=False, KeepHexAlpha=True):
    """
    A single function to convert colors to rgba colors as a tuple of float from 0-1
    ColorRGB:   [255,255,255]
    Alpha:      0-1
    """
    from matplotlib import colors as mcolors

    ColorRed = ColorRGB[0] / 255
    colorGreen = ColorRGB[1] / 255
    colorBlue = ColorRGB[2] / 255

    color = (ColorRed, colorGreen, colorBlue)

    result = mcolors.to_rgba(color, Alpha)
    if Hex is True:
        result = mcolors.to_hex((ColorRed, colorGreen, colorBlue, Alpha), KeepHexAlpha)

    return result


def OpenFile(FileName: str):
    """
    Filename = full path with filename as string
    """
    import subprocess
    import os
    import platform

    try:
        if os.path.exists(FileName):
            if platform.system() == "Darwin":  # macOS
                subprocess.call(("open", FileName))
            elif platform.system() == "Windows":  # Windows
                os.startfile(FileName)
            else:  # linux variants
                print(FileName)
                try:
                    subprocess.check_output(["xdg-open", FileName.strip()])
                except subprocess.CalledProcessError:
                    Print(
                        f"An error occurred when opening {FileName}!\n"
                        + "This can happen when running FreeCAD as an AppImage.\n"
                        + "Please install FreeCAD directly.",
                        "Error",
                    )
        else:
            print(f"Error: {FileName} does not exist.")
    except Exception as e:
        raise e


def Print(Input: str, Type: str = ""):
    """_summary_

    Args:
        Input (str): Text to print.\n
        Type (str, optional): Type of message. (enter Warning, Error or Log). Defaults to "".
    """
    import FreeCAD as App

    if Type == "Warning":
        App.Console.PrintWarning(Input + "\n")
    elif Type == "Error":
        App.Console.PrintError(Input + "\n")
    elif Type == "Log":
        App.Console.PrintLog(Input + "\n")
    else:
        App.Console.PrintMessage(Input + "\n")


def LightOrDark(rgbColor=[0, 128, 255, 255]):
    """_summary_
    reference: https://alienryderflex.com/hsp.html
    Args:
        rgbColor (list, optional): RGB color. Defaults to [0, 128, 255, 255].\n
        note: The alpha value is added for completeness, but us ignored in the equation.

    Returns:
        string: "light or dark"
    """
    [r, g, b, a] = rgbColor
    hsp = math.sqrt(0.299 * (r * r) + 0.587 * (g * g) + 0.114 * (b * b))
    if hsp > 127.5:
        return "light"
    else:
        return "dark"


def GetFileDialog(Filter="", parent=None, DefaultPath="", SaveAs: bool = True) -> str:
    """
    Set filter like:
    "Images (*.png *.xpm .jpg);;Text files (.txt);;XML files (*.xml)"
    SaveAs:\n
        If True,  as SaveAs dialog will open and the file will be overwritten\n
        If False, an OpenFile dialog will be open and the file will be opened.\n
    """
    from PySide.QtWidgets import QFileDialog

    file = ""
    if SaveAs is False:
        file = QFileDialog.getOpenFileName(
            parent=parent, caption="Select a file", dir=DefaultPath, filter=Filter
        )[0]
    if SaveAs is True:
        file = QFileDialog.getSaveFileName(
            parent=parent, caption="Select a file", dir=DefaultPath, filter=Filter
        )[0]
    return file


def GetFolder(parent=None, DefaultPath="") -> str:
    from PySide.QtWidgets import QFileDialog

    Directory = ""
    Directory = QFileDialog.getExistingDirectory(
        parent=parent, caption="Select Folder", dir=DefaultPath
    )

    return Directory


def getRepoAdress(base_path):
    import pathlib
    import os

    try:
        if base_path == "":
            base_path = os.path.dirname(__file__)

        git_dir = pathlib.Path(base_path) / ".git"
        with (git_dir / "FETCH_HEAD").open("r") as head:
            ref = head.readline().split(" ")[-1].strip()

        return ref
    except Exception:
        return ""


def CreateToolbar(Name: str, WorkBenchName: str = "Global", ButtonList: list = []):
    # Define the name for the ToolbarGroup in the FreeCAD Parameters
    ToolbarGroupName = WorkBenchName
    # Define the name for the toolbar
    ToolBarName = Name
    # define the parameter path for the toolbar
    WorkbenchToolBarsParamPath = (
        "User parameter:BaseApp/Workbench/" + ToolbarGroupName + "/Toolbar/"
    )

    # check if there is already a toolbar with the same name
    CustomToolbars: list = App.ParamGet(
        "User parameter:BaseApp/Workbench/Global/Toolbar"
    ).GetGroups()
    for Group in CustomToolbars:
        Parameter = App.ParamGet(
            "User parameter:BaseApp/Workbench/Global/Toolbar/" + Group
        )
        ItemName = Parameter.GetString("Name")
        if ItemName == ToolBarName:
            return ToolBarName

    # add the ToolbarGroup in the FreeCAD Parameters
    WorkbenchToolbar = App.ParamGet(WorkbenchToolBarsParamPath + ToolBarName)

    # Set the name.
    WorkbenchToolbar.SetString("Name", ToolBarName)

    # Set the toolbar active
    WorkbenchToolbar.SetBool("Active", True)

    # add the commands
    for Button in ButtonList:
        WorkbenchToolbar.SetString(Button, "FreeCAD")
    # endregion

    App.saveParameter()
    return ToolBarName


def RemoveWorkBenchToolbars(Name: str, WorkBenchName: str = "Global") -> None:
    # Define the name for the ToolbarGroup in the FreeCAD Parameters
    ToolbarGroupName = WorkBenchName
    # Define the name for the toolbar
    ToolBarName = Name
    # define the parameter path for the toolbar
    ToolBarsParamPath = (
        "User parameter:BaseApp/Workbench/" + ToolbarGroupName + "/Toolbar/"
    )

    custom_toolbars = App.ParamGet(ToolBarsParamPath)
    custom_toolbars.RemGroup(ToolBarName)
    return


def ReturnXML_Value(
    path: str, ElementName: str, attribKey: str = "", attribValue: str = ""
):
    import xml.etree.ElementTree as ET
    import os

    # Passing the path of the
    # xml document to enable the
    # parsing process
    PackageXML = os.path.join(os.path.dirname(__file__), path)
    tree = ET.parse(PackageXML)
    # getting the parent tag of
    # the xml document
    root = tree.getroot()
    result = ""
    for child in root:
        if str(child.tag).split("}")[1] == ElementName:
            if attribKey != "" and attribValue != "":
                for key, value in child.attrib.items():
                    if key == attribKey and value == attribValue:
                        result = child.text
                        return result
            else:
                result = child.text
    return result


def ReturnXML_Value_Git(
    User="apebbers",
    Repository="FreeCAD-Ribbon",
    Branch="main",
    File="package.xml",
    ElementName: str = "",
    attribKey: str = "",
    attribValue: str = "",
    host="https://codeberg.org",
):
    # import requests_local as requests
    import xml.etree.ElementTree as ET
    from urllib import request

    result = None
    try:
        # Passing the path of the
        # xml document to enable the
        # parsing process
        url = f"{host}/{User}/{Repository}/{Branch}/{File}"
        if host == "https://codeberg.org":
           url = f"{host}/{User}/{Repository}/src/branch/{Branch}/{File}" 
        if host == "https://github.com":
            url = f"{host}/{User}/{Repository}/blob/{Branch}/{File}" 
        url = "https://raw.githubusercontent.com/APEbbers/FreeCAD-Ribbon/refs/heads/main/package.xml"
        response = request.urlopen(url)
        data = response.read()
        root: Element[str] = ET.fromstring(data)
        result = ""
        for child in root:
            if str(child.tag).split("}")[1] == ElementName:
                if attribKey != "" and attribValue != "":
                    for key, value in child.attrib.items():
                        if key == attribKey and value == attribValue:
                            result = child.text
                            return result
                else:
                    result = child.text
    except Exception as e:
        # raise e
        pass
    return result


def GetGitData(PrintErrors=False):
    GitInstalled = True
    import os

    try:
        import git
    except ImportError:
        GitInstalled = False

    commit = None
    branch = None
    Contributers = []
    result = [commit, branch, Contributers]

    git_root = os.path.join(os.path.dirname(__file__), ".git")
    if os.path.exists(git_root) is False:
        return result
    git_head = os.path.join(git_root, "HEAD")
    if os.path.exists(git_head) is False:
        return result

    # Read .git/HEAD file
    with open(git_head, "r") as fd:
        head_ref = fd.read()

    # Find head file .git/HEAD (e.g. ref: ref/heads/master => .git/ref/heads/master)
    if not head_ref.startswith("ref: ") and PrintErrors is True:
        print(f"expected 'ref: path/to/head' in {git_head}")
        return result
    head_ref = head_ref[5:].strip()

    # Read commit id from head file
    head_path = os.path.join(git_root, head_ref)
    if os.path.exists(head_path) is False and PrintErrors is True:
        print(f"path {head_path} referenced from {git_head} does not exist")
        return result
    # Read the branch version
    branch = head_path.rsplit("/", 1)[1]
    with open(head_path, "r") as fd:
        line = fd.readlines()[0]
        commit = line.strip()

    # If gitpython is installed, get the list of contributors
    if GitInstalled is True:
        repo = git.Repo(git_root)
        Git = repo.git
        List = Git.execute(
            ["git", "shortlog", "-sn", "-e", "--all"],
            as_process=False,
            stdout_as_string=True,
        )
        UserList = []
        for line in List.splitlines():
            Commits = str(line)[: len("  1418  ") - 1]
            Commits = int(Commits.strip())
            User = str(line)[len("  1418  ") - 1 :].split("<")[0].strip()
            email = (
                str(line)[len("  1418  ") - 1 :].split("<")[1].replace(">", "").strip()
            )

            UserList.append([Commits, User, email])

        tempList = []
        for i in range(len(UserList) - 1):
            User = UserList[i]
            if User[1] not in Contributers and User[1] != "pre-commit-ci[bot]":
                Contributers.append(User[1])
                tempList.append(User)
            if User[1] in Contributers:
                for j in range(len(UserList) - 1):
                    tempUser = UserList[j]
                    if tempUser[2] == User[2] and tempUser[0] > User[0]:
                        Contributers.pop()
                        if (
                            tempUser[1] not in Contributers
                            and tempUser[1] != "pre-commit-ci[bot]"
                        ):
                            Contributers.append(tempUser[1])

        # get the short commit id
        commit = repo.git.rev_parse(repo.head, short=True)

    result = [commit, branch, Contributers]
    return result


def TranslationsMapping(WorkBenchName: str, string: str):
    result = string

    ListSpecialWB = [
        "Assembly4Workbench",
        "A2plusWorkbench",
    ]
    isSpecialWB = False
    for wb in ListSpecialWB:
        if wb == WorkBenchName:
            isSpecialWB = True

    if isSpecialWB is False:
        contextDict_Standard = {
            "WorkFeatureWorkbench": "Workbench",
            "SketcherWorkbench": "Workbench",
            "PartDesignWorkbench": "Workbench",
            "PartWorkbench": "Workbench",
            "SMWorkbench": "Workbench",
            "FrameWorkbench": "Workbench",
            "SurfaceWorkbench": "Workbench",
            "TechDrawWorkbench": "Workbench",
            "FemWorkbench": "Workbench",
            "GearWorkbench": "Workbench",
            "FastenersWorkbench": "Workbench",
            "SpreadsheetWorkbench": "Workbench",
            "InspectionWorkbench": "Workbench",
            "RenderWorkbench": "Workbench",
            "RobotWorkbench": "Workbench",
            "CfdOFWorkbench": "Workbench",
            "PlotWorkbench": "Workbench",
            "BillOfMaterialsWB": "Workbench",
            "DynamicDataWorkbench": "Workbench",
            "AssistantWorkbench": "Workbench",
            "TestWorkbench": "Workbench",
            "ThreadProfileWorkbench": "Workbench",
            "AssemblyWorkbench": "Workbench",
            "BIMWorkbench": "Workbench",
            "CAMWorkbench": "Workbench",
            "MaterialWorkbench": "Workbench",
            "Assembly3Workbench": "asm3",
        }
        try:
            context = contextDict_Standard[WorkBenchName]
        except Exception:
            context = "Workbench"
        result = translate(context, string)

    if WorkBenchName == "Assembly4Workbench":
        ListContext = [
            "Fasteners",
            "Commands",
            "Asm4_Help",
            "Commands1",
            "Asm4_showLcs",
            "Asm4_hideLcs",
        ]
        for i in range(len(ListContext)):
            context = ListContext[i]
            value = translate(context, string)
            if value != string:
                result = value
            if i == len(ListContext) - 1:
                result = string

    if WorkBenchName == "A2plusWorkbench":
        ListContext = [
            "A2p_BoM",
            "A2plus",
            "A2plus_Constraints",
            "A2plus_searchConstraintConflicts",
        ]
        for i in range(len(ListContext)):
            context = ListContext[i]
            value = translate(context, string)
            if value != string:
                result = value
            if i == len(ListContext) - 1:
                result = string

    return result


# # Add or update the dict for the Ribbon command panel
#         self.add_keys_nested_dict(
#             self.Dict_RibbonCommandPanel,
#             ["workbenches", WorkBenchName, "toolbars", Toolbar, "order"],
#         )
def add_keys_nested_dict(dict, keys, default=1, endEmpty = False):
    """_summary_

    Args:
        dict (_type_): Enter dict to create or modify
        keys (_type_): Enter key or list of keys

    Returns:
        bool: True if a new dict is created or modified. Otherwise False
    """
    for key in keys:
        result = False
        if key not in dict:
            dict[key] = {}
            result = True
        dict = dict[key]
    try:
        if endEmpty is False:
            dict.setdefault(keys[-1], default)
    except Exception:
        pass
    return result


def returnDropDownCommands(command):
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


def CommandInfoCorrections(CommandName):
    try:
        Command = Gui.Command.get(CommandName)
        if Command is not None:
            CommandInfo = Command.getInfo()

            if CommandName == "PartDesign_CompSketches":
                CommandInfo["menuText"] = "Create sketch..."
                CommandInfo["toolTip"] = "Create or edit a sketch"
                CommandInfo["whatsThis"] = "PartDesign_CompSketches"
                CommandInfo["statusTip"] = "Create or edit a sketch"

            if CommandName == "Sketcher_Grid":
                CommandInfo["pixmap"] = "Sketcher_GridToggle_Deactivated.svg"
            if CommandName == "Sketcher_Snap":
                CommandInfo["pixmap"] = "Sketcher_Snap_Deactivated.svg"
            if CommandName == "Sketcher_RenderingOrder":
                CommandInfo["pixmap"] = "Sketcher_RenderingOrder_External.svg"

            # add an extra entry for action text
            add_keys_nested_dict(CommandInfo, "ActionText")
            CommandActionList = Command.getAction()
            if len(CommandActionList) > 0:
                CommandAction = CommandActionList[0]
                CommandInfo["ActionText"] = CommandAction.text()
            else:
                CommandInfo["ActionText"] = CommandInfo["menuText"]
            if CommandInfo["ActionText"] == "":
                CommandInfo["ActionText"] = CommandInfo["menuText"]

            ChildCommands = returnDropDownCommands(Command)
            if len(ChildCommands) > 1:
                if not CommandInfo["menuText"].endswith("..."):
                    CommandInfo["menuText"] = CommandInfo["menuText"] + "..."
                if not CommandInfo["ActionText"].endswith("..."):
                    CommandInfo["ActionText"] = CommandInfo["ActionText"] + "..."

            return CommandInfo
        else:
            CommandInfo = {}
            CommandInfo["menuText"] = ""
            CommandInfo["toolTip"] = ""
            CommandInfo["whatsThis"] = ""
            CommandInfo["statusTip"] = ""
            CommandInfo["pixmap"] = ""
            CommandInfo["ActionText"] = ""
            CommandInfo["name"] = ""
    except Exception:
        CommandInfo = {}
        CommandInfo["menuText"] = ""
        CommandInfo["toolTip"] = ""
        CommandInfo["whatsThis"] = ""
        CommandInfo["statusTip"] = ""
        CommandInfo["pixmap"] = ""
        CommandInfo["ActionText"] = ""
        CommandInfo["name"] = ""
    return CommandInfo


def addMissingCommands(CommandList: list):
    MissingCommands = [
        [
            "Sketcher_NewSketch",  # commandname
            "Sketcher_NewSketch",  # iconname
            "Create sketch",  # menu text
            "SketcherWorkbench",  # workbench
        ],
        ["Draft_Line", "Draft_Line", "Line", "DraftWorkbench"],
        ["Draft_Move", "Draft_Move", "Move", "DraftWorkbench"],
        [
            "Draft_LayerManager",
            "Draft_LayerManager",
            "Manage layers...",
            "DraftWorkbench",
        ],
        ["Draft_Snap_Lock", "Draft_Snap_Lock", "Snap lock", "DraftWorkbench"],
        [
            "OpenSCAD_ReplaceObject",
            "OpenSCAD_ReplaceObject",
            "Replace Object",
            "OpenSCADWorkbench",
        ],
        [
            "Part_CheckGeometry",
            "Part_CheckGeometry",
            "Check Geometry",
            "OpenSCADWorkbench",
        ],
    ]

    CopyList = CommandList.copy()

    for Item in CommandList:
        isInList = False
        for MissingCommand in MissingCommands:
            if Item[0] == MissingCommand:
                isInList = True
                break

        if isInList is False:
            CopyList.append(MissingCommand)
    return CopyList


def returnQiCons_Commands(CommandName, pixmap=""):
    from PySide.QtGui import QIcon

    try:
        if len(CommandName.split(", ")) > 1:
            CommandName_1 = CommandName.split(", ")[0]
            ActionNumber = int(CommandName.split(", ")[1])
            ParentCommand = Gui.Command.get(CommandName_1)
            if ParentCommand is not None:
                action = ParentCommand.getAction()[ActionNumber]
                icon = action.icon()
                return icon
    except Exception:
        # raise (e)
        pass

    icon = QIcon()
    if pixmap != "" and pixmap is not None:
        icon = Gui.getIcon(pixmap)
    else:
        try:
            Command = Gui.Command.get(CommandName)
            CommandInfo = Command.getInfo()
            pixmap = CommandInfo["pixmap"]
            icon = Gui.getIcon(pixmap)
        except Exception:
            pass

    if icon is None or (icon is not None and icon.isNull()):
        try:
            Command = Gui.Command.get(CommandName)
            action = Command.getAction()[0]
            icon = action.icon()
        except Exception:
            return None
    return icon


def CorrectGetToolbarItems(ToolbarItems: dict):
    newCommands = []

    if "Structure" in ToolbarItems:
        newCommands = ToolbarItems["Structure"]
        if "Part_Datums" not in newCommands:
            newCommands.append("Part_Datums")
            ToolbarItems.update({"Structure": newCommands})

    return ToolbarItems


def ShortCutTaken(ShortCut: str):
    ListWithCommands = Gui.Command.listByShortcut(ShortCut)

    if len(ListWithCommands) > 0:
        return True
    return False


def ReturnWrappedText(text: str, max_length: int = 50, max_Lines=0, returnList=False):
    import textwrap

    result = ""

    # Wrap the text as list
    wrapped_text = textwrap.wrap(text=text, width=max_length)

    # remove spaces at the end of each line
    for line in wrapped_text:
        line = textwrap.dedent(line)

    # remove any line that is more then> allowed
    if max_Lines > 0 and len(wrapped_text) > max_Lines:
        for i in range(max_Lines, len(wrapped_text)):
            try:
                wrapped_text.pop(i)
            except Exception:
                continue

    # return the desired result
    if returnList is False:
        result = "\n".join(wrapped_text)
    else:
        result = wrapped_text
    # print(result)
    return result


def AddToClipboard(Text):
    # import subprocess
    # import platform
    from PySide import QtWidgets, QtCore

    # cmd = "clip" if platform.system() == "Windows" else "pbcopy"
    # subprocess.run(cmd, input=Text, text=True, shell=True)
    
    clipboard = QtWidgets.QApplication.clipboard()
    clipboard.setText(Text)


def checkFreeCADVersion(main: int, sub: int, patch: int, git: int):
    """Checks if the FreeCAD version is equal or newer than the given version number.

    Args:
        main (int): Main version number
        sub (int): Secundair version number
        patch (int): Patch number
        git (int): gitnumber

    Returns:
        True if the FreeCAD version is equal or higher than the given version number.
    """    
    version = App.Version()
    # print(version)

    if main >= int(version[0]):
        if sub >= int(version[1]):
            if patch >= int(version[2]):
                git_version = int(version[3].split(" ")[0])
                if git_version >= git:
                    return True

    return False
