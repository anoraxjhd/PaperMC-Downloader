from src.translate import translate
from threading import Thread
import src.download as download

def GUI(projectType: str):
  import customtkinter as ctk

  global resultLabel, versionInput
  ctk.set_appearance_mode("dark")

  app = ctk.CTk()
  app.geometry("310x220")
  app.title(f"{projectType.capitalize()} Downloader")
  app.iconbitmap("src/icon.ico")

  resultLabel = ctk.CTkLabel(app, text="/")
  resultLabel.pack(padx=20, pady=10)

  versionInput = ctk.CTkEntry(
                              app, 
                              placeholder_text=translate("label.version"), 
                              width=175
                            )
  versionInput.pack(padx=20, pady=10)

  buildInput = ctk.CTkEntry(
                              app, 
                              placeholder_text=translate("label.build.placeholder"), 
                              width=175
                            )
  buildInput.pack(padx=20, pady=10)

  btnDownload = ctk.CTkButton(
                                app, 
                                text=translate("label.download"), 
                                width=175, 
                                command=lambda: Thread(
                                  target=download.setupDownload, 
                                  args=(
                                    versionInput.get(), 
                                    buildInput.get(), 
                                    resultLabel
                                  ), 
                                  daemon=True
                                ).start()
                              )
  btnDownload.pack(padx=50, pady=7.5)

  app.mainloop()

def terminal(projectType: str):
  print(f"{translate("label.terminal.project.info")}: {projectType.capitalize()}")

  while True:
    version = input(f"{translate('label.version')}: ")
    if not version: return

    release = input(f"{translate("label.terminal.release")}") 
    ok, URLorError = download.beforeSend(version=version, build=release)
    if ok:
      if (download.download(URLorError)):
        break
    else:
      print(URLorError)
