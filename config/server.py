from config.ai import AIConfig
from config.strings import HandleStrings
from flask import Flask, request, make_response
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
  data = request.form
  localeLocal = HandleStrings.get_data(data, "locale", "en")
  responseJson = '{"id": $id,"message": "$message"}'
  response_found = False
  message = HandleStrings.get_data(data, "message", "message")
  if localeLocal in locale:
    for localeJ in locale[localeLocal]:
      matches = difflib.get_close_matches(message, localeJ["patterns"])
      if len(matches) > 0:
        responseJson = responseJson.replace("$id", str(localeJ["id"]))
        responseJson = responseJson.replace("$message", HandleStrings.replaceStrings(data, random.choice(localeJ["responses"])))
        response_found = True
        break
  
  if not response_found:
    responseJson = responseJson.replace("$id", str(locale[localeLocal][0]["id"]))
    responseJson = responseJson.replace("$message", HandleStrings.replaceStrings(data, random.choice(locale[localeLocal][0]["responses"])))
    if not message in train[localeLocal]:
      train[localeLocal].append(message)
      with open(train_files[localeLocal], "w") as f:
        json.dump(train[localeLocal], f)
  response = make_response(responseJson)
  response.headers.set('Access-Control-Allow-Origin','*')
  response.headers.set('Content-type', 'application/json;charset=utf-8')
  return response