import datetime

from model import *

from flask import Flask, redirect, request


app = Flask(__name__)


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
    user = User(request.values.get('username'), request.values.get('password'), request.values.get(
        'first_name'), request.values.get('last_name'), request.values.get('phone_number'), request.values.get('email'))
    if request.method == 'POST':

        if user.username is None:
            return "username already exist", 400
        elif user.email == None:
            return "email already exist", 400

        if(request.form['isCustomer'] == True):
            new_user = user
            # some sql line to save user to the database
        else:
            new_owner = user
            # some sql line to save owner to the database
    else:
        return "Invalid request", 400
    return "", 200


@app.route('/api/login', methods=['POST'])
def login():
    '''
        Login a user

        Login format:
            Username
            Password

    '''
    '''
    if request.method == 'POST':
        if username not exist:
            return "username not exist", 400
        else if email not exist:

        user = None  # some sql line to get user from the database
        if(request.form['password'] == user.password):
            return "login success", 200
        else:
            return "wrong password", 401
    else:
        return "Invalid request", 400
        '''
    return "", 200


if __name__ == '__main__':
    app.run(debug=True)
