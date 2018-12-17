from datetime import datetime
from Hotel import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_noKTP):
    return User.query.get(int(user_noKTP))

class User(db.Model,UserMixin):
    noKTP                   = db.Column(db.String(16),unique=True, primary_key=True)
    nama                    = db.Column(db.String(120),nullable=False)
    tipeUser                = db.Column(db.String(12),nullable=False)
    email                   = db.Column(db.String(120),unique=True, nullable=False)
    phoneNumber             = db.Column(db.String(12),unique=True, nullable=False)
    idLine                  = db.Column(db.String(20),unique=True, nullable=False)
    image_file              = db.Column(db.String(20),nullable=False, default='default.jpg')
    password                = db.Column(db.String(60),nullable=False)
    NIP                     = db.Column(db.String(20))
    saldo                   = db.Column(db.Integer, nullable=False, default=0)
    # posts       = db.relationship('Post',backref='author',lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

    def get_id(self):
        return self.noKTP
    
# class Post(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(100), nullable=False)
#     date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
#     content = db.Column(db.Text,nullable=False)
#     user_id = db.Column(db.Integer , db.ForeignKey('user.id'), nullable=False)

#     def __repr__(self):
#         return f"Post('{self.title}', '{self.date_posted}', '{self.content}')"
    
class Room(db.Model):
    id          = db.Column(db.Integer, unique = True ,primary_key=True)
    number      = db.Column(db.String(4), nullable = False)
    doubleBed   = db.Column(db.Integer, nullable = False)
    singleBed   = db.Column(db.Integer, nullable = False)
    price       = db.Column(db.Integer, nullable = False)
    guest       = db.Column(db.String(16), db.ForeignKey('user.noKTP'))
    roomIsUsed  = db.Column(db.Boolean, nullable = False)
    status      = db.Column(db.Text, nullable = True)

    def __repr__(self):
        return f"Room('{self.number}', '{self.doubleBed}', '{self.singleBed}', '{self.guest}', '{self.roomIsUsed}')"

class restaurantTransaction(db.Model):
    id          = db.Column(db.Integer, primary_key = True)
    noKTP       = db.Column(db.String(16),db.ForeignKey('user.noKTP'))
    time        = db.Column(db.DateTime, nullable = False)
    totalPrice  = db.Column(db.Integer , nullable = False)

    def __repr__(self):
        return f"restaurantTransaction('{self.time}', '{self.totalPrice}')"

class roomTransaction(db.Model):
    id          = db.Column(db.Integer, primary_key = True,nullable=False)
    noKTP       = db.Column(db.String(16),db.ForeignKey('user.noKTP'))
    checkIn     = db.Column(db.DateTime,nullable = False,default = datetime.utcnow)
    checkOut    = db.Column(db.DateTime,nullable = False,default = datetime.utcnow)
    extraBed    = db.Column(db.Integer,nullable = False)
    roomPrice   = db.Column(db.ForeignKey('room.price'),nullable = False)

    def __repr__(self):
        return f"roomTransaction('{self.id}', '{self.checkIn}', '{self.checkOut}', '{self.extraBed}','{self.roomPrice}')"

class Food(db.Model):
    id          = db.Column(db.String(10), primary_key=True, nullable=False)
    name        = db.Column(db.String(30), nullable = False)
    price       = db.Column(db.Integer, nullable = False)

    def __repr__(self):
        return f"Food('{self.id}', '{self.name}', '{self.price}')"

class Beverage(db.Model):
    id          = db.Column(db.String(10), primary_key=True, nullable=False)
    name        = db.Column(db.String(30), nullable = False)
    price       = db.Column(db.Integer, nullable = False)

    def __repr__(self):
        return f"Beverage('{self.id}', '{self.name}', '{self.price}')"

class Laundry(db.Model):
    id          = db.Column(db.String(10), primary_key=True, nullable=False)
    name        = db.Column(db.String(30), nullable = False)
    price       = db.Column(db.Integer, nullable = False)

    def __repr__(self):
        return f"Beverage('{self.id}', '{self.baju}', '{self.celana}','{self.jaket}','{self.pakaianDalam}','{self.softener}','{self.perfume}','{self.dateIn}','{self.dateOut}')"