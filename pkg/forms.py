from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField,TextAreaField,RadioField,SelectField
from wtforms.validators import DataRequired,Length,Email,EqualTo
class Login(FlaskForm):
  emailadd=StringField('Email Address',validators=[DataRequired()])
  password = PasswordField('Password',validators=[DataRequired(),Length(8,16)])
  submit= SubmitField('Submit')

class Profile(FlaskForm):
  fname=StringField('First Name',validators=[DataRequired()])
  lname=StringField('Last Name',validators=[DataRequired()])
  phone=StringField('Phone Number',validators=[DataRequired()])
  address = TextAreaField('Enter Your Address',validators=[DataRequired()])
  submit= SubmitField('Save')

class Signup(FlaskForm):
  fname=StringField('First Name',validators=[DataRequired()])
  lname=StringField('Last Name',validators=[DataRequired()])
  emailadd=StringField('Email Address',validators=[DataRequired()])
  phone=StringField('Phone Number',validators=[DataRequired()])
  password = PasswordField('Password',validators=[DataRequired(),Length(8,16),EqualTo('confirmpwd')])
  confirmpwd = PasswordField('Password',validators=[DataRequired(),Length(8,16),EqualTo('password')])
  address = TextAreaField('Enter Your Address',validators=[DataRequired()])
  submit= SubmitField('Sign Up')