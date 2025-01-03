import typing

from PySide.QtGui import QIcon, QColor
from PySide.QtWidgets import (
    QToolButton,
    QVBoxLayout,
    QWidget,
    QLayout,
    QStackedWidget,
    QGraphicsDropShadowEffect,
    QMenuBar,
    QToolBar,
)
from PySide.QtCore import (
    Qt,
    QSize,
    Signal,
    QEvent,
    QObject,
)

from .category import (
    RibbonCategory,
    RibbonContextCategories,
    RibbonContextCategory,
    RibbonNormalCategory,
)
from .constants import RibbonCategoryStyle, RibbonStyle, contextColors
from .menu import RibbonMenu
from .tabbar import RibbonTabBar
from .titlewidget import RibbonApplicationButton, RibbonTitleWidget
from .utils import DataFile


class RibbonStackedWidget(QStackedWidget):
    """Stacked widget that is used to display the ribbon."""

    def __init__(self, parent=None):
        """Create a new ribbon stacked widget.

        :param parent: The parent widget.
        """
        super().__init__(parent)
        effect = QGraphicsDropShadowEffect()
        effect.setOffset(2, 2)
        self.setGraphicsEffect(effect)


class RibbonBar(QWidget):
    """The RibbonBar class is the top level widget that contains the ribbon."""

    #: Signal, the help button was clicked.
    helpButtonClicked = Signal(bool)

    #: hide the ribbon bar automatically when the mouse press outside the ribbon bar
    _autoHideRibbon = False

    #: The categories of the ribbon.
    _categories: typing.Dict[str, RibbonCategory] = {}
    _contextCategoryCount = 0

    #: Maximum rows
    _maxRows = 6

    #: Whether the ribbon is visible.
    _ribbonVisible = True

    #: heights of the ribbon elements
    _ribbonHeight = 150

    #: current tab index
    _currentTabIndex = 0

    @typing.overload
    def __init__(self, title: str = "Ribbon Bar Title", maxRows=6, parent=None):
        pass

    @typing.overload
    def __init__(self, parent=None):
        pass

    def __init__(self, *args, **kwargs):
        """Create a new ribbon.

        :param title: The title of the ribbon.
        :param maxRows: The maximum number of rows.
        :param parent: The parent widget of the ribbon.
        """
        if (args and not isinstance(args[0], QWidget)) or ("title" in kwargs or "maxRows" in kwargs):
            title = args[0] if len(args) > 0 else kwargs.get("title", "Ribbon Bar Title")
            maxRows = args[1] if len(args) > 1 else kwargs.get("maxRows", 6)
            parent = args[2] if len(args) > 2 else kwargs.get("parent", None)
        else:
            title = ""
            maxRows = 6
            parent = args[1] if len(args) > 1 else kwargs.get("parent", None)
        super().__init__(parent)
        self._categories = {}
        self._maxRows = maxRows
        self.setFixedHeight(self._ribbonHeight)

        self._titleWidget = RibbonTitleWidget(title, self)
        self._stackedWidget = RibbonStackedWidget(self)

        # Main layout
        self._mainLayout = QVBoxLayout(self)
        self._mainLayout.setContentsMargins(0, 0, 0, 0)
        self._mainLayout.setSpacing(0)
        self._mainLayout.addWidget(self._titleWidget, 0)
        self._mainLayout.addWidget(self._stackedWidget, 1)
        self._mainLayout.setSizeConstraint(QLayout.SizeConstraint.SetMinAndMaxSize)

        # Connect signals
        self._titleWidget.helpButtonClicked.connect(self.helpButtonClicked)
        self._titleWidget.collapseRibbonButtonClicked.connect(self._collapseButtonClicked)
        self._titleWidget.tabBar().currentChanged.connect(self.showCategoryByIndex)  # type: ignore
        self.setRibbonStyle(RibbonStyle.Default)

    def autoHideRibbon(self) -> bool:
        """Return whether the ribbon bar is automatically hidden when the mouse is pressed outside the ribbon bar.

        :return: Whether the ribbon bar is automatically hidden.
        """
        return self._autoHideRibbon

    def setAutoHideRibbon(self, autoHide: bool):
        """Set whether the ribbon bar is automatically hidden when the mouse is pressed outside the ribbon bar.

        :param autoHide: Whether the ribbon bar is automatically hidden.
        """
        self._autoHideRibbon = autoHide

    def eventFilter(self, a0: QObject, a1: QEvent) -> bool:
        if self._autoHideRibbon and a1.type() == QEvent.Type.HoverMove:
            self.setRibbonVisible(self.underMouse())
        return super().eventFilter(a0, a1)

    def actionAt(self, QPoint):
        raise NotImplementedError("RibbonBar.actionAt() is not implemented in the ribbon bar.")

    def actionGeometry(self, QAction):
        raise NotImplementedError("RibbonBar.actionGeometry() is not implemented in the ribbon bar.")

    def activeAction(self):
        raise NotImplementedError("RibbonBar.activeAction() is not implemented in the ribbon bar.")

    def addMenu(self, *__args):
        raise NotImplementedError("RibbonBar.addMenu() is not implemented in the ribbon bar.")

    def addAction(self, *__args):
        raise NotImplementedError("RibbonBar.addAction() is not implemented in the ribbon bar.")

    def addSeparator(self):
        raise NotImplementedError("RibbonBar.addSeparator() is not implemented in the ribbon bar.")

    def clear(self):
        raise NotImplementedError("RibbonBar.clear() is not implemented in the ribbon bar.")

    def cornerWidget(self, corner=None, *args, **kwargs):
        raise NotImplementedError("RibbonBar.cornerWidget() is not implemented in the ribbon bar.")

    def insertMenu(self, QAction, QMenu):
        raise NotImplementedError("RibbonBar.insertMenu() is not implemented in the ribbon bar.")

    def insertSeparator(self, QAction):
        raise NotImplementedError("RibbonBar.insertSeparator() is not implemented in the ribbon bar.")

    def isDefaultUp(self):
        raise NotImplementedError("RibbonBar.isDefaultUp() is not implemented in the ribbon bar.")

    def isNativeMenuBar(self):
        raise NotImplementedError("RibbonBar.isNativeMenuBar() is not implemented in the ribbon bar.")

    def setActiveAction(self, QAction):
        raise NotImplementedError("RibbonBar.setActiveAction() is not implemented in the ribbon bar.")

    def setCornerWidget(self, QWidget, corner=None, *args, **kwargs):
        raise NotImplementedError("RibbonBar.setCornerWidget() is not implemented in the ribbon bar.")

    def setDefaultUp(self, up):
        raise NotImplementedError("RibbonBar.setDefaultUp() is not implemented in the ribbon bar.")

    def setNativeMenuBar(self, bar):
        raise NotImplementedError("RibbonBar.setNativeMenuBar() is not implemented in the ribbon bar.")

    def setRibbonStyle(self, style: RibbonStyle):
        """Set the style of the ribbon.

        :param style: The style to set.
        """
        self.setStyleSheet(
            open(DataFile("styles/base.qss"), "r").read()
            + open(DataFile(f"styles/{style.name.lower()}.qss"), "r").read()
        )

    def applicationOptionButton(self) -> RibbonApplicationButton:
        """Return the application button."""
        return self._titleWidget.applicationButton()

    def setApplicationIcon(self, icon: QIcon):
        """Set the application icon.

        :param icon: The icon to set.
        """
        self._titleWidget.applicationButton().setIcon(icon)

    def addTitleWidget(self, widget: QWidget):
        """Add a widget to the title widget.

        :param widget: The widget to add.
        """
        self._titleWidget.addTitleWidget(widget)

    def removeTitleWidget(self, widget: QWidget):
        """Remove a widget from the title widget.

        :param widget: The widget to remove.
        """
        self._titleWidget.removeTitleWidget(widget)

    def insertTitleWidget(self, index: int, widget: QWidget):
        """Insert a widget to the title widget.

        :param index: The index to insert the widget.
        :param widget: The widget to insert.
        """
        self._titleWidget.insertTitleWidget(index, widget)

    def addFileMenu(self) -> RibbonMenu:
        """Add a file menu to the ribbon."""
        return self.applicationOptionButton().addFileMenu()

    def ribbonHeight(self) -> int:
        """Get the total height of the ribbon.

        :return: The height of the ribbon.
        """
        return self._ribbonHeight

    def setRibbonHeight(self, height: int):
        """Set the total height of the ribbon.

        :param height: The height to set.
        """
        self._ribbonHeight = height
        self.setFixedHeight(height)

    def tabBar(self) -> RibbonTabBar:
        """Return the tab bar of the ribbon.

        :return: The tab bar of the ribbon.
        """
        return self._titleWidget.tabBar()

    def quickAccessToolBar(self) -> QToolBar:
        """Return the quick access toolbar of the ribbon.

        :return: The quick access toolbar of the ribbon.
        """
        return self._titleWidget.quickAccessToolBar()

    def addQuickAccessButton(self, button: QToolButton):
        """Add a button to the quick access bar.

        :param button: The button to add.
        """
        button.setAutoRaise(True)
        self._titleWidget.quickAccessToolBar().addWidget(button)

    def setQuickAccessButtonHeight(self, height: int):
        """Set the height of the quick access buttons.

        :param height: The height to set.
        """
        self._titleWidget.setQuickAccessButtonHeight(height)

    def title(self) -> str:
        """Return the title of the ribbon.

        :return: The title of the ribbon.
        """
        return self._titleWidget.title()

    def setTitle(self, title: str):
        """Set the title of the ribbon.

        :param title: The title to set.
        """
        self._titleWidget.setTitle(title)

    def setTitleWidgetHeight(self, height: int):
        """Set the height of the title widget.

        :param height: The height to set.
        """
        self._titleWidget.setTitleWidgetHeight(height)

    def rightToolBar(self) -> QToolBar:
        """Return the right toolbar of the ribbon.

        :return: The right toolbar of the ribbon.
        """
        return self._titleWidget.rightToolBar()

    def addRightToolButton(self, button: QToolButton):
        """Add a widget to the right button bar.

        :param button: The button to add.
        """
        button.setAutoRaise(True)
        self._titleWidget.addRightToolButton(button)

    def setRightToolBarHeight(self, height: int):
        """Set the height of the right buttons.

        :param height: The height to set.
        """
        self._titleWidget.setRightToolBarHeight(height)

    def helpRibbonButton(self) -> QToolButton:
        """Return the help button of the ribbon.

        :return: The help button of the ribbon.
        """
        return self._titleWidget.helpRibbonButton()

    def setHelpButtonIcon(self, icon: QIcon):
        """Set the icon of the help button.

        :param icon: The icon to set.
        """
        self._titleWidget.setHelpButtonIcon(icon)

    def removeHelpButton(self):
        """Remove the help button from the ribbon."""
        self._titleWidget.removeHelpButton()

    def collapseRibbonButton(self) -> QToolButton:
        """Return the collapse ribbon button.

        :return: The collapse ribbon button.
        """
        return self._titleWidget.collapseRibbonButton()

    def setCollapseButtonIcon(self, icon: QIcon):
        """Set the icon of the min button.

        :param icon: The icon to set.
        """
        self._titleWidget.setCollapseButtonIcon(icon)

    def removeCollapseButton(self):
        """Remove the min button from the ribbon."""
        self._titleWidget.removeCollapseButton()

    def category(self, name: str) -> RibbonCategory:
        """Return the category with the given name.

        :param name: The name of the category.
        :return: The category with the given name.
        """
        return self._categories[name]

    def categories(self) -> typing.Dict[str, RibbonCategory]:
        """Return a list of categories of the ribbon.

        :return: A dict of categories of the ribbon.
        """
        return self._categories

    def addCategoriesBy(
        self,
        data: typing.Dict[
            str,  # title of the category
            typing.Dict,  # data of the category
        ],
    ) -> typing.Dict[str, RibbonCategory]:
        """Add categories from a dict.

        :param data: The dict of categories. The dict is of the form:

            .. code-block:: python

                {
                    "category-title": {
                        "style": RibbonCategoryStyle.Normal,
                        "color": Qt.red,
                        "panels": {
                            "panel-title": {
                                "showPanelOptionButton": True,
                                "widgets": {
                                    "widget-name": {
                                        "type": "Button",
                                        "args": (),
                                        "kwargs": {  # or "arguments" for backward compatibility
                                            "key1": "value1",
                                            "key2": "value2"
                                        }
                                    },
                                }
                            },
                        },
                    }
                }
        :return: A dict of categories of the ribbon.
        """
        categories = {}
        for title, category_data in data.items():
            style = category_data.get("style", RibbonCategoryStyle.Normal)
            color = category_data.get("color", None)
            categories[title] = self.addCategory(title, style, color)
            categories[title].addPanelsBy(category_data.get("panels", {}))
        return categories

    def addCategory(
        self,
        title: str,
        style=RibbonCategoryStyle.Normal,
        color: QColor = None,
    ) -> typing.Union[RibbonNormalCategory, RibbonContextCategory]:
        """Add a new category to the ribbon.

        :param title: The title of the category.
        :param style: The button style of the category.
        :param color: The color of the context category, only used if style is Context, if None, the default color
                      will be used.
        :return: The newly created category.
        """
        if title in self._categories:
            raise ValueError(f"Category with title {title} already exists.")
        if style == RibbonCategoryStyle.Context:
            if color is None:
                color = contextColors[self._contextCategoryCount % len(contextColors)]
                self._contextCategoryCount += 1
        category = (
            RibbonContextCategory(title, color, self)  # noqa
            if style == RibbonCategoryStyle.Context
            else RibbonNormalCategory(title, self)  # noqa
        )
        category.setMaximumRows(self._maxRows)
        category.setFixedHeight(
            self._ribbonHeight
            - self._mainLayout.spacing() * 2
            - self._mainLayout.contentsMargins().top()
            - self._mainLayout.contentsMargins().bottom()
            - self._titleWidget.height()
        )  # 4: extra space for drawing lines when debugging
        self._categories[title] = category
        self._stackedWidget.addWidget(category)
        if style == RibbonCategoryStyle.Normal:
            self._titleWidget.tabBar().addTab(title, color)
        elif style == RibbonCategoryStyle.Context:
            category.hide()
        if len(self._categories) == 1:
            self._titleWidget.tabBar().setCurrentIndex(1)
            self.showCategoryByIndex(1)
        return category

    def addNormalCategory(self, title: str) -> RibbonNormalCategory:
        """Add a new category to the ribbon.

        :param title: The title of the category.
        :return: The newly created category.
        """
        return self.addCategory(title, RibbonCategoryStyle.Normal)

    def addContextCategory(
        self,
        title: str,
        color: typing.Union[QColor, Qt.GlobalColor] = Qt.GlobalColor.blue,
    ) -> RibbonContextCategory:
        """Add a new context category to the ribbon.

        :param title: The title of the category.
        :param color: The color of the context category, if None, the default color will be used.
        :return: The newly created category.
        """
        return self.addCategory(title, RibbonCategoryStyle.Context, color)

    def addContextCategories(
        self,
        name: str,
        titles: typing.List[str],
        color: typing.Union[QColor, Qt.GlobalColor] = Qt.GlobalColor.blue,
    ) -> RibbonContextCategories:
        """Add a group of context categories with the same tab color to the ribbon.

        :param name: The name of the context categories.
        :param titles: The title of the category.
        :param color: The color of the context category, if None, the default color will be used.
        :return: The newly created category.
        """
        if color is None:
            color = contextColors[self._contextCategoryCount % len(contextColors)]
            self._contextCategoryCount += 1
        categories = RibbonContextCategories(
            name,
            color,
            {title: self.addContextCategory(title, color) for title in titles},
            self,
        )
        return categories

    def showCategoryByIndex(self, index: int):
        """Show category by tab index

        :param index: tab index
        """
        self._currentTabIndex = index
        title = self._titleWidget.tabBar().tabText(index)  # 0 is the file tab
        if title in self._categories:
            self._stackedWidget.setCurrentWidget(self._categories[title])

    def showContextCategory(self, category: typing.Union[RibbonContextCategory, RibbonContextCategories]):
        """Show the given category or categories, if it is not a context category, nothing happens.

        :param category: The category to show.
        """
        if isinstance(category, RibbonContextCategory):
            self._titleWidget.tabBar().addTab(category.title(), category.color())
            self._titleWidget.tabBar().setCurrentIndex(self._titleWidget.tabBar().count() - 1)
            self._stackedWidget.setCurrentWidget(category)
        elif isinstance(category, RibbonContextCategories):
            categories = category
            titles = list(categories.keys())
            self._titleWidget.tabBar().addAssociatedTabs(categories.name(), titles, categories.color())
            self._titleWidget.tabBar().setCurrentIndex(self._titleWidget.tabBar().count() - len(titles))
            self._stackedWidget.setCurrentWidget(categories[titles[0]])

    def hideContextCategory(self, category: typing.Union[RibbonContextCategory, RibbonContextCategories]):
        """Hide the given category or categories, if it is not a context category, nothing happens.

        :param category: The category to hide.
        """
        if isinstance(category, RibbonContextCategory):
            self.tabBar().removeTab(self.tabBar().indexOf(category.title()))
        elif isinstance(category, RibbonContextCategories):
            categories = category
            for c in categories:
                self.tabBar().removeTab(self.tabBar().indexOf(c.title()))

    def categoryVisible(self, category: RibbonCategory) -> bool:
        """Return whether the category is shown.

        :param category: The category to check.

        :return: Whether the category is shown.
        """
        return category.title() in self._titleWidget.tabBar().tabTitles()

    def removeCategory(self, category: RibbonCategory):
        """Remove a category from the ribbon.

        :param category: The category to remove.
        """
        self.tabBar().removeTab(self._titleWidget.tabBar().indexOf(category.title()))
        self._stackedWidget.removeWidget(category)

    def removeCategories(self, categories: RibbonContextCategories):
        """Remove a list of categories from the ribbon.

        :param categories: The categories to remove.
        """
        for category in categories.values():
            self.removeCategory(category)

    def setCurrentCategory(self, category: RibbonCategory):
        """Set the current category.

        :param category: The category to set.
        """
        self._stackedWidget.setCurrentWidget(category)
        if category.title() in self._titleWidget.tabBar().tabTitles():
            self._titleWidget.tabBar().setCurrentIndex(self._titleWidget.tabBar().indexOf(category.title()))
        else:
            raise ValueError(
                f"Category {category.title()} is not in the ribbon, "
                f"please show the context category/categories first."
            )

    def currentCategory(self) -> RibbonCategory:
        """Return the current category.

        :return: The current category.
        """
        return self._categories[self._titleWidget.tabBar().tabText(self._titleWidget.tabBar().currentIndex())]

    def minimumSizeHint(self) -> QSize:
        """Return the minimum size hint of the widget.

        :return: The minimum size hint.
        """
        return QSize(super().minimumSizeHint().width(), self._ribbonHeight)

    def _collapseButtonClicked(self):
        self.tabBar().currentChanged.connect(self.showRibbon)  # type: ignore
        self.hideRibbon() if self._stackedWidget.isVisible() else self.showRibbon()

    def showRibbon(self):
        """Show the ribbon."""
        if not self._ribbonVisible:
            self._ribbonVisible = True
            self.collapseRibbonButton().setToolTip("Collapse Ribbon")
            self.collapseRibbonButton().setIcon(QIcon(DataFile("icons/up.png")))
            self._stackedWidget.setVisible(True)
            self.setFixedSize(self.sizeHint())

    def hideRibbon(self):
        """Hide the ribbon."""
        if self._ribbonVisible:
            self._ribbonVisible = False
            self.collapseRibbonButton().setToolTip("Expand Ribbon")
            self.collapseRibbonButton().setIcon(QIcon(DataFile("icons/down.png")))
            self._stackedWidget.setVisible(False)
            self.setFixedSize(self.sizeHint().width(), self._titleWidget.size().height() + 5)  # type: ignore

    def ribbonVisible(self) -> bool:
        """Get the visibility of the ribbon.

        :return: True if the ribbon is visible, False otherwise.
        """
        return self._ribbonVisible

    def setRibbonVisible(self, visible: bool):
        """Set the visibility of the ribbon.

        :param visible: True to show the ribbon, False to hide it.
        """
        self.showRibbon() if visible else self.hideRibbon()
