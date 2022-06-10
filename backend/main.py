import datetime
from re import I, M

from model import *

from flask import Flask, redirect, request,jsonify
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from flask_cors import CORS
import json
import traceback



keyLocation = './data/jwtKey.json'
try:
    f = open(keyLocation, 'r')
    jwtKey = json.load(f)
    f.close()
except:
    print('Error loading jwtKey.json,please make a new one')
    exit()


app = Flask(__name__)
app.config.from_object(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 1
app.config['JWT_SECRET_KEY'] = jwtKey['key']
CORS(app, resources={r'/*': {'origins': '*'}})

jwt = JWTManager(app)

@app.route('/api/register', methods=['POST'])
def register():
    print(request)
    '''
        Register a new user

        Register format:
            First name
            Last name
            Username
            Password
            Email(optional)
            Phone number

    '''
    message = {"status": "fail"}
    if request.method == 'POST':
        post_data = request.get_json()
        userExist = sql.userExist(post_data['username'])
        # real usage 
        if userExist:
            message['message'] = "User already exist"
            return jsonify(message)

        if(post_data["isSeller"]):
            owner = Owner(post_data['username'], post_data['password'], post_data['first_name'], post_data['last_name'])
            res = sql.insertSeller(owner)
            if(res == False):
                message['message'] = "Failed to register"
                return jsonify(message)
            else:
                message['status'] = "success"
                message['message'] = "Register successfully"
                return jsonify(message)
        else:
            customer = Customer(post_data['username'], post_data['password'], post_data['first_name'], post_data['last_name'])
            res = sql.insertCustomer(customer)
            if(res == False):
                message["message"] = "Failed to register"
                return jsonify(message)
            else:
                message['status'] = "success"
                message['message'] = "Register successfully"
                return jsonify(message)

    else:
        return "Invalid request", 400


@app.route('/api/login', methods=['POST'])
def login():
    '''
        Login a user

        Login format:
            Username
            Password

    '''
    message = {"status": "fail"}
    if request.method == 'POST':
        post_data = request.get_json()
        user = User(post_data["username"],"123456", None , None , None , None) # get user from sql
        userExist = True # check username is in db
        # test
        if user.username != "Lapor":
            message["message"] = "User does not exist"
            return jsonify(message), 200

        if user.check_password(post_data["password"]):
            message["message"] = "Login successful"
            message["status"] = "success"
            message['token'] = create_access_token(identity=user.username)
            message['user'] = user.username
            message['isSeller'] = False # check db
            return jsonify(message), 200
        else:
            message["message"] = "Password incorrect"
            return jsonify(message), 200


        # real
        if userExist == False:
            message["message"] = "User does not exist"
            return jsonify(message), 400

        # some sql line to get user from the database
        if user.checkPassword(request.form['password']):
            message["message"] = "Login successful"
            message["status"] = "success"
            message['token'] = create_access_token(identity=user.username)
            message['user'] = user.username
            message['isSeller'] = False # check db
            return jsonify(message), 200
        else:
            message["message"] = "Password incorrect"
            return jsonify(message), 400

    else:
        message['message'] = "Invalid request"
        return jsonify(message), 400

@app.route('/api/getStores', methods=['POST'])
@jwt_required()
def getStores():
    message = {"status": "fail"}
    if request.method == 'POST':
        post_data = request.get_json()
        search_filter = {} # get search filter from post_data
        stores = []
        for i in range(5): # tests ,real one will fetch from sql
            st = Store(i,f"RAJ's {i} Store",f"Striver Road No.{i}",f"1234567{i}","",None, None)
            st.rating = i+1
            st.price_range[0] = i * 100 + 50
            st.price_range[1] = i * 200 + 100
            obj = {
                "storeID": st.id,
                "name": st.name,
                "address": st.address,
                "phone": st.phone_numbers,
                "description": st.description,
                "rating": st.rating,
                "open_time": st.open_time,
                "close_time": st.close_time,
                "priceRange": st.price_range,
            }
            stores.append(obj)
        message["stores"] = stores
        message["status"] = "success"
        return jsonify(message), 200
    else:
        message['message'] = "Invalid request"
        return jsonify(message), 400
    

@app.route("/api/user", methods=['GET'])
@jwt_required(optional=False)
def returnUser():
    global data
    if request.method == 'GET':
        try:
            current_user = get_jwt_identity()
            # check is seller or not
            message = {"status": "success", "user": current_user}
            return jsonify(message)
        except Exception:
            print(traceback.format_exc())
            message = {"status": "failure",
                       "message": "Error in getting user info"}
            return jsonify(message)
    else:
        message = {"status": "failure",
                   "message": "Invalid request"}
        return jsonify(message)

if __name__ == '__main__':
    app.run(debug=True,port=8081)
