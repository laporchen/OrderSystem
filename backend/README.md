# Backend

## Implement with flask in python

### Package installation
```
pip3 install flask flask_jwt_extended flask_cors pymysql
```
### Project Setup

0. Create a jwtKey
1. Create a file named 'jwtJey.json' in the data folder
2. Paste the key you created into the file
```json
{
    "key": "THIS-IS-YOUR-JWT-KEY"
}

Database setting
Change the db_setting in mode/sql.py to your mysql server setting.
```
3. Run the script 
```
sh runFlask.sh
```
