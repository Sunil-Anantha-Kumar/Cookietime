
import datetime
import unittest

from mock import mock_open, patch

from .cookietime import (
    FileEmpty,
    FileFormatError,
    TooFewParams,
    compute,
    driver,
)


class TestCookieLog(unittest.TestCase):
    def setUp(self):
        self.mock_data = """cookie,timestamp
AtY0laUfhglK3lC7,2018-12-09T14:19:00+00:00
AtY0laUfhglK3lC7,2018-12-09T14:19:00+00:00
AtY0laUfhglK3lC7,2018-12-09T14:19:00+00:00
SAZuXPGUrfbcn5UA,2018-12-09T10:13:00+00:00
5UAVanZf6UtGyKVS,2018-12-09T07:25:00+00:00
AtY0laUfhglK3lC7,2018-12-09T06:19:00+00:00
SAZuXPGUrfbcn5UA,2018-12-08T22:03:00+00:00
4sMM2LxV07bPJzwf,2018-12-08T21:30:00+00:00
fbcn5UAVanZf6UtG,2018-12-08T09:30:00+00:00
4sMM2LxV07bPJzwf,2018-12-07T23:30:00+00:00
"""
        return super().setUp()

    @patch("getopt.getopt")
    def test_driver(self, mock_get_opt):
        """
        Minimal check to see if driver works 
        """
        mock_get_opt.return_value = (
            (("-f", "cookie_log.csv"), ("-d", "2018-12-09")),
            [],
        )
        driver()

    @patch("getopt.getopt")
    def test_driver_no_file(self, mock_get_opt):
        """
        check driver fn behaviour if filename absent 
        """
        mock_get_opt.return_value = ((("-d", "2018-12-09"),), [])
        with self.assertRaises(TooFewParams):
            driver()

    @patch("os.stat")
    def test_compute_no_logs(self, mm):
        """
        Test to check if file is empty and raises FileEmpty Exception
        """
        mm.return_value.st_size = 0
        with self.assertRaises(FileEmpty):
            with patch("builtins.open", mock_open(read_data="")):
                compute("f", datetime.date.fromisoformat("2021-02-02"))

    @patch("os.stat")
    def test_compute(self, mm):
        """
        Test to check compute for out of bounds date for the given log file
        """
        with patch("builtins.open", mock_open(read_data=self.mock_data)):
            self.assertEqual(
                compute("f", datetime.date.fromisoformat("2021-02-02")), ["0"]
            )

    @patch("os.stat")
    def test_compute_no_header(self, mm):
        """
        Test to check compute behaviour if header is missing in file and raise FileFormatError
        """
        self.mock_data_temp = """AtY0laUfhglK3lC7,2018-12-09T14:19:00+00:00
        AtY0laUfhglK3lC7,2018-12-09T14:19:00+00:00
        AtY0laUfhglK3lC7,2018-12-09T14:19:00+00:00
        SAZuXPGUrfbcn5UA,2018-12-09T10:13:00+00:00
        5UAVanZf6UtGyKVS,2018-12-09T07:25:00+00:00
        AtY0laUfhglK3lC7,2018-12-09T06:19:00+00:00
        SAZuXPGUrfbcn5UA,2018-12-08T22:03:00+00:00
        4sMM2LxV07bPJzwf,2018-12-08T21:30:00+00:00
        fbcn5UAVanZf6UtG,2018-12-08T09:30:00+00:00
        4sMM2LxV07bPJzwf,2018-12-07T23:30:00+00:00
        """
        mm.return_value.st_size = 1
        with self.assertRaises(FileFormatError):
            with patch(
                "builtins.open", mock_open(read_data=self.mock_data_temp)
            ):
                compute("f", datetime.date.fromisoformat("2021-02-02"))

    @patch("os.stat")
    def test_compute_one_right(self, mm):
        """
        Test to compute if compute is performed correctly when expected outcome is one record
        """
        with patch("builtins.open", mock_open(read_data=self.mock_data)):
            self.assertEqual(
                compute("f", datetime.date.fromisoformat("2018-12-09")),
                ["AtY0laUfhglK3lC7"],
            )

    @patch("os.stat")
    def test_compute_multiple_right(self, mm):
        """
        Test for compute to check if multiple cookies match the maximum number of hits 
        """
        self.mock_data_temp = """cookie,timestamp
        AtY0laUfhglK3lC7,2018-12-09T14:19:00+00:00
        AtY0laUfhglK3lC7,2018-12-09T14:19:00+00:00
        AtY0laUfhglK3lC7,2018-12-09T14:19:00+00:00
        SAZuXPGUrfbcn5UA,2018-12-09T10:13:00+00:00
        SAZuXPGUrfbcn5UA,2018-12-09T10:13:00+00:00
        SAZuXPGUrfbcn5UA,2018-12-09T10:13:00+00:00
        SAZuXPGUrfbcn5UA,2018-12-09T10:13:00+00:00
        5UAVanZf6UtGyKVS,2018-12-09T07:25:00+00:00
        AtY0laUfhglK3lC7,2018-12-09T06:19:00+00:00
        SAZuXPGUrfbcn5UA,2018-12-08T22:03:00+00:00
        4sMM2LxV07bPJzwf,2018-12-08T21:30:00+00:00
        fbcn5UAVanZf6UtG,2018-12-08T09:30:00+00:00
        4sMM2LxV07bPJzwf,2018-12-07T23:30:00+00:00"""
        with patch(
            "builtins.open", mock_open(read_data=self.mock_data_temp)
        ):
            self.assertEqual(
                compute("f", datetime.date.fromisoformat("2018-12-09")),
                ["AtY0laUfhglK3lC7", "SAZuXPGUrfbcn5UA"],
            )
