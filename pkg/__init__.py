'''Import Flask'''
from flask import Flask
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
'''Instantiate Flask Object'''
hireapp=Flask(__name__,instance_relative_config=True)
hireapp.config.from_pyfile('config.py')
csrf=CSRFProtect(hireapp)
db=SQLAlchemy(hireapp)
from pkg import mymodels
from pkg.myroutes import user_routes,admin_routes
