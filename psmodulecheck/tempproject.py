import os
# from psmodulecheck import (settings)
import settings


class TempProject:
    """Creates a configuration for a temporary PS project, and manages
    the creation of files in that directory if requested.

    """

    def __init__(self, root):
        """Create a new temporary project at ROOT.
        """
        self.path = root

        config_dict = {
            "path": self.path,
            "shortId": "qt-intro",
            "courseId": "introduction-qt-cplusplus-framework",
            "author": "tod-gentille",
            "createFullCourse": True,
            "fullCourseDestinationPrefix": os.path.join(self.path, "destination"),
            "metaSuffix": ".meta",
            "modulePrefix": "-m",
            "maxQuestionLength": 150,
            "maxAnswerLength": 100,
            "demoFiles": [os.path.join(self.path, f)
                          for f in ("no-demos.txt", "demos.zip")],
            "questionFiles": [os.path.join(self.path, f)
                              for f in ("no-questions.txt", "questions.txt")],
            "slideFiles": [os.path.join(self.path, f)
                           for f in ("slides.ppt", "slides.pptx", "slides.pdf")],
            "validQuestionFileIndex": 1,
            "questionStart": "Q)",
            "answerStart": "*",
            "discriminatorStart": "-",
            "moduleLinkStart": "=",
            "questionFileComment": "#"
        }

        self._config = settings.create_from_dict(config_dict)

    @property
    def config(self):
        """The ``Settings`` associated with this project."""
        return self._config

    def create_files(self):
        """Create the questions, demos, and meta files for the
        project.
        """
        for f in (self.config.question_files[0],
                  self.config.demo_files[0],
                  os.path.join(self.path, self.config.get_meta_filename())):
            with open(f, 'w+'):
                pass


