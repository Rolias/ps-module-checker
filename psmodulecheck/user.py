import console


def get_module_number():
    """Ask the user for the module number.
        Input is expected to conform to how the user named the module,
        """
    console.print_prompt("Enter the post m- suffix (e.g. 01, 01-intro):")
    return  input()
