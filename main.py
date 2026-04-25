# Imports
import src.ui as ui
import src.vars as vars
from os import path
from argparse import ArgumentParser

vars.savePath = path.dirname(path.abspath(__file__))

def parseArgs():
  parser = ArgumentParser()
  parser.add_argument("--lang", choices=vars.supportedLanguages, default=vars.lang)
  parser.add_argument("--no-gui", action="store_true")

  parser.add_argument("--project", choices=vars.supportedProjects, default=vars.project)

  args = parser.parse_args()
  vars.lang = args.lang
  vars.no_gui = args.no_gui
  vars.project = args.project

parseArgs()
if vars.no_gui:
  ui.terminal(projectType=vars.project)
else:
  ui.GUI(projectType=vars.project)