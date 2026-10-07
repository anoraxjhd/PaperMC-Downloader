import src.vars as vars
from json import load

with open("src/translations.json", "r", encoding="UTF-8") as f:
  translations = load(f)

def translate(text):
  try:
    return translations.get(vars.lang, {}).get(text, text)
  except:
    return text