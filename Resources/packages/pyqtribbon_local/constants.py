from enum import IntEnum

from PySide.QtGui import QColor


class RibbonCategoryStyle(IntEnum):
    """The button style of a category."""

    Normal = 0
    Context = 1


Normal = RibbonCategoryStyle.Normal
Context = RibbonCategoryStyle.Context


#: A list of context category colors
contextColors = [
    QColor(201, 89, 156),  # 玫红
    QColor(242, 203, 29),  # 黄
    QColor(255, 157, 0),  # 橙
    QColor(14, 81, 167),  # 蓝
    QColor(228, 0, 69),  # 红
    QColor(67, 148, 0),  # 绿
]


class RibbonSpaceFindMode(IntEnum):
    """Mode to find available space in a grid layout, ColumnWise or RowWise."""

    ColumnWise = 0
    RowWise = 1


ColumnWise = RibbonSpaceFindMode.ColumnWise
RowWise = RibbonSpaceFindMode.RowWise


class RibbonStyle(IntEnum):
    Default = 0
    Debug = 1


Debug = RibbonStyle.Debug
Default = RibbonStyle.Default


class RibbonButtonStyle(IntEnum):
    """Button style, Small, Medium, or Large."""

    Small = 0
    Medium = 1
    Large = 2


Small = RibbonButtonStyle.Small
Medium = RibbonButtonStyle.Medium
Large = RibbonButtonStyle.Large
