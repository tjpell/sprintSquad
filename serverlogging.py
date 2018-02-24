# Launch with
#
# gunicorn -D --threads 4 -b 0.0.0.0:8080 --access-logfile server.log --timeout 60 serverlogging:app prefix
from flask import Flask, request
import logging, logging.handlers
from procData2 import write_JSON_if_valid


app = Flask(__name__)

@app.route('/', methods=['POST'])
# def readWriteJSON(prefix):
def readWriteJSON():
	prefix = 'prefix'
	log_path = '/srv/runme/{}/Raw.txt'.format(prefix)
	my_logger = logging.getLogger('MyLogger')
	my_logger.setLevel(logging.DEBUG)
	handler = logging.handlers.TimedRotatingFileHandler(log_path, when='m', interval = 2)
	my_logger.addHandler(handler)
	json_blob = request.get_json()
	my_logger.info(repr(json_blob))
	####CHECK VALID JSON
	write_JSON_if_valid(json_blob, '/srv/runme/{}/proc.txt'.format(prefix))
	return repr(json_blob)

app.run(host= '0.0.0.0', port = 8080)
