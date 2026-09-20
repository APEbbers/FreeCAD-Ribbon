from pathlib import Path
from re import error as RegexError


def _get_version():
    # setuptools_scm is not allowed by the FreeCAD addon-manager 
    #
    # root = Path(__file__).resolve().parents[1]
    # if (root / ".git").exists() and not (root / ".git/shallow").exists():
        # try:
        #     import setuptools_scm

        #     return setuptools_scm.get_version(root=str(root))
        # except (ImportError, RegexError, LookupError):
        #     pass
    try:
        from ._version import version

        return version
    except ImportError:
        return "0.0.0-unknown"


__version__ = _get_version()
