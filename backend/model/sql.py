import pymysql
from .classes import * 

db_settings = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "root",
    "password": "yourMOM",
    "db": "OrderSystem",
    "charset": "utf8"
}


def main():
    try:
        db = pymysql.connect(**db_settings)
        cursor = db.cursor()
    except Exception as e:
        print(e)
        return False


def createDataBase():
    try:
        print("dummyy")
    except Exception as e:
        print(e, "something went wrong")
        return False


def userExist(username):
    result = True #some sql procedure to check if user exist
    return result

def insertUser(user: User):
    try:
        print("dummyy")
        # some sql procedure to insert user
        return True
    except Exception as e:
        print(e, "something went wrong")
        return False

def insertSeller(seller: Owner):
    try:
        print("dummyy")
        # some sql procedure to insert seller 
        return True
    except Exception as e:
        print(e, "something went wrong")
        return False

def getUserStore(uid):
    # query get uid's store
    return 1

def getStores(filter):
    # some sql procedure to get stores
    return [] 

def getStoreInfo(sid):
    # some sql procedure to get store info
    return {
        "storeID" : sid,
        "storeName" : "raj store",
        "storePhone" : "02123456789",
        "storeAddress": "Raj Road",
        "storeRating" : 4,
        "storeItems": [
                {"id":1, "name":"Striver Food","price":32,"sales":86,},
                {"id":2, "name":"Striver Combo","price":100,"sales":12},
        ],
        "IDcounter": 3,
    }

def getUserCart(sid,uid):
    # some sql procedure to get user cart
    return {}

def getAllUserCart(uid):
    # some sql procedure to get all user cart
    return {}

def updateStore(sid, store):
    # some sql procedure to update store
    return True

def getStoreOrders(sid):
    # some sql procedure to get store orders
    return [
            {"orderNumber":1,"orderDate":"2022/05/19","user":"Striver","orderItems" : [{"id": 32,"name":"Striver Special","quantity" : 1}, {"id" : 31,"name":"Raj Cola", "quantity": 69}],"time":"2022-06-04 13:32","status": "Pending"},
            {"orderNumber":2,"orderDate":"2022/05/19","user":"Raj","orderItems" : [{"id": 32,"name":"Striver Special","quantity" : 5}],"time":"2022-06-04 13:32","status" : "Completed"},
            {"orderNumber":4,"orderDate":"2022/05/19","user":"Ra","orderItems" : [{"id": 32,"name":"Striver Special","quantity" : 5}],"time":"2022-06-04 13:32","status" : "Pending"},
            {"orderNumber":3,"orderDate":"2022/05/19","user":"Rj","orderItems" : [{"id": 32,"name":"Striver Special","quantity" : 5}],"time":"2022-06-04 13:32","status": "Preparing"},
    ]

def updateStoreOrder(sid, oid, status):
    # some sql procedure to update store order
    return True

def getUserOders(uid):
    # some sql procedure to get user orders
    return []