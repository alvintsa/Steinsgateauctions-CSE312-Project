from flask import Flask, render_template, send_file, request, url_for, redirect, abort, make_response
from pymongo import MongoClient
import bcrypt
import random
import string
import hashlib

import authentication

app = Flask(__name__)

#just making sure framework is installed properly
#execute python app.py
#may need to update interpreter to venv

client = MongoClient("mongo")
mydatabase = client['db']

auction_db = mydatabase['auctions']
listing_db = mydatabase['listings']
cart_db = mydatabase['items']
users_db = mydatabase['users']
tokens_db = mydatabase['tokens']

def escapeHTML(input):
    return input.replace('&', "&amp;").replace('<', "&lt").replace('>', "&gt")

@app.route('/')
def home_page():
    current_listings = listing_db.find().limit(5)
    # cookie_stuff = authentication.process_cookies(request)

    if current_listings:
        if "visit_count" in request.cookies: # if logged in
            visit_count = request.cookies.get("visit_count")
            print("VISITS", visit_count, flush=True)
            cookie_stuff = authentication.process_cookies(request)
            
            token = cookie_stuff["pre_hash_auth_token"]
            visit_count = cookie_stuff["visit_count"]
            print("ANIME", visit_count, flush = True)
            username = cookie_stuff["username"]
            # hashed_token = cookie_stuff["hashed_token"]

            response = make_response(render_template("home.html", listing_vals=current_listings, token = "penis", visit_count = cookie_stuff["visit_count"], username = username))
            response.set_cookie("visit_count", str(visit_count))
            response.set_cookie("token", token, 7200, None, None, None, False, True, None)

            return response
            
        return(render_template("home.html", listing_vals=current_listings))

        # # if first time every loading page; we have to set set cookies 
        # response = make_response(render_template("home.html", listing_vals=current_listings, token = cookie_stuff["token"], visit_count = cookie_stuff["visit_count"]))

        # return render_template('home.html',listing_vals=current_listings, token = cookie_stuff["token"], visit_count = cookie_stuff["visit_count"])

    return render_template('home.html')


@app.route('/home.css')
def home_css():
    return send_file('templates/home.css', mimetype="text/css")
@app.route('/logo.png')
def send_logo():
    return send_file('images/logo.png')


@app.route('/shoppingcart')
def shopping_cart():
    cart_vals = list(cart_db.find({}))
    if(cart_vals != []):
        cart_vals = list(cart_db.find({}))
        return render_template('shoppingcart/shoppingcart.html', cart_vals=cart_vals)
    else:
        return render_template('shoppingcart/shoppingcart.html')


@app.route('/cart.css')
def shopping_cart_css():
    return send_file('templates/shoppingcart/cart.css', mimetype="text/css")

@app.route('/style.css')
def cart_css():
    return send_file('templates/cart/style.css',mimetype="text/css")

@app.route('/auctions')
def auction_page():
    auctions_vals = list(auction_db.find({}))
    if(auctions_vals != []):
        auctions_vals = list(auction_db.find({}))
        return render_template('auctions/auction.html', auctions_vals=auctions_vals)
    else:
        return render_template('auctions/auction.html')

@app.route('/image-upload', methods=('GET', 'POST'))
def image_load():
    if request.method == 'POST':
        #make sure you escape HTML for all these
        #need to make sure users can't access a different file using /../.
        image_name = 'images/' + request.files['upload'].filename
        request.files['upload'].save(image_name)
        time = escapeHTML(request.form['End_Time'])
        description = escapeHTML(request.form['Description'])
        item_name = escapeHTML(request.form['Item_Name'])

        auction_db.insert_one({'image_name': image_name, 'time': time, 'description': description, 'item_name': item_name}) #insert into database

    return redirect(url_for('auction_page'), code=302)

@app.route('/auctions/<image_name>')
def display_image(image_name):
    return send_file('images/' + image_name, mimetype="image/gif")

@app.route('/login', methods = ('GET', 'POST'))
def login():
    if request.method == 'GET':
        print("GET", request, "GET", flush = True)
        return render_template('/login/loginPage.html')
    
    if request.method == 'POST':
        # request.form

        username = request.form['username']
        password = request.form['password']
        salt = bcrypt.gensalt()
        hash = bcrypt.hashpw(password.encode(), salt)
        print("Loginhash", hash, flush = True)

        to_check = users_db.find_one({"username":username})

        if to_check != None: 
            db_pass_hash = to_check["password"]
            result = bcrypt.checkpw(password.encode(), db_pass_hash)

            if result == True:
                print("result", result, flush = True)

                print("whattoehck", db_pass_hash, flush = True)

                print("found", flush = True)

                #auth token
                random_token = "".join(random.choices(string.ascii_uppercase + string.digits, k = 64)) # generates a random alphanumeric string with length 64
    
                token_hash = hashlib.sha256(random_token.encode()).digest() # SHA256 hash for authenitcation token cookie

                users_db.update_one({"username": username}, {"$set": {"auth_token": token_hash}})

                cookie_stuff = authentication.process_cookies(request)
                response = make_response(redirect('/'))
                print("RANDOMTOKENLOGIN", random_token, flush = True)
                response.set_cookie("token", random_token, 7200, None, None, None, False, True, None)
                response.set_cookie("visit_count" , cookie_stuff["visit_count"])

                return response
            else:
                abort(404)
        else:
            abort(404)
   

@app.route('/register', methods = ('GET', 'POST'))
def register():
    print("REGISTER? Anyone there?", flush=True)
    print("REQUEST", request, "ENDREQUEST", flush = True)

    if request.method == 'GET':
        print("GET", request, "GET", flush = True)
        return render_template('register/registerPage.html')

    if request.method == 'POST':
        # request.form
        print("POST", request.form['username'], flush=True)
        print("penis", request.form['username'], flush=True)

        user_exists = users_db.find_one({'username': request.form['username']}) 

        if user_exists == None:
            print("YES", user_exists, flush = True)
            salted_hash_password = authentication.salted_hash(request.form['password'])
            users_db.insert_one({'username': request.form['username'], 'password': salted_hash_password, "auth_token": "".encode(), "xsrf": ""})
            # session['username'] = request.form['username']

            print("username", request.form['username'], flush=True)
            print("password", request.form['password'], flush=True)

            return redirect('/login')
            # return redirect(url_for('templates/user_account/home.html'))
        else:
         print("NO", flush = True)
         abort(404)

@app.route('/logstyle.css')
def login_css():
    return send_file('templates/login/logstyle.css',mimetype="text/css")

@app.route('/registerstyle.css')
def register_css():
    print("CSS", request, "CSS", flush = True)
    return send_file('templates/register/registerstyle.css', mimetype= "text/css")


@app.route('/functions.js')
def functions_js():
    return send_file("functions.js")

@app.route('/websocket')
def websockets():
    return('implement websockets')

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
    if "token" in request.cookies:
        auth_token = request.cookies.get("token")
        auth_hash = hashlib.sha256(auth_token.encode()).digest()
        user_record = users_db.find_one({"auth_token":auth_hash})
        if user_record:
            all_listings = listing_db.find({},{"_id":0})
            if all_listings:
                return render_template("listings/all_listings.html", listing_vals=all_listings)
            else:
                return render_template("listings/all_listings.html")
    return redirect(url_for('login'), code=302)

@app.route('/listings.css')
def listing_css():
    return send_file("templates/listings/all_listings.css")

@app.route('/create-listing', methods=('GET','POST'))
def new_listing():
    if request.method == 'POST':
        item_name = request.form["Name"]
        if not item_name:
            return redirect(url_for('listing_page'), code=302)
        item_name = item_name.replace("&","&amp")
        item_name = item_name.replace("<","&lt")
        item_name = item_name.replace(">","&gt")
        item_name = item_name.replace("/", " ")
        item_name = item_name.replace(' ', '-')

        prev_listing = listing_db.find_one({"Name":item_name})
        while prev_listing:
            item_name = item_name + '~'
            prev_listing = listing_db.find_one({"Name":item_name})

        item_description = request.form["Description"]
        if not item_description:
            item_description = "No Description"
        item_description = item_description.replace("&","&amp")
        item_description = item_description.replace("<","&lt")
        item_description = item_description.replace(">","&gt")
        item_price = request.form["Price"]
        if not item_price:
            return redirect(url_for('listing_page'), code=302)
        price_alphabet = ['0','1','2','3','4','5','6','7','8','9','0','.']
        for char in item_price:
            if char not in price_alphabet:
                return redirect(url_for('listing_page'), code=302)
        if not request.files["Image"]:
            return redirect(url_for('listing_page'), code=302)
        else:
            image_name = "images/" + item_name + ".jpg"
            request.files["Image"].save(image_name)
        listing_db.insert_one({"Name":item_name, "Description":item_description, "Price":item_price})
    return redirect(url_for('listing_page'), code=302)

@app.route('/listing/<itemname>')
def listing_image(itemname):
    #ensuring a record exists guarantees the image exists and that it is only accessing a file submitted by a user from the listing form
    listing_record = listing_db.find_one({"Name":itemname.replace(".jpg","")})
    if listing_record:
        image_path = "images/" + itemname
        return send_file(image_path,mimetype="image/jpg")
    else:
        abort(404)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='5000')