# Imports
from threading import Thread
from requests import get
import customtkinter as ctk
from tkinter import messagebox as mb
from json import load, dumps
from sys import argv

# VARS
app = None
terminalClose = False
paperURL = None
no_gui = False
data = None
versionURL = None

# Settings
lang = "en"
project = "paper"

ctk.set_appearance_mode("dark")
URL = f"https://fill.papermc.io/v3/projects/{project}"


allowedStatus = [200, 203]
supportedLanguages = ["de", "en"]

with open("translations.json", "r", encoding="UTF-8") as f:
  translations = load(f)
def translate(text, lang="en"):
  try:
    return translations.get(lang, {}).get(text, text)
  except:
    return text

def getData():
  response = get(URL)
  status = response.status_code
  if status in allowedStatus:
    return response.json()
  else:
    if no_gui:
      print(f"\n{translate("Error", lang=lang)}: {translate("Data is None are you Online", lang=lang)}"); terminalClose = True
    mb.showerror(str(translate("Error", lang=lang)) + " " + str(status), f'{translate("Servers response is", lang=lang)}: {status}'); app.destroy()

def download(url):
  with open(url.split("/")[-1], 'wb') as f:
    f.write(get(url).content)

def send(version, build = "latest"):
  # Setup stuff
  if not version.count(".") >= 1: return
  global paperURL, terminalClose, versionURL
  versionURL = f"https://fill.papermc.io/v3/projects/{project}/versions/{version}/builds"
  data = get(versionURL).json()
  # Checking if build is supposed to be latest
  if build == "latest":
    try:
      paperURL = data[0]["downloads"]["server:default"]["url"]
      if not no_gui:
        resultLabel.configure(text=f"Paper {version} {translate("found", lang=lang)}.\n{translate("Press ""Download"" to download Paper", lang=lang)}.")
        return paperURL
      else:
        print(f"Paper {version} {translate("found", lang=lang)}.\n{translate("Downloading", lang=lang)}...")
        return paperURL
    except KeyError:
      if not no_gui:
        resultLabel.configure(text=f"Paper {version} {translate("not found", lang=lang)}.")
        return False
      else:
        print(f"Paper {version} {translate("not found", lang=lang)}.")
        return False
  else:
    for i in data:
      if i["id"] == int(build):
        print(f"Paper {version} {translate("found", lang=lang)}.\n{translate("Downloading", lang=lang)}...")
        return i["downloads"]["server:default"]["url"]
    else:
      return False

def beforeSend(version = "", build = "latest"):
  if not no_gui and not version:
    print(f"{translate("Enter a version", lang=lang)}."); return 1
  if no_gui and not version:
    print(f"{translate("Enter a version", lang=lang)}."); return 1
  return send(version, build=build)

def GUI():
  global resultLabel, versionInput, app
  app = ctk.CTk()
  app.geometry("400x200")
  app.title("PaperMC Downloader")
  app.iconbitmap("src/icon.ico")

  resultLabel = ctk.CTkLabel(app, text="/")
  resultLabel.pack(padx=20, pady=10)

  btnDownload = ctk.CTkButton(app, text=translate("Download", lang=lang), command=lambda: download(paperURL))
  btnDownload.pack(padx=50)

  versionInput = ctk.CTkEntry(app, placeholder_text=translate("Version", lang=lang))
  versionInput.pack(padx=20, pady=20)

  submit = ctk.CTkButton(app, text=translate("Send", lang=lang), command=lambda: beforeSend(version=versionInput.get()))
  submit.pack(padx=20)

  app.mainloop()

def terminal():
  global terminalClose
  while not terminalClose:
    version = input(f"{translate('Version', lang=lang)}: ")
    if version:
      release = input(f"{translate("ReleaseTextTerminal", lang=lang)}")
      if release:
        paperURL = beforeSend(version=version, build=release)
      else:
        paperURL = beforeSend(version=version)
      if paperURL != False:
        download(paperURL)
        terminalClose = True

def parseArgs():
  global lang, no_gui
  i = 1
  while i < len(argv):
    arg = argv[i]
    if arg == '--lang':
      if i + 1 < len(argv) and argv[i + 1] in supportedLanguages:
        lang = argv[i + 1]
        i += 1
      else:
        print("Unsupported language or missing value after --lang.")
        exit(1)
    elif arg == '--no-gui':
      no_gui = True
    else:
      print(f"Unknown argument: {arg}")
      exit(1)
    i += 1

def fetchData():
  global data
  data = getData()

Thread(target=fetchData, daemon=True).start()
parseArgs()
if no_gui:
  try:
    terminal()
  except Exception as e:
    print(e)
else:
  GUI()