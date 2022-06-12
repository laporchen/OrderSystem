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
    for i in range(100):
        username = ''.join(random.choices(string.ascii_uppercase + string.digits, k = S)) 
        firstName = ''.join(random.choices(string.ascii_uppercase + string.digits, k = S)) 
        lastName = ''.join(random.choices(string.ascii_uppercase + string.digits, k = S - 2)) 
        password = ''.join(random.choices(string.ascii_uppercase + string.digits, k = S- 5)) 
        name = firstName + " " + lastName
        sql = f"insertCustomer('{username}', '{name}', '{password}')"
        cursor.execute(sql)

    db.commit()

def insertSeller():
    S = 6
    for i in range(100):
        username = ''.join(random.choices(string.ascii_uppercase + string.digits, k = S)) 
        firstName = ''.join(random.choices(string.ascii_uppercase + string.digits, k = S)) 
        lastName = ''.join(random.choices(string.ascii_uppercase + string.digits, k = S - 2)) 
        password = ''.join(random.choices(string.ascii_uppercase + string.digits, k = S- 5)) 
        name = firstName + " " + lastName
        sql = f"insertMerchant('{username}','{name}','{password}')"
        cursor.execute(sql)

    db.commit()



        
        
if __name__ == '__main__':
    main()
    insertUser()
    insertSeller()

