from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField , PasswordField, SubmitField, BooleanField, SelectField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, NumberRange, ValidationError
from Hotel.models import User

class RegistrationForm(FlaskForm):
    noKTP               = StringField('Nomor KTP', validators=[DataRequired(),Length(min=16,max=16)])
    nama                = StringField('Nama', validators=[DataRequired()])
    email               = StringField('Email',validators=[DataRequired(),Email()])
    tipeUser            = SelectField('Tipe User',choices=[('Guest','Guest'),('Receptionist','Receptionist')])
    password            = PasswordField('Password', validators=[DataRequired(),Length(min=6)])
    confirm_password    = PasswordField('Confirm Password', validators=[DataRequired(),EqualTo('password')])
    phoneNumber         = StringField('Nomor HP',validators=[DataRequired(),Length(min=10,max=12)])
    idLine              = StringField('ID LINE',validators=[DataRequired(),Length(min=6 ,max=20)])
    NIP                 = StringField('NIP (Khusus Receptionist Hotel)')
    submit              = SubmitField('Sign Up')

    def validate_noKTP(self,noKTP):

        user = User.query.filter_by(noKTP=noKTP.data).first()

        if user:
            raise ValidationError('User dengan Nomor KTP ini telah terdaftar')
    
    def validate_email(self,email):

        user = User.query.filter_by(email=email.data).first()

        if user:
            raise ValidationError('User dengan Email ini telah terdaftar')

    def validate_phoneNumber(self,phoneNumber):

        user = User.query.filter_by(phoneNumber=phoneNumber.data).first()

        if user:
            raise ValidationError('User dengan Nomor HP ini telah terdaftar')

    def validate_idLine(self,idLine):

        user = User.query.filter_by(idLine=idLine.data).first()

        if user:
            raise ValidationError('User dengan Nomor ID LINE ini telah terdaftar')

    # def validate_NIP(self,NIP):

    #     user = User.query.filter_by(NIP=NIP.data).first()

    #     if user:
    #         raise ValidationError('User dengan NIP ini telah terdaftar')

class LoginForm(FlaskForm):
    email               = StringField('Email',validators=[DataRequired(),Email()])
    password            = PasswordField('Password', validators=[DataRequired()])
    remember            = BooleanField('Remember Me')
    submit              = SubmitField('Login')
 
# class AddUserToARoom(FlaskForm):

class AddRoom(FlaskForm):
    number              = StringField('Room Number',validators=[DataRequired()])
    roomType            = SelectField('Tipe Ruangan',choices=['Executive','Reguler'],validators=[DataRequired()],coerce=str)
    doubleBed           = IntegerField('Jumlah Kasur',validators=[NumberRange(min=1)])
    singleBed           = IntegerField('Jumlah Kasur',validators=[NumberRange(min=1)])

class UpdateAccountForm(FlaskForm):
    nama                = StringField('Nama', validators=[DataRequired()])
    email               = StringField('Email',validators=[DataRequired(),Email()])
    picture             = FileField('Update Profile Picture',validators=[FileAllowed(['jpg','png'])])
    phoneNumber         = StringField('Nomor HP',validators=[DataRequired(),Length(min=10,max=12)])
    idLine              = StringField('ID LINE',validators=[DataRequired(),Length(min=6 ,max=20)])
    submit              = SubmitField('Update')
    
    def validate_email(self,email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()

            if user:
                raise ValidationError('User dengan Email ini telah terdaftar')
    
    def validate_nama(self,nama):
        if nama.data != current_user.nama:
            user = User.query.filter_by(nama=nama.data).first()

            if user:
                raise ValidationError('User dengan Email ini telah terdaftar')

    def validate_phoneNumber(self,phoneNumber):
        if phoneNumber.data != current_user.phoneNumber:    
            user = User.query.filter_by(phoneNumber=phoneNumber.data).first()

            if user:
                raise ValidationError('User dengan Nomor HP ini telah terdaftar')

    def validate_idLine(self,idLine):
        if idLine.data != current_user.idLine:
            user = User.query.filter_by(idLine=idLine.data).first()

            if user:
                raise ValidationError('User dengan Nomor ID LINE ini telah terdaftar')

class Cart(FlaskForm):
    totalBiaya          = IntegerField('Total Biaya')
    submit              = SubmitField('Submit')