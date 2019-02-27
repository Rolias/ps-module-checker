import colorama
from termcolor import colored


#black white red green yellow blue magenta cyan
def init():
    colorama.init()


def print_error(text):
    msg = "ERROR - " + text
    error_text = colored(msg, 'red')
    print(error_text)


def print_pass(text):
    msg = "PASSED - " + text
    pass_text = colored(msg, 'green')
    print(pass_text)


def print_prompt(text):
    prompt_text = colored(text, 'magenta')
    print(prompt_text)

def print_warning(text):
    warn_text = colored(text, 'yellow')
    print(warn_text)