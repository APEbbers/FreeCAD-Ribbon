import typing

from PySide.QtGui import QColor
from PySide.QtWidgets import QTabBar
from PySide.QtCore import Qt


class RibbonTabBar(QTabBar):
    """The TabBar for the title widget."""

    #: context category top margin
    _contextCategoryTopMargin = 0
    #: context category dark color height
    _contextCategoryDarkColorHeight = 5

    _tabColors: typing.Dict[str, typing.Union[Qt.GlobalColor, QColor]] = {}
    _associated_tabs = {}

    def __init__(self, parent=None):
        """Create a new tab bar.

        :param parent: The parent widget.
        """
        super().__init__(parent)

        self.currentChanged.connect(self.changeColor)
        self.setDrawBase(False)

    def indexOf(self, tabName: str) -> int:
        """Return the index of the tab with the given name.

        :param tabName: The name of the tab.
        :return: The index of the tab.
        """
        for i in range(self.count()):
            if self.tabText(i) == tabName:
                return i
        return -1

    def tabTitles(self) -> typing.List[str]:
        """Return the titles of all tabs.

        :return: The titles of all tabs.
        """
        return [self.tabText(i) for i in range(self.count())]

    def addTab(self, text: str, color: QColor = None, *args, **kwargs) -> int:
        """Add a new tab to the tab bar.

        :param text: The text of the tab.
        :param color: The color of the tab.
        :return: The index of the tab.
        """
        self._tabColors[text] = color
        return super().addTab(text)

    def addAssociatedTabs(
        self, name: str, texts: typing.List[str], color: QColor
    ) -> typing.List[int]:
        """Add associated multiple tabs which have the same color to the tab bar.

        :param name: The name of the context category.
        :param texts: The texts of the tabs.
        :param color: The color of the tabs.
        :return: The indices of the tabs.
        """
        self._tabColors[name] = color
        for text in texts:
            self._associated_tabs[text] = [t for t in texts if t != text]
        return [self.addTab(text, color) for text in texts]

    def removeAssociatedTabs(self, titles: typing.List[str]) -> None:
        """Remove tabs with the given titles.

        :param titles: The titles of the tabs to remove.
        """
        tabTitles = self.tabTitles()
        for title in titles:
            if title in tabTitles:
                self.removeTab(self.indexOf(title))
                del self._tabColors[title]
                if title in self._associated_tabs:
                    del self._associated_tabs[title]

    def currentTabColor(self) -> QColor:
        """Current tab color

        :return: Current tab color
        """
        return self._tabColors[self.tabText(self.currentIndex())]

    def changeColor(self, inx: int) -> None:
        """Change tab's color."""

        if self.count() > 0:
            currentTabText = self.tabText(inx)
            currentTabColor = self._tabColors[currentTabText]
            if currentTabColor is not None:
                self.setStyleSheet(
                    "RibbonTabBar::tab:selected {color: %s;}"
                    % QColor(currentTabColor).name()
                )
            else:
                self.setStyleSheet("RibbonTabBar::tab:selected {color: black;}")
