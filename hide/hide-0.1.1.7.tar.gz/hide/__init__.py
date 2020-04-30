from prompt_toolkit import prompt


def hide(input=""):
    try:
       return prompt(unicode(input),is_password=True)
    except NameError:
       return prompt(input,is_password=True)
