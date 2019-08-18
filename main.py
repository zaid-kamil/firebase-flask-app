from flask import Flask,render_template,request,redirect,flash,session
import firebase_admin
import userManager,dbManager
from firebase_admin import credentials

try:
    cred = credentials.Certificate('serviceAccountKey.json')
    firebase_admin.initialize_app(cred)
except Exception as e:
    print(e)

app = Flask(__name__)
app.secret_key = "ooga booga"

@app.route('/',methods=['POST','GET'])
def start():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        if email and password:
            user = userManager.verify_user(email,password)
            
            session['is_logged'] = True
            session['user_id'] = user.uid
            session['name'] = user.display_name
            session['email'] = user.email

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
                user = userManager.register_user(email,phone,password,name)
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


@app.route('/home',methods=['POST','GET'])
def home():
    if not session.get('is_logged'):
        return redirect('/')
    #save data
    if request.method == 'POST':
        pname = request.form.get('pname')
        pprice = request.form.get('pprice')
        pqty = request.form.get('pqty')
        if pname and pprice and pqty:
            data={'name':pname,'price':pprice,'qty':pqty}
            if dbManager.add_product_to_cloud(data=data):
                flash("data sucessfully added", 'success')
                return redirect("/home")
            else:
                flash("data could not be added", "danger")
        else:
            flash("please fill all details", "danger")
    # load data
    data = dbManager.get_product_from_cloud()
    return render_template('data.html',data=list(data))

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')



if __name__ == '__main__':
    app.run(debug=True)