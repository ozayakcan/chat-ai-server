from config.ai import AIConfig
from config.strings import HandleStrings
from flask import Flask, request
from locales.locale import locale
import random

app = Flask(AIConfig.app_name)


@app.route("/")
def home():
  return "AI Active"

@app.route(AIConfig.conversation_path, methods=['POST'])
def talk():
  data = request.json
  lang = HandleStrings.get_data(data, "lang", "en")
  response = {
    "id": -1,
    "message": ""
  }
  response_found = False
  if lang in locale:
    for langJ in locale[lang]:
      if HandleStrings.get_data(data, "message", "message") in langJ["patterns"]:
        response["message"] = HandleStrings.replaceStrings(data, random.choice(langJ["responses"]))
        response["id"] = langJ["id"]
        response_found = True
        break
  if response_found:
    return str(response)
  else:
    response["message"] = HandleStrings.replaceStrings(data, random.choice(locale[lang][0]["responses"]))
    response["id"] = locale[lang][0]["id"]
    return str(response)