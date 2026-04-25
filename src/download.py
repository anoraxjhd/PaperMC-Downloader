from requests import get
import src.translate as translate
from threading import Thread
import src.vars as vars

mb = None

def setupDownload(version, build, resultLabel = None):
  Thread(target=download, args=(beforeSend(version, build, resultLabel=resultLabel),), daemon=True).start()

def download(URL : str):
  if URL == 1 or not URL.startswith("https://") and not URL.startswith("http://"): return 1
  if vars.no_gui:
    print(f"{translate.translate("download started")}")
  else:
    mb.showinfo(translate.translate("Download"), f"{translate.translate("download started")}")
  with open(str(URL).split("/")[-1], 'wb') as f:
    f.write(get(URL).content)
  if vars.no_gui:
    print(f"\n{translate.translate("File saved to")}: {vars.savePath}\\{str(URL).split("/")[-1]}")
  else:
    mb.showinfo(translate.translate("Download"), f"{translate.translate("File saved to")}: {vars.savePath}\\{str(URL).split("/")[-1]}")

def send(version, build="latest", resultLabel=None):
  if version.count(".") < 1:
    return False

  # Helper to notify via GUI or CLI
  def notify(msg):
    if vars.no_gui:
      print(msg)
    elif resultLabel:
      resultLabel.configure(text=msg)

  global versionURL
  versionURL = f"https://fill.papermc.io/v3/projects/{vars.project}/versions/{version}/builds"

  try:
    data = get(versionURL).json()
  except Exception:
    data = None

  if not isinstance(data, list):
    notify(f"Paper {version} {translate.translate('not found')}.")
    return False

  # Find the target build entry
  try:
    if build == "latest":
      entry = data[0]
      build_label = version
    else:
      build_id = int(build)
      entry = next((i for i in data if isinstance(i, dict) and i.get("id") == build_id), None)
      build_label = f"{version} Build: {build}"

    if entry is None:
      raise ValueError("Build not found")

    url = entry["downloads"]["server:default"]["url"]

  except (KeyError, IndexError, ValueError, TypeError):
    notify(f"Paper {version}{f' Build: {build}' if build != 'latest' else ''} {translate.translate('not found')}.")
    return False

  if vars.no_gui:
    notify(f"Paper {build_label} {translate.translate('found')}.\n{translate.translate('Downloading')}...")
  else:
    notify(f"Paper {build_label} {translate.translate('found')}.\n{translate.translate('Press \"Download\" to download Paper')}.")

  return url
    
def beforeSend(version = "", build = "latest", resultLabel = None):
  global mb
  if not vars.no_gui:
    import tkinter.messagebox as mb
  if not vars.no_gui and not version:
    mb.showinfo(f"{translate.translate("Enter a version")}.", f"{translate.translate("Enter a version")}."); return 1
  if vars.no_gui and not version:
    print(f"{translate.translate("Enter a version")}."); return 1
  if not build: build = "latest"
  data = send(version=version, build=build, resultLabel=resultLabel)
  return data