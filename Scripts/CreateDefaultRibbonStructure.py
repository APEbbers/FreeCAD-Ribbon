# *************************************************************************
# *                                                                       *
# * Copyright (c) 2024 Paul Ebbers                                        *
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

# This script can be used to generate a default json file.
# You can add any customization that you have in this file.
# For workbenches and toolbars that don't have a customization, for each toolbar, the first command is set to large.
# The goal of this script is to provide a starting point for your own ribbon customization.
# The file "RibbonStructure_default.json" is used by the reset button to replace RibbonStructure.json with "RibbonStructure_default.json".

import FreeCAD as App
import FreeCADGui as Gui
import os

import json

from PySide.QtWidgets import QToolBar, QToolButton

ParentPath = os.path.dirname(os.path.dirname(__file__))

# Set the path where you want to save this new Json file
# JsonPath = os.path.dirname(__file__)
JsonPath = ParentPath

# Set the file name. Default is "RibbonStructure_default.json".
# This is the file used to reset the ribbon.
JsonName = "RibbonStructure_default.json"

# Enable inclusion of customized workbenches.
# See row 101
IncludeCustomJson = True  # Set to false if not needed

# Set the size for the first icon in every toolbar/panel
FirstIconSize = "large"  # set to "small" or medium as per preference
# Set the size for the remaining icons in every toolbar
OtherIconSize = "small"  # set to "medium" or "large" as per preference

# Define list of the workbenches, toolbars and commands on class level
List_Workbenches = []
StringList_Toolbars = []
List_Commands = []

# Create lists for the several list in the json file.
List_IgnoredToolbars = [
    "Clipboard",
    "Edit",
    "File",
    "Help",
    "Macro",
    "View",
    "Workbench",
]
List_IconOnlyToolbars = ["Structure", "Individual views"]
List_QuickAccessCommands = [
    "Std_New",
    "Std_Open",
    "Std_Save",
    "Std_Undo",
    "Std_Redo",
    "Std_Refresh",
    "Std_Cut",
    "Std_Copy",
    "Std_Paste",
]
List_IgnoredWorkbenches = [
    "Inspection",
    "OpenSCAD",
    "Points",
    "Reverse Engineering",
    "Robot",
    "Test Framework",
]
# Empty definitions of the Dicts for the ribbon and custom panels
Dict_RibbonCommandPanel = {}
Dict_CustomPanels = {}

# Add workbenches here that you want to exclude from this script.
skipWorkbenchList = []
# skipWorkbenchList = ["PartDesignWorkbench", "AssemblyWorkbench", "SketcherWorkbench"]

# Add toolbars which must have only small icons:
smallOnlyToolbars = ["Structure", "Individual views"]

# Add here your customized panels (toolbars)
Dict_CustomPanels = {
    "customToolbars": {
        "FemWorkbench": {
            "Loads & Constraints_custom": {
                "commands": {
                    "Electromagnetic boundary conditions": "Electromagnetic boundary conditions",
                    "Initial flow velocity condition": "Fluid boundary conditions",
                    "Initial pressure condition": "Fluid boundary conditions",
                    "Flow velocity boundary condition": "Fluid boundary conditions",
                    "Fixed boundary condition": "Mechanical boundary conditions and loads",
                    "Rigid body constraint": "Mechanical boundary conditions and loads",
                    "Displacement boundary condition": "Mechanical boundary conditions and loads",
                    "Contact constraint": "Mechanical boundary conditions and loads",
                    "Tie constraint": "Mechanical boundary conditions and loads",
                    "Spring": "Mechanical boundary conditions and loads",
                    "Force load": "Mechanical boundary conditions and loads",
                    "Pressure load": "Mechanical boundary conditions and loads",
                    "Centrifugal load": "Mechanical boundary conditions and loads",
                    "Gravity load": "Mechanical boundary conditions and loads",
                    "Initial temperature": "Thermal boundary conditions and loads",
                    "Heat flux load": "Thermal boundary conditions and loads",
                    "Temperature boundary condition": "Thermal boundary conditions and loads",
                    "Body heat source": "Thermal boundary conditions and loads",
                }
            }
        },
        "TechDrawWorkbench": {
            "TechDraw Dimensions_custom": {
                "commands": {
                    "Dimension": "TechDraw Dimensions",
                    "Insert Balloon Annotation": "TechDraw Dimensions",
                    "Axonometric length dimension": "TechDraw Dimensions",
                    "Insert Landmark Dimension - EXPERIMENTAL": "TechDraw Dimensions",
                    "Repair Dimension References": "TechDraw Dimensions",
                    "Insert '\u2300' Prefix": "TechDraw Extend Dimensions",
                    "Increase Decimal Places": "TechDraw Extend Dimensions",
                }
            }
        },
    },
}

# Add here your customized workbenches to include.
CustomJson_Workbenches = {
    "workbenches": {
        "PartDesignWorkbench": {
            "toolbars": {
                "Part Design Helper": {
                    "order": [
                        "Create datum",
                        "Create datum",
                        "Create body",
                        "Check Geometry",
                        "Create a sub-object(s) shape binder",
                        "Create a clone",
                        "Validate sketch",
                    ],
                    "commands": {
                        "PartDesign_CompSketches": {
                            "size": "large",
                            "text": "Create datum",
                            "icon": "",
                        },
                        "PartDesign_Body": {
                            "size": "small",
                            "text": "Create body",
                            "icon": "PartDesign_Body",
                        },
                        "Sketcher_ValidateSketch": {
                            "size": "small",
                            "text": "Validate sketch",
                            "icon": "Sketcher_ValidateSketch",
                        },
                        "Part_CheckGeometry": {
                            "size": "small",
                            "text": "Check Geometry",
                            "icon": "Part_CheckGeometry",
                        },
                        "PartDesign_SubShapeBinder": {
                            "size": "small",
                            "text": "Create a sub-object(s) shape binder",
                            "icon": "PartDesign_SubShapeBinder",
                        },
                        "PartDesign_Clone": {
                            "size": "small",
                            "text": "Create a clone",
                            "icon": "PartDesign_Clone",
                        },
                        "PartDesign_CompDatums": {
                            "size": "large",
                            "text": "Create datum",
                            "icon": "",
                        },
                    },
                },
                "Part Design Modeling": {
                    "order": [
                        "Pad",
                        "Revolution",
                        "2_separator_PartDesignWorkbench",
                        "Pocket",
                        "Hole",
                        "Groove",
                        "Additive helix",
                        "Additive loft",
                        "Additive pipe",
                        "8_separator_PartDesignWorkbench",
                        "Subtractive loft",
                        "Subtractive pipe",
                        "Subtractive helix",
                        "Boolean operation",
                        "Create an additive primitive",
                        "Create a subtractive primitive",
                    ],
                    "commands": {
                        "PartDesign_Pad": {
                            "size": "large",
                            "text": "Pad",
                            "icon": "PartDesign_Pad",
                        },
                        "PartDesign_Revolution": {
                            "size": "large",
                            "text": "Revolution",
                            "icon": "PartDesign_Revolution",
                        },
                        "PartDesign_AdditiveLoft": {
                            "size": "large",
                            "text": "Additive loft",
                            "icon": "PartDesign_AdditiveLoft",
                        },
                        "PartDesign_AdditivePipe": {
                            "size": "small",
                            "text": "Additive pipe",
                            "icon": "PartDesign_AdditivePipe",
                        },
                        "PartDesign_AdditiveHelix": {
                            "size": "large",
                            "text": "Additive helix",
                            "icon": "PartDesign_AdditiveHelix",
                        },
                        "PartDesign_CompPrimitiveAdditive": {
                            "size": "small",
                            "text": "Add a primitive",
                            "icon": "",
                        },
                        "PartDesign_Pocket": {
                            "size": "large",
                            "text": "Pocket",
                            "icon": "PartDesign_Pocket",
                        },
                        "PartDesign_Hole": {
                            "size": "large",
                            "text": "Hole",
                            "icon": "PartDesign_Hole",
                        },
                        "PartDesign_Groove": {
                            "size": "large",
                            "text": "Groove",
                            "icon": "PartDesign_Groove",
                        },
                        "PartDesign_SubtractiveLoft": {
                            "size": "small",
                            "text": "Subtractive loft",
                            "icon": "PartDesign_SubtractiveLoft",
                        },
                        "PartDesign_SubtractivePipe": {
                            "size": "small",
                            "text": "Subtractive pipe",
                            "icon": "PartDesign_SubtractivePipe",
                        },
                        "PartDesign_SubtractiveHelix": {
                            "size": "small",
                            "text": "Subtractive helix",
                            "icon": "PartDesign_SubtractiveHelix",
                        },
                        "PartDesign_CompPrimitiveSubtractive": {
                            "size": "small",
                            "text": "Substract a primitive",
                            "icon": "",
                        },
                        "PartDesign_Boolean": {
                            "size": "large",
                            "text": "Boolean",
                            "icon": "PartDesign_Boolean",
                        },
                    },
                },
                "Individual views": {
                    "order": [
                        "Isometric",
                        "Front",
                        "Top",
                        "Right",
                        "Rear",
                        "Bottom",
                        "Left",
                    ],
                    "commands": {
                        "Std_ViewIsometric": {
                            "size": "small",
                            "text": "Isometric",
                            "icon": "view-axonometric",
                        },
                        "Std_ViewFront": {
                            "size": "small",
                            "text": "Front",
                            "icon": "view-front",
                        },
                        "Std_ViewTop": {
                            "size": "small",
                            "text": "Top",
                            "icon": "view-top",
                        },
                        "Std_ViewRight": {
                            "size": "small",
                            "text": "Right",
                            "icon": "view-right",
                        },
                        "Std_ViewRear": {
                            "size": "small",
                            "text": "Rear",
                            "icon": "view-rear",
                        },
                        "Std_ViewBottom": {
                            "size": "small",
                            "text": "Bottom",
                            "icon": "view-bottom",
                        },
                        "Std_ViewLeft": {
                            "size": "small",
                            "text": "Left",
                            "icon": "view-left",
                        },
                    },
                },
                "order": [
                    "Individual views",
                    "Structure",
                    "Part Design Helper",
                    "Part Design Modeling",
                    "Part Design Dressup",
                    "Part Design Patterns",
                ],
                "Structure": {
                    "order": [
                        "Create part",
                        "Create group",
                        "Link actions",
                        "Create a variable set",
                    ],
                    "commands": {
                        "Std_Part": {
                            "size": "small",
                            "text": "Create part",
                            "icon": "Geofeaturegroup",
                        },
                        "Std_Group": {
                            "size": "small",
                            "text": "Create group",
                            "icon": "folder",
                        },
                        "Std_LinkActions": {
                            "size": "small",
                            "text": "Link actions",
                            "icon": "",
                        },
                        "Std_VarSet": {
                            "size": "small",
                            "text": "Create a variable set",
                            "icon": "VarSet",
                        },
                    },
                },
                "Part Design Dressup": {
                    "order": ["Fillet", "Chamfer", "Draft", "Thickness"],
                    "commands": {
                        "PartDesign_Fillet": {
                            "size": "large",
                            "text": "Fillet",
                            "icon": "PartDesign_Fillet",
                        },
                        "PartDesign_Chamfer": {
                            "size": "large",
                            "text": "Chamfer",
                            "icon": "PartDesign_Chamfer",
                        },
                        "PartDesign_Draft": {
                            "size": "small",
                            "text": "Draft",
                            "icon": "PartDesign_Draft",
                        },
                        "PartDesign_Thickness": {
                            "size": "small",
                            "text": "Thickness",
                            "icon": "PartDesign_Thickness",
                        },
                    },
                },
                "Part Design Patterns": {
                    "order": [
                        "LinearPattern",
                        "Mirrored",
                        "PolarPattern",
                        "Create MultiTransform",
                    ],
                    "commands": {
                        "PartDesign_Mirrored": {
                            "size": "large",
                            "text": "Mirrored",
                            "icon": "PartDesign_Mirrored",
                        },
                        "PartDesign_LinearPattern": {
                            "size": "large",
                            "text": "LinearPattern",
                            "icon": "PartDesign_LinearPattern",
                        },
                        "PartDesign_PolarPattern": {
                            "size": "small",
                            "text": "PolarPattern",
                            "icon": "PartDesign_PolarPattern",
                        },
                        "PartDesign_MultiTransform": {
                            "size": "small",
                            "text": "Create MultiTransform",
                            "icon": "PartDesign_MultiTransform",
                        },
                    },
                },
            }
        },
        "BIMWorkbench": {
            "toolbars": {
                "Drafting tools": {
                    "order": [
                        "Sketch",
                        "Line",
                        "Polyline",
                        "Circle",
                        "Arc",
                        "Arc by 3 points",
                        "Fillet",
                        "Ellipse",
                        "Polygon",
                        "Rectangle",
                        "B-spline",
                        "B\u00e9zier curve",
                        "Cubic B\u00e9zier curve",
                        "Point",
                    ],
                    "commands": {
                        "BIM_Sketch": {
                            "size": "large",
                            "text": "Sketch",
                            "icon": "Sketch",
                        },
                        "Draft_Line": {
                            "size": "small",
                            "text": "Line",
                            "icon": "Draft_Line",
                        },
                        "Draft_Wire": {
                            "size": "small",
                            "text": "Polyline",
                            "icon": "Draft_Wire",
                        },
                        "Draft_Circle": {
                            "size": "small",
                            "text": "Circle",
                            "icon": "Draft_Circle",
                        },
                        "Draft_Arc": {
                            "size": "small",
                            "text": "Arc",
                            "icon": "Draft_Arc",
                        },
                        "Draft_Arc_3Points": {
                            "size": "small",
                            "text": "Arc by 3 points",
                            "icon": "Draft_Arc_3Points",
                        },
                        "Draft_Fillet": {
                            "size": "small",
                            "text": "Fillet",
                            "icon": "Draft_Fillet",
                        },
                        "Draft_Ellipse": {
                            "size": "small",
                            "text": "Ellipse",
                            "icon": "Draft_Ellipse",
                        },
                        "Draft_Polygon": {
                            "size": "small",
                            "text": "Polygon",
                            "icon": "Draft_Polygon",
                        },
                        "Draft_Rectangle": {
                            "size": "small",
                            "text": "Rectangle",
                            "icon": "Draft_Rectangle",
                        },
                        "Draft_BSpline": {
                            "size": "small",
                            "text": "B-spline",
                            "icon": "Draft_BSpline",
                        },
                        "Draft_BezCurve": {
                            "size": "small",
                            "text": "B\u00e9zier curve",
                            "icon": "Draft_BezCurve",
                        },
                        "Draft_CubicBezCurve": {
                            "size": "small",
                            "text": "Cubic B\u00e9zier curve",
                            "icon": "Draft_CubicBezCurve",
                        },
                        "Draft_Point": {
                            "size": "small",
                            "text": "Point",
                            "icon": "Draft_Point",
                        },
                    },
                },
                "Draft snap": {
                    "order": [
                        "Snap lock",
                        "Snap endpoint",
                        "Snap midpoint",
                        "Snap center",
                        "Snap angle",
                        "Snap intersection",
                        "Snap perpendicular",
                        "Snap extension",
                        "Snap parallel",
                        "Snap special",
                        "Snap near",
                        "Snap ortho",
                        "Snap grid",
                        "Snap working plane",
                        "Snap dimensions",
                        "Toggle grid",
                    ],
                    "commands": {
                        "Draft_Snap_Lock": {
                            "size": "large",
                            "text": "Snap lock",
                            "icon": "Draft_Snap_Lock",
                        }
                    },
                },
                "3D/BIM tools": {
                    "order": [
                        "Project",
                        "Site",
                        "Building",
                        "Level",
                        "Space",
                        "Wall",
                        "Curtain Wall",
                        "Column",
                        "Beam",
                        "Slab",
                        "Door",
                        "Window",
                        "Pipe",
                        "Connector",
                        "Stairs",
                        "Roof",
                        "Panel",
                        "Frame",
                        "Fence",
                        "Truss",
                        "Equipment",
                        "Custom Rebar",
                        "Generic 3D tools",
                    ],
                    "commands": {
                        "BIM_Project": {
                            "size": "large",
                            "text": "Project",
                            "icon": "BIM_Project",
                        }
                    },
                },
                "Annotation tools": {
                    "order": [
                        "Text",
                        "Shape from text",
                        "Aligned dimension",
                        "Horizontal dimension",
                        "Vertical dimension",
                        "Leader",
                        "Label",
                        "Axis",
                        "Axis System",
                        "Grid",
                        "Section Plane",
                        "Hatch",
                        "Page",
                        "View",
                        "Shape-based view",
                    ],
                    "commands": {
                        "BIM_Text": {
                            "size": "large",
                            "text": "Text",
                            "icon": "Draft_Text",
                        }
                    },
                },
                "General modification tools": {
                    "order": [
                        "Move",
                        "Copy",
                        "Rotate",
                        "Clone",
                        "Create simple copy",
                        "Make compound",
                    ],
                    "commands": {
                        "Draft_Move": {
                            "size": "large",
                            "text": "Move",
                            "icon": "Draft_Move",
                        }
                    },
                },
                "2D modification tools": {
                    "order": [
                        "Offset",
                        "2D Offset",
                        "Trimex",
                        "Join",
                        "Split",
                        "Scale",
                        "Stretch",
                        "Draft to sketch",
                    ],
                    "commands": {
                        "Draft_Offset": {
                            "size": "large",
                            "text": "Offset",
                            "icon": "Draft_Offset",
                        }
                    },
                },
                "Object modification tools": {
                    "order": [
                        "Upgrade",
                        "Downgrade",
                        "Add component",
                        "Remove component",
                    ],
                    "commands": {
                        "Draft_Upgrade": {
                            "size": "large",
                            "text": "Upgrade",
                            "icon": "Draft_Upgrade",
                        }
                    },
                },
                "3D modification tools": {
                    "order": [
                        "Array",
                        "Path array",
                        "Polar array",
                        "Point array",
                        "Cut with plane",
                        "Mirror",
                        "Extrude",
                        "Difference",
                        "Union",
                        "Intersection",
                    ],
                    "commands": {
                        "Draft_OrthoArray": {
                            "size": "large",
                            "text": "Array",
                            "icon": "Draft_Array",
                        }
                    },
                },
                "Manage tools": {
                    "order": [
                        "BIM Setup",
                        "Views manager",
                        "Manage project",
                        "Manage doors and windows",
                        "Manage IFC elements",
                        "Manage IFC quantities",
                        "Manage IFC properties",
                        "Manage classification",
                        "Manage layers",
                        "Material",
                        "Schedule",
                        "Preflight checks",
                        "Annotation styles",
                    ],
                    "commands": {
                        "BIM_Setup": {
                            "size": "large",
                            "text": "BIM Setup...",
                            "icon": ":icons/preferences-system.svg",
                        }
                    },
                },
                "order": [],
                "Individual views": {
                    "order": [
                        "Isometric",
                        "Front",
                        "Top",
                        "Right",
                        "Rear",
                        "Bottom",
                        "Left",
                    ],
                    "commands": {
                        "Std_ViewIsometric": {
                            "size": "small",
                            "text": "Isometric",
                            "icon": "view-axonometric",
                        },
                        "Std_ViewFront": {
                            "size": "small",
                            "text": "Front",
                            "icon": "view-front",
                        },
                        "Std_ViewTop": {
                            "size": "small",
                            "text": "Top",
                            "icon": "view-top",
                        },
                        "Std_ViewRight": {
                            "size": "small",
                            "text": "Right",
                            "icon": "view-right",
                        },
                        "Std_ViewRear": {
                            "size": "small",
                            "text": "Rear",
                            "icon": "view-rear",
                        },
                        "Std_ViewBottom": {
                            "size": "small",
                            "text": "Bottom",
                            "icon": "view-bottom",
                        },
                        "Std_ViewLeft": {
                            "size": "small",
                            "text": "Left",
                            "icon": "view-left",
                        },
                    },
                },
                "Structure": {
                    "order": [
                        "Create part",
                        "Create group",
                        "Link actions",
                        "Create a variable set",
                    ],
                    "commands": {
                        "Std_Part": {
                            "size": "small",
                            "text": "Create part",
                            "icon": "Geofeaturegroup",
                        },
                        "Std_Group": {
                            "size": "small",
                            "text": "Create group",
                            "icon": "folder",
                        },
                        "Std_LinkActions": {
                            "size": "small",
                            "text": "Link actions",
                            "icon": "",
                        },
                        "Std_VarSet": {
                            "size": "small",
                            "text": "Create a variable set",
                            "icon": "VarSet",
                        },
                    },
                },
            }
        },
        "CAMWorkbench": {
            "toolbars": {
                "Project Setup": {
                    "order": [
                        "Job",
                        "Post Process",
                        "Check the CAM job for common errors",
                    ],
                    "commands": {"CAM_Job": {"size": "large", "text": "Job", "icon": "CAM_Job"}},
                },
                "Tool Commands": {
                    "order": [
                        "Inspect toolPath Commands",
                        "CAM Simulator",
                        "New CAM Simulator",
                        "Finish Selecting Loop",
                        "Toggle the Active State of the Operation",
                        "ToolBit Dock",
                    ],
                    "commands": {
                        "CAM_Inspect": {
                            "size": "large",
                            "text": "Inspect toolPath",
                            "icon": "CAM_Inspect",
                        },
                        "CAM_Simulator": {
                            "size": "small",
                            "text": "CAM Simulator",
                            "icon": "CAM_Simulator",
                        },
                        "CAM_SimulatorGL": {
                            "size": "small",
                            "text": "New CAM Simulator",
                            "icon": "CAM_SimulatorGL",
                        },
                        "CAM_SelectLoop": {
                            "size": "small",
                            "text": "Finish Selecting Loop",
                            "icon": "CAM_SelectLoop",
                        },
                        "CAM_OpActiveToggle": {
                            "size": "small",
                            "text": "Toggle the Active State of the Operation",
                            "icon": "CAM_OpActive",
                        },
                        "CAM_ToolBitDock": {
                            "size": "small",
                            "text": "ToolBit Dock",
                            "icon": "CAM_ToolTable",
                        },
                    },
                },
                "New Operations": {
                    "order": [
                        "Profile",
                        "Pocket Shape",
                        "Drilling",
                        "Face",
                        "Helix",
                        "Adaptive",
                        "Engraving Operations",
                        "3D Pocket",
                    ],
                    "commands": {
                        "CAM_Profile": {
                            "size": "large",
                            "text": "Profile",
                            "icon": "CAM_Profile",
                        }
                    },
                },
                "Path Modification": {
                    "order": ["Copy the operation in the job", "Array", "Simple Copy"],
                    "commands": {
                        "CAM_OperationCopy": {
                            "size": "large",
                            "text": "Copy operation",
                            "icon": "CAM_OpCopy",
                        },
                        "CAM_Array": {
                            "size": "small",
                            "text": "Array",
                            "icon": "CAM_Array",
                        },
                        "CAM_SimpleCopy": {
                            "size": "small",
                            "text": "Simple Copy",
                            "icon": "CAM_SimpleCopy",
                        },
                    },
                },
                "order": [],
                "Individual views": {
                    "order": [
                        "Isometric",
                        "Front",
                        "Top",
                        "Right",
                        "Rear",
                        "Bottom",
                        "Left",
                    ],
                    "commands": {
                        "Std_ViewIsometric": {
                            "size": "small",
                            "text": "Isometric",
                            "icon": "view-axonometric",
                        },
                        "Std_ViewFront": {
                            "size": "small",
                            "text": "Front",
                            "icon": "view-front",
                        },
                        "Std_ViewTop": {
                            "size": "small",
                            "text": "Top",
                            "icon": "view-top",
                        },
                        "Std_ViewRight": {
                            "size": "small",
                            "text": "Right",
                            "icon": "view-right",
                        },
                        "Std_ViewRear": {
                            "size": "small",
                            "text": "Rear",
                            "icon": "view-rear",
                        },
                        "Std_ViewBottom": {
                            "size": "small",
                            "text": "Bottom",
                            "icon": "view-bottom",
                        },
                        "Std_ViewLeft": {
                            "size": "small",
                            "text": "Left",
                            "icon": "view-left",
                        },
                    },
                },
            }
        },
        "FemWorkbench": {
            "toolbars": {
                "Model": {
                    "order": [
                        "Analysis container",
                        "Material for solid",
                        "Material for fluid",
                        "Nonlinear mechanical material",
                        "Reinforced material (concrete)",
                        "Material editor",
                        "Beam cross section",
                        "Beam rotation",
                        "Shell plate thickness",
                        "Fluid section for 1D flow",
                    ],
                    "commands": {
                        "FEM_Analysis": {
                            "size": "large",
                            "text": "Analysis container",
                            "icon": "FEM_Analysis",
                        }
                    },
                },
                "Electromagnetic boundary conditions": {
                    "order": ["Electromagnetic boundary conditions"],
                    "commands": {
                        "FEM_CompEmConstraints": {
                            "size": "large",
                            "text": "Electromagnetic boundary conditions",
                            "icon": "",
                        }
                    },
                },
                "Fluid boundary conditions": {
                    "order": [
                        "Initial flow velocity condition",
                        "Initial pressure condition",
                        "Flow velocity boundary condition",
                    ],
                    "commands": {
                        "FEM_ConstraintInitialFlowVelocity": {
                            "size": "large",
                            "text": "Initial flow velocity condition",
                            "icon": "FEM_ConstraintInitialFlowVelocity",
                        }
                    },
                },
                "Geometrical analysis features": {
                    "order": [
                        "Plane multi-point constraint",
                        "Section print feature",
                        "Local coordinate system",
                    ],
                    "commands": {
                        "FEM_ConstraintPlaneRotation": {
                            "size": "large",
                            "text": "Multi-point constraint",
                            "icon": "FEM_ConstraintPlaneRotation",
                        },
                        "FEM_ConstraintSectionPrint": {
                            "size": "small",
                            "text": "Section print feature",
                            "icon": "FEM_ConstraintSectionPrint",
                        },
                        "FEM_ConstraintTransform": {
                            "size": "small",
                            "text": "Local coordinate system",
                            "icon": "FEM_ConstraintTransform",
                        },
                    },
                },
                "Mechanical boundary conditions and loads": {
                    "order": [
                        "Fixed boundary condition",
                        "Rigid body constraint",
                        "Displacement boundary condition",
                        "Contact constraint",
                        "Tie constraint",
                        "Spring",
                        "Force load",
                        "Pressure load",
                        "Centrifugal load",
                        "Gravity load",
                    ],
                    "commands": {
                        "FEM_ConstraintFixed": {
                            "size": "large",
                            "text": "Fixed boundary condition",
                            "icon": "FEM_ConstraintFixed",
                        }
                    },
                },
                "Thermal boundary conditions and loads": {
                    "order": [
                        "Initial temperature",
                        "Heat flux load",
                        "Temperature boundary condition",
                        "Body heat source",
                    ],
                    "commands": {
                        "FEM_ConstraintInitialTemperature": {
                            "size": "large",
                            "text": "Initial temperature",
                            "icon": "FEM_ConstraintInitialTemperature",
                        },
                        "FEM_ConstraintHeatflux": {
                            "size": "small",
                            "text": "Heat flux load",
                            "icon": "FEM_ConstraintHeatflux",
                        },
                        "FEM_ConstraintTemperature": {
                            "size": "small",
                            "text": "Temperature boundary condition",
                            "icon": "FEM_ConstraintTemperature",
                        },
                        "FEM_ConstraintBodyHeatSource": {
                            "size": "small",
                            "text": "Body heat source",
                            "icon": "FEM_ConstraintBodyHeatSource",
                        },
                    },
                },
                "Mesh": {
                    "order": [
                        "FEM mesh from shape by Netgen",
                        "FEM mesh from shape by Gmsh",
                        "FEM mesh boundary layer",
                        "FEM mesh refinement",
                        "FEM mesh group",
                        "FEM mesh to mesh",
                    ],
                    "commands": {
                        "FEM_MeshNetgenFromShape": {
                            "size": "large",
                            "text": "Netgen mesh",
                            "icon": "FEM_MeshNetgenFromShape",
                        },
                        "FEM_MeshGmshFromShape": {
                            "size": "small",
                            "text": "FEM mesh from shape by Gmsh",
                            "icon": "FEM_MeshGmshFromShape",
                        },
                        "FEM_MeshBoundaryLayer": {
                            "size": "small",
                            "text": "FEM mesh boundary layer",
                            "icon": "FEM_MeshBoundaryLayer",
                        },
                        "FEM_MeshRegion": {
                            "size": "small",
                            "text": "FEM mesh refinement",
                            "icon": "FEM_MeshRegion",
                        },
                        "FEM_MeshGroup": {
                            "size": "small",
                            "text": "FEM mesh group",
                            "icon": "FEM_MeshGroup",
                        },
                        "FEM_FEMMesh2Mesh": {
                            "size": "small",
                            "text": "FEM mesh to mesh",
                            "icon": "FEM_FEMMesh2Mesh",
                        },
                    },
                },
                "Solve": {
                    "order": [
                        "Solver CalculiX Standard",
                        "Mechanical equations",
                        "Electromagnetic equations",
                        "Flow equation",
                        "Flux equation",
                        "Heat equation",
                        "Solver job control",
                        "Run solver calculations",
                    ],
                    "commands": {
                        "FEM_SolverCalculiXCcxTools": {
                            "size": "large",
                            "text": "CalculiX solver",
                            "icon": "FEM_SolverStandard",
                        },
                        "FEM_CompMechEquations": {
                            "size": "small",
                            "text": "Mechanical equations",
                            "icon": "",
                        },
                        "FEM_CompEmEquations": {
                            "size": "small",
                            "text": "Electromagnetic equations",
                            "icon": "",
                        },
                        "FEM_EquationFlow": {
                            "size": "small",
                            "text": "Flow equation",
                            "icon": "FEM_EquationFlow",
                        },
                        "FEM_EquationFlux": {
                            "size": "small",
                            "text": "Flux equation",
                            "icon": "FEM_EquationFlux",
                        },
                        "FEM_EquationHeat": {
                            "size": "small",
                            "text": "Heat equation",
                            "icon": "FEM_EquationHeat",
                        },
                        "FEM_SolverControl": {
                            "size": "small",
                            "text": "Solver job control",
                            "icon": "FEM_SolverControl",
                        },
                        "FEM_SolverRun": {
                            "size": "small",
                            "text": "Run solver calculations",
                            "icon": "FEM_SolverRun",
                        },
                    },
                },
                "Results": {
                    "order": [
                        "Purge results",
                        "Show result",
                        "Apply changes to pipeline",
                        "Post pipeline from result",
                        "Warp filter",
                        "Scalar clip filter",
                        "Function cut filter",
                        "Region clip filter",
                        "Contours filter",
                        "Line clip filter",
                        "Stress linearization plot",
                        "Data at point clip filter",
                        "Filter functions",
                    ],
                    "commands": {
                        "FEM_ResultsPurge": {
                            "size": "large",
                            "text": "Purge results",
                            "icon": "FEM_ResultsPurge",
                        },
                        "FEM_ResultShow": {
                            "size": "small",
                            "text": "Show result",
                            "icon": "FEM_ResultShow",
                        },
                        "FEM_PostApplyChanges": {
                            "size": "small",
                            "text": "Apply changes to pipeline",
                            "icon": "view-refresh",
                        },
                        "FEM_PostPipelineFromResult": {
                            "size": "small",
                            "text": "Post pipeline from result",
                            "icon": "FEM_PostPipelineFromResult",
                        },
                        "FEM_PostFilterWarp": {
                            "size": "small",
                            "text": "Warp filter",
                            "icon": "FEM_PostFilterWarp",
                        },
                        "FEM_PostFilterClipScalar": {
                            "size": "small",
                            "text": "Scalar clip filter",
                            "icon": "FEM_PostFilterClipScalar",
                        },
                        "FEM_PostFilterCutFunction": {
                            "size": "small",
                            "text": "Function cut filter",
                            "icon": "FEM_PostFilterCutFunction",
                        },
                        "FEM_PostFilterClipRegion": {
                            "size": "small",
                            "text": "Region clip filter",
                            "icon": "FEM_PostFilterClipRegion",
                        },
                        "FEM_PostFilterContours": {
                            "size": "small",
                            "text": "Contours filter",
                            "icon": "FEM_PostFilterContours",
                        },
                        "FEM_PostFilterDataAlongLine": {
                            "size": "small",
                            "text": "Line clip filter",
                            "icon": "FEM_PostFilterDataAlongLine",
                        },
                        "FEM_PostFilterLinearizedStresses": {
                            "size": "small",
                            "text": "Stress linearization plot",
                            "icon": "FEM_PostFilterLinearizedStresses",
                        },
                        "FEM_PostFilterDataAtPoint": {
                            "size": "small",
                            "text": "Data at point clip filter",
                            "icon": "FEM_PostFilterDataAtPoint",
                        },
                        "FEM_PostCreateFunctions": {
                            "size": "small",
                            "text": "Filter functions",
                            "icon": "",
                        },
                    },
                },
                "Utilities": {
                    "order": [
                        "Clipping plane on face",
                        "Remove all clipping planes",
                        "Open FEM examples",
                    ],
                    "commands": {
                        "FEM_ClippingPlaneAdd": {
                            "size": "large",
                            "text": "Clipping plane",
                            "icon": "FEM_ClippingPlaneAdd",
                        },
                        "FEM_ClippingPlaneRemoveAll": {
                            "size": "small",
                            "text": "Remove all clipping planes",
                            "icon": "FEM_ClippingPlaneRemoveAll",
                        },
                        "FEM_Examples": {
                            "size": "small",
                            "text": "Open FEM examples",
                            "icon": "FemWorkbench",
                        },
                    },
                },
                "order": [
                    "Individual views",
                    "Structure",
                    "Model",
                    "Geometrical analysis features",
                    "Loads & Constraints_custom",
                    "Mesh",
                    "Solve",
                    "Results",
                    "Utilities",
                ],
                "Individual views": {
                    "order": [
                        "Isometric",
                        "Front",
                        "Top",
                        "Right",
                        "Rear",
                        "Bottom",
                        "Left",
                    ],
                    "commands": {
                        "Std_ViewIsometric": {
                            "size": "small",
                            "text": "Isometric",
                            "icon": "view-axonometric",
                        },
                        "Std_ViewFront": {
                            "size": "small",
                            "text": "Front",
                            "icon": "view-front",
                        },
                        "Std_ViewTop": {
                            "size": "small",
                            "text": "Top",
                            "icon": "view-top",
                        },
                        "Std_ViewRight": {
                            "size": "small",
                            "text": "Right",
                            "icon": "view-right",
                        },
                        "Std_ViewRear": {
                            "size": "small",
                            "text": "Rear",
                            "icon": "view-rear",
                        },
                        "Std_ViewBottom": {
                            "size": "small",
                            "text": "Bottom",
                            "icon": "view-bottom",
                        },
                        "Std_ViewLeft": {
                            "size": "small",
                            "text": "Left",
                            "icon": "view-left",
                        },
                    },
                },
                "Structure": {
                    "order": [
                        "Create part",
                        "Create group",
                        "Link actions",
                        "Create a variable set",
                    ],
                    "commands": {
                        "Std_Part": {
                            "size": "small",
                            "text": "Create part",
                            "icon": "Geofeaturegroup",
                        },
                        "Std_Group": {
                            "size": "small",
                            "text": "Create group",
                            "icon": "folder",
                        },
                        "Std_LinkActions": {
                            "size": "small",
                            "text": "Link actions",
                            "icon": "",
                        },
                        "Std_VarSet": {
                            "size": "small",
                            "text": "Create a variable set",
                            "icon": "VarSet",
                        },
                    },
                },
                "Loads & Constraints_custom": {
                    "order": [
                        "Fixed boundary condition",
                        "Rigid body constraint",
                        "Displacement boundary condition",
                        "Contact constraint",
                        "Tie constraint",
                        "Spring",
                        "separator_FemWorkbench_6",
                        "Force load",
                        "Pressure load",
                        "Centrifugal load",
                        "Gravity load",
                        "separator_FemWorkbench_11",
                        "Electromagnetic boundary conditions",
                        "Initial flow velocity condition",
                        "Initial pressure condition",
                        "Flow velocity boundary condition",
                        "separator_FemWorkbench_16",
                        "Initial temperature",
                        "Heat flux load",
                        "Temperature boundary condition",
                        "Body heat source",
                    ],
                    "commands": {
                        "FEM_CompEmConstraints": {
                            "size": "large",
                            "text": "Electromagnetic constraints",
                            "icon": "",
                        },
                        "FEM_ConstraintInitialFlowVelocity": {
                            "size": "small",
                            "text": "Initial flow velocity condition",
                            "icon": "FEM_ConstraintInitialFlowVelocity",
                        },
                        "FEM_ConstraintInitialPressure": {
                            "size": "small",
                            "text": "Initial pressure condition",
                            "icon": "FEM_ConstraintInitialPressure",
                        },
                        "FEM_ConstraintFlowVelocity": {
                            "size": "small",
                            "text": "Flow velocity boundary condition",
                            "icon": "FEM_ConstraintFlowVelocity",
                        },
                        "FEM_ConstraintFixed": {
                            "size": "large",
                            "text": "Fixed constraint",
                            "icon": "FEM_ConstraintFixed",
                        },
                        "FEM_ConstraintRigidBody": {
                            "size": "small",
                            "text": "Rigid body constraint",
                            "icon": "FEM_ConstraintRigidBody",
                        },
                        "FEM_ConstraintDisplacement": {
                            "size": "small",
                            "text": "Displacement constraint",
                            "icon": "FEM_ConstraintDisplacement",
                        },
                        "FEM_ConstraintContact": {
                            "size": "small",
                            "text": "Contact constraint",
                            "icon": "FEM_ConstraintContact",
                        },
                        "FEM_ConstraintTie": {
                            "size": "small",
                            "text": "Tie constraint",
                            "icon": "FEM_ConstraintTie",
                        },
                        "FEM_ConstraintSpring": {
                            "size": "small",
                            "text": "Spring",
                            "icon": "FEM_ConstraintSpring",
                        },
                        "FEM_ConstraintForce": {
                            "size": "large",
                            "text": "Force load",
                            "icon": "FEM_ConstraintForce",
                        },
                        "FEM_ConstraintPressure": {
                            "size": "small",
                            "text": "Pressure load",
                            "icon": "FEM_ConstraintPressure",
                        },
                        "FEM_ConstraintCentrif": {
                            "size": "small",
                            "text": "Centrifugal load",
                            "icon": "FEM_ConstraintCentrif",
                        },
                        "FEM_ConstraintSelfWeight": {
                            "size": "small",
                            "text": "Gravity load",
                            "icon": "FEM_ConstraintSelfWeight",
                        },
                        "FEM_ConstraintInitialTemperature": {
                            "size": "large",
                            "text": "Initial temperature",
                            "icon": "FEM_ConstraintInitialTemperature",
                        },
                        "FEM_ConstraintHeatflux": {
                            "size": "small",
                            "text": "Heat flux load",
                            "icon": "FEM_ConstraintHeatflux",
                        },
                        "FEM_ConstraintTemperature": {
                            "size": "small",
                            "text": "Temperature boundary condition",
                            "icon": "FEM_ConstraintTemperature",
                        },
                        "FEM_ConstraintBodyHeatSource": {
                            "size": "small",
                            "text": "Body heat source",
                            "icon": "FEM_ConstraintBodyHeatSource",
                        },
                    },
                },
            }
        },
        "PartWorkbench": {
            "toolbars": {
                "Solids": {
                    "order": [
                        "Cube",
                        "Cylinder",
                        "Sphere",
                        "Cone",
                        "Torus",
                        "Create tube",
                        "Create primitives",
                        "Shape builder",
                    ],
                    "commands": {
                        "Part_Box": {
                            "size": "large",
                            "text": "Cube",
                            "icon": "Part_Box_Parametric",
                        },
                        "Part_Cylinder": {
                            "size": "large",
                            "text": "Cylinder",
                            "icon": "Part_Cylinder_Parametric",
                        },
                        "Part_Sphere": {
                            "size": "small",
                            "text": "Sphere",
                            "icon": "Part_Sphere_Parametric",
                        },
                        "Part_Cone": {
                            "size": "small",
                            "text": "Cone",
                            "icon": "Part_Cone_Parametric",
                        },
                        "Part_Torus": {
                            "size": "small",
                            "text": "Torus",
                            "icon": "Part_Torus_Parametric",
                        },
                        "Part_Tube": {
                            "size": "small",
                            "text": "Create tube",
                            "icon": "Part_Tube_Parametric",
                        },
                        "Part_Primitives": {
                            "size": "small",
                            "text": "Create primitives...",
                            "icon": "Part_Primitives",
                        },
                        "Part_Builder": {
                            "size": "small",
                            "text": "Shape builder...",
                            "icon": "Part_Shapebuilder",
                        },
                    },
                },
                "Part tools": {
                    "order": [
                        "Create sketch",
                        "Extrude",
                        "Revolve",
                        "Mirroring",
                        "Scale",
                        "Fillet",
                        "Chamfer",
                        "7_separator_PartWorkbench",
                        "Make face from wires",
                        "Create ruled surface",
                        "Loft",
                        "Sweep",
                        "Thickness",
                        "Offset:",
                        "14_separator_PartWorkbench",
                        "Section",
                        "Cross-sections",
                        "17_separator_PartWorkbench",
                        "Create projection on surface",
                        "Color per face",
                    ],
                    "commands": {
                        "Sketcher_NewSketch": {
                            "size": "large",
                            "text": "Create sketch",
                            "icon": "Sketcher_NewSketch",
                        },
                        "Part_Extrude": {
                            "size": "small",
                            "text": "Extrude...",
                            "icon": "Part_Extrude",
                        },
                        "Part_Revolve": {
                            "size": "small",
                            "text": "Revolve...",
                            "icon": "Part_Revolve",
                        },
                        "Part_Mirror": {
                            "size": "small",
                            "text": "Mirroring",
                            "icon": "Part_Mirror",
                        },
                        "Part_Scale": {
                            "size": "small",
                            "text": "Scale",
                            "icon": "Part_Scale",
                        },
                        "Part_Fillet": {
                            "size": "small",
                            "text": "Fillet",
                            "icon": "Part_Fillet",
                        },
                        "Part_Chamfer": {
                            "size": "small",
                            "text": "Chamfer",
                            "icon": "Part_Chamfer",
                        },
                        "Part_MakeFace": {
                            "size": "small",
                            "text": "Make face from wires",
                            "icon": "Part_MakeFace",
                        },
                        "Part_RuledSurface": {
                            "size": "small",
                            "text": "Create ruled surface",
                            "icon": "Part_RuledSurface",
                        },
                        "Part_Loft": {
                            "size": "small",
                            "text": "Loft",
                            "icon": "Part_Loft",
                        },
                        "Part_Sweep": {
                            "size": "small",
                            "text": "Sweep",
                            "icon": "Part_Sweep",
                        },
                        "Part_Section": {
                            "size": "small",
                            "text": "Section",
                            "icon": "Part_Section",
                        },
                        "Part_CrossSections": {
                            "size": "small",
                            "text": "Cross-sections",
                            "icon": "Part_CrossSections",
                        },
                        "Part_CompOffset": {
                            "size": "small",
                            "text": "Offset:",
                            "icon": "",
                        },
                        "Part_Thickness": {
                            "size": "small",
                            "text": "Thickness",
                            "icon": "Part_Thickness",
                        },
                        "Part_ProjectionOnSurface": {
                            "size": "small",
                            "text": "Create projection on surface",
                            "icon": "Part_ProjectionOnSurface",
                        },
                        "Part_ColorPerFace": {
                            "size": "small",
                            "text": "Color per face",
                            "icon": "Part_ColorFace",
                        },
                    },
                },
                "Boolean": {
                    "order": [
                        "Compound tools",
                        "Boolean",
                        "Cut",
                        "Union",
                        "Intersection",
                        "Join objects",
                        "Split objects",
                        "Check Geometry",
                        "Defeaturing",
                    ],
                    "commands": {
                        "Part_CompCompoundTools": {
                            "size": "large",
                            "text": "Compound tools",
                            "icon": "",
                        },
                        "Part_Boolean": {
                            "size": "small",
                            "text": "Boolean",
                            "icon": "Part_Booleans",
                        },
                        "Part_Cut": {
                            "size": "small",
                            "text": "Cut",
                            "icon": "Part_Cut",
                        },
                        "Part_Fuse": {
                            "size": "small",
                            "text": "Union",
                            "icon": "Part_Fuse",
                        },
                        "Part_Common": {
                            "size": "small",
                            "text": "Intersection",
                            "icon": "Part_Common",
                        },
                        "Part_CompJoinFeatures": {
                            "size": "small",
                            "text": "Join objects",
                            "icon": "",
                        },
                        "Part_CompSplitFeatures": {
                            "size": "small",
                            "text": "Split objects",
                            "icon": "",
                        },
                        "Part_CheckGeometry": {
                            "size": "small",
                            "text": "Check Geometry",
                            "icon": "Part_CheckGeometry",
                        },
                        "Part_Defeaturing": {
                            "size": "small",
                            "text": "Defeaturing",
                            "icon": "Part_Defeaturing",
                        },
                    },
                },
                "order": [
                    "Individual views",
                    "Structure",
                    "Solids",
                    "Part tools",
                    "Boolean",
                ],
                "Individual views": {
                    "order": [
                        "Isometric",
                        "Front",
                        "Top",
                        "Right",
                        "Rear",
                        "Bottom",
                        "Left",
                    ],
                    "commands": {
                        "Std_ViewIsometric": {
                            "size": "small",
                            "text": "Isometric",
                            "icon": "view-axonometric",
                        },
                        "Std_ViewFront": {
                            "size": "small",
                            "text": "Front",
                            "icon": "view-front",
                        },
                        "Std_ViewTop": {
                            "size": "small",
                            "text": "Top",
                            "icon": "view-top",
                        },
                        "Std_ViewRight": {
                            "size": "small",
                            "text": "Right",
                            "icon": "view-right",
                        },
                        "Std_ViewRear": {
                            "size": "small",
                            "text": "Rear",
                            "icon": "view-rear",
                        },
                        "Std_ViewBottom": {
                            "size": "small",
                            "text": "Bottom",
                            "icon": "view-bottom",
                        },
                        "Std_ViewLeft": {
                            "size": "small",
                            "text": "Left",
                            "icon": "view-left",
                        },
                    },
                },
            }
        },
        "SketcherWorkbench": {
            "toolbars": {
                "Sketcher": {
                    "order": [
                        "Create sketch",
                        "Edit sketch",
                        "Attach sketch",
                        "Reorient sketch",
                        "Validate sketch",
                        "Merge sketches",
                        "Mirror sketch",
                    ],
                    "commands": {
                        "Sketcher_NewSketch": {
                            "size": "large",
                            "text": "Create sketch",
                            "icon": "Sketcher_NewSketch",
                        },
                        "Sketcher_EditSketch": {
                            "size": "small",
                            "text": "Edit sketch",
                            "icon": "Sketcher_EditSketch",
                        },
                        "Sketcher_MapSketch": {
                            "size": "small",
                            "text": "Attach sketch",
                            "icon": "Sketcher_MapSketch",
                        },
                        "Sketcher_ReorientSketch": {
                            "size": "small",
                            "text": "Reorient sketch",
                            "icon": "Sketcher_ReorientSketch",
                        },
                        "Sketcher_ValidateSketch": {
                            "size": "small",
                            "text": "Validate sketch...",
                            "icon": "Sketcher_ValidateSketch",
                        },
                        "Sketcher_MergeSketches": {
                            "size": "small",
                            "text": "Merge sketches",
                            "icon": "Sketcher_MergeSketch",
                        },
                        "Sketcher_MirrorSketch": {
                            "size": "small",
                            "text": "Mirror sketch",
                            "icon": "Sketcher_MirrorSketch",
                        },
                    },
                },
                "Sketcher edit mode": {
                    "order": ["Leave sketch", "View sketch", "View section"],
                    "commands": {
                        "Sketcher_LeaveSketch": {
                            "size": "large",
                            "text": "Leave sketch",
                            "icon": "Sketcher_LeaveSketch",
                        },
                        "Sketcher_ViewSketch": {
                            "size": "small",
                            "text": "View sketch",
                            "icon": "Sketcher_ViewSketch",
                        },
                        "Sketcher_ViewSection": {
                            "size": "small",
                            "text": "View section",
                            "icon": "Sketcher_ViewSection",
                        },
                    },
                },
                "Sketcher geometries": {
                    "order": [
                        "Create polyline",
                        "Create point",
                        "Create line",
                        "Create arc",
                        "Create conic",
                        "Create rectangle",
                        "Create regular polygon",
                        "Slots",
                        "Create B-spline",
                        "Toggle construction geometry",
                    ],
                    "commands": {
                        "Sketcher_CreatePoint": {
                            "size": "small",
                            "text": "Create point",
                            "icon": "Sketcher_CreatePoint",
                        },
                        "Sketcher_CreatePolyline": {
                            "size": "large",
                            "text": "Create polyline",
                            "icon": "Sketcher_CreatePolyline",
                        },
                        "Sketcher_CreateLine": {
                            "size": "small",
                            "text": "Create line",
                            "icon": "Sketcher_CreateLine",
                        },
                        "Sketcher_CompCreateArc": {
                            "size": "small",
                            "text": "Create arc",
                            "icon": "",
                        },
                        "Sketcher_CompCreateConic": {
                            "size": "small",
                            "text": "Create conic",
                            "icon": "",
                        },
                        "Sketcher_CompCreateRectangles": {
                            "size": "small",
                            "text": "Create rectangle",
                            "icon": "",
                        },
                        "Sketcher_CompCreateRegularPolygon": {
                            "size": "small",
                            "text": "Create regular polygon",
                            "icon": "",
                        },
                        "Sketcher_CompSlot": {
                            "size": "small",
                            "text": "Slots",
                            "icon": "",
                        },
                        "Sketcher_CompCreateBSpline": {
                            "size": "small",
                            "text": "Create B-spline",
                            "icon": "",
                        },
                        "Sketcher_ToggleConstruction": {
                            "size": "small",
                            "text": "Toggle construction geometry",
                            "icon": "Sketcher_ToggleConstruction",
                        },
                    },
                },
                "Sketcher constraints": {
                    "order": [
                        "Dimension",
                        "Constrain horizontal distance",
                        "Constrain vertical distance",
                        "Constrain distance",
                        "Constrain arc or circle",
                        "Constrain angle",
                        "Constrain lock",
                        "Constrain coincident",
                        "Constrain point on object",
                        "Constrain horizontal/vertical",
                        "Constrain parallel",
                        "Constrain perpendicular",
                        "Constrain tangent or collinear",
                        "Constrain equal",
                        "Constrain symmetric",
                        "Constrain block",
                        "Toggle constraints",
                    ],
                    "commands": {
                        "Sketcher_Dimension": {
                            "size": "large",
                            "text": "Dimension",
                            "icon": "Constraint_Dimension",
                        },
                        "Sketcher_ConstrainDistanceX": {
                            "size": "small",
                            "text": "Constrain horizontal distance",
                            "icon": "Constraint_HorizontalDistance",
                        },
                        "Sketcher_ConstrainDistanceY": {
                            "size": "small",
                            "text": "Constrain vertical distance",
                            "icon": "Constraint_VerticalDistance",
                        },
                        "Sketcher_ConstrainDistance": {
                            "size": "small",
                            "text": "Constrain distance",
                            "icon": "Constraint_Length",
                        },
                        "Sketcher_CompConstrainRadDia": {
                            "size": "small",
                            "text": "Constrain arc or circle",
                            "icon": "",
                        },
                        "Sketcher_ConstrainAngle": {
                            "size": "small",
                            "text": "Constrain angle",
                            "icon": "Constraint_InternalAngle",
                        },
                        "Sketcher_ConstrainLock": {
                            "size": "small",
                            "text": "Constrain lock",
                            "icon": "Constraint_Lock",
                        },
                        "Sketcher_ConstrainCoincident": {
                            "size": "small",
                            "text": "Constrain coincident",
                            "icon": "Constraint_PointOnPoint",
                        },
                        "Sketcher_ConstrainPointOnObject": {
                            "size": "small",
                            "text": "Constrain point on object",
                            "icon": "Constraint_PointOnObject",
                        },
                        "Sketcher_CompHorVer": {
                            "size": "small",
                            "text": "Constrain horizontal/vertical",
                            "icon": "",
                        },
                        "Sketcher_ConstrainParallel": {
                            "size": "small",
                            "text": "Constrain parallel",
                            "icon": "Constraint_Parallel",
                        },
                        "Sketcher_ConstrainPerpendicular": {
                            "size": "small",
                            "text": "Constrain perpendicular",
                            "icon": "Constraint_Perpendicular",
                        },
                        "Sketcher_ConstrainTangent": {
                            "size": "small",
                            "text": "Constrain tangent or collinear",
                            "icon": "Constraint_Tangent",
                        },
                        "Sketcher_ConstrainEqual": {
                            "size": "small",
                            "text": "Constrain equal",
                            "icon": "Constraint_EqualLength",
                        },
                        "Sketcher_ConstrainSymmetric": {
                            "size": "small",
                            "text": "Constrain symmetric",
                            "icon": "Constraint_Symmetric",
                        },
                        "Sketcher_ConstrainBlock": {
                            "size": "small",
                            "text": "Constrain block",
                            "icon": "Constraint_Block",
                        },
                        "Sketcher_CompToggleConstraints": {
                            "size": "small",
                            "text": "Toggle constraints",
                            "icon": "",
                        },
                    },
                },
                "Sketcher tools": {
                    "order": [
                        "Create fillet or chamfer",
                        "Curve Edition",
                        "Create external geometry",
                        "Create carbon copy",
                        "Move / Array transform",
                        "Rotate / Polar transform",
                        "Scale transform",
                        "Offset geometry",
                        "Symmetry",
                        "Remove axes alignment",
                    ],
                    "commands": {
                        "Sketcher_CompCreateFillets": {
                            "size": "large",
                            "text": "Create Fillet/Chamfer",
                            "icon": "",
                        },
                        "Sketcher_CompCurveEdition": {
                            "size": "small",
                            "text": "Curve Edition",
                            "icon": "",
                        },
                        "Sketcher_External": {
                            "size": "small",
                            "text": "Create external geometry",
                            "icon": "Sketcher_External",
                        },
                        "Sketcher_CarbonCopy": {
                            "size": "small",
                            "text": "Create carbon copy",
                            "icon": "Sketcher_CarbonCopy",
                        },
                        "Sketcher_Translate": {
                            "size": "small",
                            "text": "Move / Array transform",
                            "icon": "Sketcher_Translate",
                        },
                        "Sketcher_Rotate": {
                            "size": "small",
                            "text": "Rotate / Polar transform",
                            "icon": "Sketcher_Rotate",
                        },
                        "Sketcher_Scale": {
                            "size": "small",
                            "text": "Scale transform",
                            "icon": "Sketcher_Scale",
                        },
                        "Sketcher_Offset": {
                            "size": "small",
                            "text": "Offset geometry",
                            "icon": "Sketcher_Offset",
                        },
                        "Sketcher_Symmetry": {
                            "size": "small",
                            "text": "Symmetry",
                            "icon": "Sketcher_Symmetry",
                        },
                        "Sketcher_RemoveAxesAlignment": {
                            "size": "small",
                            "text": "Remove axes alignment",
                            "icon": "Sketcher_RemoveAxesAlignment",
                        },
                    },
                },
                "Sketcher B-spline tools": {
                    "order": [
                        "Convert geometry to B-spline",
                        "Increase B-spline degree",
                        "Decrease B-spline degree",
                        "Modify knot multiplicity",
                        "Insert knot",
                        "Join curves",
                    ],
                    "commands": {
                        "Sketcher_BSplineConvertToNURBS": {
                            "size": "large",
                            "text": "Convert to B-spline",
                            "icon": "Sketcher_BSplineConvertToNURBS",
                        },
                        "Sketcher_BSplineIncreaseDegree": {
                            "size": "small",
                            "text": "Increase B-spline degree",
                            "icon": "Sketcher_BSplineIncreaseDegree",
                        },
                        "Sketcher_BSplineDecreaseDegree": {
                            "size": "small",
                            "text": "Decrease B-spline degree",
                            "icon": "Sketcher_BSplineDecreaseDegree",
                        },
                        "Sketcher_CompModifyKnotMultiplicity": {
                            "size": "small",
                            "text": "Modify knot multiplicity",
                            "icon": "",
                        },
                        "Sketcher_BSplineInsertKnot": {
                            "size": "small",
                            "text": "Insert knot",
                            "icon": "Sketcher_BSplineInsertKnot",
                        },
                        "Sketcher_JoinCurves": {
                            "size": "small",
                            "text": "Join curves",
                            "icon": "Sketcher_JoinCurves",
                        },
                    },
                },
                "Sketcher visual": {
                    "order": [
                        "Select associated constraints",
                        "Select associated geometry",
                        "Show/hide circular helper for arcs",
                        "Show/hide B-spline information layer",
                        "Show/hide internal geometry",
                        "Switch virtual space",
                    ],
                    "commands": {
                        "Sketcher_SelectConstraints": {
                            "size": "large",
                            "text": "Select constraints",
                            "icon": "Sketcher_SelectConstraints",
                        },
                        "Sketcher_SelectElementsAssociatedWithConstraints": {
                            "size": "small",
                            "text": "Select associated geometry",
                            "icon": "Sketcher_SelectElementsAssociatedWithConstraints",
                        },
                        "Sketcher_ArcOverlay": {
                            "size": "small",
                            "text": "Show/hide circular helper for arcs",
                            "icon": "Sketcher_ArcOverlay",
                        },
                        "Sketcher_CompBSplineShowHideGeometryInformation": {
                            "size": "small",
                            "text": "Show/hide B-spline information layer",
                            "icon": "",
                        },
                        "Sketcher_RestoreInternalAlignmentGeometry": {
                            "size": "small",
                            "text": "Show/hide internal geometry",
                            "icon": "Sketcher_Element_Ellipse_All",
                        },
                        "Sketcher_SwitchVirtualSpace": {
                            "size": "small",
                            "text": "Switch virtual space",
                            "icon": "Sketcher_SwitchVirtualSpace",
                        },
                    },
                },
                "Sketcher edit tools": {
                    "order": [
                        "Toggle grid",
                        "Toggle snap",
                        "Configure rendering order",
                    ],
                    "commands": {
                        "Sketcher_Grid": {
                            "size": "large",
                            "text": "Toggle grid",
                            "icon": "",
                        },
                        "Sketcher_Snap": {
                            "size": "small",
                            "text": "Toggle snap",
                            "icon": "",
                        },
                        "Sketcher_RenderingOrder": {
                            "size": "small",
                            "text": "Configure rendering order",
                            "icon": "",
                        },
                    },
                },
                "order": [
                    "Individual views",
                    "Structure",
                    "Sketcher",
                    "Sketcher edit mode",
                    "Sketcher geometries",
                    "Sketcher constraints",
                    "Sketcher tools",
                    "Sketcher B-spline tools",
                    "Sketcher visual",
                    "Sketcher edit tools",
                ],
                "Individual views": {
                    "order": [
                        "Isometric",
                        "Front",
                        "Top",
                        "Right",
                        "Rear",
                        "Bottom",
                        "Left",
                    ],
                    "commands": {
                        "Std_ViewIsometric": {
                            "size": "small",
                            "text": "Isometric",
                            "icon": "view-axonometric",
                        },
                        "Std_ViewFront": {
                            "size": "small",
                            "text": "Front",
                            "icon": "view-front",
                        },
                        "Std_ViewTop": {
                            "size": "small",
                            "text": "Top",
                            "icon": "view-top",
                        },
                        "Std_ViewRight": {
                            "size": "small",
                            "text": "Right",
                            "icon": "view-right",
                        },
                        "Std_ViewRear": {
                            "size": "small",
                            "text": "Rear",
                            "icon": "view-rear",
                        },
                        "Std_ViewBottom": {
                            "size": "small",
                            "text": "Bottom",
                            "icon": "view-bottom",
                        },
                        "Std_ViewLeft": {
                            "size": "small",
                            "text": "Left",
                            "icon": "view-left",
                        },
                    },
                },
            }
        },
        "SpreadsheetWorkbench": {
            "toolbars": {
                "Spreadsheet": {
                    "order": [
                        "Create spreadsheet",
                        "Import spreadsheet",
                        "Export spreadsheet",
                        "3_separator_SpreadsheetWorkbench",
                        "Merge cells",
                        "Split cell",
                        "6_separator_SpreadsheetWorkbench",
                        "Align left",
                        "Align center",
                        "Align right",
                        "Align top",
                        "Vertically center-align",
                        "Align bottom",
                        "13_separator_SpreadsheetWorkbench",
                        "Bold text",
                        "Italic text",
                        "Underline text",
                        "17_separator_SpreadsheetWorkbench",
                        "Set alias",
                    ],
                    "commands": {
                        "Spreadsheet_CreateSheet": {
                            "size": "large",
                            "text": "Create spreadsheet",
                            "icon": "Spreadsheet",
                        },
                        "Spreadsheet_Import": {
                            "size": "small",
                            "text": "Import spreadsheet",
                            "icon": "SpreadsheetImport",
                        },
                        "Spreadsheet_Export": {
                            "size": "small",
                            "text": "Export spreadsheet",
                            "icon": "SpreadsheetExport",
                        },
                        "Spreadsheet_MergeCells": {
                            "size": "small",
                            "text": "Merge cells",
                            "icon": "SpreadsheetMergeCells",
                        },
                        "Spreadsheet_SplitCell": {
                            "size": "small",
                            "text": "Split cell",
                            "icon": "SpreadsheetSplitCell",
                        },
                        "Spreadsheet_AlignLeft": {
                            "size": "small",
                            "text": "Align left",
                            "icon": "SpreadsheetAlignLeft",
                        },
                        "Spreadsheet_AlignCenter": {
                            "size": "small",
                            "text": "Align center",
                            "icon": "SpreadsheetAlignCenter",
                        },
                        "Spreadsheet_AlignRight": {
                            "size": "small",
                            "text": "Align right",
                            "icon": "SpreadsheetAlignRight",
                        },
                        "Spreadsheet_AlignTop": {
                            "size": "small",
                            "text": "Align top",
                            "icon": "SpreadsheetAlignTop",
                        },
                        "Spreadsheet_AlignVCenter": {
                            "size": "small",
                            "text": "Vertically center-align",
                            "icon": "SpreadsheetAlignVCenter",
                        },
                        "Spreadsheet_AlignBottom": {
                            "size": "small",
                            "text": "Align bottom",
                            "icon": "SpreadsheetAlignBottom",
                        },
                        "Spreadsheet_StyleBold": {
                            "size": "small",
                            "text": "Bold text",
                            "icon": "SpreadsheetStyleBold",
                        },
                        "Spreadsheet_StyleItalic": {
                            "size": "small",
                            "text": "Italic text",
                            "icon": "SpreadsheetStyleItalic",
                        },
                        "Spreadsheet_StyleUnderline": {
                            "size": "small",
                            "text": "Underline text",
                            "icon": "SpreadsheetStyleUnderline",
                        },
                        "Spreadsheet_SetAlias": {
                            "size": "small",
                            "text": "Set alias",
                            "icon": "SpreadsheetAlias",
                        },
                    },
                },
                "order": ["Individual views", "Structure", "Spreadsheet"],
                "Individual views": {
                    "order": [
                        "Isometric",
                        "Front",
                        "Top",
                        "Right",
                        "Rear",
                        "Bottom",
                        "Left",
                    ],
                    "commands": {
                        "Std_ViewIsometric": {
                            "size": "small",
                            "text": "Isometric",
                            "icon": "view-axonometric",
                        },
                        "Std_ViewFront": {
                            "size": "small",
                            "text": "Front",
                            "icon": "view-front",
                        },
                        "Std_ViewTop": {
                            "size": "small",
                            "text": "Top",
                            "icon": "view-top",
                        },
                        "Std_ViewRight": {
                            "size": "small",
                            "text": "Right",
                            "icon": "view-right",
                        },
                        "Std_ViewRear": {
                            "size": "small",
                            "text": "Rear",
                            "icon": "view-rear",
                        },
                        "Std_ViewBottom": {
                            "size": "small",
                            "text": "Bottom",
                            "icon": "view-bottom",
                        },
                        "Std_ViewLeft": {
                            "size": "small",
                            "text": "Left",
                            "icon": "view-left",
                        },
                    },
                },
                "Structure": {
                    "order": [
                        "Create part",
                        "Create group",
                        "Link actions",
                        "Create a variable set",
                    ],
                    "commands": {
                        "Std_Part": {
                            "size": "small",
                            "text": "Create part",
                            "icon": "Geofeaturegroup",
                        },
                        "Std_Group": {
                            "size": "small",
                            "text": "Create group",
                            "icon": "folder",
                        },
                        "Std_LinkActions": {
                            "size": "small",
                            "text": "Link actions",
                            "icon": "",
                        },
                        "Std_VarSet": {
                            "size": "small",
                            "text": "Create a variable set",
                            "icon": "VarSet",
                        },
                    },
                },
            }
        },
        "TechDrawWorkbench": {
            "toolbars": {
                "TechDraw Pages": {
                    "order": [
                        "Insert Default Page",
                        "Insert Page using Template",
                        "Update template fields",
                        "Redraw Page",
                        "Print All Pages",
                    ],
                    "commands": {
                        "TechDraw_PageDefault": {
                            "size": "large",
                            "text": "Insert Default Page",
                            "icon": "actions/TechDraw_PageDefault",
                        },
                        "TechDraw_PageTemplate": {
                            "size": "small",
                            "text": "Insert Page using Template",
                            "icon": "actions/TechDraw_PageTemplate",
                        },
                        "TechDraw_FillTemplateFields": {
                            "size": "small",
                            "text": "Update template fields",
                            "icon": "actions/TechDraw_FillTemplateFields.svg",
                        },
                        "TechDraw_RedrawPage": {
                            "size": "small",
                            "text": "Redraw Page",
                            "icon": "actions/TechDraw_RedrawPage",
                        },
                        "TechDraw_PrintAll": {
                            "size": "small",
                            "text": "Print All Pages",
                            "icon": "actions/TechDraw_PrintAll",
                        },
                    },
                },
                "TechDraw Views": {
                    "order": [
                        "Insert View",
                        "Insert Broken View",
                        "Insert Active View (3D View)",
                        "Insert a simple or complex Section View",
                        "Insert Detail View",
                        "Insert Draft Workbench Object",
                        "Insert Clip Group",
                    ],
                    "commands": {
                        "TechDraw_View": {
                            "size": "large",
                            "text": "Insert View",
                            "icon": "actions/TechDraw_View",
                        },
                        "TechDraw_BrokenView": {
                            "size": "small",
                            "text": "Insert Broken View",
                            "icon": "actions/TechDraw_BrokenView",
                        },
                        "TechDraw_ActiveView": {
                            "size": "small",
                            "text": "Insert Active View (3D View)",
                            "icon": "actions/TechDraw_ActiveView",
                        },
                        "TechDraw_SectionGroup": {
                            "size": "small",
                            "text": "Insert a simple or complex Section View",
                            "icon": "",
                        },
                        "TechDraw_DetailView": {
                            "size": "small",
                            "text": "Insert Detail View",
                            "icon": "actions/TechDraw_DetailView",
                        },
                        "TechDraw_DraftView": {
                            "size": "small",
                            "text": "Insert Draft Workbench Object",
                            "icon": "actions/TechDraw_DraftView",
                        },
                        "TechDraw_ClipGroup": {
                            "size": "small",
                            "text": "Insert Clip Group",
                            "icon": "actions/TechDraw_ClipGroup",
                        },
                    },
                },
                "TechDraw Stacking": {
                    "order": ["Adjust stacking order of views"],
                    "commands": {
                        "TechDraw_StackGroup": {
                            "size": "large",
                            "text": "View stacking order",
                            "icon": "",
                        }
                    },
                },
                "TechDraw Dimensions": {
                    "order": [
                        "Dimension",
                        "Insert Balloon Annotation",
                        "Axonometric length dimension",
                        "Insert Landmark Dimension - EXPERIMENTAL",
                        "Repair Dimension References",
                    ],
                    "commands": {
                        "TechDraw_CompDimensionTools": {
                            "size": "large",
                            "text": "Dimension",
                            "icon": "",
                        }
                    },
                },
                "TechDraw Attributes": {
                    "order": [
                        "Select Line Attributes, Cascade Spacing and Delta Distance",
                        "Change Line Attributes",
                        "Extend Line",
                        "Lock/Unlock View",
                        "Position Section View",
                        "Customize Format Label",
                    ],
                    "commands": {
                        "TechDraw_ExtensionSelectLineAttributes": {
                            "size": "large",
                            "text": "Line properties",
                            "icon": "TechDraw_ExtensionSelectLineAttributes",
                        },
                        "TechDraw_ExtensionChangeLineAttributes": {
                            "size": "small",
                            "text": "Change Line Attributes",
                            "icon": "TechDraw_ExtensionChangeLineAttributes",
                        },
                        "TechDraw_ExtensionExtendShortenLineGroup": {
                            "size": "small",
                            "text": "Extend Line",
                            "icon": "",
                        },
                        "TechDraw_ExtensionLockUnlockView": {
                            "size": "small",
                            "text": "Lock/Unlock View",
                            "icon": "TechDraw_ExtensionLockUnlockView",
                        },
                        "TechDraw_ExtensionPositionSectionView": {
                            "size": "small",
                            "text": "Position Section View",
                            "icon": "TechDraw_ExtensionPositionSectionView.svg",
                        },
                        "TechDraw_ExtensionCustomizeFormat": {
                            "size": "small",
                            "text": "Customize Format Label",
                            "icon": "TechDraw_ExtensionCustomizeFormat",
                        },
                    },
                },
                "TechDraw Centerlines": {
                    "order": [
                        "Add Circle Centerlines",
                        "Add Cosmetic Thread Hole Side View",
                        "",
                        "Add Cosmetic Circle",
                        "Add Cosmetic Parallel Line",
                    ],
                    "commands": {
                        "TechDraw_ExtensionCircleCenterLinesGroup": {
                            "size": "large",
                            "text": "Circle Centerlines",
                            "icon": "",
                        },
                        "TechDraw_ExtensionThreadsGroup": {
                            "size": "small",
                            "text": "Cosmetic Thread",
                            "icon": "",
                        },
                        "TechDraw_CommandVertexCreationGroup": {
                            "size": "small",
                            "text": "test",
                            "icon": "TechDraw_ExtensionVertexAtIntersection",
                        },
                        "TechDraw_ExtensionDrawCirclesGroup": {
                            "size": "small",
                            "text": "Add Cosmetic Circle",
                            "icon": "",
                        },
                        "TechDraw_CosmeticCircle": {
                            "size": "small",
                            "text": "Add Cosmetic Circle",
                            "icon": "actions/TechDraw_CosmeticCircle",
                        },
                        "TechDraw_ExtensionLinePPGroup": {
                            "size": "small",
                            "text": "Add Cosmetic Parallel Line",
                            "icon": "",
                        },
                    },
                },
                "TechDraw Extend Dimensions": {
                    "order": ["Insert '\u2300' Prefix", "Increase Decimal Places"],
                    "commands": {
                        "TechDraw_ExtensionInsertPrefixGroup": {
                            "size": "large",
                            "text": "Insert '\u2300' Prefix",
                            "icon": "",
                        }
                    },
                },
                "TechDraw File Access": {
                    "order": ["Export Page as SVG", "Export Page as DXF"],
                    "commands": {
                        "TechDraw_ExportPageSVG": {
                            "size": "large",
                            "text": "Export SVG",
                            "icon": "actions/TechDraw_ExportPageSVG",
                        },
                        "TechDraw_ExportPageDXF": {
                            "size": "small",
                            "text": "Export DXF",
                            "icon": "actions/TechDraw_ExportPageDXF",
                        },
                    },
                },
                "TechDraw Decoration": {
                    "order": [
                        "Apply Geometric Hatch to Face",
                        "Hatch a Face using Image File",
                        "Turn View Frames On/Off",
                    ],
                    "commands": {
                        "TechDraw_Hatch": {
                            "size": "small",
                            "text": "Hatch (Image file)",
                            "icon": "actions/TechDraw_Hatch",
                        },
                        "TechDraw_GeometricHatch": {
                            "size": "large",
                            "text": "Hatch",
                            "icon": "actions/TechDraw_GeometricHatch",
                        },
                        "TechDraw_ToggleFrame": {
                            "size": "small",
                            "text": "Turn View Frames On/Off",
                            "icon": "actions/TechDraw_ToggleFrame",
                        },
                    },
                },
                "TechDraw Annotation": {
                    "order": [
                        "Insert Annotation",
                        "Add Leaderline to View",
                        "Insert Rich Text Annotation",
                        "Insert Cosmetic Vertex",
                        "Insert Center Line",
                        "Add Cosmetic Line Through 2 Points",
                        "Add Cosmetic Circle",
                        "Change Appearance of Lines",
                        "Show/Hide Invisible Edges",
                        "Add Welding Information to Leaderline",
                        "Create a Surface Finish Symbol",
                        "Add hole or shaft fit",
                    ],
                    "commands": {
                        "TechDraw_Annotation": {
                            "size": "large",
                            "text": "Insert Annotation",
                            "icon": "actions/TechDraw_Annotation",
                        }
                    },
                },
                "TitleBlock Toolbar": {
                    "order": [
                        "Populate titleblock",
                        "Import data from the FreeCAD source file",
                        "Import data from titleblock",
                    ],
                    "commands": {
                        "FillTitleBlock": {
                            "size": "large",
                            "text": "Populate titleblock",
                            "icon": "FillTitleBlock.svg",
                        },
                        "ImportFreeCAD": {
                            "size": "small",
                            "text": "Import data from the FreeCAD source file",
                            "icon": "ImportFreeCAD.svg",
                        },
                        "FillSpreadsheet": {
                            "size": "small",
                            "text": "Import data from titleblock",
                            "icon": "FillSpreadsheet.svg",
                        },
                    },
                },
                "order": [
                    "Individual views",
                    "Structure",
                    "TechDraw Pages",
                    "TechDraw Views",
                    "TechDraw Stacking",
                    "TechDraw Dimensions_custom",
                    "TechDraw Attributes",
                    "TechDraw Centerlines",
                    "TechDraw File Access",
                    "TechDraw Decoration",
                    "TechDraw Annotation",
                    "TitleBlock Toolbar",
                ],
                "Individual views": {
                    "order": [
                        "Isometric",
                        "Front",
                        "Top",
                        "Right",
                        "Rear",
                        "Bottom",
                        "Left",
                    ],
                    "commands": {
                        "Std_ViewIsometric": {
                            "size": "small",
                            "text": "Isometric",
                            "icon": "view-axonometric",
                        },
                        "Std_ViewFront": {
                            "size": "small",
                            "text": "Front",
                            "icon": "view-front",
                        },
                        "Std_ViewTop": {
                            "size": "small",
                            "text": "Top",
                            "icon": "view-top",
                        },
                        "Std_ViewRight": {
                            "size": "small",
                            "text": "Right",
                            "icon": "view-right",
                        },
                        "Std_ViewRear": {
                            "size": "small",
                            "text": "Rear",
                            "icon": "view-rear",
                        },
                        "Std_ViewBottom": {
                            "size": "small",
                            "text": "Bottom",
                            "icon": "view-bottom",
                        },
                        "Std_ViewLeft": {
                            "size": "small",
                            "text": "Left",
                            "icon": "view-left",
                        },
                    },
                },
                "TechDraw Dimensions_custom": {
                    "order": [
                        "Dimension",
                        "Insert Balloon Annotation",
                        "Axonometric length dimension",
                        "Insert Landmark Dimension - EXPERIMENTAL",
                        "Repair Dimension References",
                        "Insert '\\u2300' Prefix",
                        "Increase Decimal Places",
                    ],
                    "commands": {
                        "TechDraw_CompDimensionTools": {
                            "size": "large",
                            "text": "Dimension",
                            "icon": "",
                        },
                        "TechDraw_Balloon": {
                            "size": "small",
                            "text": "Insert Balloon Annotation",
                            "icon": "TechDraw_Balloon",
                        },
                        "TechDraw_AxoLengthDimension": {
                            "size": "small",
                            "text": "Axonometric length dimension",
                            "icon": "actions/TechDraw_AxoLengthDimension.svg",
                        },
                        "TechDraw_LandmarkDimension": {
                            "size": "small",
                            "text": "Insert Landmark Dimension - EXPERIMENTAL",
                            "icon": "TechDraw_LandmarkDimension",
                        },
                        "TechDraw_DimensionRepair": {
                            "size": "small",
                            "text": "Repair Dimension References",
                            "icon": "TechDraw_DimensionRepair",
                        },
                        "TechDraw_ExtensionInsertPrefixGroup": {
                            "size": "small",
                            "text": "Insert '\u2300' Prefix",
                            "icon": "",
                        },
                        "TechDraw_ExtensionIncreaseDecreaseGroup": {
                            "size": "small",
                            "text": "Increase Decimal Places",
                            "icon": "",
                        },
                    },
                },
            }
        },
    },
}

# a list to store replaced toolbars
List_IgnoredToolbars_internal = []


def main():
    CreateLists()
    CreateJson()
    WriteJson()


def CreateJson():
    # Add your custom workbenches
    if CustomJson_Workbenches != "" and CustomJson_Workbenches is not None and IncludeCustomJson is True:
        for Workbench in CustomJson_Workbenches["workbenches"]:
            skipWorkbenchList.append(Workbench)
        Dict_RibbonCommandPanel.update(CustomJson_Workbenches)

    # Go through the workbenches
    for WorkbenchItem in List_Workbenches:
        WorkBenchName = WorkbenchItem[0]

        # Exclude the workbenches that you want to exclude
        WorkbenchToBeSkipped = False
        for WorkbenchToSkip in skipWorkbenchList:
            if WorkbenchToSkip == WorkBenchName:
                WorkbenchToBeSkipped = True
        # Exclude the workbenches that will be ignored in the RibbonBar
        for WorkbenchToSkip in List_IgnoredWorkbenches:
            if WorkbenchToSkip == WorkBenchName:
                WorkbenchToBeSkipped = True

        if WorkbenchToBeSkipped is False:
            # Activate the workbench. Otherwise, .listToolbars() returns empty
            Gui.activateWorkbench(WorkBenchName)
            # Get the toolbars of this workbench
            wbToolbars = Gui.getWorkbench(WorkBenchName).getToolbarItems()
            CustomCommands = Dict_ReturnCustomToolbars(WorkBenchName)
            wbToolbars.update(CustomCommands)
            CustomPanelCommands = Dict_AddCustomToolbarsToWorkbench(WorkBenchName)
            wbToolbars.update(CustomPanelCommands)

            # Set the standard toolbar order
            ToolbarOrder = []
            ToolbarOrder.append("Individual views")
            ToolbarOrder.append("Structure")
            for key, value in list(wbToolbars.items()):
                IsInList = False
                for item in ToolbarOrder:
                    if item == key:
                        IsInList = True

                if IsInList is False:
                    ToolbarOrder.append(key)
            add_keys_nested_dict(
                Dict_RibbonCommandPanel,
                [
                    "workbenches",
                    WorkBenchName,
                    "toolbars",
                    "order",
                ],
            )
            Dict_RibbonCommandPanel["workbenches"][WorkBenchName]["toolbars"]["order"] = ToolbarOrder

            # Go through the toolbars
            for key, value in list(wbToolbars.items()):
                Toolbar = key

                # Exclude the toolbars that will be ignored in the RibbonBar
                ToolbarToBeSkipped = False
                for ignoredToolbar in List_IgnoredToolbars:
                    if ignoredToolbar == key:
                        ToolbarToBeSkipped = True
                # Exclude the toolbars that must have only small icons
                for ToolbarToSkip in smallOnlyToolbars:
                    if ToolbarToSkip == key:
                        ToolbarToBeSkipped = True

                if ToolbarToBeSkipped is False:
                    # create a empty size string
                    Size = OtherIconSize
                    # Define empty strings for the command name and icon name
                    CommandName = ""
                    IconName = ""

                    for i2 in range(len(value)):
                        CommandName = value[i2]
                        Command = Gui.Command.get(CommandName)
                        if Command is not None:
                            IconName = Command.getInfo()["pixmap"]
                            MenuName = Command.getInfo()["menuText"].replace("&", "")

                            # Create an empty list for orders
                            Order = []
                            for i3 in range(len(value)):
                                CommandOrder = Gui.Command.get(value[i3])
                                if CommandOrder is not None:
                                    MenuNameOrder = (
                                        CommandOrder.getInfo()["menuText"].replace("&", "").replace("...", "")
                                    )
                                    Order.append(MenuNameOrder)

                            # Set the first command to large
                            if i2 == 0:
                                Size = FirstIconSize

                                add_keys_nested_dict(
                                    Dict_RibbonCommandPanel,
                                    [
                                        "workbenches",
                                        WorkBenchName,
                                        "toolbars",
                                        Toolbar,
                                        "order",
                                    ],
                                )
                                add_keys_nested_dict(
                                    Dict_RibbonCommandPanel,
                                    [
                                        "workbenches",
                                        WorkBenchName,
                                        "toolbars",
                                        Toolbar,
                                        "commands",
                                        CommandName,
                                    ],
                                )

                                Dict_RibbonCommandPanel["workbenches"][WorkBenchName]["toolbars"][Toolbar][
                                    "order"
                                ] = Order
                                Dict_RibbonCommandPanel["workbenches"][WorkBenchName]["toolbars"][Toolbar]["commands"][
                                    CommandName
                                ] = {
                                    "size": Size,
                                    "text": MenuName,
                                    "icon": IconName,
                                }
                            if i2 > 0:
                                Size = "small"

                            i2 = i2 + 1
    return


def CreateLists():
    # Create a list of all workbenches with their icon
    List_Workbenches.clear()
    Workbenches = Gui.listWorkbenches()
    for WorkBenchName in Workbenches:
        if str(WorkBenchName) != "":
            if str(WorkBenchName) != "NoneWorkbench" or WorkBenchName is not None:
                Icon = None
                IconName = str(Gui.getWorkbench(WorkBenchName).Icon)
                if IconName != "":
                    Icon = Gui.getIcon(IconName)
                WorkbenchTitle = Gui.getWorkbench(WorkBenchName).MenuText
                List_Workbenches.append([str(WorkBenchName), Icon, WorkbenchTitle])

    # Create a list of all toolbars
    StringList_Toolbars.clear()
    # Store the current active workbench
    ActiveWB = Gui.activeWorkbench().name()
    # Go through the list of workbenches
    for workbench in List_Workbenches:
        # Activate the workbench. Otherwise, .listToolbars() returns empty
        Gui.activateWorkbench(workbench[0])
        # Get the toolbars of this workbench
        wbToolbars = Gui.getWorkbench(workbench[0]).listToolbars()
        # Go through the toolbars
        for Toolbar in wbToolbars:
            # Go through the list of toolbars. If already present, skip it.
            # Otherwise add it the the list.
            IsInList = False
            for i in range(len(StringList_Toolbars)):
                if Toolbar == StringList_Toolbars[i][0]:
                    IsInList = True

            if IsInList is False:
                StringList_Toolbars.append([Toolbar, workbench[2]])
    CustomToolbars = List_ReturnCustomToolbars()
    for Customtoolbar in CustomToolbars:
        StringList_Toolbars.append(Customtoolbar)
    # re-activate the workbench that was stored.
    Gui.activateWorkbench(ActiveWB)

    # Create a list of all commands with their icon
    List_Commands.clear()
    # Create a list of command names
    CommandNames = []
    for i in range(len(List_Workbenches)):
        WorkBench = Gui.getWorkbench(List_Workbenches[i][0])
        ToolbarItems = WorkBench.getToolbarItems()
        for key, value in list(ToolbarItems.items()):
            for j in range(len(value)):
                Item = [value[j], List_Workbenches[i][0]]
                IsInList = False
                for k in range(len(CommandNames)):
                    if CommandNames[k][0] == value[j]:
                        IsInList = True
                if IsInList is False:
                    CommandNames.append(Item)

    # Go through the list
    for CommandName in CommandNames:
        # get the command with this name
        command = Gui.Command.get(CommandName[0])
        WorkBenchName = CommandName[1]
        if command is not None:
            # get the icon for this command
            if command.getInfo()["pixmap"] != "":
                Icon = Gui.getIcon(command.getInfo()["pixmap"])
            else:
                Icon = None
            MenuName = command.getInfo()["menuText"].replace("&", "")
            List_Commands.append([CommandName[0], Icon, MenuName, WorkBenchName])
    # add also custom commands
    Toolbars = List_ReturnCustomToolbars()
    for Toolbar in Toolbars:
        WorkbenchTitle = Toolbar[1]
        for WorkBench in List_Workbenches:
            if WorkbenchTitle == WorkBench[2]:
                WorkBenchName = WorkBench[0]
                for CustomCommand in Toolbar[2]:
                    command = Gui.Command.get(CustomCommand)
                    if command.getInfo()["pixmap"] != "":
                        Icon = Gui.getIcon(command.getInfo()["pixmap"])
                    else:
                        Icon = None
                    MenuName = command.getInfo()["menuText"].replace("&", "")
                    List_Commands.append([CustomCommand, Icon, MenuName, WorkBenchName])
    # endregion ----------------------------------------------------------------------

    return


def WriteJson():
    # Create a resulting dict
    resultingDict = {}
    # add the various lists to the resulting dict.
    resultingDict["ignoredToolbars"] = List_IgnoredToolbars
    resultingDict["iconOnlyToolbars"] = List_IconOnlyToolbars
    resultingDict["quickAccessCommands"] = List_QuickAccessCommands
    resultingDict["ignoredWorkbenches"] = List_IgnoredWorkbenches
    resultingDict.update(Dict_CustomPanels)

    # RibbonTabs
    # Get the Ribbon dictionary
    resultingDict.update(Dict_RibbonCommandPanel)

    # get the path for the Json file
    JsonFile = os.path.join(JsonPath, JsonName)

    # Writing to sample.json
    with open(JsonFile, "w") as outfile:
        json.dump(resultingDict, outfile, indent=4)

    outfile.close()
    return


def add_keys_nested_dict(dict, keys):
    for key in keys:
        if key not in dict:
            dict[key] = {}
        dict = dict[key]
    try:
        dict.setdefault(keys[-1], 1)
    except Exception:
        pass
    return


def List_ReturnCustomToolbars():
    # Get the main window of FreeCAD
    mw = Gui.getMainWindow()
    Toolbars = []

    List_Workbenches = Gui.listWorkbenches().copy()
    for WorkBenchName in List_Workbenches:
        WorkbenchTitle = Gui.getWorkbench(WorkBenchName).MenuText
        if str(WorkBenchName) != "" or WorkBenchName is not None:
            if str(WorkBenchName) != "NoneWorkbench":
                CustomToolbars: list = App.ParamGet(
                    "User parameter:BaseApp/Workbench/" + WorkBenchName + "/Toolbar"
                ).GetGroups()

                for Group in CustomToolbars:
                    Parameter = App.ParamGet("User parameter:BaseApp/Workbench/" + WorkBenchName + "/Toolbar/" + Group)
                    Name = Parameter.GetString("Name")

                    ListCommands = []
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

    return Toolbars


def Dict_ReturnCustomToolbars(WorkBenchName):
    # Get the main window of FreeCAD
    mw = Gui.getMainWindow()
    Toolbars = {}

    if str(WorkBenchName) != "" or WorkBenchName is not None:
        if str(WorkBenchName) != "NoneWorkbench":
            CustomToolbars: list = App.ParamGet(
                "User parameter:BaseApp/Workbench/" + WorkBenchName + "/Toolbar"
            ).GetGroups()

            for Group in CustomToolbars:
                Parameter = App.ParamGet("User parameter:BaseApp/Workbench/" + WorkBenchName + "/Toolbar/" + Group)
                Name = Parameter.GetString("Name")

                if Name != "":
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


def Dict_AddCustomToolbarsToWorkbench(WorkBenchName):
    Toolbars = {}

    try:
        for CustomToolbar in Dict_CustomPanels["customToolbars"][WorkBenchName]:
            ListCommands = []
            Commands = Dict_CustomPanels["customToolbars"][WorkBenchName][CustomToolbar]["commands"]

            for key, value in list(Commands.items()):
                for i in range(len(List_Commands)):
                    if List_Commands[i][2] == key:
                        Command = List_Commands[i][0]
                        ListCommands.append(Command)

                if List_IgnoredToolbars_internal.__contains__(value) is False:
                    List_IgnoredToolbars_internal.append(value)

            Toolbars[CustomToolbar] = ListCommands
    except Exception:
        pass

    return Toolbars


main()
