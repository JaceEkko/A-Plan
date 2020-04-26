from flask import Flask, render_template, flash, redirect, url_for, session,logging, request, send_from_directory, send_file
from flaskext.mysql import MySQL
#from flask_wtf import Form, StringField, TestAreaField, PasswordField, validators
from wtforms import Form, StringField, BooleanField, validators, PasswordField, IntegerField, DateField, TextField, SubmitField
from wtforms.validators import DataRequired, Email, Regexp, EqualTo
from passlib.hash import sha256_crypt
from flask import request
import mysql.connector
import pymysql.cursors
from functools import wraps
from datetime import datetime
from flask_wtf.file import FileField, FileAllowed, FileRequired
from werkzeug import secure_filename
from flask_sqlalchemy import SQLAlchemy
import os
import time
from datetime import datetime, timedelta
from flask_login import LoginManager, login_user, login_required, current_user
from flask_login import logout_user



app = Flask(__name__)
# Config mysql
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'A-PLAN'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 300
# init MySQL
mysql = MySQL(app)

#Initialize the app for use with this MySQL class
mysql.init_app(app)


login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

# Check the loggin status of the user
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login ', 'danger')
            return redirect(url_for('login'))
    return wrap


@app.route("/")
def main():
    return render_template('index.html')

@app.route("/aboutUs")
def aboutUS():
    return render_template('about_us.html')

@app.after_request
def add_header(response):
    response.cache_control.max_age = 300
    response.cache_control.public = True
    return response


## THE REGISTER FROM 
class RegisterForm(Form):
    ## This should match all var names in register.html
    NYU_ID = StringField('Net ID', [validators.Length(min=4, max=25),validators.DataRequired(), validators.Regexp('^\w+$', message="Net ID must contain only letters and numbers!")])
    First_Name = StringField('First Name', [validators.Length(min=1, max=50),validators.DataRequired(), Regexp('[A-Za-z]*$', 0, 'Only letters Please')])
    Last_Name = StringField('Last Name', [validators.Length(min=1, max=50), validators.DataRequired(), Regexp('[A-Za-z]*$', 0, 'Only letters Please')])
    #^(?=^.{8,}$)(?=.*\d)(?=.*\W+)(?=.*[a-z])(?=.*[A-Z])(?i-msnx:(?!.*pass|.*password|.*word|.*god|.*\s))(?!^.*\n).*$
    Major = StringField('Major', [validators.Length(min=1, max=30), validators.DataRequired(), Regexp('[A-Za-z ]*$',0, 'Only letters Please')])
    N_ID = StringField('N_ID', [validators.Length(min=8, max=9), validators.DataRequired(), Regexp('[0-9]',0, 'Only Numbers Please')])

    Password = PasswordField('Password',[
      validators.DataRequired(),
      validators.EqualTo('confirm', message='Password do not match'),
      # (?-i)(?=^.{8,}$)((?!.*\s)(?=.*[A-Z])(?=.*[a-z]))((?=(.*\d){1,})|(?=(.*\W){1,}))^.*$
      # ^(?=.*[a-z])(?=.*[A-Z])(?=.*\d.*)(?=.*\W.*)[a-zA-Z0-9\S]{8,15}$
      # ^(?=.*[a-z])(?=.*[A-Z]) Pa$sw0rd
      Regexp('^(?=.*[a-z])(?=.*[A-Z])(?=.*\d.*)(?=.*\W.*)[a-zA-Z0-9\S]{8,15}$', 0,'Must contain at least 1 digit. Must contain at least 1 lower case letter. Must contain at least 1 Upper case letter. Must contain at least 1 non-character (such as !,#,%,@, etc).')
    ])
    confirm = PasswordField('Confirm Password',[validators.DataRequired(), Regexp('^(?=.*[a-z])(?=.*[A-Z])(?=.*\d.*)(?=.*\W.*)[a-zA-Z0-9\S]{8,15}$', 0,'Must contain at least 1 digit. Must contain at least 1 lower case letter. Must contain at least 1 upper case letter. Must contain at least 1 non-character (such as !,#,%,@, etc).')])

## The Password Reset Form
class PasswordResetForm(Form):
    New_password = PasswordField('new_Password',
        [validators.DataRequired(), 
        validators.Length(min=8, max=20), Regexp('^(?=.*[a-z])(?=.*[A-Z])(?=.*\d.*)(?=.*\W.*)[a-zA-Z0-9\S]{8,15}$', 0,'Must contain at least 1 digit. Must contain at least 1 lower case letter. Must contain at least 1 Upper case letter. Must contain at least 1 non-character (such as !,#,%,@, etc).') ])
    Confirm_New_Password = PasswordField('confirm_Password', validators=[DataRequired(),
        EqualTo('new_Password'), Regexp('^(?=.*[a-z])(?=.*[A-Z])(?=.*\d.*)(?=.*\W.*)[a-zA-Z0-9\S]{8,15}$', 0,'Must contain at least 1 digit. Must contain at least 1 lower case letter. Must contain at least 1 Upper case letter. Must contain at least 1 non-character (such as !,#,%,@, etc).')])
    Submit_new_password = SubmitField('Requst Password Reset')

### Request password reset form
class ResetPasswordRequestForm(Form):
    Current_email = StringField('Net ID', validators=[DataRequired(), Email()])
    submit_request = SubmitField('Request Password Reset')

class LoginForm(Form):
    student_net_ID = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')



@app.route('/signUp', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    print('Hello')
    #print( form )
    #print ( m )
    if request.method == 'POST'and form.validate():
        MY_NYU_ID = form.NYU_ID.data
        MY_NYU_ID += "@nyu.edu"
        FirstName = form.First_Name.data
        LastName = form.Last_Name.data
        MY_Major = form.Major.data
        MY_N_ID = form.N_ID.data
        MY_Password = sha256_crypt.encrypt(str(form.Password.data))
        
        connection = pymysql.connect("localhost", "root", "", "A-PLAN")
        cursor = connection.cursor();
        #cur = mysql.connection.connect()
        #cur = mysql.get_db().cursor()
        print("Hello World")
        #usernameOne = request.form['username']
        query = 'SELECT NYU_Net_ID FROM Student WHERE NYU_Net_ID = %s'
        cursor.execute(query, (MY_NYU_ID))
        #stores the restuls in a variable

        data = cursor.fetchone()
        #use fetchall() if you are expecting more than 1 data
        error = None
        #the_username = data.values()

        if(data):
            #if the previous query returns data, then a user exist with that user name
            error = ("Net ID already exisit ! Please try again !")
            return render_template('signup.html', error = error, form=form)

        
        try:
            with connection.cursor() as cursor:

                #cursor.execute("INSERT INTO Person(username, password, fname, lname, avatar, bio, isPrivate) VALUES (%s, %s, %s, %s, %s, %s, %s)",(username, password, FirstName, LastName, AvatarName, BioName, five ))
                cursor.execute("INSERT INTO Student(NYU_Net_ID, First_name, Last_name, Major, N_ID, Password) VALUES (%s, %s, %s, %s, %s,%s)", (MY_NYU_ID, FirstName, LastName, MY_Major, MY_N_ID, MY_Password))
            connection.commit()
            #print(m)
        finally:
            connection.close()
        #excute query
        #cursor.execute("INSERT INTO users(name, email, username, password) VALUES (%s, %s, %s, %s)",(name, email, username, password))

        # Commit to Database
        #connection.commit()

        # Close connection
        #cursor.close()

        flash('You are now registered to A-PLAN and can log in', 'success')

        return redirect(url_for('login'))

        #return render_template('register.html')

    return render_template('signup.html', form=form)


#User login
@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        #form = LoginForm(request.form)
        # Get the fields of the form
        net_username = request.form['student_net_ID']
        password_candidate = request.form['password']

        ## Create a cursor
        connection = pymysql.connect("localhost", "root", "", "A-PLAN")
        cursor = connection.cursor(pymysql.cursors.DictCursor);
        #cur = connection.cursor(dictionary=True);

        ## Get the name of the user
        result = cursor.execute("SELECT * FROM Student WHERE NYU_Net_ID = %s", [net_username])

        if result > 0:
            # Get the stored hash value
            data = cursor.fetchone()
            password = data['Password']
            student_name = data['First_Name']
            # Compare Passwords
            if sha256_crypt.verify(password_candidate, password):
                # if the passwords Pass
                session['logged_in'] = True
                session['student_net_ID'] = net_username
                session['student'] = student_name
                #login_user(session['student_net_ID'])
                #login_user(session['student_net_ID'])
                #user_obj = User(data['NYU_Net_ID'])
                
                #mysql.filter
                #login_user(form.student_net_ID.data)
                flash('You are now logged in', 'success')
                return redirect(url_for('dashboard'))
            else:
                error = "Invalid login"
                return render_template('login.html',  error=error)
            connection.close()
        else:
            error = "Username is not found "
            return render_template('login.html',  error=error)
    return render_template('login.html')

## CLEAR THE USER SESSION AND SENDS THE USER A MESSAGE THAT THE LOG OUT WAS SUCCESSFUL.
@app.route('/logout')
@is_logged_in
def logout():
    if(session['logged_in'] == True ):
        session['logged_in'] = False
    flash('You are now logged out','success')
    session.clear()
    #session.pop('NYU_Net_ID',None)
    logout_user()
    return redirect(url_for('login'))

@app.route('/dashboard', methods= ['GET'])
@is_logged_in
def dashboard():
    #session['logged_in'] = False
    print(session['student'])
    print session['logged_in']
    #print(m)
    if(session['logged_in'] == False ):
        print "Hello"
        #flash('You need to log in first', 'danger')
        return redirect(url_for('login'))
    #print session['student_net_ID']
    return render_template("dashboard.html", name=session['student'])

if __name__=='__main__':

    app.secret_key='secretadmin'
    app.run(debug=True)

'''
DELIMITER;
CREATE DEFINER=`root`@`localhost` PROCEDURE `aplanSignUp`( 
    IN p_fname VARCHAR(20), 
    IN p_lname VARCHAR(20), 
    IN p_email VARCHAR(20), 
    IN p_password VARCHAR(150) 
    ) 
BEGIN if ( select exists (select 1 from tbl_user where email = p_email) ) THEN select 'Username Exists !!'; 
    ELSE insert into tbl_user 
        ( f_name, l_name, password, email ) 
    values 
        ( p_fname, p_lname, p_password, p_email ); 
    END IF; 
END$$
DELIMITER;
'''

'''
DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `aplanValidateLogin`(
IN p_email VARCHAR(20)
)
BEGIN
    select * from tbl_user where email = p_email;
END$$
DELIMITER ;
'''

