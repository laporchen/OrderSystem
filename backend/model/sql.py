import pymysql
from .classes import * 

db_settings = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "12345678",
    "db": "OrderSystem",
    "charset": "utf8"
}



def main():
    print("sql main")
    try:
        global db
        global cursor 
        db = pymysql.connect(**db_settings)
        cursor = db.cursor()
        return cursor
    except Exception as e:
        print(e)
        return None 


def createDataBase():
    try:
        print("dummyy")
    except Exception as e:
        print(e, "something went wrong")
        return False


def userExist(username):
    global cursor
    try:
        fetchUserFromCustomer = f"SELECT username FROM Customer where username = '{username}'"
        fetchUserFromSeller = f"SELECT username FROM MERCHANT where username = '{username}'"
        print(fetchUserFromCustomer)
        print(fetchUserFromSeller)
        cursor.execute(fetchUserFromCustomer)
        if cursor.rowcount != 0:
            return True 
        cursor.execute(fetchUserFromSeller)
        if cursor.rowcount != 0:
            return True 

        return False 

    except Exception as e:
        print(e, "something went wrong")
        return False

def userIsSeller(username):
    global cursor
    try:
        fetchUserFromSeller = f"SELECT username FROM MERCHANT where username = '{username}'"
        print(fetchUserFromSeller)
        cursor.execute(fetchUserFromSeller)
        return cursor.rowcount == 1

    except Exception as e:
        print(e, "something went wrong")
        return False


def getUser(username):
    global cursor
    try:
        fetchUserFromCustomer = f"SELECT * FROM Customer where username = '{username}'"
        fetchUserFromSeller = f"SELECT * FROM MERCHANT where username = '{username}'"
        isSeller = userIsSeller(username)

        if isSeller:
            cursor.execute(fetchUserFromSeller)
        else:
            cursor.execute(fetchUserFromCustomer)
            
        userTuple = cursor.fetchone()
        user = User(userTuple[0],userTuple[2],None,None,isSeller)
        return user 

    except Exception as e:
        print(e, "something went wrong")
        return False

def insertCustomer(user: User):
    global cursor
    try:
        name = user.first_name + " " + user.last_name
        print("insert user " + name)
        sql = f"INSERT INTO CUSTOMER VALUES ('{user.username}','{name}','{user.password}')"
        print("Execute " + sql)
        cursor.execute(sql)
        db.commit()
        print(f"user {user.username} inserted") 
        return True
    except Exception as e:
        print(e, "something went wrong")
        return False

def insertSeller(seller: User):
    global cursor
    try:
        name = seller.first_name + " " + seller.last_name
        sql = f"CALL insertMerchant('{seller.username}','{seller.username} store','{seller.password}')"
        print("Execute " + sql)
        cursor.execute(sql)
        sql = f"CALL insertShop('{seller.username}','{seller.username} Shop','00:00:00','12:00:00',NULL,NULL,' ',' ',' ',' ',' ',0,0)"
        cursor.execute(sql)
        db.commit()
        print(f"seller {seller.username} inserted") 
        return True
    except Exception as e:
        print(e, "something went wrong")
        return False

def getUserStore(uid):
    # query get uid's store
    global cursor
    try:
        sql = f"SELECT ID FROM SHOP WHERE mer_uname = '{uid}'" # some precedure that can get shopID,shopName,shopAddress,minPrice,maxPrice,rating
        cursor.execute(sql)
        if cursor.rowcount == 0:
            return None
        return cursor.fetchone()[0] 
    except Exception as e:
        print(e, "something went wrong")
        return False

def getStores(filter):
    # some sql procedure to get stores
    global cursor
    try:
        sql = "SELECT * FROM SHOP" # some precedure that can get shopID,shopName,shopAddress,minPrice,maxPrice,rating
        cursor.execute(sql)
        fetched_shops = cursor.fetchall()
        shops = [] 
        for shop in  fetched_shops:
            shops.append({
                "storeID":shop[0],
                "name":shop[2],
                "priceRange": [0,1002],
                "rating":3
            })

        return shops 
    except Exception as e:
        print(e, "something went wrong")
        return False

def getStoreInfo(sid):
    # some sql procedure to get store info
    global cursor
    try:
        sql = f"SELECT * FROM SHOP WHERE ID = {sid}" # some precedure that can get shopID,shopName,shopAddress,minPrice,maxPrice,rating
        cursor.execute(sql)
        if cursor.rowcount == 0:
            return None
        store = cursor.fetchone()

        sql = f"SELECT * FROM ITEM WHERE shop_id = {sid}"
        cursor.execute(sql)
        items = cursor.fetchall()
        menu = []
        
        sql = f"SELECt * FROM ADDRESS WHERE shop_id = {sid}"
        cursor.execute(sql)
        addrTuple = cursor.fetchone()
        address = addrTuple[1] + addrTuple[2] + addrTuple[3]+ addrTuple[4]+ addrTuple[5]+ str(addrTuple[6]) + " 號" + str(addrTuple[7]) + " 樓"


        maxID = 0
        for item in items:
            menu.append({
                {
                    "id":item[0],
                    "name":item[2],
                    "price":item[4]
                }
            })
            maxID = max(maxID,item[0])
        
        return {
            "storeID" : sid,
            "storeName" : store[2],
            "storePhone" : store[5],
            "storeAddress": address,
            "storeRating" : store[7],
            "storeItems": menu,
            "IDcounter": maxID, # 
        }

    except Exception as e:
        print(e, "getStoreInfo went wrong")
        return None 
    
def updateStore(sid,storeInfo):
    global cursor
    global db
    try:
        modify = storeInfo.modifyItem
        delID = storeInfo.delItemID
        newItem = storeInfo.newItem

        try:
            for item in modify:
                sql = f"CALL modifyItem({sid},{item.id},{item.name},{item.price})"
                cursor.execute(sql)
            for did in delID:
                sql = f"CALL delItem({sid},{did})"
                cursor.execute(sql)
            for item in newItem:
                sql = f"CALL insertItem({sid},{item.name},{item.price})"
                cursor.execute(sql)

            #update address,phone and shop name
        except Exception as e:
            print(e, "updateStorewent wrong")
            return None 
        db.commit()
        return True
    except Exception as e:
        print(e, "updateStorewent wrong")
        return False 

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

def updateFav(uid,sid):
    global cursor
    try:
        sql = f"SELECT * FROM FAVORITE WHERE cus_name = '{uid}' and shop_id = '{sid}'"
        cursor.execute(sql)
        if cursor.rowcount == 1:
            sql = f"DELETE FROM FAVORITE WHERE cus_name = '{uid}' and shop_id = '{sid}'"
            cursor.execute(sql)
        else:
            sql = f"INSERT INTO FAVORITE VALUES('{uid}',{sid})"
            cursor.execute(sql)
        db.commit()

        return True
    except Exception as e:
        print(e, "something went wrong")
        return False

def changeUserPassword(uid, npw):
    global cursor
    try:
        sql = f"UPDATE MERCHANT SET password = '{npw}' WHERE username = '{uid}'"
        cursor.execute(sql)
        sql = f"UPDATE CUSTOMER SET password = '{npw}' WHERE username = '{uid}'"
        cursor.execute(sql)
        db.commit()

        return True
    except Exception as e:
        print(e, "something went wrong")
        return False
