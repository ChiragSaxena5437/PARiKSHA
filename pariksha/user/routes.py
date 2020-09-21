from flask import render_template,request,redirect,Blueprint,url_for

user = Blueprint("user",__name__,url_prefix="/user",template_folder='templates')

