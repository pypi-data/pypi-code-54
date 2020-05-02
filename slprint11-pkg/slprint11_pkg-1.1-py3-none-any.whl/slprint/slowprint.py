import time
from os import system


system("   ") #Enable vt100 in windows

bk = '\b'
lup = '\033[A\b'


def slowprint(text, delay=0.2, yoyo=False, vertical=False ):
  '''    
      Displays a text on the terminal imposing a fixed interval of time between the display of each character.
      The display can be vertically or horizontally.
      The text can also be displayed in the yoyo mode where after the last character is displayed the text is removed regressively by means of a fixed interval of time between the deletion of each character.

    Use:
      slowprint ("Hello World my friend.", delay = 0.05, yoyo = True, vertical = True)
      slowprint ("Hello World my friend.", delay = 0.05, yoyo = True, vertical = False)
      slowprint ("Hello World my friend.", delay = 0.05, yoyo = False, vertical = True)
      slowprint ("Hello World my friend.", delay = 0.05, yoyo = False, vertical = False)

    Parameters:
      text
        The text to be displayed on the terminal.
      delay
        The time in seconds between the display of each character. Default is 0.2 seconds.
      yoyo
        If True after displaying the last character, it begins to remove character by character regressively. Default is False.
      vertical
        If True displays the text vertically, if False displays the text horizontally. Default is False.
  '''
  for c in text:
    print(c, end='\n' if vertical else '' , flush=True)
    time.sleep(delay)
  if yoyo:
    for c in text[::-1]:
      print(f'{bk} {lup if vertical else bk}', end='', flush=True)
      time.sleep(delay)
  