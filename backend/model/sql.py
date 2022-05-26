import pymysql


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
