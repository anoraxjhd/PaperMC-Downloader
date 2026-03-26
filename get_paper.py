# Imports
from threading import Thread
from requests import get
import customtkinter as ctk
from tkinter import messagebox as mb
from webbrowser import open as wbopen
from json import load
from sys import argv

# VARS

app = None
terminalClose = False
paperURL = None
no_gui = False
data = None
# Settings

lang = "en"
ctk.set_appearance_mode("dark")
URL = "https://qing762.is-a.dev/api/papermc/"
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
      print(f"\n{translate("Error", lang=lang)}: {translate("Data is None are you Online", lang=lang)}"); exit(1)
    mb.showerror(str(translate("Error", lang=lang)) + " " + str(status), f'{translate("Servers response is", lang=lang)}: {status}'); app.destroy(); exit(1)

def send(version = "", data = ""):
  global paperURL, terminalClose
  if version in data['versions']:
    if no_gui:
      print(f"Paper {version} {translate("found", lang=lang)}. \n{translate("Open the Link to download Paper", lang=lang)}: {data['versions'][version]}.")
      terminalClose = True
    else:
      resultLabel.configure(text=f"Paper {version} {translate("found", lang=lang)}. \n {translate("Press ""Download"" to download Paper", lang=lang)}.")
      paperURL = data['versions'][version]
  else:
    if no_gui:
      print(f"Paper {version} {translate("not found", lang=lang)}.")
    else:
      resultLabel.configure(text=f"Paper {version} {translate("not found", lang=lang)}.")

def beforeSend(version = "", data = ""):
  if no_gui and not data:
    print(f"{translate("Error", lang=lang)}: {translate("Data is None are you Online?", lang=lang)}"); return 1
  else:
    if not version: resultLabel.configure(text=f"{translate("Enter a version", lang=lang)}."); return 1
    if not data: mb.showerror(translate("Error", lang=lang), f'{translate("Data is None are you Online?", lang=lang)}'); return 1
  send(version, data)

def openBrowser(URL):
  if not URL: resultLabel.configure(text=f"{translate("Enter a Version and Click Send", lang=lang)}."); return 1
  wbopen(URL)

def GUI():
  global resultLabel, versionInput, app
  app = ctk.CTk()
  app.geometry("400x200")
  app.title("PaperMC Downloader")
  app.iconbitmap("icon.ico")

  resultLabel = ctk.CTkLabel(app, text="/")
  resultLabel.pack(padx=20, pady=10)

  download = ctk.CTkButton(app, text=translate("Download", lang=lang), command=lambda: openBrowser(paperURL))
  download.pack(padx=50)

  versionInput = ctk.CTkEntry(app, placeholder_text=translate("Version", lang=lang))
  versionInput.pack(padx=20, pady=20)

  submit = ctk.CTkButton(app, text=translate("Send", lang=lang), command=lambda: beforeSend(version=versionInput.get(), data=data))
  submit.pack(padx=20)

  app.mainloop()

def terminal():
  while not terminalClose:
    version = input(f"{translate('Version', lang=lang)}: ")
    if version:
      beforeSend(version=version, data=data)

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