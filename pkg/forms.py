from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField,TextAreaField,FileField
from wtforms.validators import DataRequired,Length,Email,EqualTo
class Login(FlaskForm):
  emailadd=StringField('Email Address',validators=[DataRequired(),Email()])
  password = PasswordField('Password',validators=[DataRequired(),Length(8,16)])
  submit= SubmitField('Login')
class SeviceForm(FlaskForm):
  service_name=StringField('Service Name')
  submit= SubmitField('Submit')

class PriceForm(FlaskForm):
  sub_amount=StringField('Subscription Amount')
  submit= SubmitField('Submit')

class AdminForm(FlaskForm):
  emailadd=StringField('Email Address',validators=[DataRequired(),Email()])
  password = PasswordField('Password',validators=[DataRequired(),Length(8,16)])
  submit= SubmitField('Submit')

class Profile(FlaskForm):
  fname=StringField('First Name',validators=[DataRequired()])
  image=FileField('Profile Image',validators=[DataRequired()])
  lname=StringField('Last Name',validators=[DataRequired()])
  phone=StringField('Phone Number',validators=[DataRequired()])
  address = TextAreaField('Enter Your Address',validators=[DataRequired()])
  summary = TextAreaField('Enter Your Address',validators=[DataRequired(),Length(55,255)])
  submit= SubmitField('Save')
class MessageForm(FlaskForm):
  title=StringField('First Name',validators=[DataRequired()])
  message = TextAreaField('Enter Your Address',validators=[DataRequired()])
  submit= SubmitField('Send')

class ReviewForm(FlaskForm):
  user_name=StringField('First Name',validators=[DataRequired()])
  review = TextAreaField('Enter Your Address',validators=[DataRequired()])
  submit= SubmitField('Send')

class Reply(FlaskForm):
  reply_content = TextAreaField('Enter Your Reply',validators=[DataRequired()])
  submit= SubmitField('Send')

class Signup(FlaskForm):
  fname=StringField('First Name',validators=[DataRequired()])
  lname=StringField('Last Name',validators=[DataRequired()])
  emailadd=StringField('Email Address',validators=[DataRequired(),Email()])
  phone=StringField('Phone Number',validators=[DataRequired()])
  password = PasswordField('Password',validators=[DataRequired(),Length(8,16),EqualTo('confirmpwd')])
  confirmpwd = PasswordField('Password',validators=[DataRequired(),Length(8,16),EqualTo('password')])
  address = TextAreaField('Enter Your Address',validators=[DataRequired()])
  submit= SubmitField('Sign Up')