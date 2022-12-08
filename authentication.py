import bcrypt
import string
import random
import hashlib
import app

from flask import Flask, render_template, send_file, request, url_for, redirect, abort, make_response
from pymongo import MongoClient

client = MongoClient("mongo")
mydatabase = client['db']

users_db = mydatabase['users']
tokens_db = mydatabase['tokens']

def salted_hash(password):
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(password.encode(), salt)

    return hash


def process_cookies(request):
    if "Cookie" in request.headers: # if we already have cookies, aka not first time loading page
        print("cookies set", request.cookies, flush = True)
        if("token" in request.cookies): # check if this user has already registered before which would mean token cookie is there
            a = {}
            print("tokens set", flush = True)


            visit_count = int(request.cookies.get("visit_count")) + 1
            token = str(request.cookies.get("token"))

            print(visit_count)
            print(token)

            hashed_token = hashlib.sha256(token.encode()).digest() #auth token 

            print(users_db.find_one({"auth_token":hashed_token}))

            user_info = users_db.find_one({"auth_token":hashed_token}) # parsing and hashing to get ready to authenticate
            print("userinfo", user_info, flush = True)

            if(user_info != None): # authenticate that token in cookie after hash matches the one in database
                # self.chat_username = user_info['username'] # now we have username and password of this token
                random_token = "".join(random.choices(string.ascii_uppercase + string.digits, k = 64)) # generates a random alphanumeric string with length 16 
                users_db.update_one({"username": user_info['username']}, {"$set": {"xsrf": random_token}})
                

                # response = "HTTP/1.1" + " " + "200 " + " OK\r\nContent-Type: " + "text/html; charset=utf-8" + "\r\nX-Content-Type-Options: nosniff\r\n" + "Set-Cookie: visits=" + str(visit_count)+ "; token=" + str(hashed_token) +"; Max-Age=3600; HttpOnly"
                return ({"token": random_token, "visit_count": str(visit_count), "username": app.escapeHTML(user_info['username']), "pre_hash_auth_token": token})
                # response = make_response(render_template("home.html", token =  random_token, visit_count = str(visit_count), username = app.escape_html(user_info['username'])))
                # response.headers["location"] = url_for("")
                # response.set_cookie("visits", str(visit_count), 7200)
                # response.set_cookie("token",str(hashed_token))

                # return (response, 302)


                # print("this is response", response)
            # else:
            #     response = "HTTP/1.1" + " " + "301 " + "Moved Permanently\r\n"+ "Content-Length: 0"+ "\r\n" + "Location: /"
            #     self.request.sendall(response.encode())


        else: # if there is no token cookie, which means first time registering, SO THIS IS WHEN THEY FIRST REGISTER!
            visit_count = int(request.headers["Cookie"].strip().split("=")[1]) + 1
            # response = "HTTP/1.1" + " " + "200 " + " OK\r\nContent-Type: " + "text/html; charset=utf-8" + "\r\nX-Content-Type-Options: nosniff\r\n" + "Set-Cookie: visits=" + str(visit_count)+"; Max-Age=3600; HttOnly"
            print("DOESNT GO TO TEMPLATE")
            random_token = "".join(random.choices(string.ascii_uppercase + string.digits, k = 64)) # generates a random alphanumeric string with length 16
            print(random_token)
            tokens_db.insert_one({"token": random_token})
            # template = template_engine.render_template('index.html', {"token": random_token, "visit_count": str(visit_count)})
            return ({"token": random_token, "visit_count": str(visit_count)})

            # print("this is response", response)
            
        print("THISISVISITS", visit_count)

    else: # first ever time loading page 
        print("cookies not set", flush=True)
        # response = "HTTP/1.1" + " " + "200 " + " OK\r\nContent-Type: " + "text/html; charset=utf-8" + "\r\nX-Content-Type-Options: nosniff\r\n" + "Set-Cookie: visits=1; Max-Age=3600; HttpOnly"
        visit_count = 0
        print("DOESNT GO TO TEMPLATE")
        random_token = "".join(random.choices(string.ascii_uppercase + string.digits, k = 64)) # generates a random alphanumeric string with length 16
        print(random_token)
        tokens_db.insert_one({"token": random_token})
        # template = template_engine.render_template('index.html', {"token": random_token, "visit_count": str(visit_count)})
        return ({"token": random_token, "visit_count": str(visit_count)})
        # response = make_response(render_template("home.html", token =  random_token, visit_count = str(visit_count)))
        # response.headers["location"] = url_for("")
        # response.set_cookie("visits", str(1), 7200)
        # return (response, 302)





# user, password = parsing.parse_authentication_multiform(received_data, reqpath, contype, conlength)
#                 salt = bcrypt.gensalt()
#                 hash = bcrypt.hashpw(password.encode(), salt)
#                 print("Register hash", hash)

#                 print("registerinfo", user, password)
#                 print("registerusername", user)
                
#                 #store username, salted password hash, an empty token hash for later use, and an empty xsrf for later use when we update it
#                 registration_collections.insert_one({"username": user, "password": hash, "token_hash": "".encode(), "xsrf": ""}) 
                
#                 response = "HTTP/1.1" + " " + "301 " + "\r\nContent-Length: " + "0" + "\r\nLocation: /" + "\r\n\r\n" + ""
#                 self.request.sendall(response.encode()) 