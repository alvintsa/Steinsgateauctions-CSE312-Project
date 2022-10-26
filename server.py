from flask import Flask, render_template, send_file
app = Flask(__name__)

#just making sure framework is installed properly
#execute export FLASK_APP=server.py and flask run
#for debug_mode execute export FLASK_DEBUG=1
@app.route('/')
def home_page():
    return render_template('home.html')

@app.route('/home.css') 
def home_css():
    return send_file('templates/home.css',mimetype="text/css")

@app.route('/testimage/dog.jpg')
def ret_template():
    return send_file("testimage/dog.jpg",mimetype="image/gif")

