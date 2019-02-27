#!/usr/bin/env python3
"""Check that a PluralSight module folder is ready for submission. If it is copy all the
    needed files to the distribution folder, renaming them if desired.

    Checks both that files exist with proper names and validates contents of various files.
    See the READ_ME.md file for a full description
    Has an option to create  a new folder with new names. Useful if a short name is used for naming everything
    and it needs to be replaced with the full-course-id name before submission. Will rename modules,
    and references to the modules in the meta and question files.
"""
import sys
import os

sys.path.append(os.path.dirname(os.path.realpath(__file__)))
import console
import filechecker
import fullcoursecreator
import metachecker
import settings
import questions
import user
import utilities

def main(user_suffix='--'):
    starting_dir = os.getcwd()
    try:
        if sys.stdout.isatty():  # this is false in PyCharm Python console
            console.init()       # doing init from there causes colors to NOT work

        print(starting_dir)
        settings_dir = os.path.dirname(os.path.realpath(__file__))
        config = settings.create_from_file(os.path.join(settings_dir, settings.SETTINGS_FILE))
        fc = filechecker.FileChecker(config)

        keep_looping = True
        while keep_looping:

            if '--' == user_suffix:  # user didn't provide command line argument
                user_suffix = user.get_module_number()
            dest_path = config.user_set_full_path(user_suffix)

            good_path = False
            try:
                os.chdir(dest_path)
                good_path = True
            except IOError:
                print("The system could not change to the directory:\n\t {0}".format(dest_path))

            if good_path:
                files_good = fc.check_files()

                if files_good:
                    print("All files are valid.\n")
                    if config.create_full_course:
                        create_full_course(config)
                else:
                    console.print_error("Please correct the error and try again.")
            user_suffix = '--'
            keep_looping = utilities.get_user_response_yn('Do you want to run another module?')
    finally:
        os.chdir(starting_dir)


def create_full_course(config):
    print('Creating the course\n')
    creator = fullcoursecreator.FullCourseCreator(config)
    creator.create_course_folder()
    metachecker.move_and_rename_clips(config, creator)
    creator.copy_module()
    creator.copy_question_file()
    validate_full_course(config)


def validate_full_course(config):
    """Just to be safe double-check the newly moved files and verify the files specified
    in both the meta and question files exist in the new target directory
    """
    folder_path = config.get_full_course_path()
    os.chdir(folder_path)
    meta_filename = ''.join([os.path.basename(folder_path), config.meta_suffix])
    metachecker.check_meta_contents(meta_filename, config.author)
    q = questions.Question(config)
    q.validate_all_module_links(folder_path)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main()