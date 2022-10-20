from flask import render_template,request,redirect,url_for,flash,session
from werkzeug.security import check_password_hash,generate_password_hash
from pkg.mymodels import Sp,State
from pkg import hireapp,db
from pkg.forms import Signup,Login,Profile
@hireapp.route('/')
def home_page():
  return render_template('user/hire.html')
@hireapp.route('/profile')
def profile_page():
  return render_template('user/profx.html')
@hireapp.route('/form',methods=['GET','POST'])
def form_page():
  form=Login()
  if request.method =='GET':
    return render_template('user/form.html',form=form)
  else:
    emailadd=form.emailadd.data
    passwd=form.password.data
    records=db.session.query(Sp).filter(Sp.sp_email==emailadd).first()
    if records and check_password_hash(records.sp_password,passwd):
      session['loggedin']=records.sp_id
      return redirect(url_for('sp_dashboard'))
    else:
      flash('Wrong Credentials')
      return redirect(url_for('form_page'))
@hireapp.route('/signup',methods=['GET','POST'])
def signup_page():
  y=Signup()
  state=State.query.all()
  if request.method == 'GET':
    return render_template('user/signup.html',y=y,state=state)
  else:
    fname=y.fname.data
    lname=y.lname.data
    emailadd=y.emailadd.data
    phone=y.phone.data
    pwd=generate_password_hash(y.password.data)
    addresss=y.address.data
    gender=request.form.get('gender')
    location=request.form.get('state')
    b=Sp(sp_email=emailadd,sp_password=pwd,sp_fname=fname,sp_lname=lname,sp_location=location,sp_phone=phone,sp_address=addresss,sp_gender=gender)
    db.session.add(b)
    db.session.commit()
    return redirect(url_for('form_page'))
@hireapp.route('/sp_payment')
def sp_payment():
  if session.get('loggedin') != None:
    return render_template('service_providers/payment.html')
  else:
    return redirect(url_for('form_page'))
@hireapp.route('/sp_subscription')
def sp_subscription():
  if session.get('loggedin')!=None:
    return render_template('service_providers/subscription.html')
  else:
    return redirect(url_for('form_page'))
@hireapp.route('/sp_dashboard')
def sp_dashboard():
  loggedin=session.get('loggedin')
  if loggedin != None:
    records=db.session.query(Sp).filter(Sp.sp_id==loggedin).first()
    name=records.sp_fname
    emailx=records.sp_email
    return render_template('service_providers/sp_dashboard.html',emailx=emailx,name=name)
  else:
    return redirect(url_for('form_page'))
@hireapp.route('/sp_message')
def sp_message():
  if session.get('loggedin')!=None:
    return render_template('service_providers/message.html')
  else:
    return redirect(url_for('form_page'))
@hireapp.route('/sp_faq')
def sp_faq():
  if session.get('loggedin')!=None:
    return render_template('service_providers/faq.html')
  else:
    return redirect(url_for('form_page'))
@hireapp.route('/sp_profile')
def sp_profile():
  b=Profile()
  if session.get('loggedin')!=None:
    records=db.session.query(Sp).filter(Sp.sp_id==session.get('loggedin')).first()
    deets=db.session.query(Sp).all()
    fname=b.fname.data
    lname=b.lname.data
    phone=b.phone.data
    service=request.form.get('service')
    state=request.form.get('state')
    address=request.form.get('address')
    return render_template('service_providers/sp_profile.html',b=b,records=records,deets=deets)
  else:
    return redirect(url_for('form_page'))
@hireapp.route('/sp_logout')
def sp_logout():
  if session.get('loggedin')!=None:
    session.pop('loggedin')
  return redirect(url_for('home_page'))