from config.ai import AIConfig
from config.strings import HandleStrings
from flask import Flask, request
import random
import json
import difflib

app = Flask(AIConfig.app_name)


@app.route("/")
def home():
  return "AI Active"

locale = {
  "en":json.load(open('locales/en/messages.json')),
  "tr":json.load(open('locales/tr/messages.json'))
}
train_files = {
  "en":"locales/en/train.json",
  "tr":"locales/tr/train.json"
}
train = {
  "en":json.load(open(train_files["en"])),
  "tr":json.load(open(train_files["tr"]))
}
@app.route(AIConfig.conversation_path, methods=['POST'])
def talk():
  data = request.json
  lang = HandleStrings.get_data(data, "lang", "en")
  response = {
    "id": -1,
    "message": ""
  }
  response_found = False
  message = HandleStrings.get_data(data, "message", "message")
  if lang in locale:
    for langJ in locale[lang]:
      matches = difflib.get_close_matches(message, langJ["patterns"])
      if len(matches) > 0:
        response["message"] = HandleStrings.replaceStrings(data, random.choice(langJ["responses"]))
        response["id"] = langJ["id"]
        response_found = True
        break
#      if message in langJ["patterns"]:
#        response["message"] = HandleStrings.replaceStrings(data, random.choice(langJ["responses"]))
#        response["id"] = langJ["id"]
#        response_found = True
#        break
        
  if response_found:
    return str(response)
  else:
    response["message"] = HandleStrings.replaceStrings(data, random.choice(locale[lang][0]["responses"]))
    response["id"] = locale[lang][0]["id"]
    if not message in train[lang]:
      train[lang].append(message)
      with open(train_files[lang], "w") as f:
        json.dump(train[lang], f)
    return str(response)