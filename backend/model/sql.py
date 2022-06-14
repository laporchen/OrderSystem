import pymysql
import threading
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
        global lock
        lock = threading.Lock()
        db = pymysql.connect(**db_settings)
        cursor = db.cursor()
        return cursor
    except Exception as e:
        print(e)
        return None 

def userExist(username):
    global cursor
    global lock
    try:
        fetchUserFromCustomer = f"SELECT username FROM Customer where username = '{username}'"
        fetchUserFromSeller = f"SELECT username FROM MERCHANT where username = '{username}'"
        lock.acquire() 
        cursor.execute(fetchUserFromCustomer)
        if cursor.rowcount != 0:
            lock.release() 
            return True 
        cursor.execute(fetchUserFromSeller)
        if cursor.rowcount != 0:
            lock.release() 
            return True 

        lock.release() 
        return False 

    except Exception as e:
        print(e, "userExist went wrong")
        lock.release() 
        return False

def userIsSeller(username):
    global cursor
    global lock
    try:
        fetchUserFromSeller = f"SELECT username FROM MERCHANT where username = '{username}'"
        lock.acquire()
        cursor.execute(fetchUserFromSeller)
        lock.release() 
        return cursor.rowcount == 1

    except Exception as e:
        print(e, "userIsSeller went wrong")
        lock.release() 
        return False

def getUser(username):
    global cursor
    global lock
    try:
        fetchUserFromCustomer = f"SELECT * FROM Customer where username = '{username}'"
        fetchUserFromSeller = f"SELECT * FROM MERCHANT where username = '{username}'"
        isSeller = userIsSeller(username)

        lock.acquire()
        if isSeller:
            cursor.execute(fetchUserFromSeller)
        else:
            cursor.execute(fetchUserFromCustomer)
            
        userTuple = cursor.fetchone()
        user = User(userTuple[0],userTuple[2],None,None,isSeller)
        lock.release() 
        return user 

    except Exception as e:
        print(e, "getUser went wrong")
        lock.release() 
        return None 

def insertCustomer(user: User):
    global cursor
    global lock
    try:
        name = user.first_name + " " + user.last_name
        sql = f"INSERT INTO CUSTOMER VALUES ('{user.username}','{name}','{user.password}')"
        lock.acquire()
        cursor.execute(sql)
        db.commit()
        lock.release()
        return True
    except Exception as e:
        print(e, "insertCustomer went wrong")
        lock.release()
        return False

def insertSeller(seller: User):
    global cursor
    global lock
    try:
        name = seller.first_name + " " + seller.last_name
        sql = f"CALL insertMerchant('{seller.username}','{seller.username} store','{seller.password}')"
        lock.acquire()
        cursor.execute(sql)
        sql = f"CALL insertShop('{seller.username}','{seller.username} Shop','00:00:00','12:00:00',NULL,NULL,' ',' ',' ',' ',' ',0,0)"
        cursor.execute(sql)
        db.commit()
        lock.release()
        return True
    except Exception as e:
        print(e, "isertSeller went wrong")
        lock.release()
        return False

def getUserStore(uid):
    # query get uid's store
    global cursor
    global lock
    try:
        sql = f"SELECT ID FROM SHOP WHERE mer_uname = '{uid}'" # some precedure that can get shopID,shopName,shopAddress,minPrice,maxPrice,rating
        lock.acquire()
        cursor.execute(sql)
        lock.release()
        if cursor.rowcount == 0:
            return None
        return cursor.fetchone()[0] 
    except Exception as e:
        print(e, "getUserStore went wrong")
        lock.release()
        return False

def getStores(filter):
    # some sql procedure to get stores
    global cursor
    global lock
    try:
        sql = "SELECT * FROM SHOP" # some precedure that can get shopID,shopName,shopAddress,minPrice,maxPrice,rating
        lock.acquire()
        cursor.execute(sql)
        fetched_shops = cursor.fetchall()
        shops = [] 
        for shop in  fetched_shops:
            sql = f"SELECT MIN(price),MAX(price) FROM ITEM WHERE shop_id = {shop[0]}"
            cursor.execute(sql)
            p = cursor.fetchone()
            minPrice = p[0]
            maxPrice = p[1] 
            shops.append({
                "storeID":shop[0],
                "name":shop[2],
                "priceRange": [minPrice,maxPrice],
                "rating":shop[7]
            })
        lock.release()

        return shops 
    except Exception as e:
        print(e, "getStores went wrong")
        lock.release()
        return False

def getStoreInfo(sid,isSeller):
    # some sql procedure to get store info
    global cursor
    global lock
    try:
        sql = f"SELECT * FROM SHOP WHERE ID = {sid}" # some precedure that can get shopID,shopName,shopAddress,minPrice,maxPrice,rating
        lock.acquire()
        cursor.execute(sql)
        if cursor.rowcount == 0:
            lock.release()
            return None
        store = cursor.fetchone()

        sql = f"SELECT * FROM ITEM WHERE shop_id = {sid}"
        cursor.execute(sql)
        items = cursor.fetchall()
        menu = []
        
        sql = f"SELECt * FROM ADDRESS WHERE shop_id = {sid}"
        cursor.execute(sql)
        addrTuple = cursor.fetchone()
        address = ""
        if isSeller == False:
            address = f"{addrTuple[1]} {addrTuple[2]} {addrTuple[3]} {addrTuple[4]} {addrTuple[5]} {str(addrTuple[6])} 號 {str(addrTuple[7])} 樓"
        else:
            address = {
                "city": addrTuple[1],
                "district" : addrTuple[2],
                "road" : addrTuple[3],
                "lane" : addrTuple[4],
                "alley": addrTuple[5],
                "no" : addrTuple[6],
                "floor" : addrTuple[7]
            }

        maxID = 0
        for item in items:
            menu.append({
                    "id":item[0],
                    "name":item[2],
                    "price":item[4]
            })
            maxID = max(maxID,item[0])
        res =  {
            "storeID" : sid,
            "storeName" : store[2],
            "storePhone" : store[5],
            "storeAddress": address,
            "storeRating" : store[7],
            "storeItems": menu,
            "IDcounter": maxID,  
        }
        lock.release() 

        return res
    except Exception as e:
        print(e, "getStoreInfo went wrong")
        lock.release() 
        return None 
    
def updateStore(sid,storeInfo):
    global cursor
    global db
    global lock
    try:
        lock.acquire()
        modify = storeInfo["modifyItem"]
        delID = storeInfo["delItemID"]
        newItem = storeInfo["newItem"]
        sql = f"CALL updateShopInfo({sid},'{storeInfo['storeName']}','00:00:00','12:00:00','{storeInfo['storePhone']}',NULL)"            
        cursor.execute(sql)
        
        addr = storeInfo["storeAddress"]
        sql = f"CALL updateShopAddress({sid},'{addr['city']}','{addr['district']}','{addr['road']}','{addr['lane']}','{addr['alley']}',{addr['no']},{addr['floor']})"            
        cursor.execute(sql)
        
        try:
            for item in modify:
                sql = f"CALL updateItem({sid},{item['id']},'{item['name']}',{item['price']})"
                cursor.execute(sql)
            for did in delID:
                sql = f"CALL deleteItem({sid},{did})"
                cursor.execute(sql)
            for item in newItem:
                sql = f"CALL insertItem({sid},'{item['name']}',NULL,{item['price']})"
                cursor.execute(sql)

            #update address,phone and shop name
        except Exception as e:
            print(e, "updateStore went wrong")
            lock.release() 
            return None 
        db.commit()
        lock.release() 
        return True
    except Exception as e:
        print(e, "updateStorewent wrong")
        lock.release() 
        return False 

def getUserCart(sid,uid):
    # some sql procedure to get user cart
    global cursor
    global lock
    try:
        sql = f"CALL getUserCart({sid},'{uid}')"
        lock.acquire()
        
        cursor.execute(sql)
        cart = cursor.fetchall()
        print(cart)
        res = {}
        oid = 0
        for item in cart:
            oid = item[0]
            res[item[1]] = item[2]
        lock.release()
        return {"oid":oid,"cart" : res} 
    except Exception as e:
        print(e,"getUserCart went wrong")
        lock.release() 
        return {} 

def getAllUserCart(uid):
    global cursor
    global lock
    try:
        lock.acquire()
        sql = f"CALL getAllUserCart('{uid}')" # get orders procedure
        cursor.execute(sql)
        f = cursor.fetchall()
        print(f)
        carts = []
        for cart in f:
            carts.append({
                "orderNumber" : cart[0],
                "storeID" : cart[4],
                "name": cart[1],
                "itemCount" : int(cart[2]),
                "totalPrice" : cart[3]
            })
            # should be able to get order item here 
        
        lock.release() 
        return carts 
    except Exception as e:
        print(e,"getAllUserCart went wrong")
        lock.release() 
        return False

def getStoreOrders(sid):
    # some sql procedure to get store orders
    global cursor
    global lock
    try:
        lock.acquire()
        sql = f"CALL getShopOrders({sid})"
        res = {} 
        orders = []
        cursor.execute(sql)
        orderItem = cursor.fetchall()
        print(orderItem)

        for item in orderItem:
            if(item[0] not in res):
                res[item[0]] = {"orderItems" : []}
            res[item[0]]["orderItems"].append({
                "name" : item[2],
                "quantity" : item[4],
                "price" : item[3] * item[4],
            })
            res[item[0]]["user"] = item[1]
            res[item[0]]["time"] = item[6]
            res[item[0]]["status"] = item[7]
            res[item[0]]["total"] = item[5]
        for k,v in res.items():
            order = v
            order["orderNumber"] = k
            orders.append(order)
        lock.release() 
        return orders 
    except Exception as e:
        print(e,"getUserOrders went wrong")
        lock.release() 
        return None 

def updateStoreOrder(sid, oid, status):
    global cursor
    global db
    global lock
    try:
        lock.acquire()
        sql = ""
        if status == "PREPARING":
            sql = f"CALL receiveOrder({oid})"
        elif status == "CANCELED":
            sql = f"CALL cancelOrder({oid})"
        elif status == "COMPLETED":
            sql = f"CALL completeOrder({oid})"

        cursor.execute(sql)
        
        db.commit()
        lock.release() 
        return True 
    except Exception as e:
        print(e,"getUserOrders went wrong")
        lock.release() 
        return False 

def getUserOrders(uid):
    # some sql procedure to get user orders
    global cursor
    global lock
    try:
        lock.acquire()
        sql = f"CALL getUserOrders('{uid}')"
        cursor.execute(sql)
        orderItem = cursor.fetchall()
        res = {} 
        for item in orderItem:
            if(item[0] not in res):
                res[item[0]] = {"orderItems" : []}
            res[item[0]]["orderItems"].append({
                "name" : item[2],
                "quantity" : item[4],
                "price" : item[3] * item[4],
            })
            res[item[0]]["rating"] = item[6]
            res[item[0]]["storeName"] = item[1]
            res[item[0]]["time"] = item[8]
            res[item[0]]["status" ] = item[7]
        orders = []
        for k,v in res.items():
            order = v
            order["orderNumber"] = k
            orders.append(order)
        lock.release() 
        return orders 
    except Exception as e:
        print(e,"getUserOrders went wrong")
        lock.release() 
        return None 

def updateFav(uid,sid):
    global cursor
    global lock
    try:
        lock.acquire()
        sql = f"CALL updateFav('{uid}',{sid})"
        cursor.execute(sql)
        db.commit()
        lock.release() 

        return True
    except Exception as e:
        print(e, "updateFav went wrong")
        lock.release() 
        return False

def isUserFav(sid,uid):
    global cursor
    global lock
    try:
        sql = f"SELECT * FROM FAVORITE WHERE shop_id = {sid} AND cus_uname = '{uid}'"
        lock.acquire()
        cursor.execute(sql)

        res = cursor.rowcount == 1

        lock.release()
        return res 
    except Exception as e:
        print(e,"isUserFav went wrong")
        lock.release() 
        return False 

def changeUserPassword(uid, npw):
    global cursor
    global lock
    try:
        lock.acquire()
        sql = f"CALL updatePwd('{uid}','{npw}')"
        cursor.execute(sql)
        db.commit()
        lock.release() 
        return True
    except Exception as e:
        print("changeUserPassword went wrong")
        lock.release() 
        return False


def updateCart(uid,sid,cart,total):
    global cursor
    global db
    global lock
    try:
        lock.acquire()
        sql = f"CALL getOrderIdAsCart('{uid}',{sid},{total})"
        cursor.execute(sql)
        res = cursor.fetchall()
        oid = res[0][0]
        db.commit()
        for itemID,num in cart.items():
            sql = f"CALL updateContainItem({oid},{sid},{int(itemID)},{num})"
            cursor.execute(sql)

        db.commit()
        lock.release() 
        return True
    except Exception as e:
        print(e,"updateCart failed")
        lock.release() 
        return False


def placeOrder(uid,sid,cart,total):
    global cursor
    global db
    global lock
    try:
        lock.acquire()
        sql = f"CALL getOrderIdAsCart('{uid}',{sid},{total})"
        cursor.execute(sql)
        res = cursor.fetchall()
        oid = res[0][0]
        db.commit()
        for itemID,num in cart.items():
            sql = f"CALL updateContainItem({oid},{sid},{int(itemID)},{num})"
            cursor.execute(sql)

        sql = f"CALL placeOrder({oid})"
        cursor.execute(sql)
        db.commit()
        lock.release() 
        return True
    except Exception as e:
        print(e,"placeOrder failed")
        lock.release() 
        return False

def clearCart(uid,sid,cart):
    try:
        #clear the cart
        return True
    except Exception as e:
        return False

def rateOrder(oid,rating):
    global cursor
    global db
    global lock
    try:
        lock.acquire()
        sql = f"CALL rateOrder({oid},{rating})"
        print(sql)
        cursor.execute(sql)
        db.commit()
        lock.release() 
        return True
    except Exception as e:
        print(e,"rateOrder went wrong")
        lock.release() 
        return False 

 

def getUserFav(uid):
    global cursor
    global lock
    try:
        lock.acquire()
        sql = f"SELECT shop_id FROM FAVORITE WHERE cus_uname = '{uid}'"
        cursor.execute(sql)
        fav = cursor.fetchall()
        res = []
        for f in fav:
            res.append(f[0])
        lock.release() 
        return res 
    except Exception as e:
        print(e,"getUserFav went wrong")
        lock.release() 
        return False


