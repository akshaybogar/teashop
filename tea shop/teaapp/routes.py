from teaapp import app
from flask import render_template, url_for
from flask import request
from flask import Response
from flask import json
from flask import flash
from flask import redirect
from teaapp.models import UserModel, ProductModel, PurchaseModel
from teaapp.forms import LoginForm, RegisterForm
from teaapp.alchemy_db import db

obj_count = 1

@app.route('/')
@app.route('/index')
@app.route('/home')
def index():
    return render_template('index.html', index=True)

@app.route('/products/')
def products():
    products = ProductModel.get()
    return render_template('products.html', product_data=products, products=True)

@app.route('/register', methods=['GET', 'POST'])
def register():
    global obj_count
    form = RegisterForm()
    if form.validate_on_submit():
        user_id = obj_count + 1
        email = form.email.data
        password = form.password.data
        firstname = form.firstname.data
        lastname = form.lastname.data

        user = UserModel(user_id=user_id, email=email, password=password, firstname=firstname, lastname=lastname)
        user.save_to_db()
        flash('Successfully registered', 'success')
        return redirect('/index')
    return render_template('register.html', form=form, register=True)

@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = UserModel.find_by_email(email)
        if user and password==user.password:
            flash('You are successfully logged in!', "success")
            return redirect('/index')
        else:
            flash('Something went wrong! Try again', "danger")
    return render_template('login.html', form=form, login=True)

@app.route('/purchase', methods=["GET", "POST"])
def purchase():
    # To be completed
    product_id = request.form.get('product_id')
    title = request.form.get('title')
    user_id = 2
    if product_id:
        if PurchaseModel.find_by_product_user(user_id=user_id,product_id=product_id):
            flash('Item already in your cart!', "success")
            return redirect('/products')
        else:
            purchase_item = PurchaseModel(user_id=user_id, product_id=product_id)
            purchase_item.save_to_db()

    classes = None
    return render_template('purchase.html', purchase=True, classes=classes)

@app.route('/api/')
@app.route('/api/<id>/')
def api(id=None):
    if not id:
        data = ProductModel.get()
    else:
        data = ProductModel.find_by_id(id)
    return Response(json.dumps(data), mimetype='application/json')

@app.route('/user')
def user():
    users = UserModel.get()
    return render_template("user.html", users=users)
