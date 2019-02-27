"""Tests for validating the questions.txt file.

    Checks that Questions all have at least one answer, one discriminator,
    and a module link. Validates that all questions end with a module link

    Attributes:
        _config: gets the current settings from the settings factory
        _data: holds the contents of the question file
"""

import os
from console import (print_error, print_pass)


class Question:
    def __init__(self, config):
        self._config = config

    def load_data(self, parent_path):
        full_path = os.path.join(parent_path, self._config.get_question_filename())
        with open(full_path, 'r') as f:
            data = f.read().splitlines()
        return data

    def load_and_check_data(self, parent_path):
        data = self.load_data(parent_path)
        return self.check_entries(data)

    def check_entries(self, data):
        """Check the entries in the question.txt file one line at a time.
        If it's a question line make sure it doesn't exceed question length.
        If it's a comment line skip it.
        If it's an answer line check against answer line length
        Then call :func:`check_question_format`

        Returns:
            boolean - true if all tests pass
        """
        overall_result = True
        for line in data:
            if line.startswith(self._config.question_start):
                result = self.check_question_length(line)
                overall_result = overall_result and result
            elif line.startswith(self._config.question_file_comment):
                continue
            else:  # assume an answer or module link
                result = self.check_answer_length(line)
                overall_result = overall_result and result

        result = self.check_question_format(data)
        overall_result = overall_result and result
        return overall_result

    def check_question_length(self, line):
        """return true if the question line isn't too long; otherwise print error and return false"""
        if len(line) > self._config.max_question_length:
            print_error(''.join(['Question is too long.', '\t', line]))
            return False
        return True

    def check_answer_length(self, line):
        """return true if  an answer line isn't too long - otherwise print error and return false"""
        if len(line) > self._config.max_answer_length:
            print_error(''.join(['Answer is too long.', '\t', line]))
            return False
        return True

    def check_question_format(self, data):
        """Check that the format of a question is correct and complete. A question should
        have a question line, and answer line at least one discriminator and a module link
        line. Call :func``validate_module_link``

         Returns
            boolean - true if all tests pass
        """
        question_ended = True
        answer_found = False
        discriminator_found = False
        result = True

        for line in data:
            if line.startswith(self._config.question_start):

                if not question_ended:
                    msg = 'Question File - new question started but old question was not complete.'
                    print_line_error(msg, line)
                    result = False
                else:
                    question_ended = False

            elif not question_ended:
                if line.startswith(self._config.answer_start):
                    if answer_found:
                        result = False
                        msg = "More than one answer found for a question."
                        print_line_error(msg, line)
                    answer_found = True

                elif line.startswith(self._config.discriminator_start):
                    discriminator_found = True
                elif line.startswith(self._config.module_link_start):
                    result = validate_module_link(line)
                    question_ended = answer_found and discriminator_found
                    if not question_ended:
                        msg = "Found a module link but didn't have answer and discriminator"
                        print_line_error(msg, line)
            elif line.startswith(self._config.question_file_comment):
                pass
            elif question_ended:
                if len(line) > 1:
                    print_error('.'.join(['Question completed, unexpected line:',
                                          '\t', line]))
            if question_ended:
                answer_found = False
                discriminator_found = False
                #end for loop

        if not question_ended:
            result = False
            print_error('Question File - ends with an incomplete question.')
        return result

    def rename_links_and_move_file(self, data):
        """
        Rename both the names of the question answer links
         Write out the new question.txt file to the full course
        destination
        Args:
            info:the settings class
            creator: the class that knows where the full course is
        """
        config = self._config
        for index, line in enumerate(data):
            if line.startswith(config.module_link_start):
                data[index] = line.replace(config.short_course_id, config.full_course_id, 1)

        path = self._config.get_full_course_path()
        filename = self._config.get_question_filename()
        full_path = os.path.join(path, filename)
        with open(full_path, 'w+') as f:
            for line in data:
                f.write(''.join([line, '\n']))

    def validate_all_module_links(self, parent_path):
        data = self.load_data(parent_path)
        overall_result = True
        for line in data:
            if line.startswith(self._config.module_link_start):
                result = validate_module_link(line)
                if not result:
                    overall_result = False
                else:
                    print_pass(''.join(['found question module ', line]))

        return overall_result


def validate_module_link(line):
    """return true if the module link has the name of a file that exists on the disk
    otherwise print an error message and return false"""
    file_name = line.strip('= ')
    if os.path.exists(file_name):
        return True
    print_error("Question File - Module link: {0} does not match any clip file in folder.".format(file_name))
    return False


def print_line_error(msg, line):
    full_msg = ''.join([msg, '\n\t', line])
    print_error(full_msg)


# UNIT TESTS
