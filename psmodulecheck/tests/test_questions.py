import unittest
import os
import sys
import tempfile

package_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(package_path)
import console
import questions
import tempproject


class QuestionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if sys.stdout.isatty():
            console.init()
        print("Testing with good data.")
        cls.cur_dir = os.getcwd()
        cls.tempdir = tempfile.TemporaryDirectory()

        proj = tempproject.TempProject(cls.tempdir.name)
        proj.config.user_set_full_path("01")
        cls.meta_filename = proj.config.get_meta_filename()
        cls.q = questions.Question(proj.config)
        os.chdir(proj.path)

        cls.good_data = ['Q) What is Qt?',
                         '- An IDE that runs on windows',
                         '- A C++ toolchain similar to gcc',
                         '* A set of comprehensive C++ libraries and associated tools',
                         '- A very advanced text editor.',
                         '= qt-intro-m01-c01.wmv',
                         '#Allowed comment line', ]

        cls.good_link_file = "qt-intro-m01-c01.wmv"
        open(cls.good_link_file, 'w+').close()
        cls.config = proj.config
        # cls.destination_path = proj.config.full_course_destination_prefix

    @classmethod
    def tearDownClass(cls):
        print("Good data testing complete.")
        os.chdir(cls.cur_dir)
        cls.tempdir.cleanup()
        # noinspection PyBroadException
        try:
            os.remove(cls.good_link_file)
        except:
            pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_validate_module_link(self):
        actual = questions.validate_module_link(self.good_link_file)
        self.assertTrue(actual)

    def test_check_question_length_good(self):
        actual = self.q.check_question_length("This is a good line of text")
        self.assertTrue(actual)

    def test_check_answer_length_good(self):
        actual = self.q.check_answer_length("* This is a valid length for an answer")
        self.assertTrue(actual)

    def test_validate_module_link_good(self):
        actual = questions.validate_module_link("=" + self.good_link_file)
        self.assertTrue(actual)

    def test_check_question_format_is_good(self):
        actual = self.q.check_question_format(self.good_data)
        self.assertTrue(actual)

    def test_check_entries(self):
        actual = self.q.check_entries(self.good_data)
        self.assertTrue(actual)

    def test_rename_links_and_move_file(self):
        self.q.rename_links_and_move_file(self.good_data)
        dest_q_file = os.path.join(self.config.full_course_destination_prefix, self.config.get_question_filename())
        actual = os.path.isfile(dest_q_file)
        self.assertTrue(actual)


class QuestionTestsBadData(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if sys.stdout.isatty():
            console.init()
        console.print_warning("Error messages are to be expected here."
                              "Testing bad question data.")
        cls.tempdir = tempfile.TemporaryDirectory()
        proj = tempproject.TempProject(cls.tempdir.name)
        proj.config.user_set_full_path("01")
        cls.meta_filename = proj.config.get_meta_filename()
        cls.q = questions.Question(proj.config)

        cls.bad_link_file = "this-file-does-not-exist.wmv"

        cls.bad_data = ['Q) First Question?',
                        ' An IDE that runs on windows',
                        '* A C++ toolchain similar to gcc',
                        '* This is the second line marked as an answer ',
                        '- A very advanced text editor.',
                        '= qt-intro-m01-c01.wmv',
                        'Q) Second Question?',
                        '* An answer but no discriminator',
                        '= qt-intro-m01-c01.wmv',
                        '#Allowed comment line',
                        '- A discriminator that is out of place.',
                        'Q) Third Question?',
                        '- An unfinished questions', ]

    @classmethod
    def tearDownClass(cls):
        cls.tempdir.cleanup()
        # noinspection PyBroadException
        try:
            os.remove(cls.bad_link_file)
        except:
            pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_check_question_length_bad(self):
        msg = 151 * 'x'
        actual = self.q.check_question_length(msg)
        self.assertFalse(actual)

    def test_check_answer_length_bad(self):
        msg = 101 * 'x'
        actual = self.q.check_answer_length(msg)
        self.assertFalse(actual)

    def test_validate_module_link_bad(self):
        actual = questions.validate_module_link("=" + self.bad_link_file)
        self.assertFalse(actual)

    def test_check_question_format_is_bad(self):
        actual = self.q.check_question_format(self.bad_data)
        self.assertFalse(actual)


if __name__ == '__main__':
    unittest.main()
