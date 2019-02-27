"""A collection of useful utilities"""
import console
import os


def get_user_response_yn(prompt):
    """Prompt the user with the passed message and add (Y/N) to end
    Keeps prompting until yYNn is entered
    Returns: true if Y/y entered, false if N/n"""
    while True:
        console.print_prompt(prompt + ' (Y/N)')
        answer = input()
        if answer[0].upper() == 'Y':
            return True
        if answer[0].upper() == 'N':
            return False
        console.print_error('Please enter a Y or N')


def create_ancestor_paths(fullpath):
    """Given a path work our way up it recursively and create any folders
    in the path that don't already exist
    """
    parent = os.path.dirname(fullpath)
    if len(parent) < 1:
        print("Couldn't create a folder from:" + fullpath)
        return
    if os.path.isdir(parent):
        return
    create_ancestor_paths(parent)
    print("making directory " + parent)
    os.mkdir(parent)



    # import adjustpath
        # sys.path.append(os.path.dirname(os.path.realpath(__file__)))
        # for path in sys.path:
        #     print (path)