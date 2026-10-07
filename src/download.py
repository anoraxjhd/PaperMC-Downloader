from requests import HTTPError, RequestException, JSONDecodeError, get as reqGet
from src.translate import translate
from urllib.parse import urlsplit
from tempfile import NamedTemporaryFile
from pathlib import Path
import src.vars as vars

def notify(msg, resultLabel):
  if vars.no_gui:
    print(msg)
  elif resultLabel:
    resultLabel.after(0, lambda: resultLabel.configure(text=msg))

def setupDownload(version, build, resultLabel = None) -> None:
  bfrSnd = beforeSend(version, build, resultLabel=resultLabel)

  if (bfrSnd[0] == False):
    notify(bfrSnd[1], resultLabel)
    return

  download(bfrSnd[1], resultLabel)

def download(URL: str, resultLabel=None) -> bool:
  notify(translate("label.download.started"), resultLabel)

  filename = Path(urlsplit(URL).path).name
  target = Path(str(vars.savePath)) / filename
  temp_path = None

  try:
    with reqGet(URL, timeout=20, stream=True) as response:
      if response.status_code == 404:
        notify(translate("error.status.download.badUrl"), resultLabel)
        return False

      response.raise_for_status()

      with NamedTemporaryFile(
        mode="wb",
        dir=target.parent,
        prefix=f".{filename}.",
        suffix=".part",
        delete=False,
      ) as file:
        temp_path = Path(file.name)

        for chunk in response.iter_content(chunk_size=64 * 1024):
          if chunk:
            file.write(chunk)

    temp_path.replace(target)
    temp_path = None

  except HTTPError:
    notify(translate("error.status.bad"), resultLabel)
    return False
  except RequestException:
    notify(translate("error.webrequest.failed"), resultLabel)
    return False
  except OSError:
    notify(translate("error.file.open"), resultLabel)
    return False
  finally:
    if temp_path is not None:
      temp_path.unlink(missing_ok=True)
  

  notify(f"{translate('note.file.saved.location')}: {target}", resultLabel)
  return True

def send(version, build="latest", resultLabel=None) -> tuple[bool, str]:

  if version.count(".") == 0 or version.count(".") > 2:
    return False, \
           f"{vars.project.capitalize()} {version} {translate("label.not.found")}."

  versionURL = f"https://fill.papermc.io/v3/projects/{vars.project}/versions/{version}/builds"

  try:
    data = reqGet(versionURL, timeout=10)
    if (data.status_code == 404):
      return False, translate("error.status.badUrl")
    data.raise_for_status()
    data = data.json()
  except HTTPError:
    return False, translate("error.status.bad")
  except JSONDecodeError:
    return False, translate("error.invalid.json")
  except ValueError:
    return False, translate("error.invalid.json")
  except RequestException:
    return False, translate("error.webrequest.failed")
  
  if data == None or not isinstance(data, list):
    return False, translate("error.invalid.json")

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
    if not isinstance(url, str):
      return False, translate("error.invalid.url")
    if not url:
      return False, translate("error.no.download.url")

    parsed_url = urlsplit(url)
    if parsed_url.scheme not in ("http", "https") or not parsed_url.hostname:
      return False, translate("error.invalid.url")
  except (KeyError, IndexError, ValueError, TypeError):
    return False, f"{vars.project.capitalize()} {version}{f' Build: {build}' if build != 'latest' else ''} {translate("label.not.found")}."

  notify(f"{vars.project.capitalize()} {build_label} {translate("label.found")}.\n \
          {translate("label.downloading")}...", resultLabel)
  
  return True, url

def beforeSend(version = "", build = "latest", resultLabel = None) -> tuple[bool, str]:
  if not version:    
    return False, translate("label.enter.version")
    
  data = send(version=version, build=build or "latest", resultLabel=resultLabel)
  return data