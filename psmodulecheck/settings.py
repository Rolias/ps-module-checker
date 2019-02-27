"""Read the JSON settings  file and store the results in members.
Will also prompt user to enter the module number they want to check.
(See get_suffix) The file checker can be run multiple times so a
different suffix can be entered each time updating the member variable
_lastFullPath."""

import json
import os

SETTINGS_FILE = 'settings.json'

class Settings:


    def __init__(self, data):
        """
        Initialize all the members except _lastFullPath and module_folder
        which are set after the user provides the module number.
        """
        self.create_full_course = data["createFullCourse"]
        self.partial_path = data['path']
        self.meta_suffix = data['metaSuffix']
        self._module_prefix = data['modulePrefix']
        self.short_course_id = data['shortId']
        self.full_course_id = data['courseId']
        self.full_course_destination_prefix = data["fullCourseDestinationPrefix"]
        self.author = data['author']
        self.demo_files = data['demoFiles']
        self.question_files = data['questionFiles']
        self.slide_files = data['slideFiles']
        self.valid_question_file_index = data["validQuestionFileIndex"]
        self.max_question_length = data['maxQuestionLength']
        self.max_answer_length = data['maxAnswerLength']
        self.last_full_path = ''
        self.module_suffix = ''
        self.question_start = data["questionStart"]
        self.answer_start = data["answerStart"]
        self.discriminator_start = data["discriminatorStart"]
        self.module_link_start = data["moduleLinkStart"]
        self.question_file_comment = data["questionFileComment"]
        self.module_folder = None

    def user_set_full_path(self, user_suffix):
        """set _lastFullPath to the full pathname to the module folder
        Args:
            user_suffix - full module suffix as entered  by user the part after m- (e.g. 01-dist)
        Returns:
            a string containing the full path name"""
        self.module_suffix = self._module_prefix + user_suffix
        return self.set_last_full_path()

    def set_last_full_path(self):
        self.module_folder = ''.join([self.short_course_id, self.module_suffix])
        self.last_full_path = os.path.join(self.partial_path,self.module_folder)
        return self.last_full_path

    def get_full_course_path(self):
        module_folder_name = self.full_course_id + self.module_suffix
        prefix = self.full_course_destination_prefix
        full_path = os.path.join(prefix, self.full_course_id)
        return os.path.join(full_path, module_folder_name)

    def get_meta_filename(self):
        """Construct the name expected for the meta file from the folder path
        and suffix (typically .meta) specified in the settings file"""
        return os.path.basename(self.last_full_path) + self.meta_suffix

    def get_meta_filepath(self):
        """ A version that supports creating files in a temp folder for unit testing"""
        filename = self.get_meta_filename()
        return os.path.join(self.partial_path,self.module_folder,filename)

    def get_new_meta_filename(self):
        return os.path.basename(self.full_course_id + self.module_suffix + self.meta_suffix)

    def get_question_filename(self):
        index = self.valid_question_file_index
        return self.question_files[index]

def create_from_file(filename):
    with open(filename, 'rt') as json_file:
        return create_from_dict(json.load(json_file))

def create_from_dict(data):
    return Settings(data)