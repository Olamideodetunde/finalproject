import datetime
from pkg import db


class State(db.Model): 
    __tablename__='state'
    state_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    state_name = db.Column(db.String(255), nullable=False)

class Gender(db.Model): 
    __tablename__='gender'
    gender_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    gender_name = db.Column(db.String(255), nullable=False)
  
class Service(db.Model): 
    __tablename__='service'
    service_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    service_name = db.Column(db.String(255), nullable=False)

class Provider(db.Model): 
    __tablename__='provider_services'
    provider_service_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    sp_id = db.Column(db.Integer(),db.ForeignKey('service_providers.sp_id'))
    service_id = db.Column(db.Integer(),db.ForeignKey('service.service_id'))
    spdeets=db.relationship('Sp',backref='provserv')
    servicedeets=db.relationship('Service',backref='provserv')
class User(db.Model): 
    __tablename__='user'
    user_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    user_email = db.Column(db.String(255), nullable=False)
    user_password = db.Column(db.String(255), nullable=False)
    user_fname = db.Column(db.String(255), nullable=False)
    user_lname = db.Column(db.String(255), nullable=False)
    user_state = db.Column(db.Integer(),db.ForeignKey('state.state_id'))
    user_address = db.Column(db.String(255), nullable=True)
    user_gender = db.Column(db.Integer(),db.ForeignKey('gender.gender_id'), nullable=False)
    user_phone = db.Column(db.String(100), nullable=True)
    user_reg = db.Column(db.DateTime(), default=datetime.datetime.utcnow())
    statedeets=db.relationship('State',backref='users')
    genderdeets=db.relationship('Gender',backref='users')
class Subscription(db.Model):
    __tablename__='subscription' 
    subscription_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    sp_id = db.Column(db.Integer(),db.ForeignKey('service_providers.sp_id'))
    subscription_amount = db.Column(db.Float(), nullable=False)
    subscription_date = db.Column(db.DateTime(), default=datetime.datetime.utcnow())
    date_of_expiry = db.Column(db.DateTime(), default=datetime.datetime.utcnow())
    subscription_discount = db.Column(db.Float(), nullable=False)
    spdeets=db.relationship('Sp',backref='subscribe')
class Payment(db.Model):
    __tablename__='payment' 
    payment_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    subscription_id = db.Column(db.Integer(),db.ForeignKey('subscription.subscription_id'))
    sp_id = db.Column(db.Integer(),db.ForeignKey('service_providers.sp_id'))
    amt_paid = db.Column(db.Float(), nullable=False)
    date_paid = db.Column(db.DateTime(), default=datetime.datetime.utcnow())
    spdeets=db.relationship('Sp',backref='payment')

class Sp(db.Model):
    __tablename__='service_providers' 
    sp_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    sp_email = db.Column(db.String(255), nullable=False)
    sp_password = db.Column(db.String(255), nullable=False)
    sp_fname = db.Column(db.String(255), nullable=False)
    sp_lname = db.Column(db.String(255), nullable=False)
    sp_location = db.Column(db.Integer(),db.ForeignKey('state.state_id'), nullable=True)
    sp_phone = db.Column(db.String(100), nullable=True)
    sp_services = db.Column(db.Integer(),db.ForeignKey('service.service_id'), nullable=True)
    sp_address=db.Column(db.String(255),nullable=False)
    sp_gender = db.Column(db.Integer(),db.ForeignKey('gender.gender_id'), nullable=False)
    sp_reg = db.Column(db.DateTime(), default=datetime.datetime.utcnow())
    statedeets=db.relationship('State',backref='sp')
    genderdeets=db.relationship('Gender',backref='sp')