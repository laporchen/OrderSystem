import pymysql


db_settings = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "12345678",
    "charset": "utf8"
}

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
        global db
        cursor.execute("CREATE DATABASE OrderSystem")
        db.commit()
    except Exception as e:
        print(e)

def source():
    try:
        global cursor
        global db
        sqls = parse_sql("./DDL.sql")
        for sql in sqls:
            cursor.execute(sql)
        sqls = parse_sql("./procedure.sql")
        for sql in sqls:
            cursor.execute(sql)
    except Exception as e:
        print(e)

def use():
    try:
        global cursor
        global db
        cursor.execute("USE OrderSystem")
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
            stmt += line
            stmts.append(stmt.strip())
            stmt = ''
        else:
            stmts.append(line.strip())
    return stmts

if __name__ == '__main__':
    connect()
    create()
    use()
    source()
    global db
    db.commit()
    print("DONE.")
