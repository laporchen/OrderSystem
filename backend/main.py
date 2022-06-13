import datetime
from email import message
from glob import escape


from model.classes import *
import model.sql as sql

from flask import Flask,  request,jsonify
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

sql.main() # db cursor
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

        if post_data["isSeller"] == True:
            owner = User(post_data['username'], post_data['password'], post_data['first_name'], post_data['last_name'],True)
            res = sql.insertSeller(owner)
            if(res == False):
                message['message'] = "Failed to register"
                return jsonify(message)
            else:
                message['status'] = "success"
                message['message'] = "Register successfully"
                return jsonify(message)
        else:
            customer = User(post_data['username'], post_data['password'], post_data['first_name'], post_data['last_name'],False)
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
        username = post_data["username"]
        password = post_data["password"]
        userExist = sql.userExist(username)# check username is in db
        
        if userExist == False:
            message["message"] = "User does not exist"
            return jsonify(message), 200

        user = sql.getUser(username)
        # some sql line to get user from the database
        if user.checkPassword(password):
            message["message"] = "Login successful"
            message["status"] = "success"
            message['token'] = create_access_token(identity=user.username)
            message['user'] = user.username
            message['isSeller'] = user.is_seller # check db
            return jsonify(message), 200 
        else:
            message["message"] = "Password incorrect"
            return jsonify(message), 200

    else:
        message['message'] = "Invalid request"
        return jsonify(message), 400

@app.route('/api/getStores', methods=['POST'])
def getStores():
    message = {"status": "fail"}
    if request.method == 'POST':
        post_data = request.get_json()
        search_filter = post_data# get search filter from post_data
        stores = sql.getStores(search_filter) 
        message["stores"] = stores
        message["status"] = "success"
        return jsonify(message), 200
    else:
        message['message'] = "Invalid request"
        return jsonify(message), 400
    

@app.route("/api/user", methods=['GET'])
@jwt_required()
def returnUser():
    if request.method == 'GET':
        try:
            current_user = get_jwt_identity()
            # check is seller or not
            user = sql.getUser(current_user)
            message = {"status": "success", "user": user.username,"isSeller": user.is_seller}
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

@app.route("/api/store", methods=['POST'])
@jwt_required()
def returnStore():
    if request.method == 'POST':
        post_data = request.get_json()
        uid = post_data["username"]
        sid = None 
        if post_data["isSeller"] == False:
            sid = post_data["storeID"]
            cart = sql.getUserCart(sid, post_data["username"])
            message["cart"] = cart
        else:
            sid = sql.getUserStore(uid)

        if sid == None:
            message = {"status": "failed","message":"Cannot find the store"}
            return jsonify(message)

        store = sql.getStoreInfo(sid)
        message = {"status": "success"}
        message["store"] = store
        return jsonify(message)
    else:
        message = {"status": "failure",
                   "message": "Invalid request"}
        return jsonify(message)

@app.route("/api/updateStore", methods=['POST'])
@jwt_required()
def updateStore():
    if request.method == 'POST':
        message = {"status": "failed"}
        post_data = request.get_json()
        if post_data["isSeller"] == False:
            message["message"] = "You are not a seller"
            return jsonify(message), 400
        sid = post_data["storeID"]
        status = sql.updateStore(sid, post_data["store"])
        if status == False:
            message["message"] = "Failed to update store"
            return jsonify(message), 400
        message["status"] = "success"
        message["message"] = "Store updated"
        return jsonify(message)

@app.route("/api/getStoreOrders", methods=['POST'])
@jwt_required()
def getStoreOrders():
    if request.method == 'POST':
        message = {"status": "failed"}
        post_data = request.get_json()
        if post_data["isSeller"] == False:
            message["message"] = "You are not a seller"
            return jsonify(message), 400
        sid = sql.getUserStore(post_data["userID"])
        storeOrders = sql.getStoreOrders(sid)
        message["message"] = "Store orders"
        message["status"] = "success"
        message["orders"] = storeOrders
        return jsonify(message)
    

@app.route("/api/updateStoreOrder", methods=['POST'])
@jwt_required()
def updateStoreOrder():
    if request.method == 'POST':
        post_data = request.get_json()
        message = {"status": "failed"}
        if post_data["isSeller"] == False:
            message["message"] = "You are not a seller"
            return jsonify(message), 400
        sid = sql.getUserStore(post_data["userID"])
        oid = post_data["orderID"]
        new_status = post_data["newStatus"]
        status = sql.updateStoreOrder(sid,oid, new_status)
        if status == False:
            message["message"] = "Failed to update order"
            return jsonify(message), 400
        message["status"] = "success"
        message["message"] = "Order updated"
        return jsonify(message)


@app.route("/api/userFavStoreUpdate",methods=["POST"])
@jwt_required()
def userFavStoreUpdate():
    if request.method == "POST":
        post_data = request.get_json()
        uid = post_data["username"]
        sid = post_data["storeID"]
        res = sql.updateFav(uid,sid) 
        if res == True:
            message = {"status":"success"}
            return jsonify(message)
        message = {"status":"failed"}
        return jsonify(message)
    

@app.route("/api/changePassword",methods=["POST"])
@jwt_required()
def changePassword():
    if request.method == "POST":
        pd = request.get_json()
        username = pd["username"]
        npw = pd["newPassword"]
        opw = pd["oldPassword"]
        if npw != pd["confirmPassword"]:
            message = {"status":"failed","message" : "New password does not match"}
            return jsonify(message), 200
        user = sql.getUser(username)
        
        if user == False:
            message = {"status":"failed","message" : "User does not exist"}
            return jsonify(message), 400
        
        if user.checkPassword(opw) == False:
            message = {"status":"failed","message" : "Old password does not match"}
            return jsonify(message), 200
        
        if sql.changeUserPassword(username,npw) == True:
            message = {"status":"success","message" : "Password has been updated"}
            return jsonify(message), 200

        message = {"status":"failed","message" : "Password did not change"}
        return jsonify(message), 200

    else:
        return "Invalid request", 400

if __name__ == '__main__':
    app.run(debug=True,port=8081)
