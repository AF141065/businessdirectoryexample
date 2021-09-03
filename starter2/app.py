import json
from operator import indexOf
from datetime import datetime
import re
from flask import (
    Flask, 
    render_template, 
    request, 
    Response, 
    flash, 
    redirect, 
    url_for,
    jsonify,
    session,
    abort
)
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
import bleach
from logging import Formatter, FileHandler
from flask_wtf import Form
from models import setup_db, Category, Listing, User, Email_Confirmation
from flask_cors import CORS
from flask_wtf.csrf import CSRFProtect
from states import State
from email.utils import parseaddr
import random
import os

def generate_email_token():
  token = ""
  for i in range(1,200):
    num = chr(random.randint(48,57))
    lc = chr(random.randint(97,122))
    uc = chr(random.randint(65,90))
    j = random.randint(0,2)
    token += [num,lc,uc][i%3-j]
  return token

def generate_category_link(categoryname):
  return ''.join([j for j in categoryname if str(j)!=' ']).lower()

def is_bleached(original,bleached):
  return True if original!=bleached else False

def is_legit_name(bname, rbname):
  if not len(bname) or not all([(str(i).isalpha() or str(i) in " &',.") for i in bname]) or is_bleached(bname,rbname):
    print("Name!")
    return "E:Not a valid business name|"+bname
  else:
    return bname
def is_legit_address(baddress,rbaddress):
  if is_bleached(baddress,rbaddress):
    print("Address!")
    return "E:Not a valid address|"+baddress
  else:
    return baddress
def is_legit_state(bstate,rbstate):
  if len(bstate)==2 and not is_bleached(bstate,rbstate):
    #print("State!")
    for i in State.choices():
      print(i)
      if i==bstate:
        return bstate
    #print("State!f2")
    return "E:Not a valid state|"+bstate
  else:
    print("State!f1")
    return "E:Not a valid state|"+bstate
def is_legit_city(bcity,rbcity):
  if len(bcity) and all([(str(i).isalpha() or str(i) in " &',.") for i in bcity]) and not is_bleached(bcity,rbcity):
    return bcity
  else:
    print("City!")
    return "E:Not a valid city|"+bcity
def is_legit_hours(bhours,rbhours):
  if len(bhours) and all([(str(i).isalpha() or str(i) in " &',.:-" or str(i).isdigit()) for i in bhours]) and not is_bleached(bhours,rbhours):
    return bhours
  else:
    print("Hours!")
    return "E:Not valid hours|"+bhours
def is_legit_payment(bpayment,rbpayment):
  if len(bpayment) and all([(str(i).isalpha() or str(i) in " &',.") for i in bpayment]) and not is_bleached(bpayment,rbpayment):
    return bpayment
  else:
    print("payment!")
    return "E:Not valid payment method|"+bpayment
def is_legit_url(burl,rburl):
  if len(burl) and "http" in burl and not is_bleached(burl,rburl):
    return burl
  else:
    print("url!")
    return "E:Not a valid website|"+burl
def is_legit_phone(bphone,rbphone):
  if len(bphone)==10 and all([str(i).isdigit() for i in bphone]) and not is_bleached(bphone,rbphone):
    return bphone
  else:
    print("phone!")
    return "E:Not a valid phone number|"+bphone
def is_legit_category(bcategory,rbcategory):
  if len(bcategory) and not is_bleached(bcategory,rbcategory):
    for i in Category.query.all():
      if i.catagory_name==bcategory:
        return bcategory
    print("Category!")
    return "E:Not a valid category|"+bcategory
  else:
    print("Categoryb!")
    return "E:Not a valid category|"+bcategory
def is_legit_keyword(bkeyword,rbkeyword):
  if len(bkeyword) and all([(str(i).isalpha() or str(i) in " &',.") for i in bkeyword]) and not is_bleached(bkeyword,rbkeyword):
    return bkeyword
  else:
    print("keyword!")
    return "E:Not valid keywords|"+bkeyword
def is_legit_email(bemail,rbemail):
  if len(bemail) and len(parseaddr(bemail)) and not is_bleached(bemail,rbemail):
    return bemail
  else:
    print("email!")
    return "E:Not a valid email address|"+bemail
def is_legit_description(bdescription,rbdescription):
  if len(bdescription)>49 and not is_bleached(bdescription, rbdescription):
    return bdescription
  else:
    print("Desc!")
    return "E:Not a valid description. Please make sure the length is above 49 characters.|"+bdescription

def search_for_listing(search_term,search_city=None,category=None):
  if search_term=="" and search_city==None and category==None: #Brings up a list of random listings since the user didn't specify.
    listings = [i for i in Listing.query.all()]
    return listings
  elif search_term=="" and search_city==None and len(category):
    cat = [i for i in Category.query.all()]
    picked=None
    for i in cat:
      print(i.catagory_name)
      if category == generate_category_link(i.catagory_name):
        picked = i
        #print(picked.catagory_name)
        break
    if not picked:
      abort(404)
    listings = [i for i in Listing.query.filter() if i.cid==picked.category_id]
    return listings
  return []

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__,template_folder='C:/pythonscripts/udacity/FSND/projects/capstone/starter2')
  app.config.from_object('config')
  app.jinja_env.globals.update(generate_category_link=generate_category_link)
  setup_db(app)
  #cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
  CORS(app)
  @app.after_request
  def after_request(response):
    response.headers.add("Access-Control-Allow-Headers", "Content-type, Authorization")
    response.headers.add("Access-Control-Allow-Methods", "GET, POST, PUT, PATCH, DELETE, UPDATE")
    return response

# HOME PAGE CONTROLLERS
  @app.route('/')
  def home():
    return render_template("home.html")
  @app.route('/home')
  def home2():
    return render_template("home.html")

# SIGN UP / SIGN IN CONTROLLERS
  @app.route('/signinup')
  def signinup():
    if 'id' in session:
      cuser = User.query.get(session['id'])
      return redirect(url_for('account',account_id=session['id']))
    else:
      return render_template("Signinup.html")
  
  @app.route('/signup', methods=['POST'])
  def signup():
    email = bleach.clean(request.form.get("signupemailbox"))
    if is_bleached(email,request.form.get("signupemailbox")): #if the input is bleached, which means it contains potentially invasive code.
      flash('Please enter a valid email')
      return render_template("Signinup.html")
    if User.query.filter(User.user_email == email).first():
      flash('Email already exists. Try signing in.')
      return render_template("Signinup.html")
    newUser = User(user_email=email,user_password="")
    newUser.insert()
    newUser = User.query.filter(User.user_email == email).first()
    newEmailC = Email_Confirmation(code=generate_email_token(), uid=newUser.user_id)
    newEmailC.insert()
    #TODO: Finish the email confirmation process i.e get the email sent to the user and have them confirm it.
    return render_template("emailconfirmsuccess.html")

  @app.route('/signin',methods=['POST'])
  def signin():
    email = bleach.clean(request.form.get("signinemailbox"))
    password = bleach.clean(request.form.get("signinPassword"))
    if is_bleached(email,request.form.get("signinemailbox")) or is_bleached(password,request.form.get("signinPassword")):
      flash('Please enter valid credentials.')
      return render_template("Signinup.html")
    currentUser = User.query.filter(User.user_email == email).first()
    if currentUser: #user exists
      if currentUser.user_password == password: #password matches. TODO: implement hashing.
        session['id'] = currentUser.user_id
        return redirect(url_for('account',account_id=currentUser.user_id))
      else:
        flash('incorrect password.')
        return render_template("Signinup.html")
    else:
      flash('Email doesn\'t exist.')
      return render_template("Signinup.html")

# ACCOUNT CONTROLLERS
  @app.route('/account/<int:account_id>')
  def account(account_id):
    if 'id' in session:
      luser = User.query.get(session['id'])
      return render_template("Account.html", cuser=luser)
    else:
      return redirect(url_for('home'))
  
  @app.route('/account/<int:account_id>#deleteDialog')
  def accountd():
    if 'id' in session:
      return redirect(url_for('account',account_id=session['id'])+'#deleteDialog')
    else:
      return redirect(url_for('home'))
  
  @app.route('/account')
  def accountt():
    return render_template("Account.html")

  @app.route('/submitlisting', methods=['GET','POST'])
  def submitlisting():
    if request.method == 'GET':
      if 'id' in session:
        cat_names = [i.catagory_name for i in Category.query.all()]
        states = State.choices()
        return render_template("SubmitListingPage.html", catgori=cat_names, stat=states,data={})
      else:
        return redirect(url_for('home'))
    if request.method == 'POST':
      error = False
      if 'id' in session:
        info = {} #info is used in two ways: to construct the listing object, and give any errors.
        try:
          info['name']=is_legit_name(request.form.get('BusinessNameBox'),bleach.clean(request.form.get('BusinessNameBox')))
          info['address']=is_legit_address(request.form.get('AddressBox'),bleach.clean(request.form.get('AddressBox')))
          info['city']=is_legit_city(request.form.get('CityBox'),bleach.clean(request.form.get('CityBox')))
          info['hours']=is_legit_hours(request.form.get('HoursBox'),bleach.clean(request.form.get('HoursBox')))
          info['payment']=is_legit_payment(request.form.get('PaymentBox'),bleach.clean(request.form.get('PaymentBox')))
          info['url']=is_legit_url(request.form.get('WebsiteBox'),bleach.clean(request.form.get('WebsiteBox')))
          info['phone']=is_legit_phone(request.form.get('PhoneBox'),bleach.clean(request.form.get('PhoneBox')))
          info['keywords']=is_legit_keyword(request.form.get('KeywordBox'),bleach.clean(request.form.get('KeywordBox')))
          info['email']=is_legit_email(request.form.get('BusinessEmailBox'),bleach.clean(request.form.get('BusinessEmailBox')))
          info['description']=is_legit_description(request.form.get('DescTextArea'),bleach.clean(request.form.get('DescTextArea')))
          info['state']=is_legit_state(request.form.get('StateComboBox'),bleach.clean(request.form.get('StateComboBox')))
          info['category']=is_legit_category(request.form.get('CategoryComboBox'),bleach.clean(request.form.get('CategoryComboBox')))
          for i in info.values():
            if i[0:2]=="E:":
              error = True
          if not error:
            d = datetime.utcnow()
            print(d)
            catid = Category.query.filter_by(catagory_name = info['category']).first()
            catid = catid.category_id
            nlisting = Listing(company_name=info['name'],address=info['address'],state=info['state'],city=info['city'],
                               hours=info['hours'], payment_type=info['payment'],website_link=info['url'],phone=info['phone'],
                               keywords=info['keywords'],business_email=info['email'],description=info['description'],layout_id=0,style_id=0,
                               time_of_creation=d,cid=catid)
            nlisting.insert()
            luser = User.query.get(session['id'])
            luser.lid = nlisting.listing_id
            luser.update()
            return redirect(url_for('get_listing',category_name=info['category'],listing_id=nlisting.listing_id)) #success! TODO: Add routing to listing page.
          else:
            for i in info.values():
              if i[0:2]=="E:":
                print(i)
                flash(i[0:i.index('|')-1])
                i=i[i.index('|')+1:]
            cat_names = [i.catagory_name for i in Category.query.all()]
            states = State.choices()
            return render_template("SubmitListingPage.html", catgori=cat_names, stat=states, data=info)
        except SQLAlchemyError as e:
          v = str(e.__dict__['orig']) #displays exception message
          if 'id' in session:
            flash(v)
            for i in info:
              if i[0:2]=="E:":
                flash(i[0:i.index('|')-1])
                i=i[i.index('|')+1:]
            cat_names = [i.catagory_name for i in Category.query.all()]
            states = State.choices()
            return render_template("SubmitListingPage.html", catgori=cat_names, stat=states, data=info)
          else:
            return redirect(url_for('home'))
      else:
        return redirect(url_for('home'))
  
  @app.route('/categories/<string:category_name>/listings/<string:listing_id>', methods=['DELETE'])
  def delete_listing(category_name,listing_id):
    if 'id' in session:
      listing = Listing.query.get(listing_id)
      cuser = User.query.get(session['id'])
      cuser.lid = None
      listing.delete()
      return jsonify({'success':True})
    else:
      return redirect(url_for('home'))

  @app.route('/logout')
  def loggingout():
    session.pop('id',None)
    return redirect(url_for('home'))

#LISTING PAGE CONTROLLER
  @app.route('/categories/<string:category_name>/listings/<string:listing_id>', methods=['GET'])
  def get_listing(category_name,listing_id):
    listing = Listing.query.get(listing_id)
    if listing.get_category_name().lower() == category_name.lower():
      return render_template("ListingPage.html",listt=listing)
    else:
      print(listing.get_category_name())
      print(category_name)
      return redirect(url_for('home'))
      
#SEARCH CONTROLLERS

  @app.route('/categories')
  def categories():
    cat_names = [i.catagory_name for i in Category.query.all()]
    cat_names_segment = []
    c = 0
    row=[]
    for i in cat_names:
      if c%3==0 and c!=0:
        cat_names_segment.append(row.copy())
        row.clear()
        row.append(i)
        c+=1
      else:
        print(i)
        row.append(i)
        c+=1
    if len(row):
      cat_names_segment.append(row.copy())
      row.clear()
    print(cat_names_segment)
    return render_template("CategoryPage.html", cat_list=cat_names_segment)
  
  @app.route('/categories/<string:category_name>')
  def get_category_listings(category_name):
    if not is_bleached(category_name,bleach.clean(category_name)):
      lis = search_for_listing("",None,category_name)
      return render_template("Search.html",category_n=category_name, Listings=lis)
    
  # @app.route('/search', methods=['POST'])
  # def testsearch():
  #   if request.method == 'POST':
  #     print(request.form.get("searchterm"))
  #     searchterm = bleach.clean(request.form.get("searchterm"))
  #     if not is_bleached(searchterm,request.form.get("searchterm")):
  #       list = search_for_listing(searchterm)
  #       return render_template("Search.html",listings=list)
  #     else:
  #       return redirect(url_for('home'))

#MISCELLANEOUS CONTROLLERS
  @app.route('/contact')
  def contact():
    return render_template("Contact.html")
  @app.route('/about')
  def about():
    return render_template("About.html")
  return app
