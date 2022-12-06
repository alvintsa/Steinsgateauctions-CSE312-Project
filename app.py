from flask import Flask, render_template, send_file, request, url_for, redirect
from pymongo import MongoClient

app = Flask(__name__)

#just making sure framework is installed properly
#execute python app.py
#may need to update interpreter to venv

client = MongoClient('0.0.0.0', 16969) #host and port of current server
db = client.flask_db

#database for auction
todos = db.todos


@app.route('/')
def home_page():
    return render_template('home.html')

@app.route('/auctions')
def auction_page():
    return render_template('auctions/auction.html')

@app.route('/home.css') 
def home_css():
    return send_file('templates/home.css',mimetype="text/css")

@app.route('/image-upload', methods=('GET', 'POST'))
def image_load():
    print("HELLOOOOO")
    if request.method == 'POST':
        print(request.form)
    return render_template('auctions/auction.html')

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/login.css') 
def login_css():
    return send_file('templates/login.css',mimetype="text/css")

@app.route('/dog.jpg')
def ret_dog():
    return send_file("images/dog.jpg",mimetype="image/gif")

@app.route('/backdrop.jpg')
def ret_backdrop():
    return send_file("images/backdrop.jpg",mimetype="image/gif")

@app.route('/okabe.jpg')
def ret_okabe():
   return send_file("images/okabe.jpg", mimetype="image/gif")

@app.route('/kurisu.jpg')
def ret_kurisu():
   return send_file("images/kurisu.jpg", mimetype="image/gif")

@app.route('/auction.css')
def auction_css():
   return send_file('templates/auctions/auction.css', mimetype="text/css")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',port='16969')