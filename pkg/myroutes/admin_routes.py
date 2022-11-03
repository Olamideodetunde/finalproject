import re,os,random,string
from flask import render_template,request,redirect,url_for,flash,session,jsonify
from werkzeug.security import check_password_hash,generate_password_hash
from pkg import hireapp,db
from pkg.forms import AdminForm,SeviceForm,PriceForm
from pkg.mymodels import Admin, Spmessage, Service,Sp,Payment,State, Subscription, Transaction
@hireapp.route('/admin/login',methods=['POST','GET'])
def admin_login():
  if request.method=='GET':
    form=AdminForm()
    return render_template('admin/admin_login.html',form=form)
  else:
    email=request.form.get('emailadd')
    password=request.form.get('password')
    rec=db.session.query(Admin).filter(Admin.admin_email==email).filter(Admin.admin_password==password).first()
    if rec:
      session['admin']=rec.admin_id
      return redirect(url_for('admin_home'))
    else:
      return redirect(url_for('admin_login'))
@hireapp.route('/admin/home')
def admin_home():
  if session.get('admin')!=None:
    return render_template('admin/admin_home.html')
  else:
    return redirect(url_for('admin_login'))
@hireapp.route('/admin/all_registered')
def all_registered():
  admin_user=session.get('admin')
  if admin_user:
    regs=db.session.query(Sp,State).join(State).all()
    return render_template('admin/all_registration.html',regs=regs)
  else:
    return redirect('/admin/login')
@hireapp.route('/admin/all_payments')
def all_payments():
  admin_user=session.get('admin')
  if admin_user:
    regs=db.session.query(Transaction).all()
    return render_template('admin/all_payments.html',regs=regs)
  else:
    return redirect('/admin/login')
@hireapp.route('/admin/add-service',methods=['POST','GET'])
def add_service():
  admin_user=session.get('admin')
  if admin_user:
    frm=SeviceForm()
    if request.method == 'GET':
      return render_template('admin/add_services.html',frm=frm)
    else:
      if frm.validate_on_submit():
        service_name=request.form.get('service_name')
        rec=db.session.query(Service).filter(Service.service_name==service_name)
        if rec:
          r=Service(service_name=service_name)
          db.session.add(r)
          db.session.commit()
          return redirect(url_for('all_services'))
        else:
          return redirect(url_for('all_services'))
      else:
        return render_template('admin/add_services.html',frm=frm)
  else:
    return redirect('/admin/login')
@hireapp.route('/admin/change-price',methods=['POST','GET'])
def change_price():
  admin_user=session.get('admin')
  if admin_user:
    frm=PriceForm()
    if request.method == 'GET':
      return render_template('admin/change_price.html',frm=frm)
    else:
      if frm.validate_on_submit():
        sub_amount=request.form.get('sub_amount')
        r=db.session.query(Subscription).filter(Subscription.subscription_id=='1').first()
        r.subscription_amount=sub_amount
        db.session.commit()
        return redirect(url_for('change_price'))
      else:
        return render_template('admin/change_price.html',frm=frm)
  else:
    return redirect('/admin/login')
@hireapp.route('/admin/all_services')
def all_services():
  admin_user=session.get('admin')
  if admin_user:
    regs=db.session.query(Service).all()
    return render_template('admin/all_services.html',regs=regs)
  else:
    return redirect('/admin/login')
@hireapp.route('/admin/all_message')
def all_message():
  admin_user=session.get('admin')
  if admin_user:
    msg=db.session.query(Spmessage).all()
    return render_template('admin/all_message.html',msg=msg)
  else:
    return redirect('/admin/login')
@hireapp.route('/admin/delete/<id>')
def delete_user(id):
  admin_user=session.get('admin')
  if admin_user:
    user_del=db.session.query(Sp).get(id)
    db.session.delete(user_del)
    db.session.commit()
    return redirect(url_for('all_registered'))
  else:
    return redirect('/admin/login')
@hireapp.route('/admin/details/<id>')
def details(id):
  admin_user=session.get('admin')
  if admin_user:
    user=db.session.query(Sp).filter(Sp.sp_id==id).first()
    return render_template('admin/details.html',user=user)
  else:
    return redirect(url_for('admin_login'))
@hireapp.route('/admin/logout')
def admin_logout():
  if session['admin'] !=None:
    session.pop('admin')
  return redirect(url_for('home_page'))