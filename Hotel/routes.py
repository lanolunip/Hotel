from flask import render_template , flash, redirect, url_for, request
from Hotel import app, db, bcrypt
from Hotel.forms import RegistrationForm, LoginForm 
from Hotel.models import User,Beverage,Food,Laundry,Room,roomTransaction,restaurantTransaction
from flask_login import login_user, current_user, logout_user, login_required

author = {
    'name'      :   'Michael',
    'age'       :   '19',
    'address'   :   'Kanser.11'

}

@app.route('/')
def home():
    return render_template('home.html',author=author,title='HOME')

@app.route('/about')
def about():
    return render_template('about.html',title="About")

@app.route('/1')
def makudonarudo():
    return render_template('layout1.html')

@app.route('/register', methods=['GET','POST'])
@login_required
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(noKTP=form.noKTP.data, nama=form.nama.data, email=form.email.data, password=hashed_password,tipeUser=form.tipeUser.data,phoneNumber=form.phoneNumber.data,idLine=form.idLine.data,NIP=form.NIP.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.nama.data}!','success')
        return redirect(url_for('login'))
    return render_template('register.html',title="Register", form=form)

@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user,remember=form.remember.data)
            next_page = request.args.get('next')
            flash('Login Successful!','success')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password','danger')
    return render_template('login.html',title="Login", form=form)
    
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/account')
@login_required
def account():
    return render_template('account.html',title='Account')