# Imports
from sys import argv
import src.ui as ui
import src.vars as vars
from os import path

vars.savePath = path.dirname(path.abspath(__file__))

def parseArgs():
  global lang, no_gui
  i = 1
  while i < len(argv):
    arg = argv[i]
    if arg == '--lang':
      if i + 1 < len(argv) and argv[i + 1] in vars.supportedLanguages:
        vars.lang = argv[i + 1]
        i += 1
      else:
        print("Unsupported language or missing value after --lang.")
        exit(1)
    elif arg == '--no-gui':
      vars.no_gui = True
    else:
      print(f"Unknown argument: {arg}")
      exit(1)
    i += 1

parseArgs()
if vars.no_gui:
  ui.terminal()
else:
  ui.GUI()