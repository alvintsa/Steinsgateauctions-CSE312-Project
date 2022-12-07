from flask import Flask, render_template, send_file, request, url_for, redirect
from pymongo import MongoClient


app = Flask(__name__)

#just making sure framework is installed properly
#execute python app.py
#may need to update interpreter to venv

client = MongoClient("mongo")
mydatabase = client['db']


auction_db = mydatabase['auctions']
listing_db = mydatabase['listings']

@app.route('/')
def home_page():
    return render_template('home.html')

@app.route('/auctions')
def auction_page():
    auctions_vals = list(auction_db.find({}))
    if(auctions_vals != []):
        auctions_vals = list(auction_db.find({}))[0]
        image_name = auctions_vals['image_name'][6:] #has /root/ infront for somr reason
        item_name = auctions_vals['item_name']
        time = auctions_vals['time']
        description = auctions_vals['description']

        return render_template('auctions/auction.html', image_name=image_name, item_name=item_name, time=time, description=description)
    else:
        return render_template('auctions/auction.html')


@app.route('/home.css')
def home_css():
    return send_file('templates/home.css',mimetype="text/css")


@app.route('/image-upload', methods=('GET', 'POST'))
def image_load():
    if request.method == 'POST':
        #make sure you escape HTML for all these
        image_name = 'images/' + request.files['upload'].filename
        request.files['upload'].save(image_name)
        time = request.form['End_Time']
        description = request.form['Description']
        item_name = request.form['Item_Name']

        auction_db.insert_one({'image_name': image_name, 'time': time, 'description': description, 'item_name': item_name}) #insert into database

    return redirect(url_for('auction_page'), code=302)

@app.route('/<image_name>')
def display_image(image_name):
    return send_file('images/' + image_name, mimetype="image/gif")

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
    app.run(debug=True, host='0.0.0.0', port='5000')