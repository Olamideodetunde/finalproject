import re,os,random,string
from flask import render_template,request,redirect,url_for,flash,session,jsonify
from werkzeug.security import check_password_hash,generate_password_hash
from pkg import hireapp,db
from pkg.forms import AdminForm
from pkg.mymodels import Admin,Sp,Payment
@hireapp.route('/admin/login',methods=['POST','GET'])
def admin_login():
  if request.method=='GET':
    form=AdminForm()
    return render_template('admin/admin_login.html',form=form)
  else:
    email=request.form.get('emailadd')
    password=request.form.get('password')
    rec=db.session.query(Admin).filter(Admin.admin_email==email,Admin.admin_password==password)
    if rec:
      session['admin']=rec.admin_id
      return redirect(url_for('admin_home'))
    else:
      return redirect(url_for('admin_login'))