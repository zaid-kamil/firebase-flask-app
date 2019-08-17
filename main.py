from flask import Flask,render_template,request,redirect,flash,session
import firebase_admin
import adduser
from firebase_admin import credentials

app = Flask(__name__)
app.secret_key = "ooga booga"

@app.route('/',methods=['POST','GET'])
def start():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        if email and password:
            user = adduser.verify_user(email,password)
            
            session['is_logged'] = True
            session['user_id'] = user.get('uid')
            session['name'] = user.get('display_name')
            session['email'] = user.get('email')

            return redirect('/home')
        else:
            flash("could not find user details! try again")

    return render_template('login.html')

@app.route('/register',methods=['POST','GET'])
def register():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        name = request.form.get('name')
        phone = request.form.get('phone')
        if email and password and name and phone:
            if len(password) > 5:
                user = adduser.register_user(email,phone,password,name)
                if user:
                    flash("registered successfully",'success')
                    return redirect('/')
                else:
                    flash("something bad happened, check console or cry","danger")
            else:
                flash("password is invalid, should be greater than 5","danger")
        else:
            flash("invalid details",'danger')
    return render_template('register.html')


@app.route('/home')
def home():
    if not session.get('is_logged'):
        return redirect('/')
    return render_template('data.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')



if __name__ == '__main__':
    app.run(debug=True)