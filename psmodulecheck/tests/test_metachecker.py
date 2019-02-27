import unittest
import os
import sys
import tempfile

package_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(package_path)
import metachecker
import console
import tempproject


class MetacheckerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if sys.stdout.isatty():  # this is false in PyCharm Python console
            console.init()       # doing init from there causes colors to NOT work

        cls.author = 'tod-gentille'
        cls.tempdir = tempfile.TemporaryDirectory()
        proj = tempproject.TempProject(cls.tempdir.name)
        proj.config.user_set_full_path("01")
        proj.config.author = cls.author
        cls.meta_filepath = os.path.join(proj.path, proj.config.get_meta_filename())

    def setUp(self):
        # noinspection PyBroadException
        try:
            os.remove(self.meta_filepath)
        except:
            pass

    def tearDown(self):
        pass

    def test_empty_meta_fails(self):
        open(self.meta_filepath, 'w+').close()
        actual = metachecker.check_meta_contents(self.meta_filepath, self.author)
        self.assertFalse(actual)

    def test_no_author_fails(self):
        with open(self.meta_filepath, 'w+') as f:
            f.write(
                '<clips>\n'
                '<clip href="qt-intro-m01-c01.wmv" title="What is Qt?" />\n'
                '</clips>\n')
        actual = metachecker.check_meta_contents(self.meta_filepath, self.author)
        self.assertFalse(actual)

    def test_no_clip_fails(self):
        with open(self.meta_filepath, 'w+') as f:
            f.write('<?xml version="1.0" encoding="utf-8"?>\n'
                    '<module>\n'
                    '<author>{0}</author>\n'
                    '</module>'.format(self.author))
        actual = metachecker.check_meta_contents(self.meta_filepath, self.author)
        self.assertFalse(actual)


    def test_meta(self):
        with open(self.meta_filepath, 'w+') as f:
            f.write('<?xml version="1.0" encoding="utf-8"?>\n'
                    '<module>\n'
                    '<author>{0}</author>\n'
                    '<clips>\n'
                    '<clip href="qt-intro-m01-c01.wmv" title="What is Qt?" />\n'
                    '</clips>'
                    '</module>'.format(self.author))
        test_wmv = 'qt-intro-m01-c01.wmv'
        open(test_wmv, 'w+').close()
        actual = metachecker.check_meta_contents(self.meta_filepath, self.author)
        self.assertTrue(actual)
        os.remove(test_wmv)
        os.remove(self.meta_filepath)


if __name__ == '__main__':
    unittest.main()