import src.translate as translate
import src.download as download
from src.vars import terminalClose

def GUI():
  import customtkinter as ctk
  global resultLabel, versionInput
  ctk.set_appearance_mode("dark")

  app = ctk.CTk()
  app.geometry("350x250")
  app.title("PaperMC Downloader")
  app.iconbitmap("src/icon.ico")

  resultLabel = ctk.CTkLabel(app, text="/")
  resultLabel.pack(padx=20, pady=10)

  btnDownload = ctk.CTkButton(app, text=translate.translate("Download"), width=175, command=lambda: download.setupDownload(versionInput.get(), buildInput.get(), resultLabel=resultLabel))
  btnDownload.pack(padx=50, pady=7.5)

  versionInput = ctk.CTkEntry(app, placeholder_text=translate.translate("Version"), width=175)
  versionInput.pack(padx=20, pady=10)

  buildInput = ctk.CTkEntry(app, placeholder_text=translate.translate("Build (leave empty for newest)"), width=175)
  buildInput.pack(padx=20, pady=10)

  submit = ctk.CTkButton(app, text=translate.translate("Send"), command=lambda: download.beforeSend(version=versionInput.get(), build=buildInput.get(), resultLabel=resultLabel), width=175)
  submit.pack(padx=20, pady=7.5)

  app.mainloop()

def terminal():
  global terminalClose
  while not terminalClose:
    version = input(f"{translate.translate('Version')}: ")
    if version:
      release = input(f"{translate.translate("ReleaseTextTerminal")}") 
      URL = download.beforeSend(version=version, build=release)
      if URL != False:
        download.download(URL)
        terminalClose = True
      else:
        print(translate.translate("Error Unknown release or version."))
 