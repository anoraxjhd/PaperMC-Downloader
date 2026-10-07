# Imports
from os import path
import src.ui as ui
import src.vars as vars
from argparse import ArgumentParser

vars.savePath = path.dirname(path.abspath(__file__))

def parseArgs():
  parser = ArgumentParser()

  parser.add_argument("--project", choices=vars.supportedProjects, default="paper")
  parser.add_argument("--lang", choices=vars.supportedLanguages, default="en")
  parser.add_argument("--no-gui", action="store_true", default=False)

  args = parser.parse_args()

  vars.project = args.project
  vars.no_gui = args.no_gui
  vars.lang = args.lang

parseArgs()
if not vars.no_gui:
  ui.GUI(projectType=vars.project)
else:
  ui.terminal(projectType=vars.project)