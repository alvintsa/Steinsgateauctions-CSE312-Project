from flask import Flask, render_template, send_file
from flask_socketio import SocketIO, send

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


# just making sure framework is installed properly
# execute python app.py
# may need to update interpreter to venv

@socketio.on('message')
def handleMessage(msg):
    print('Message: ' + msg)
    send(msg, broadcast=True)


@app.route('/')
def home_page():
    return render_template('home.html')


@app.route('/home.css')
def home_css():
    return send_file('templates/home.css', mimetype="text/css")

@app.route('/auction')
def auction_page():
    return render_template('auction.html')

@app.route('/auction.css')
def auction_css():
    return send_file('templates/auction.css', mimetype="text/css")


@app.route('/login')
def login_page():
    return render_template('login.html')


@app.route('/login.css')
def login_css():
    return send_file('templates/login.css', mimetype="text/css")


@app.route('/dog.jpg')
def ret_dog():
    return send_file("images/dog.jpg", mimetype="image/gif")


@app.route('/backdrop.jpg')
def ret_backdrop():
    return send_file("images/backdrop.jpg", mimetype="image/gif")


if __name__ == '__main__':
    socketio.run(app)
    # app.run(debug=True, host='0.0.0.0', port='16969')
