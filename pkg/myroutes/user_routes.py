from datetime import datetime,timedelta
import os,random,string
import requests
from flask_mail import Message
from flask import render_template,request,redirect,url_for,flash,session,jsonify,json
from werkzeug.security import check_password_hash,generate_password_hash
from pkg.mymodels import Review, Sp, Spreply,State,Service,Spmessage,Homesearch, Subscription,Transaction,Payment
from pkg import hireapp,db
from pkg.forms import MessageForm, Reply, ReviewForm, Signup,Login,Profile
@hireapp.route('/',methods=['POST','GET'])
def home_page():
  records=db.session.query(State).all()
  service=db.session.query(Service).all()
  if request.method =='GET':
    return render_template('user/index.html',state=records,service=service)
  else:
    if session.get('loggedin')==None:
      services=request.form.get('services')
      state=request.form.get('state')
      records =Homesearch(search_service=services,search_state=state)
      db.session.add(records)
      db.session.commit()
      session['search']=records.search_id
      return redirect(url_for('profile_page'))
    else:
      return redirect(url_for('sp_dashboard'))
@hireapp.route('/profile',methods=['GET','POST'])
def profile_page():
  if session.get('loggedin')==None:
    if session.get('search')==None:
      records=db.session.query(Sp,Transaction).join(Transaction).filter(Transaction.trx_status=='paid').all()
      service=db.session.query(Service).all()
      state=db.session.query(State).all()
      return render_template('user/profx.html',records=records,service=service,state=state)
    else:
      search=db.session.query(Homesearch).filter(Homesearch.search_id==session.get('search')).first()
      if search:
        records=db.session.query(Sp,Transaction).join(Transaction).filter(Sp.sp_location==search.search_state,Sp.sp_services==search.search_service,Transaction.trx_status=='paid').all()
        service=db.session.query(Service).all()
        state=db.session.query(State).all()
        return render_template('user/profx.html',records=records,service=service,state=state,search=search)
      else:
        return redirect(url_for('home_page'))
  else:
    return redirect(url_for('sp_dashboard'))

@hireapp.route('/ajaxemail',methods=['GET'])
def ajaxemail():
  email=request.args.get('emailadd')
  records=db.session.query(Sp).filter(Sp.sp_email==email).first()
  x={'error':'','success':''}
  if records:
    x['error']='Email Address already in use'
    return jsonify(x)
  else:
    x['success']='Email Address is Available'
    return jsonify(x)

@hireapp.route('/ajaxphone',methods=['GET'])
def ajaxphone():
  phone=request.args.get('phone')
  records=db.session.query(Sp).filter(Sp.sp_phone==phone).first()
  x={'error':'','success':''}
  if records:
    x['error']='Phone Number already taken'
    return jsonify(x)
  else:
    x['success']= 'Phone Number is available'
    return jsonify(x)

@hireapp.route('/filter_search',methods=['GET'])
def filter_search():
      state=request.args.get('state')
      service=request.args.get('services')
      if state=='' and service=='':
        record=db.session.query(Sp,Transaction).join(Transaction).filter(Transaction.trx_status=='paid').all()
      elif state=='' and service!='':
        record=db.session.query(Sp,Transaction).join(Transaction).filter(Sp.sp_services==service,Transaction.trx_status=='paid').all()
      elif state!='' and service=='':
        record=db.session.query(Sp,Transaction).join(Transaction).filter(Sp.sp_location==state,Transaction.trx_status=='paid').all()
      else:
        record=db.session.query(Sp,Transaction).join(Transaction).filter(Sp.sp_location==state,Sp.sp_services==service,Transaction.trx_status=='paid').all()
      data2send=''
      if record:
        for i,y in record:
          data2send=f'''<div class="row border my-3 bg-white">
            <div class="col-md-11 m-3">
              <div>
                <div>
                  <img src="/static/uploads/{i.sp_image}" class="img-fluid m-3 rounded-pill" style="width:50px;height:50px;">
                  <span class="text-center"><a href="/sp_details/{i.sp_id}" class=" h4 text-decoration-none text-primary title2" style="font-family: 'Unna', serif;">{i.sp_fname} {i.sp_lname}</a></span>
                </div>
                <div class="d-flex">
                  <div class="me-5">
                    <div><b>Service:</b>{i.servicedeets.service_name}</div>
                  </div>
                  <div>
                    <div><b>Location:</b>{i.statedeets.state_name}</div>
                  </div>
                </div>
              </div>
            </div>
          </div>'''
        return data2send
      else:
        data2send='<h1>No Records Found</h1>'
        return data2send
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
      return redirect(url_for('sp_profile'))
    else:
      flash('Wrong Credentials')
      return redirect(url_for('form_page'))
@hireapp.route('/signup',methods=['GET','POST'])
def signup_page():
  y=Signup()
  state=State.query.all()
  service=Service.query.all()
  if request.method == 'GET':
    return render_template('user/signup.html',y=y,state=state,service=service)
  else:
    fname=y.fname.data
    lname=y.lname.data
    emailadd=y.emailadd.data
    phone=y.phone.data
    pwd=generate_password_hash(y.password.data)
    addresss=y.address.data
    service=request.form.get('service')
    gender=request.form.get('gender')
    location=request.form.get('state')
    email=db.session.query(Sp).filter(Sp.sp_email==emailadd).first()
    phone=db.session.query(Sp).filter(Sp.sp_phone==phone).first()
    if email==None and phone==None:
      b=Sp(sp_email=emailadd,sp_password=pwd,sp_fname=fname,sp_lname=lname,sp_location=location,sp_phone=phone,sp_address=addresss,sp_gender=gender,sp_services=service)
      db.session.add(b)
      db.session.commit()
      return redirect(url_for('form_page'))
    else:
      return redirect(url_for('signup_page'))
@hireapp.route('/sp_payment',methods=['POST','GET'])
def sp_payment():
  if session.get('loggedin') != None:
    if request.method=='GET':
      sub=db.session.query(Subscription).first()
      spdetails=db.session.query(Sp).filter(Sp.sp_id==session.get('loggedin')).first()
      transdeets=db.session.query(Transaction).filter(Transaction.trx_status=='paid',Transaction.trx_user==session.get('loggedin')).first()
      return render_template('service_providers/payment.html',sub=sub,spdetails=spdetails,transdeets=transdeets)
    else:
        userid = session.get('loggedin')
        refno = int(random.random() * 1000000000)
        session['tref'] = refno
        trans = Transaction(trx_user=userid,trx_refno=refno,trx_totalamt=1,trx_status='pending',trx_method='cash')            
        db.session.add(trans) 
        db.session.commit()
        id = trans.trx_id
        totalamt=''
        pobj = Payment(sp_id=userid,subscription_id=1,pay_trxid=id)
        db.session.add(pobj)
        db.session.commit() 
         
        return redirect('/confirm') 
  else:
    return redirect(url_for('form_page'))
@hireapp.route('/confirm')
def confirm_subscription():
    """The button here takes them to Paystack"""
    userid = session.get('loggedin')
    transaction_ref = session.get('tref')
    if userid !=None:
        records=Sp.query.get(userid)
        '''Retrieve all the things this user has selected from Purchases table
        save it in a variable and Then send it to the template'''        
        data = db.session.query(Transaction).filter(Transaction.trx_refno==transaction_ref,Transaction.trx_user==userid).first()       
        return render_template('service_providers/confirm_subscription.html',data=data,records=records)
    else:
        return redirect('/login')
@hireapp.route('/paystack_step1',methods=['POST'])
def paystack():
  if session.get('loggedin')!=None:
    url='https://api.paystack.co/transaction/initialize'
    userdeets=Sp.query.get(session.get('loggedin'))
    deets=Transaction.query.filter(Transaction.trx_refno==session.get('tref')).first()
    data={'email':userdeets.sp_email,'amount':deets.amount_paid.subscription_amount*100,'reference':deets.trx_refno}
    headers={'Content_Type':'application/json','Authorization':'Bearer sk_test_fb58555bf41a08607aca1beff850bae08805faa7'}
    response = requests.post(url, headers=headers, data=json.dumps(data))
    rspjson = json.loads(response.text) 
    return redirect(rspjson['data']['authorization_url'])
  else:
    return redirect(url_for('user_login'))
@hireapp.route('/paystack_reponse')
def paystack_response():
    userid = session.get('loggedin')
    if userid != None:
        refno = session.get('tref')

        headers = {"Content-Type": "application/json","Authorization":"Bearer sk_test_fb58555bf41a08607aca1beff850bae08805faa7"}

        response = requests.get(f"https://api.paystack.co/transaction/verify/{refno}",headers=headers)
        rspjson = response.json()
        if rspjson['data']['status'] =='success':
            amt = rspjson['data']['amount']
            ipaddress = rspjson['data']['ip_address']
            t = Transaction.query.filter(Transaction.trx_refno==refno).first()
            t.trx_status = 'paid'
            t.trx_expiry=datetime.now()+timedelta(days=30)
            db.session.add(t)
            db.session.commit()
            
            return redirect(url_for('sp_payment'))  #update database and redirect them to the feedback page
        else:
            t = Transaction.query.filter(Transaction.trx_refno==refno).first()
            t.trx_status = 'failed'
            db.session.add(t)
            db.session.commit()
            return "Payment Failed" 
    else:
        return redirect('/login')
@hireapp.route('/sp_reviews')
def sp_reviews():
  loggedin=session.get('loggedin')
  
  if loggedin != None:
    records=db.session.query(Sp).filter(Sp.sp_id==loggedin).first()
    reviews=db.session.query(Review).filter(Review.review_for==loggedin).all()
    return render_template('service_providers/sp_review.html',records=records,reviews=reviews)
  else:
    return redirect(url_for('form_page'))
@hireapp.route('/sp_reply/<id>')
def sp_reply(id):
  loggedin=session.get('loggedin')
  reply=Reply()
  if loggedin != None:
    records=db.session.query(Sp).filter(Sp.sp_id==loggedin).first()
    return render_template('service_providers/sp_reply.html',records=records,reply=reply,id=id)
  else:
    return redirect(url_for('form_page'))
@hireapp.route('/sp_replyget',methods=['GET','POST'])
def sp_replyget():
  loggedin=session.get('loggedin')
  reply=Reply()
  reply_cont=reply.reply_content.data
  reply_for=request.form.get('review_id')
  records=db.session.query(Sp).get(loggedin)
  reviews=db.session.query(Review).filter(Review.review_for==loggedin,Review.review_id==reply_for).first()
  r=Spreply(reply_by=loggedin,reply_content=reply_cont,reply_for=reply_for)
  reviews.reply_status='True'
  db.session.add(r)
  db.session.commit()
  rsp='Your reply has been sent'
  return rsp
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
@hireapp.route('/sp_message',methods=['POST','GET'])
def sp_message():
  if session.get('loggedin')!=None:
      x=MessageForm()
      records=db.session.query(Sp).filter(Sp.sp_id==session.get('loggedin')).first()
      return render_template('service_providers/message.html',message=x,records=records)
  else:
    return redirect(url_for('form_page'))
@hireapp.route('/sp_messageget',methods=['GET','POST'])
def sp_messageget():
  if session.get('loggedin')!=None:
    title=request.form.get('title')
    content=request.form.get('message')
    rec=Spmessage(message_title=title,message_content=content,message_by=session.get('loggedin'))
    db.session.add(rec)
    db.session.commit()
    rsp='Your message has been received. We will get back to you in due time'
    data2send=jsonify(rsp)
    return data2send
  else:
    return redirect(url_for('form_page'))
@hireapp.route('/sp_faq')
def sp_faq():
  if session.get('loggedin')!=None:
    msg=db.session.query(Spmessage).limit(5).all()
    records=db.session.query(Sp).filter(Sp.sp_id==session.get('loggedin')).first()
    return render_template('service_providers/faq.html',message=msg,records=records)
  else:
    return redirect(url_for('form_page'))
@hireapp.route('/sp_details/<id>',methods=['POST','GET'])
def sp_details(id):
  v=ReviewForm()
  records=db.session.query(Sp).get(id)
  data=db.session.query(Review).filter(Review.review_for==id).all()
  reply=db.session.query(Spreply).all()
  if reply:
    for i in reply:
      x=i
    return render_template('user/details.html',records=records,data=data,reply=x,v=v)
  else:
    return render_template('user/details.html',records=records,data=data,reply='',v=v)
@hireapp.route('/review_details/<id>',methods=['POST','GET'])
def review_details(id):
    records=db.session.query(Sp).get(id)
    user_name=request.form.get('user_name')
    review=request.form.get('review')
    r=Review(review_by=user_name,review_content=review,review_for=records.sp_id)
    db.session.add(r)
    db.session.commit()
    data2return={'madeby':r.review_by,'review':r.review_content}
    data_json=jsonify(data2return)
    return data_json
@hireapp.route('/sp_profile',methods=['POST','GET'])
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
      file_obj=request.files['image']
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
      summary=request.form.get('summary')
      records.sp_fname=fname
      records.sp_lname=lname
      records.sp_summary=summary
      records.sp_services=service
      records.sp_phone=phone
      records.sp_location=state
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