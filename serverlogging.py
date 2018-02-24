from flask import Flask, request,logging
import logging, logging.handlers

# logging.basicConfig()

app = Flask(__name__)

flask.logger.create_logger() 

LOG_PATH = 'logs/Raw.txt'

@app.route('/', methods=['POST'])
def readWriteJSON():
	del app.logger.handlers[:]
	timed_handler = logging.handlers.TimedRotatingFileHandler(LOG_PATH, when='m', interval = 2)
	timed_handler.setLevel(logging.DEBUG)
	app.logger.addHandler(timed_handler)
	result = request.get_json()
	app.logger.warn(repr(result))
	####CHECK VALID JSON
	valid_json = True
	if valid_json:
		with open("proc.txt","a") as fo:
			 fo.write(repr(result))
	return repr(result)

app.run(host= '0.0.0.0', port = 8080)
