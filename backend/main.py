import datetime
from flask import Flask, redirect

import './model/class.py'


app = Flask(__name__)


@app.route('/api/register', methods='POST')
def register():
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
    
    if request.method == 'POST':

        if ''' username exist ''':
            return "username already exist" , 400
        else if ''' email exist ''':
            return "email already exist" , 400

        if(request.form['isCustomer'] == True):
            new_user = User(request.form['username'], 
                            request.form['password'], 
                            request.form['email'], 
                            request.form['first_name'],
                            request.form['last_name'])
            # some sql line to save user to the database
        else:
            new_owner = Owner(request.form['username'], 
                            request.form['password'], 
                            request.form['email'], 
                            request.form['first_name'],
                            request.form['last_name'])
            # some sql line to save owner to the database
    else :
        return "Invalid request" , 400 


@app.route('/api/login', methods='POST')
def login():
    '''
        Login a user

        Login format:
            Username
            Password
        
    '''
    
    if request.method == 'POST':
        if ''' username not exist ''':
            return "username not exist" , 400
        else if ''' email not exist ''':

        user = None # some sql line to get user from the database
        if(request.form['password'] == user.password):
            return "login success" , 200
        else:
            return "wrong password" , 401
    else :
        return "Invalid request" , 400

        

