"""
https://timlehr.com/python-exception-hooks-with-qt-message-box/
"""

import logging
import sys
import traceback

from PySide.QtWidgets import (
    QApplication,
    QMessageBox,
    QStyle,
)
from PySide.QtCore import (
    Qt,
    QObject,
)

log = logging.getLogger(__name__)
log.addHandler(logging.StreamHandler(stream=sys.stdout))


class UncaughtHook(QObject):
    def __init__(self, *args, **kwargs):
        super(UncaughtHook, self).__init__(*args, **kwargs)

        # this registers the exception_hook() function as hook with the Python interpreter
        sys.excepthook = self.exception_hook

    @staticmethod
    def show_exception_box(log_msg):
        """Checks if a QApplication instance is available and shows a messagebox with the exception message.
        If unavailable (non-console application), log an additional notice.
        """
        if QApplication.instance() is not None:
            errorbox = QMessageBox()
            errorbox.setWindowIcon(
                QApplication.style().standardIcon(
                    QStyle.StandardPixmap.SP_MessageBoxCritical
                )
            )
            errorbox.setWindowTitle("Critical error occurred")
            errorbox.setText(
                f"Oops. An unexpected error occurred:\n```\n{log_msg}\n```"
            )
            errorbox.setTextFormat(Qt.TextFormat.MarkdownText)
            errorbox.exec()
        else:
            log.debug("No QApplication instance available.")

    def exception_hook(self, exc_type, exc_value, exc_traceback):
        """Function handling uncaught exceptions.
        It is triggered each time an uncaught exception occurs.
        """
        if issubclass(exc_type, KeyboardInterrupt):
            # ignore keyboard interrupt to support console applications
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
        else:
            exc_info = (exc_type, exc_value, exc_traceback)
            log_msg = "\n".join(
                [
                    "".join(traceback.format_tb(exc_traceback)),
                    f"{exc_type.__name__}: {exc_value}",
                ]
            )
            log.critical(f"Uncaught exception:\n {log_msg}", exc_info=exc_info)

            # trigger message box show
            self.show_exception_box(log_msg)


# create a global instance of our class to register the hook
qt_exception_hook = UncaughtHook()
