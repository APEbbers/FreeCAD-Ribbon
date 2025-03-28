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

# This code is based on the serialize function of the SearBar Addon.
# Original developer for the SearchBar addon is Suzanne Soy.
from PySide.QtGui import QIcon, QPixmap
from PySide.QtCore import (
    Qt,
    QSize,
    QBuffer,
    QIODevice,
    QTextStream,
    QByteArray,
)


def iconToBase64(
    icon: QIcon, sz=QSize(64, 64), mode=QIcon.Mode.Normal, state=QIcon.State.On
):
    """
    Converts a QIcon to a Base64-encoded string representation of its pixmap.

    Args:
        icon (QIcon): The icon to encode.
        sz (QSize): The size of the pixmap to generate.
        mode (QIcon.Mode): The mode of the pixmap (e.g., Normal, Disabled).
        state (QIcon.State): The state of the pixmap (e.g., On, Off).

    Returns:
        str: The Base64-encoded string of the icon's pixmap.
    """
    buf = QBuffer()
    buf.open(QIODevice.OpenModeFlag.WriteOnly)

    # Save the pixmap of the icon to the buffer in PNG format
    pixmap: QPixmap = icon.pixmap(sz, mode, state)
    try:
        pixmap.save(buf, "PNG")
    except Exception as e:
        # raise ValueError("Failed to save icon to buffer. Ensure the icon is valid.")
        print(e)

    # Use standard Base64 encoding
    base64_data = buf.data().toBase64().data().decode("utf-8")
    buf.close()
    return base64_data


def serializeIcon(icon):
    iconPixmaps = {}
    for sz in icon.availableSizes():
        strW = str(sz.width())
        strH = str(sz.height())
        iconPixmaps[strW] = {}
        iconPixmaps[strW][strH] = {}
        for strMode, mode in {
            "normal": QIcon.Mode.Normal,
            "disabled": QIcon.Mode.Disabled,
            "active": QIcon.Mode.Active,
            "selected": QIcon.Mode.Selected,
        }.items():
            iconPixmaps[strW][strH][strMode] = {}
            for strState, state in {
                "off": QIcon.State.Off,
                "on": QIcon.State.On,
            }.items():
                iconPixmaps[strW][strH][strMode][strState] = iconToBase64(
                    icon, sz, mode, state
                )
    return iconPixmaps


def deserializeIcon(iconPixmaps):
    ico = QIcon()
    for strW, wPixmaps in iconPixmaps.items():
        for strH, hPixmaps in wPixmaps.items():
            for strMode, modePixmaps in hPixmaps.items():
                mode = {
                    "normal": QIcon.Mode.Normal,
                    "disabled": QIcon.Mode.Disabled,
                    "active": QIcon.Mode.Active,
                    "selected": QIcon.Mode.Selected,
                }[strMode]
                for strState, statePixmap in modePixmaps.items():
                    state = {"off": QIcon.State.Off, "on": QIcon.State.On}[strState]
                    pxm = QPixmap()
                    pxm.loadFromData(
                        QByteArray.fromBase64(bytearray(statePixmap.encode("utf-8")))
                    )
                    ico.addPixmap(pxm, mode, state)
    return ico
