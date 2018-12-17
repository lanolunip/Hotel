import os
import secrets
from PIL import Image 
from flask import render_template , flash, redirect, url_for, request
from Hotel import app, db, bcrypt
from Hotel.forms import RegistrationForm, LoginForm , UpdateAccountForm, Cart 
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
    if current_user.is_authenticated and current_user.tipeUser != 'Receptionist':
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

def save_picture(form_picture,width=125,height=125):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path,'static/profile_pics',picture_fn)

    output_size = (width,height)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@app.route('/account',methods=['GET','POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.nama       = form.nama.data
        current_user.email      = form.email.data
        current_user.phoneNumber= form.phoneNumber.data
        current_user.idLine     = form.idLine.data
        db.session.commit()
        flash('Your account has been updated!',category='success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.nama.data          = current_user.nama
        form.email.data         = current_user.email
        form.phoneNumber.data   = current_user.phoneNumber
        form.idLine.data        = current_user.idLine
    image_file = url_for('static',filename='profile_pics/' + current_user.image_file)
    return render_template('account.html',title='Account',image_file = image_file,form=form)

@app.route('/restaurant',methods=['GET','POST'])
def restaurant():
    return render_template('restaurant.html',title='Restaurant',Beverages=Beverage , Foods=Food)

@app.route('/laundry',methods=['GET','POST'])
def laundry():
    form = Cart()
    return render_template('laundry.html',title='Laundry',Laundry=Laundry,form=form)

@app.route('/room',methods=['GET','POST'])
@login_required
def room():
    if current_user.tipeUser == 'Receptionist':
        return render_template('roomReceptionist.html',title='Room')
    else:
        return redirect(url_for('home'))

@app.route('/roomTransaction')
@login_required
def roomReceptionist():
    if current_user.tipeUser == 'Guest':
        return render_template('room.html',title='Room Transaction')
    else:
        return redirect(url_for('home'))