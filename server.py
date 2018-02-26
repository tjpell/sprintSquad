from flask import Flask, render_template, request
from jinja2 import Environment
import sys

app = Flask(__name__)

# fire up server with the following
# gunicorn -D --threads 4 -b 0.0.0.0:5000 --access-logfile server.log --timeout 360 server:app prefix


#########################################################################################################

# HTML = """
""""""
#
# header, data = mycsv.readcsv(mycsv.getdata())
#
# def print_html_doc():
#     print Environment().from_string(HTML).render(header=header, data=data)

#########################################################################################################


@app.route('/')
def login():
    return render_template('sprint.html', prefix=prefix)


@app.route("/", methods=['POST'])
def runme():
    """Host the server"""
    result = request.get_json()
    with open("Raw.txt", "wb") as fo:
        fo.write(repr(result))
    return repr(result)

    # now we need to rotate this Raw.txt




i = sys.argv.index('server:app')
prefix = sys.argv[i + 1]