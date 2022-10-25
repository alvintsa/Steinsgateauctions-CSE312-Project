from flask import Flask, render_template
app = Flask(__name__)

#just making sure framework is installed properly
#execute export FLASK_APP=server.py and flask run
#for debug_mode execute export FLASK_DEBUG=1
@app.route('/')
def home_page():
    return render_template('home.html')

#dynamic routing
#@app.route("/test/<anything>")
#def route_other(anything):
#    return f'Hello, {anything}!'