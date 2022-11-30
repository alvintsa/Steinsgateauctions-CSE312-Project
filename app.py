from flask import Flask, render_template, send_file

app = Flask(__name__)

#just making sure framework is installed properly
#execute python app.py
#may need to update interpreter to venv

@app.route('/')
def home_page():
    return render_template('home.html')

@app.route('/home.css') 
def home_css():
    return send_file('templates/home.css',mimetype="text/css")

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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',port='16969')