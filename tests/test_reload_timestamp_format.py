"""
Regression tests for the ReloadTimeStamp format used in CacheFunctions.py,
LoadAddCommands.py and LoadDesign_Ribbon.py.

These are plain stdlib unittest tests (no FreeCAD import required) because
the bug is purely about datetime <-> string round-tripping under different
locales, not about anything FreeCAD-specific.

Run with:
    python -m unittest tests/test_reload_timestamp_format.py -v
"""

import locale
import unittest
from datetime import datetime

# Keep this in sync with the format string used in CacheFunctions.py,
# LoadAddCommands.py and LoadDesign_Ribbon.py for the "ReloadTimeStamp"
# preference.
CURRENT_FORMAT = "%Y-%m-%d %H:%M:%S"

# The format that used to be used, kept here only to document/reproduce
# the original bug.
OLD_FORMAT = "%B %d, %Y, %H:%M:%S"

# A representative sample of locales. Locales not installed on the machine
# running the tests are skipped rather than failing the run, since available
# locales vary by OS/distro/CI image.
CANDIDATE_LOCALES = [
    "C",
    "en_US.UTF-8",
    "es_ES.UTF-8",
    "de_DE.UTF-8",
    "fr_FR.UTF-8",
    "ja_JP.UTF-8",
    "ru_RU.UTF-8",
]


def _available_locales():
    available = []
    original = locale.setlocale(locale.LC_TIME)
    try:
        for loc in CANDIDATE_LOCALES:
            try:
                locale.setlocale(locale.LC_TIME, loc)
            except locale.Error:
                continue
            available.append(loc)
    finally:
        locale.setlocale(locale.LC_TIME, original)
    return available


class ReloadTimeStampFormatTests(unittest.TestCase):
    def setUp(self):
        self._original_locale = locale.setlocale(locale.LC_TIME)

    def tearDown(self):
        locale.setlocale(locale.LC_TIME, self._original_locale)

    def test_current_format_round_trips_across_locales(self):
        """
        The timestamp can be written under one locale and read back under a
        *different* one without raising - this is exactly the scenario that
        used to crash the Load Design / Reload dialogs (see
        test_old_format_reproduces_the_reported_bug below).
        """
        now = datetime(2026, 6, 19, 21, 12, 44)
        locales = _available_locales()
        self.assertGreaterEqual(
            len(locales), 2,
            "Need at least two installed locales on this machine to "
            "meaningfully exercise the round trip; install e.g. es_ES.UTF-8 "
            "and de_DE.UTF-8 to run this test.",
        )

        for write_locale in locales:
            locale.setlocale(locale.LC_TIME, write_locale)
            written = now.strftime(CURRENT_FORMAT)

            for read_locale in locales:
                locale.setlocale(locale.LC_TIME, read_locale)
                with self.subTest(write_locale=write_locale, read_locale=read_locale):
                    parsed = datetime.strptime(written, CURRENT_FORMAT)
                    self.assertEqual(parsed, now)

    def test_old_format_reproduces_the_reported_bug(self):
        """
        Regression guard documenting the original crash: a timestamp written
        under a non-English locale (e.g. Spanish "junio") could not be parsed
        back once the process locale changed, raising ValueError.
        """
        try:
            locale.setlocale(locale.LC_TIME, "es_ES.UTF-8")
        except locale.Error:
            self.skipTest("es_ES.UTF-8 locale not installed")

        now = datetime(2026, 6, 19, 21, 12, 44)
        written = now.strftime(OLD_FORMAT)
        self.assertIn("junio", written)

        locale.setlocale(locale.LC_TIME, "C")
        with self.assertRaises(ValueError):
            datetime.strptime(written, OLD_FORMAT)


if __name__ == "__main__":
    unittest.main()
