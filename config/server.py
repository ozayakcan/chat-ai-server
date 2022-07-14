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
  responseArray = '{"id": $id,"message": "$message", "image": "$image"}'
  response_found = False
  message = HandleStrings.get_data(data, "message", "message")
  if localeLocal in locale:
    for localeJ in locale[localeLocal]:
      matches = difflib.get_close_matches(message, localeJ["patterns"])
      if len(matches) > 0:
        responseArray = getResponse(data, localeJ, responseArray)
        response_found = True
        break
  
  if not response_found:
    responseArray = getResponse(data, locale[localeLocal][0], responseArray)
    if not message in train[localeLocal]:
      train[localeLocal].append(message)
      with open(train_files[localeLocal], "w") as f:
        json.dump(train[localeLocal], f)
  response = make_response(responseArray)
  response.headers.set('Access-Control-Allow-Origin','*')
  response.headers.set('Content-type', 'application/json;charset=utf-8')
  return response

def getResponse(data, jsonArray, responseArray):
  responseArray = responseArray.replace("$id", str(jsonArray["id"]))
  choice = random.choice(jsonArray["responses"])
  responseArray = responseArray.replace("$message", HandleStrings.replaceStrings(data, choice["response"]))
  if "image" in jsonArray:
    image = jsonArray["image"]
    responseArray = responseArray.replace("$image", image)
  else:
    responseArray = responseArray.replace("$image", "none")
  return responseArray
  