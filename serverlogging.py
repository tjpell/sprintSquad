# Launch with
# gunicorn -D --threads 4 -b 0.0.0.0:8080 --log-level=debug --access-logfile serveraccess.log --error-logfile servererror.log --timeout 360 serverlogging:app prefix
import sys
import os
from flask import Flask, request
import logging, logging.handlers
from procData import write_JSON_if_valid

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def readWriteJSON():
    prefix = app.config.get('prefix')  # pull prefix out of provided configuration (see main method)
    outpath = '/srv/runme/' + prefix

    os.chdir(os.path.expanduser(os.getcwd()))  # move to home directory
    os.system('cd ..')  # move one directory up to
    if not os.path.exists(outpath):
        os.mkdir(outpath, 0777)

    log_path = outpath + '/Raw.txt'  # initialize logging process
    my_logger = logging.getLoggger('serverlogging')
    my_logger.setLevel(logging.DEBUG)
    handler = logging.handlers.TimedRotatingFileHandler(log_path, when='m', interval=2)
    my_logger.handlers = []
    my_logger.addHandler(handler)

    my_logger.info(request.data.strip())  ##logs HTTP POST with hard returns removed
    json_blob = request.get_json(silent=True)  # won't even load blobs that aren't JSON format
    write_JSON_if_valid(json_blob, outpath + '/proc.txt')  # writes processed JSON
    return repr(json_blob)


if __name__ == "__main__":
    i = sys.argv.index('sprintSquad/serverlogging.py')
    prefix = sys.argv[i + 1]  # collect the prefix

    app.config['prefix'] = prefix  # pass prefix into app
    app.run(host='0.0.0.0', port=8080)  # may need to remove this if using gunicorn
