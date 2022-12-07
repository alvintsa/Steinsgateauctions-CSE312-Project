from flask import Flask, render_template, send_file, request, url_for, redirect, Response
from helpers.render_listings import *
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
@app.route('/home.css')
def home_css():
    return send_file('templates/home.css',mimetype="text/css")
@app.route('/logo.png')
def send_logo():
    return send_file('images/logo.png')

@app.route('/auctions')
def auction_page():
    #auctions_vals = auctions.find()
    #, auction_db=auctions_vals
    return render_template('auctions/auction.html')



@app.route('/image-upload', methods=('GET', 'POST'))
def image_load():
    if request.method == 'POST':
        #make sure you escape HTML for all these
        image_name = 'images/' + request.files['upload'].filename
        #request.files['upload'].save(image_name)
        time = request.form['End_Time']
        description = request.form['Description']
        item_name = request.form['Item_Name']


        auction_db.insert_one({'image_name': image_name, 'time': time, 'description': description, 'item_name': item_name}) #insert into database

    return redirect(url_for('auction_page'), code=302)

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

@app.route('/listings')
def listing_page():
    with open('templates/listings/all_listings.html') as html_template:
        template = html_template.read()
        loop_start = "{{LOOP}}"
        loop_end = "{{ENDLOOP}}"
        start_index = template.find(loop_start)
        end_index = template.find(loop_end)
        current_listings = listing_db.find({},{"_id":0})
        if current_listings:
            loop_template = template[start_index + len(loop_start):end_index]
            loop_content = ""
            for content in current_listings:
                itemname = content.get("Name", "No Name")
                itemprice = content.get("Price", "0.00")
                itemdesc = content.get("Price","No Description")
                loop_content = loop_content + loop_template
                loop_content.replace("{{ITEMNAME}}",itemname)
                loop_content.replace("{{ITEMPRICE}}",itemprice)
                loop_content.replace("{{ITEMDESC}}",itemdesc)
            final_content = template[:start_index] + loop_content + template[end_index + len(loop_end):]
            return app.response_class(final_content,status=200,mimetype='text/html')
        else:
            final_content = template[:start_index] + template[end_index + len(loop_end):]
            return app.response_class(final_content,status=200,mimetype='text/html')

@app.route('/listings.css')
def listing_css():
    return send_file("templates/listings/all_listings.css")

@app.route('/create-listing', methods=('GET','POST'))
def new_listing():
    if request.method == 'POST':
        item_name = request.form.get("Name","")
        item_name = item_name.replace("&","&amp")
        item_name = item_name.replace("<","&lt")
        item_name = item_name.replace(">","&gt")
        item_description = request.form.get("Description","")
        item_description = item_description.replace("&","&amp")
        item_description = item_description.replace("<","&lt")
        item_description = item_description.replace(">","&gt")
        item_price = request.form.get("Price","")
        item_price = item_price.replace("&","&amp")
        item_price = item_price.replace("<","&lt")
        item_price = item_price.replace(">","&gt")
        item_image = request.form.get("Image",None)

        listing_db.insert_one({"Name":item_name, "Description":item_description, "Price":item_price, "Image":item_image})
    
    return redirect(url_for('listing_page'), code=302)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='5000')