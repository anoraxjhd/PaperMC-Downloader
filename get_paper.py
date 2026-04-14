# Imports
from threading import Thread
from requests import get
from json import load
from sys import argv
from os import path

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
  global terminalClose
  response = get(URL)
  status = response.status_code
  if status in allowedStatus:
    return response.json()
  else:
    if no_gui:
      print(f"\n{translate("Error", lang=lang)}: {translate("Data is None are you Online", lang=lang)}"); terminalClose = True; return
    mb.showerror(str(translate("Error", lang=lang)) + " " + str(status), f'{translate("Servers response is", lang=lang)}: {status}'); app.destroy()

def download(url):
  storage = url
  if storage:
    if not no_gui:
      mb.showinfo(translate("download started", lang=lang), translate("download started", lang=lang))
    with open(str(storage).split("/")[-1], 'wb') as f:
      f.write(get(storage).content)
    if not no_gui:
      mb.showinfo(translate("Download", lang=lang), f"{translate("File saved to", lang=lang)} {path.dirname(path.abspath(__file__))}.")

def send(version, build = "latest"):
  # Setup stuff
  if not version.count(".") >= 1: return False
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
  data = send(version, build=build)
  return data

def setupDownload(version, build):
  if build:
    url = beforeSend(version, build)
    Thread(target=download, args=(url,), daemon=True).start()
  else:
    url = beforeSend(version)
    Thread(target=download, args=(url,), daemon=True).start()

def GUI():
  global mb
  import customtkinter as ctk
  from tkinter import messagebox as mb
  global resultLabel, versionInput, app

  ctk.set_appearance_mode("dark")

  app = ctk.CTk()
  app.geometry("350x250")
  app.title("PaperMC Downloader")
  app.iconbitmap("src/icon.ico")

  resultLabel = ctk.CTkLabel(app, text="/")
  resultLabel.pack(padx=20, pady=10)

  btnDownload = ctk.CTkButton(app, text=translate("Download", lang=lang), width=175, command=lambda: setupDownload(versionInput.get(), buildInput.get()))
  btnDownload.pack(padx=50, pady=7.5)

  versionInput = ctk.CTkEntry(app, placeholder_text=translate("Version", lang=lang), width=175)
  versionInput.pack(padx=20, pady=10)

  buildInput = ctk.CTkEntry(app, placeholder_text=translate("Build (leave empty for newest)", lang=lang), width=175)
  buildInput.pack(padx=20, pady=10)

  submit = ctk.CTkButton(app, text=translate("Send", lang=lang), command=lambda: beforeSend(version=versionInput.get()), width=175)
  submit.pack(padx=20, pady=7.5)

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
        print(translate("Download", lang=lang), f"{translate("File saved to", lang=lang)} {path.dirname(path.abspath(__file__))}.")
        terminalClose = True
      else:
        print(translate("Error Unknown release or version.", lang=lang))

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