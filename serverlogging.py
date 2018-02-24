from flask import Flask, request
import logging, logging.handlers

app = Flask(__name__)

LOG_PATH = 'logs/Raw.txt'

@app.route('/', methods=['POST'])
def readWriteJSON():
	del app.logger.handlers[:]
	timed_handler = logging.handlers.TimedRotatingFileHandler(LOG_PATH, when='m', interval = 2)
	app.logger.setLevel(logging.INFO)
	app.logger.addHandler(timed_handler)
	result = request.get_json()
	app.logger.info(repr(result))
	####CHECK VALID JSON
	valid_json = True
	if valid_json:
		with open("proc.txt","a") as fo:
			 fo.write(repr(result))
	return repr(result)

app.run(host= '0.0.0.0', port = 8080)
