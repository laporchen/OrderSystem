import pymysql


db_settings = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "12345678",
    "charset": "utf8"
}
db_name = "team18"

def connect():
    try:
        global cursor 
        global db
        db = pymysql.connect(**db_settings)
        cursor = db.cursor()
    except Exception as e:
        print(e)

def create():
    try:
        global cursor
        global db_name
        global db
        cursor.execute(f"CREATE DATABASE {db_name}")
    except Exception as e:
        print(e)

def source(file):
    try:
        global cursor
        sqls = parse_sql(file)
        for sql in sqls:
            cursor.execute(sql)
        print(f"Script {file} is loaded")
    except Exception as e:
        print(e)

def use():
    try:
        global cursor
        global db_name
        global db
        cursor.execute(f"USE {db_name}")
    except Exception as e:
        print(e)

def parse_sql(filename):
    data = open(filename, 'r').readlines()
    stmts = []
    DELIMITER = ';'
    stmt = ''

    for lineno, line in enumerate(data):
        if not line.strip():
            continue

        if line.startswith('--'):
            continue

        if 'DELIMITER' in line:
            DELIMITER = line.split()[1]
            continue

        if (DELIMITER not in line):
            stmt += line.replace(DELIMITER, ';')
            continue

        if stmt:
            stmt += line.replace(DELIMITER,';')
            stmts.append(stmt.strip())
            stmt = ''
        else:
            stmts.append(line.strip())
    return stmts

if __name__ == '__main__':
    connect()
    create()
    use()
    source("./DDL.sql")
    source("./procedure.sql")
    global db
    db.commit()
    print("DONE.")
