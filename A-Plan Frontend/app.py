from flask import Flask, render_template, json, request,redirect, session
from flaskext.mysql import MySQL
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.secret_key = 'aplan'

mysql = MySQL()

#MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'aplan'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_PORT'] = 8889
mysql.init_app(app)


@app.route("/")
def main():
    return render_template('index.html')

@app.route("/aboutUs")
def aboutUS():
    return render_template('about_us.html')


@app.route('/signUp', methods = ['POST','GET'])
def signUp():
    try:
        if request.method == 'POST':
            _fname = request.form['inputFName']
            _lname = request.form['inputLName']
            _pwd   = request.form['inputpwd']
            _confirmPwd = request.form['confirmpwd']
            _email = request.form['inputEmail']
            _nnum = request.form['inputNnum']
            _major = request.form['inputMajor']

            #Figure out later
            # _hashedPwd = generate_password_hash(_pwd)

            if _fname and _lname and _email and _pwd and _confirmPwd and _nnum and _major:
                if _pwd != _confirmPwd:
                    return render_template('error.html', error = "Your password don't match")
                else:
                    conn = mysql.connect()
                    cursor = conn.cursor()
                    #using unhashed password (has a security issue)
                    cursor.callproc('aplanSignUp', (_fname, _lname, _pwd, _email, _nnum, _major))
                    data = cursor.fetchall()

                    if len(data) == 0:
                        conn.commit()
                        redirect('/login')
                    else:
                        return render_template('error.html', error = str(data[0]))

                    cursor.close()
                    conn.close()
            else:
                return render_template('error.html', error = "Enter the required field")
    except Exception as e:
        return render_template('error.html', error = str(data[0]))

    return render_template('signup.html')


@app.route('/login', methods = ['GET','POST'])
def login():
    try:
        if request.method == 'POST':
            _email = request.form['txt_email']
            _pwd = request.form['txt_pwd']

            #connect to mysql
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tbl_user WHERE email = %s", _email)
            data = cursor.fetchall()

            #check if input password and password in the db match
            if len(data) > 0:
                if _pwd == data[0][2]:
                    session['user'] = data[0][0]
                    return redirect('/dashboard')
                else:
                    return render_template('error.html', error = 'Wrong email address or password')
            else:
                return render_template('error.html', error = 'Wrong email address or password')

            cursor.close()
            conn.close()

        return render_template('login.html')
    except Exception as e:
        return render_template('error.html', error = str(e))

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')

@app.route('/dashboard')
def dashboard():
    if session.get('user'):
        _username = session['user']
        return render_template('dashboard.html', username = _username)
    else:
        return render_template('error', error = "unauthorized access")

if __name__ == "__main__":
    app.debug = True
    app.run(port=8080)

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

