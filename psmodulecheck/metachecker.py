from xml.dom import minidom
import os
from console import (print_pass, print_error)


def check_meta_contents(meta_file_name, author_name):
    """
    Verify that the clip names in the meta file all correspond to a file
    named the same.
    Args:
        info: instance of the settings class
    Returns:
        a boolean, true if all files are found
    """
    author_result = False
    clip_result = False
    # noinspection PyBroadException
    try:
        xmldoc = minidom.parse(meta_file_name)
        author_result = check_meta_author(xmldoc, author_name)
        clip_result = check_meta_clips(xmldoc)
    except:
        print_error("Meta file {0} parsing error".format(meta_file_name))

    return author_result and clip_result


# noinspection PyBroadException
def check_meta_author(xmldoc, author_name):
    """check that the author name in the meta file matches the author name from the settings"""
    try:
        author = xmldoc.getElementsByTagName('author')
        name = author[0].firstChild.nodeValue
        if name == author_name:
            return True
        print_error('Expected author name of "{0}", but meta file has "{1}"'.format(
            author_name, name))
    except:
        print_error("Unable to parse the author name from the meta file.")
    return False


def check_meta_clips(xmldoc):
    """check that a file exists that matches the href in all the clip tags"""
    clip_list = xmldoc.getElementsByTagName('clip')
    for clip in clip_list:
        clip_name = clip.attributes['href'].value
        if os.path.exists(clip_name):
            print_pass('found a clip named: ' + clip_name)
        else:
            print_error('did not find a file named: ' + clip_name)
            return False
    if len(clip_list) == 0:
        print_error("No clips were found in the meta file.")
        return False
    return True


def move_and_rename_clips(config, creator):
    """
    Rename both the names of the clips in the meta file and the actual
    names of the files on disk. Write out the new meta file with the new full
    course id name and delete the original meta file named with the short name.
    Args:
        info:the settings class
    """
    xml_doc = minidom.parse(config.get_meta_filename())
    clip_list = xml_doc.getElementsByTagName('clip')
    for clip in clip_list:
        clip_name = clip.attributes['href'].value
        new_name = clip_name.replace(config.short_course_id, config.full_course_id, 1)
        clip.attributes['href'].value = new_name
        try:
            creator.copy(clip_name, new_name)
        except FileNotFoundError:
            print_error("unable to rename from: '" + clip_name + "' to: '" + new_name + "'")

    creator.create_meta_file(xml_doc)
