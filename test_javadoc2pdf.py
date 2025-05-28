import unittest

from code_1 import *


class TestShipFunctions(unittest.TestCase):
    def test_read_java_files(self):
        self.assertEqual(
            read_java_files("./test_java_files"),
            [
                "./test_java_files/test_file.java",
                "./test_java_files/parent/test_file_2.java",
            ],
        )

    def test_get_html(self):
        with open("test_html.txt") as f:
            test_html = f.read()
        recievd_html = get_html(read_java_files("./test_java_files"))
        recievd_html = repr(recievd_html)
        self.assertEqual(recievd_html, test_html)
