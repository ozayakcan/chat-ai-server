from config.stats import Stats
from flask import Flask
from flask import request
from gevent.pywsgi import WSGIServer
import json
import random
app = Flask(Stats.app_name)

en = json.load(open('locales/en.json'))
tr = json.load(open('locales/tr.json'))

def replaceStrings(data, response):
  if "{name}" in response:
    response = response.replace("{name}", get_data(data, "name"))
  return response
    
def get_data(data, arg):
  str = data[arg]
  if str is None:
    return arg
  else:
    return str

@app.route("/")
def home():
  return "Status:" + "Active" if Stats.active == True else "Not Active"

@app.route("/talk", methods=['POST'])
def talk():
  data = request.json
  lang = get_data(data, "lang")
  langJson = en
  if lang == "tr":
    langJson = tr
  response = {
    "id": -1,
    "message": ""
  }
  for langJ in langJson:
    if get_data(data, "message") in langJ["patterns"]:
      response["message"] = replaceStrings(data, random.choice(langJ["responses"]))
      response["id"] = langJ["id"]
      break
  return str(response)
http_server = WSGIServer(('0.0.0.0', Stats.port), app)
http_server.serve_forever()
#app.run(host="0.0.0.0", port=Stats.port)