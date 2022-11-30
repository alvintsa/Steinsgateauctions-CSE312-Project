from flask import Flask, render_template, send_file

app = Flask(__name__)

#test with terminal: python app.py

@app.route('/')
def home_page():
    return render_template('home.html')

@app.route('/home.css') 
def home_css():
    return send_file('templates/home.css',mimetype="text/css")

@app.route('/login')
def login_page():
    return render_template('login/login.html')

@app.route('/login.css') 
def login_css():
    return send_file('templates/login/login.css',mimetype="text/css")

@app.route('/listings')
def listings_page():
    return render_template('listings/all_listings.html')

@app.route('/listings.css')
def listings_css():
    return send_file('templates/listings/all_listings.css',mimetype="text/css")

@app.route('/auctions')
def auction_page():
    return render_template('auctions/all_auctions.html')

@app.route('/auctions.css')
def auction_css():
    return send_file('templates/auctions/all_auctions.css',mimetype="text/css")

@app.route('/create')
def create_page():
    return render_template('create_listing/create.html')

@app.route('/create.css')
def create_css():
    return send_file('templates/create_listing/create.css',mimetype="text/css")

@app.route('/account')
def account_page():
    return render_template('user_account/account.html')

@app.route('/account.css')
def account_css():
    return send_file('templates/user_account/account.css',mimetype="text/css")

@app.route('/dog.jpg')
def ret_dog():
    return send_file("images/dog.jpg",mimetype="image/gif")

@app.route('/logo.png')
def ret_logo():
    return send_file("images/logo.png",mimetype="image/gif")

@app.route('/backdrop.jpg')
def ret_backdrop():
    return send_file("images/backdrop.jpg",mimetype="image/gif")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',port='16969')