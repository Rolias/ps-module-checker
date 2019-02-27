import os
import shutil
import questions
import console
import utilities


class FullCourseCreator():
    def __init__(self, config):
        self._config = config
        self.full_course_id_path = self._config.get_full_course_path()


    def create_course_folder(self):
        utilities.create_ancestor_paths(self.full_course_id_path)
        if not os.path.isdir(self.full_course_id_path):
            os.mkdir(self.full_course_id_path)

    def copy(self, source, new_name):
        """copy the file named 'source' in the current directory to the full course
        directory and rename it to new_name. Both source and new_name can be the same."""
        new_file_path = os.path.join(self.full_course_id_path, new_name)
        shutil.copy(source, new_file_path)

    def copy_dir(self, source, new_name):
        new_file_path = os.path.join(self.full_course_id_path, new_name)
        if not os.path.isdir(new_file_path):
            shutil.copytree(source, new_file_path)

    def create_meta_file(self, xmldoc):
        new_meta_file_path = os.path.join(self.full_course_id_path, self._config.get_new_meta_filename())
        with open(new_meta_file_path, 'w+') as file:
            xmldoc.writexml(file)

    def copy_module(self):
        """Copy all the files or folders in the current folder that don't end with .wmv or .meta"""
        files = os.listdir('.')
        for file in files:
            if file.endswith('.wmv'):
                continue
            if file.endswith('.meta'):
                continue
            if os.path.isdir(file):
                self.copy_dir(file, file)
            else:
                self.copy(file, file)

    def copy_question_file(self):
        config = self._config
        q = questions.Question(config)
        parent_path = config.last_full_path
        data = q.load_data(parent_path)
        q.rename_links_and_move_file(data)
