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

# This script can be used to fix errors in the file "RibbonStructure.json".
# It will look for panels under workbenches that shouldn't be there and removes them.
# This cleansup the file and can help resolve issues with errors like unable to remove separators.

import json
import os

ParentPath = os.path.dirname(os.path.dirname(__file__))
JsonName = "RibbonStructure.json"
# get the path for the Json file
JsonFile = os.path.join(ParentPath, JsonName)

# Get the datafile
DataFile = os.path.join(ParentPath, "RibbonDataFile.dat")

# create a dict from the data file and close the data file
Data = {}
# read ribbon structure from JSON file
with open(DataFile, "r") as file:
    Data.update(json.load(file))

# Create a list with workbench data
ListWorkbenchesData = []
for item in Data["List_Workbenches"]:
    ListWorkbenchesData.append([item[0], item[3]])

# Load the standard lists for Workbenches, toolbars and commands
List_Workbenches = Data["List_Workbenches"]
StringList_Toolbars = Data["StringList_Toolbars"]
List_Commands = Data["List_Commands"]

# Create two identical dicts from the json file
RibbonData = {}
with open(JsonFile, "r") as file:
    RibbonData.update(json.load(file))
RibbonStructure = {}
with open(JsonFile, "r") as file:
    RibbonStructure.update(json.load(file))

# Create a .bak file
JsonNameBackUp = "RibbonStructure.json.bak"
JsonFileBackUp = os.path.join(ParentPath, JsonNameBackUp)
with open(JsonFileBackUp, "w") as outfile:
    json.dump(RibbonData, outfile, indent=4)

# Go through the workbenches in the json file
for WorkBench in RibbonStructure["workbenches"]:
    # Go through the data file to find the same workbench
    for data in ListWorkbenchesData:
        if data[0] == WorkBench:
            # Go through the list of toolbars
            for toolbar in RibbonStructure["workbenches"][WorkBench]["toolbars"]:
                # Define a boolan to state if a toolbar should be present in the json file
                isCorrect = False
                # Go through the data
                for key, value in data[1].items():
                    # if the toolbar is in the data, it is correct
                    if (
                        toolbar == key
                        or toolbar == "order"
                        or toolbar.endswith("_custom")
                        or toolbar.endswith("_newPanel")
                    ):
                        isCorrect = True
                # if the toolbar is wrong, remove it
                if isCorrect is False:
                    del RibbonData["workbenches"][WorkBench]["toolbars"][toolbar]
# update the ribbonstructure dict
RibbonStructure.update(RibbonData)

# Write it to disk
ParentPath = os.path.dirname(os.path.dirname(__file__))
# get the path for the Json file
JsonFile = os.path.join(ParentPath, JsonName)
# Writing to sample.json
with open(JsonFile, "w") as outfile:
    json.dump(RibbonData, outfile, indent=4)
