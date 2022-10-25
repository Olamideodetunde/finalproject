import re,os,random,string
from flask import render_template,request,redirect,url_for,flash,session,jsonify
from werkzeug.security import check_password_hash,generate_password_hash
from pkg import hireapp,db
from pkg.forms import AdminForm
from pkg.mymodels import Admin,Sp,Payment,State, Transaction
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
    return render_template('admin/all_payments')
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