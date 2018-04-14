# Author: Daryll Osis
# Date: April 13, 2018
# Description: A simple website that let the user add users with informations, edit users, 
#              and delete users, and show the information. This website shows a good practice 
#              of RESTful routes. 



from flask import Flask, redirect, render_template, request, flash, session
# import the function connectToMySQL from the file mysqlconnection.pycopy
from mysqlconnection import connectToMySQL
import re

app = Flask(__name__)
app.secret_key = 'denvernuggets'

# invoke the connectToMySQL function and pass it the name of the database we're using
# connectToMySQL returns an instance of MySQLConnection, which we will store in the variable 'mysql'
mysql = connectToMySQL('useraccount')
# now, we may invoke the query_db method

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

#ROOT route
@app.route('/')
def index(): 
    all_users = mysql.query_db("SELECT * FROM users")
    return render_template('index.html', users = all_users)


#POST route for CREATE
@app.route('/users/create', methods=['POST'])
def addNew():
    query_add = "INSERT INTO users (first_name, last_name, email) VALUES (%(first_name)s, %(last_name)s, %(email)s);"
    data = {
             'first_name': request.form['firstname'],
             'last_name':  request.form['lastname'],
             'email':  request.form['email']
           }
    mysql.query_db(query_add, data)

    return redirect('/')


#GET Route for NEW
@app.route('/users/new', methods=['GET'])
def newuserForm():
    return render_template('new.html')


#GET Route for EDIT
@app.route('/users/<id>/edit', methods=['GET'])
def editForm(id):
    users1 = mysql.query_db("SELECT * FROM users WHERE id = {}".format(id))
    return render_template('edit.html', users1 = users1)
    

#POST Route for EDIT
@app.route("/users/<id>", methods=['POST'])
def edit(id):
    query_edit = "UPDATE users SET first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s WHERE id = {}".format(id)
    data = {
        'first_name': request.form['firstname'],
        'last_name':  request.form['lastname'],
        'email':  request.form['email']
    }
    mysql.query_db(query_edit, data)
    
    return redirect('/')


#GET Route for DESTROY
@app.route('/users/<id>/destroy', methods=['GET'])
def destroy(id):
    user_destroy = "DELETE FROM users WHERE id = {}".format(id)
    mysql.query_db(user_destroy)
    
    return redirect('/')


#GET Route for VIEW user
@app.route('/users/<id>', methods=['GET'])   
def view(id):
    user = mysql.query_db("SELECT * FROM users WHERE id = {}".format(id))
    return render_template('view.html', user = user)


if __name__ == "__main__":
    app.run(debug=True)