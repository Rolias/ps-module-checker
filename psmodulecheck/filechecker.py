"""Check that all expected file names exist in module folder and that that they
conform to the expected names."""
import os
from console import (print_error, print_pass)
import metachecker
import questions


class FileChecker:
    def __init__(self, config):
        """The json setting data is passed in and set to a member variable"""
        self._config = config

    @property
    def config(self):
        return self._config

    def check_files(self):
        """Make sure the demo and question files exist."""
        pass_demo = self.check_demo_files()
        pass_slide = self.check_slide_files()
        pass_questions = self.check_question_files()
        pass_meta = self.check_meta_file()
        if pass_meta:
            pass_meta = metachecker.check_meta_contents(self.config.get_meta_filename(),
                                                        self.config.author)
        return pass_demo and pass_questions and pass_meta and pass_slide

    def check_demo_files(self):
        """Make sure the demo file exists"""
        for file in self.config.demo_files:
            if os.path.exists(file):
                print_pass("Demo file exists.")
                return True

        print_error_result(self.config.demo_files)
        return False

    def check_slide_files(self):
        """check that the folder has a slide file in one of the accepted formats"""
        for file in self.config.slide_files:
            if os.path.exists(file):
                print_pass("Slide file exists.")
                return True
        print_error_result(self.config.slide_files)
        return False

    def check_question_files(self):
        """return true if a no-questions file exists or if a questions file
        exists and it validates"""
        for file in self.config.question_files:
            if os.path.exists(file):
                print_pass("Question file exists.")
                if os.path.split(file)[1].startswith("no-"):
                    return True
                return self.check_question_contents()

        print_error_result(self.config.question_files)
        return False

    def check_question_contents(self):
        """Use the Question class and do a slew of checks to make sure the file is valid."""
        tester = questions.Question(self.config)
        parent_path = self.config.last_full_path
        return tester.load_and_check_data(parent_path)

    def check_meta_file(self):
        """Verify that meta file is named after enclosing folder.
        If properly named check the contents of the meta file"""
        full_name = self.config.get_meta_filename()
        # full_path = self._config.get_meta_filepath()
        if os.path.exists(full_name):
            print_pass("PASSED - Meta file {0} exists".format(full_name))
            return True
        print_error("Did not find: " + full_name)
        return False


def print_error_result(files):
    """Print an error message showing file names searched when a file isn't found"""
    print_error('Expected to find a file or folder with one of the following names')
    for file in files:
        print('\t' + file)