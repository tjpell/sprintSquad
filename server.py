from flask import Flask, render_template
from jinja2 import Environment

import sys

app = Flask(__name__)


#########################################################################################################
# HTML = """
# <html>
#     <body>
#         <table>
#             <tr>{% for h in header %}<th>{{h}}</th>{% endfor %}</tr>{% for row in data %}
#             <tr>{% for i in row %}<td>{{i}}</td>{% endfor %}</tr>{% endfor %}
#         </table>
#     </body>
# </html>"""
#
# header, data = mycsv.readcsv(mycsv.getdata())
#
# def print_html_doc():
#     print Environment().from_string(HTML).render(header=header, data=data)

#########################################################################################################


@app.route("/")
def runme():
    """Host the server"""

    tedeps

    return render_template('articles.html', prefix=prefix)