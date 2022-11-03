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
class Admin(db.Model): 
    __tablename__='admin'
    admin_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    admin_email = db.Column(db.String(255), nullable=False)
    admin_password = db.Column(db.String(255), nullable=False)
class Transaction(db.Model):
    trx_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    trx_user = db.Column(db.Integer(),db.ForeignKey('service_providers.sp_id'), nullable=False)
    trx_refno= db.Column(db.String(255), nullable=True)
    trx_totalamt = db.Column(db.Integer(),db.ForeignKey('subscription.subscription_id'), nullable=True)
    trx_status = db.Column(db.Enum('pending','paid','failed'), nullable=True)
    trx_method=db.Column(db.Enum('card','cash'), nullable=True)
    trx_paygate=db.Column(db.Text(), nullable=True)
    trx_date=db.Column(db.DateTime(), default=datetime.datetime.utcnow())
    trx_expiry=db.Column(db.DateTime())
    user_whopaid=db.relationship('Sp',backref='mytrxs')
    amount_paid=db.relationship('Subscription',backref='trx_made')
class Subscription(db.Model):
    __tablename__='subscription' 
    subscription_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    subscription_amount = db.Column(db.Float(), nullable=False)
class Payment(db.Model):
    __tablename__='payment' 
    payment_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    subscription_id = db.Column(db.Integer(),db.ForeignKey('subscription.subscription_id'))
    sp_id = db.Column(db.Integer(),db.ForeignKey('service_providers.sp_id'))
    pay_trxid= db.Column(db.Integer(),db.ForeignKey('transaction.trx_id'))
    spdeets=db.relationship('Sp',backref='payment')
    subdeets=db.relationship('Subscription',backref='paymentdeets')
    trxdeets=db.relationship('Transaction',backref='payment')

class Review(db.Model): 
    review_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    review_content = db.Column(db.String(255), nullable=False)
    review_by = db.Column(db.String(255), nullable=False)
    review_for = db.Column(db.Integer(),db.ForeignKey('service_providers.sp_id'), nullable=False)
    review_date=db.Column(db.DateTime(), default=datetime.datetime.utcnow())
    sp_deets=db.relationship('Sp',backref='reviewme')
    reply_status= db.Column(db.Enum('True','False'), nullable=True)
class Spreply(db.Model): 
    reply_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    reply_content = db.Column(db.String(255), nullable=False)
    reply_by = db.Column(db.Integer(),db.ForeignKey('service_providers.sp_id'), nullable=False)
    reply_for= db.Column(db.Integer(),db.ForeignKey('review.review_id'), nullable=False)
    reply_date=db.Column(db.DateTime(), default=datetime.datetime.utcnow())
    sp=db.relationship('Sp',backref='reply')
    reviewdeets=db.relationship('Review',backref='reply')
class Sp(db.Model):
    __tablename__='service_providers' 
    sp_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    sp_email = db.Column(db.String(255), nullable=False)
    sp_password = db.Column(db.String(255), nullable=False)
    sp_fname = db.Column(db.String(255), nullable=False)
    sp_lname = db.Column(db.String(255), nullable=False)
    sp_summary = db.Column(db.String(255), nullable=True)
    sp_image = db.Column(db.String(255), nullable=True)
    sp_location = db.Column(db.Integer(),db.ForeignKey('state.state_id'), nullable=False)
    sp_phone = db.Column(db.String(100), nullable=True)
    sp_services = db.Column(db.Integer(),db.ForeignKey('service.service_id'), nullable=True)
    sp_address=db.Column(db.String(255),nullable=False)
    sp_gender = db.Column(db.Integer(),db.ForeignKey('gender.gender_id'), nullable=False)
    sp_reg = db.Column(db.DateTime(), default=datetime.datetime.utcnow())
    servicedeets=db.relationship('Service',backref='spserv')
    statedeets=db.relationship('State',backref='spstate')
    genderdeets=db.relationship('Gender',backref='spgender')
class Homesearch(db.Model): 
    search_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    search_state=db.Column(db.Integer(), nullable=True)
    search_service=db.Column(db.Integer(), nullable=True)
class Spmessage(db.Model):
    __tablename__='message' 
    message_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    message_content = db.Column(db.String(255), nullable=False)
    message_title=db.Column(db.String(255),nullable=False)
    message_by = db.Column(db.Integer(),db.ForeignKey('service_providers.sp_id'), nullable=False)
    message_date=db.Column(db.DateTime(), default=datetime.datetime.utcnow())
    userdeets=db.relationship('Sp',backref='comments')