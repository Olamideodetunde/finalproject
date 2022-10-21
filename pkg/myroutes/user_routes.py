import re,os,random,string
from flask import render_template,request,redirect,url_for,flash,session
from werkzeug.security import check_password_hash,generate_password_hash
from pkg.mymodels import Sp,State,Service
from pkg import hireapp,db
from pkg.forms import Signup,Login,Profile
@hireapp.route('/',methods=['POST','GET'])
def home_page():
  records=db.session.query(State).all()
  service=db.session.query(Service).all()
  if request.method =='GET':
    return render_template('user/hire.html',state=records,service=service)
  else:
    sp_name=request.form.get('servprov')
    services=request.form.get('services')
    state=request.form.get('state')
    return redirect(url_for('profile_page'))
@hireapp.route('/profile')
def profile_page():
  records=db.session.query(Sp).all()
  service=db.session.query(Service).all()
  return render_template('user/profx.html',records=records,service=service)
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
@hireapp.route('/sp_details/<id>')
def sp_details(id):
  records=db.session.query(Sp).filter(Sp.sp_id==id)
  return render_template('user/details.html',records=records)
@hireapp.route('/sp_profile')
def sp_profile():
  b=Profile()
  if session.get('loggedin')!=None:
    if request.method == 'GET':
      records=db.session.query(Sp).filter(Sp.sp_id==session.get('loggedin')).first()
      service=db.session.query(Service).all()
      records1=db.session.query(State).all()
      return render_template('service_providers/sp_profile.html',b=b,records=records,service=service,records1=records1)
    else:
      records=db.session.query(Sp).filter(Sp.sp_id==session.get('loggedin')).first()
      file_obj=request.files['sp_image']
      allowed=['.jpg','.png','.jpeg']
      newfilename=''
      if file_obj.filename!='':
        original_name=file_obj.filename
        filename,ext=os.path.splitext(original_name)
        if ext.lower() in allowed:
          xter_list=random.sample(string.ascii_letters,12)
          newfilename=''.join(xter_list)+ext
          file_obj.save('pkg/static/uploads/'+newfilename)
      fname=request.form.get('fname')
      lname=request.form.get('lname')
      phone=request.form.get('phone')
      service=request.form.get('service')
      state=request.form.get('state')
      address=request.form.get('address')
      records.sp_fname=fname
      records.sp_lname=lname
      records.sp_service=service
      records.sp_phone=phone
      records.sp_state=state
      records.sp_address=address
      records.sp_image=newfilename
      db.session.commit()
      return redirect(url_for('sp_profile'))
  else:
    return redirect(url_for('form_page'))
@hireapp.route('/sp_logout')
def sp_logout():
  if session.get('loggedin')!=None:
    session.pop('loggedin')
  return redirect(url_for('home_page'))