from flask import Flask, render_template, send_file


app = Flask(__name__)


# just making sure framework is installed properly
# execute python app.py
# may need to update interpreter to venv


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

@app.route('/kurisu.jpg')
def ret_kurisu():
    return send_file("images/kurisu.jpg", mimetype="image/gif")

@app.route('/okabe.jpg')
def ret_okabe():
    return send_file("images/okabe.jpg", mimetype="image/gif")

@app.route('/mayuri.jpeg')
def ret_mayuri():
    return send_file("images/mayuri.jpeg", mimetype="image/gif")

@app.route('/ruka.jpeg')
def ret_ruka():
    return send_file("images/ruka.jpeg", mimetype="image/gif")

@app.route('/itaru.jpeg')
def ret_itaru():
    return send_file("images/itaru.jpeg", mimetype="image/gif")

@app.route('/suzuha.jpeg')
def ret_suzuha():
    return send_file("images/suzuha.jpeg", mimetype="image/gif")

@app.route('/logo.png')
def ret_logo():
    return send_file("images/logo.png", mimetype="image/gif")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='16969')
