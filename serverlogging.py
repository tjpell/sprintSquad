# Launch with
# gunicorn -D --threads 4 -b 0.0.0.0:8080 --access-logfile server.log --timeout 60 serverlogging:app prefix
import sys
import os
from flask import Flask, request
import logging, logging.handlers
from procData2 import write_JSON_if_valid


app = Flask(__name__)

@app.route('/', methods=['POST'])
# def readWriteJSON(prefix):
def readWriteJSON():
	prefix = 'prefix'
	outpath = '/srv/runme/' + prefix
	os.chdir(os.path.expanduser(os.getcwd())) #move to home directory
	os.system('cd ..') #move one directory up
	if not os.path.exists(outpath):
		os.mkdir(outpath, 0777)
	log_path = outpath + '/Raw.txt'
	my_logger = logging.getLogger('serverlogging')
	my_logger.setLevel(logging.DEBUG)
	handler = logging.handlers.TimedRotatingFileHandler(log_path, when='m', interval = 2)
	my_logger.handlers = []
	my_logger.addHandler(handler)
	my_logger.info(request.data.strip()) ##logs HTTP POST with hard returns removed
	json_blob = request.get_json(silent=True) #won't even load blobs that aren't JSON format
	write_JSON_if_valid(json_blob, outpath + '/proc.txt') #writes processed JSON
	return repr(json_blob)

# initialization
# i = sys.argv.index('serverlogging:app')
# prefix = sys.argv[i+1]

# app.run(host= '0.0.0.0', port = 8080)
