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

# Fill the correction list -> {workbenchname [[new toolbar, old toolbar], [new toolbar, old toolbar]]}
CorrectionList = {
    "PartDesignWorkbench": [
        ['Part Design Helper Features', "Part Design Helper"],
        ['Part Design Modeling Features', "Part Design Modeling"],
        ['Part Design Dress-Up Features', "Part Design Derssup"],
        ['Part Design Transformation Features', "Part Design Patterns"],
    ]
}

ParentPath = os.path.dirname(os.path.dirname(__file__))
JsonName = "RibbonStructure.json"
# get the path for the Json file
JsonFile = os.path.join(ParentPath, JsonName)

# Create a dict from the json file
RibbonStructure = {}
with open(JsonFile, "r") as file:
    RibbonStructure.update(json.load(file))

# Create a .bak file
JsonNameBackUp = "RibbonStructure.json.bak"
JsonFileBackUp = os.path.join(ParentPath, JsonNameBackUp)
with open(JsonFileBackUp, "w") as outfile:
    json.dump(RibbonStructure, outfile, indent=4)

# Go through the workbenches in the json file
for WorkBench in RibbonStructure["workbenches"]:
    # if the workench is in the correction list, continue
    if WorkBench in CorrectionList:
        # Get the corresponding toolbar correction list
        ToolBarCorrectionList = CorrectionList[WorkBench]
        # Go through the toolbars of the workbench in the json file
        for toolbar in RibbonStructure["workbenches"][WorkBench]["toolbars"]:
            for ToolBarToCorrect in ToolBarCorrectionList:
                # If the toolbars match, update the json file
                Dict: dict = RibbonStructure["workbenches"][WorkBench]["toolbars"]
                if ToolBarToCorrect[1] == toolbar:
                    Dict.update({ToolBarToCorrect[0]: Dict.pop(toolbar)}) 
                    

# Write it to disk
with open(JsonFile, "w") as outfile:
    json.dump(RibbonStructure, outfile, indent=4)
