from PySide import QtCore, QtWidgets


class RibbonScreenShotWindow(QtWidgets.QMainWindow):
    """This class is just for taking a screenshot of the window, the window will be closed 0.1s after it is shown."""

    _fileName = "shot.jpg"

    def __init__(self, fileName: str = "shot.jpg", *args, **kwargs):
        """Initialize the class.

        :param fileName: The file name for the screenshot.
        """
        super().__init__(*args, **kwargs)
        QtCore.QTimer().singleShot(3000, self.takeScreenShot)
        self.setScreenShotFileName(fileName)
        self.setWindowFlags(QtCore.Qt.WindowType.WindowStaysOnTopHint)

    def setScreenShotFileName(self, fileName: str):
        """Set the file name for the screenshot.

        :param fileName: The file name for the screenshot.
        """
        self._fileName = fileName

    def takeScreenShot(self):
        """Take a screenshot of the window."""
        screen = QtWidgets.QApplication.primaryScreen()
        screenshot = screen.grabWindow(self.winId())
        screenshot.save(self._fileName)
        self.close()
