import pymysql
import string
import random


db_settings = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "12345678",
    "db": "OrderSystem",
    "charset": "utf8"
}


class User:
    def __init__(self, username: str, password: str,first_name: str, last_name: str, is_seller: bool):
        self.username = username
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.is_seller = is_seller
        

def main():
    try:
        global db
        global cursor 
        db = pymysql.connect(**db_settings)
        cursor = db.cursor()
        return cursor
    except Exception as e:
        print(e)
        return None 


def insertUser():
    S = 10
    for i in range(10):
        username = ''.join(random.choices(string.ascii_uppercase + string.digits, k = S)) 
        firstName = ''.join(random.choices(string.ascii_uppercase + string.digits, k = S)) 
        lastName = ''.join(random.choices(string.ascii_uppercase + string.digits, k = S - 2)) 
        password = ''.join(random.choices(string.ascii_uppercase + string.digits, k = S- 5)) 
        name = firstName + " " + lastName
        sql = f"CALL insertCustomer('{username}', '{name}','{password}')"
        cursor.execute(sql)

    db.commit()

def fakeSeller():
    S = 6
    for i in range(10):
        username = ''.join(random.choices(string.ascii_uppercase + string.digits, k = S)) 
        firstName = ''.join(random.choices(string.ascii_uppercase + string.digits, k = S)) 
        lastName = ''.join(random.choices(string.ascii_uppercase + string.digits, k = S - 2)) 
        password = ''.join(random.choices(string.ascii_uppercase + string.digits, k = S- 5)) 
        insertSeller(User(username,password,firstName,lastName,True))
    db.commit()



def insertSeller(seller: User):
    global cursor
    global db
    try:
        name = seller.first_name + " " + seller.last_name
        sql = f"CALL insertMerchant('{seller.username}', '{name}', '{seller.password}')"
        cursor.execute(sql)
        db.commit() 
        sql = f"CALL insertShop('{seller.username}','{name} shop','00:00:00','12:00:00',NULL,NULL,'test city','mock district', 'raj road', '{seller.username} lane','some alley', 1,1)"
        cursor.execute(sql)
        db.commit() 
        return True
    except Exception as e:
        print(e, "insertSeller went wrong")
        return False

        
        
if __name__ == '__main__':
    main()
    #insertUser()
    fakeSeller()

