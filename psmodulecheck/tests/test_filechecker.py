import os
import sys
import tempfile
import unittest

package_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(package_path)

import tempproject
from psmodulecheck import (console,
                           filechecker,
                           )


class FilecheckerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if sys.stdout.isatty():  # this is false in PyCharm Python console
            console.init()       # doing init from there causes colors
                                 # to NOT work
        cls.tempdir = tempfile.TemporaryDirectory()
        proj = tempproject.TempProject(cls.tempdir.name)
        proj.config.user_set_full_path("01")
        proj.create_files()
        cls.fc = filechecker.FileChecker(proj.config)

    @classmethod
    def tearDownClass(cls):
        cls.tempdir.cleanup()

    def test_check_demo_files(self):
        actual = self.fc.check_demo_files()
        self.assertTrue(actual)

    def test_check_question_files(self):
        actual = self.fc.check_question_files()
        self.assertTrue(actual)

    def test_validate_meta(self):
        cur_dir = os.getcwd()
        os.chdir(self.fc.config.partial_path)
        actual = self.fc.check_meta_file()
        self.assertTrue(actual)
        os.chdir(cur_dir)


class FileCheckerTestsNoFiles(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if sys.stdout.isatty():  # this is false in PyCharm Python console
            console.init()       # doing init from there causes colors
                                 # to NOT work
        cls.tempdir = tempfile.TemporaryDirectory()
        proj = tempproject.TempProject(cls.tempdir.name)
        proj.config.user_set_full_path("01")
        cls.fc = filechecker.FileChecker(proj.config)
        console.print_warning("Error messages will appear if these tests pass")

    @classmethod
    def tearDownClass(cls):
        cls.tempdir.cleanup()

    def test_check_demo_files_fails(self):
        actual = self.fc.check_demo_files()
        self.assertFalse(actual)

    def test_check_question_files_fails(self):
        actual = self.fc.check_question_files()
        self.assertFalse(actual)

    def test_validate_meta_fails(self):
        actual = self.fc.check_meta_file()
        self.assertFalse(actual)


if __name__ == '__main__':
    unittest.main()
