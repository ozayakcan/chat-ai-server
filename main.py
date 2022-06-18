from config.ai import AIConfig
from config.server import app
from gevent.pywsgi import WSGIServer

http_server = WSGIServer(('0.0.0.0', AIConfig.port), app)
http_server.serve_forever()
#app.run(host="0.0.0.0", port=AIConfig.port)