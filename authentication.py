import bcrypt

def salted_hash(password):
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(password.encode(), salt)

    return hash




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