from flask import Flask, render_template, request, session, redirect, url_for, flash
from datetime import datetime
from werkzeug.utils import secure_filename
from models import Cart, Category, Customer, Feedback, Order, Product, Vendor
from exts import login_user, login_vendor, register_user, register_vendor, get_customer_id, get_vendor_id, \
    on_sales_product, search_products, get_user_cart_items, show_vendor_products, add_product, edit_product, \
    delete_product, get_orders_for_vendor, allowed_file, get_vendor_name, get_category_id, get_customer_name, \
    get_products_by_category, get_product_by_id, get_comment_by_id, update_like_count, update_dislike_count, \
    save_feedback, add_to_cart_db, delete_cart_item_db, get_user_orders, update_order_status, get_cart_item_by_id, \
    create_order_db, get_pending_orders, delete_product_order, delete_product_cart
import os
import bcrypt

app = Flask(__name__)
app.secret_key = 'kn010211'

UPLOAD_FOLDER = 'static/product_images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# index
@app.route('/')
def index():
    products = on_sales_product()
    customer_name = session.get('name')
    customer_id = session.get('id')
    return render_template('user/product_list.html', products=products, customer_name=customer_name,
                           customer_id=customer_id)


@app.route('/category_product/<category_id>')
def category_product(category_id):  # put application's code here
    products = get_products_by_category(category_id)
    customer_name = session.get('name')
    customer_id = session.get('id')
    return render_template('user/product_list.html', products=products, customer_name=customer_name,
                           customer_id=customer_id)


@app.route('/search_product', methods=['GET', 'POST'])
def search_product():  # put application's code here
    customer_name = session.get('name')
    customer_id = session.get('id')
    if request.method == 'POST':
        keyword = request.form.get('keyword')
        products = search_products(keyword)
        return render_template('user/product_list.html', products=products, customer_name=customer_name,
                               customer_id=customer_id)
    else:
        return redirect(url_for('index'))


@app.route('/product_detail/<int:product_id>', methods=['GET', 'POST'])
def product_detail(product_id):
    customer_name = session.get('name')
    customer_id = session.get('id')
    if request.method == 'POST':
        if 'id' not in session:
            return redirect(url_for('user_login'))

        feedback_content = request.form.get('review')
        feedback_time = datetime.now()

        save_feedback(customer_id, product_id, feedback_time, feedback_content)
        return redirect(url_for('product_detail', product_id=product_id))

    product = get_product_by_id(product_id)
    comments = get_comment_by_id(product_id)
    return render_template('user/product_detail.html', product=product, comments=comments, customer_name=customer_name,
                           customer_id=customer_id)


@app.route('/like/<int:product_id>', methods=['POST'])
def like(product_id):
    update_like_count(product_id)
    return redirect(url_for('product_detail', product_id=product_id))


@app.route('/dislike/<int:product_id>', methods=['POST'])
def dislike(product_id):
    update_dislike_count(product_id)
    return redirect(url_for('product_detail', product_id=product_id))


# login, logout and register
@app.route('/user_login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        customer_email = request.form.get('customer_email')
        password = request.form.get('customer_password')
        hashed_password = login_user(customer_email)

        if hashed_password is not None and bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
            session['customer_email'] = customer_email
            session['id'] = get_customer_id(customer_email)
            session['name'] = get_customer_name(customer_email)
            return redirect(url_for('index', name=session['name'], id=session['id']))
        else:
            error_message = 'Incorrect email or password'
            return render_template('user/login.html', error_message=error_message)
    else:
        error_message = None
        return render_template('user/login.html', error_message=error_message)


@app.route('/user_register', methods=['GET', 'POST'])
def user_register():  # put application's code here
    if request.method == 'POST':
        customer_email = request.form.get('customer_email')
        pwd_db = login_user(customer_email)

        if pwd_db is None:
            customer_name = request.form.get('customer_name')
            customer_phone = request.form.get('customer_phone')
            customer_address = request.form.get('customer_address')
            customer_password = request.form.get('customer_password')

            hashed_password = bcrypt.hashpw(customer_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            customer = Customer(None, customer_name, customer_phone, customer_email, customer_address,
                                hashed_password)
            register_user(customer)
            return redirect(url_for('user_login'))
        else:
            error_message = 'The email already exit'
            return render_template('user/register.html', error_message=error_message)
    return render_template('user/register.html')


@app.route('/vendor_login', methods=['GET', "POST"])
def vendor_login():  # put application's code here
    if request.method == 'POST':
        vendor_email = request.form.get('vendor_email')
        password = request.form.get('vendor_password')
        hashed_password = login_vendor(vendor_email)

        if hashed_password is not None and bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
            session['vendor_email'] = vendor_email
            vendor_id = get_vendor_id(vendor_email)
            session['id'] = vendor_id
            return redirect(url_for('vendor_index', vendor_id=vendor_id))
        else:
            error_message = 'Incorrect E_mail or password'
            return render_template('vendor/login.html', error_message=error_message)
    else:
        return render_template('vendor/login.html')


@app.route('/vendor_register', methods=['GET', 'POST'])
def vendor_register():  # put application's code here
    if request.method == 'POST':
        vendor_email = request.form.get('vendor_email')
        hashed_password = login_vendor(vendor_email)

        if hashed_password is None:
            vendor_name = request.form.get('vendor_name')
            vendor_password = request.form.get('vendor_password')
            vendor_phone = request.form.get('vendor_phone')
            vendor_address = request.form.get('vendor_address')
            hashed_password = bcrypt.hashpw(vendor_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            vendor = Vendor(None, vendor_name, vendor_phone, vendor_email, vendor_address, hashed_password)
            register_vendor(vendor)
            return redirect(url_for('vendor_login'))
        else:
            error_message = 'The email already exit'
            return render_template('vendor/register.html', error_message=error_message)
    return render_template('vendor/register.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


# customer
@app.route('/cart')
def cart():
    customer_name = session.get('name')
    customer_id = session.get('id')
    cart_items = get_user_cart_items(customer_id)

    return render_template('user/cart.html', cart_items=cart_items, customer_name=customer_name, customer_id=customer_id)


@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    if 'id' not in session:
        return redirect(url_for('user_login'))

    customer_id = session['id']
    product_amount = request.form.get('product_amount')

    if not product_amount or not product_amount.isdigit():
        flash('Invalid product quantity.')
        return redirect(url_for('product_detail', product_id=product_id))

    product_amount = int(product_amount)
    add_to_cart_db(customer_id, product_id, product_amount)

    return redirect(url_for('cart'))


@app.route('/cart/delete/<int:cart_item_id>', methods=['POST'])
def delete_cart_item(cart_item_id):
    if 'id' not in session:
        return redirect(url_for('user_login'))

    customer_id = session['id']
    delete_cart_item_db(customer_id, cart_item_id)

    return redirect(url_for('cart'))


@app.route('/create_order/<int:cart_item_id>', methods=['POST'])
def create_order(cart_item_id):
    if 'id' not in session:
        return redirect(url_for('user_login'))

    customer_id = session['id']
    cart_item = get_cart_item_by_id(customer_id, cart_item_id)

    if cart_item is None:
        return redirect(url_for('cart'))

    product_id = cart_item.product_id
    product = get_product_by_id(product_id)

    if product is None:
        return redirect(url_for('cart'))

    vendor_id = product['vendor_id']
    product_amount = cart_item.product_amount
    order_total = product['product_price'] * product_amount
    order_create_time = datetime.now()
    order_status = '0'

    order = Order(None, product_id, vendor_id, customer_id, product_amount, order_create_time, order_total,
                  order_status)

    order_id = create_order_db(order)

    delete_cart_item_db(customer_id, cart_item_id)

    return redirect(url_for('user_order', order_id=order_id))


@app.route('/buy_now/<int:product_id>', methods=['POST'])
def buy_now(product_id):
    if 'id' not in session:
        return redirect(url_for('user_login'))

    customer_id = session['id']
    product_amount = request.form['product_amount']

    product = get_product_by_id(product_id)
    if not product:
        flash('Product not found.')
        return redirect(url_for('product_detail', product_id=product_id))

    vendor_id = product['vendor_id']
    order_total = product['product_current_price'] * int(product_amount)
    order_status = 0

    order = Order(
        id=None,
        product_id=product_id,
        vendor_id=vendor_id,
        customer_id=customer_id,
        product_amount=product_amount,
        order_create_time=datetime.now(),
        order_total=order_total,
        order_status=order_status
    )

    order_id = create_order_db(order)

    return redirect(url_for('user_order', order_id=order_id))


@app.route('/user_order')
def user_order():  # put application's code here
    customer_name = session.get('name')
    customer_id = session.get('id')
    orders = get_user_orders(customer_id)
    return render_template('user/order.html', orders=orders, customer_id=customer_id, customer_name=customer_name)


# vendor
@app.route('/vendor_index')
def vendor_index():  # put application's code here
    vendor_id = session['id']
    vendor_name = get_vendor_name(vendor_id)
    products = show_vendor_products(vendor_id)
    orders = get_pending_orders(vendor_id)
    if orders:
        inform = 'Please process your order in time'
    else:
        inform = None

    return render_template('vendor/index.html', vendor_name=vendor_name, products=products, vendor_id=vendor_id,
                           inform=inform)


@app.route('/vendor_order', methods=['GET', 'POST'])
def vendor_order():  # put application's code here
    vendor_id = session['id']
    vendor_name = get_vendor_name(vendor_id)
    orders = get_orders_for_vendor(vendor_id)
    if request.method == 'POST':
        order_id = request.form.get('order_id')
        update_order_status(order_id, 1)  # Update order status to 1 (delivered) in the database
        return redirect(url_for('vendor_order'))

    return render_template('vendor/order.html', orders=orders, vendor_name=vendor_name)


@app.route('/vendor_add_product', methods=['GET', 'POST'])
def vendor_add_product():
    vendor_id = session['id']
    vendor_name = get_vendor_name(vendor_id)
    if request.method == 'POST':
        category = request.form.get('category')
        category_id = get_category_id(category)
        product_name = request.form.get('product_name')
        origin_price = float(request.form.get('origin_price'))
        discount_checkbox = request.form.get('discount_checkbox')
        product_discount_status = 0
        if discount_checkbox == 'on':
         product_discount_status = 1
        current_price = float(request.form.get('current_price')) if discount_checkbox else origin_price
        discount_deadline = request.form.get('discount_deadline') if discount_checkbox else None
        product_description = request.form.get('product_description')
        image = request.files['image']

        if image and allowed_file(image.filename):
          filename = secure_filename(image.filename)
          image.path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
          image.save(image.path)

        product = Product(
          id=None,
          category_id=category_id,
          vendor_id=vendor_id,
          product_name=product_name,
          product_desc=product_description,
          product_price=origin_price,
          product_img=image.path,
          product_discount_status=product_discount_status,
          product_discount_price=current_price,
          product_discount_deadline=discount_deadline,
          product_like=0,
          product_dislike=0
        )
        print(product)
        add_product(product)
        return redirect(url_for('vendor_index', vendor_id=vendor_id))
    return render_template('vendor/add_product.html', view_vendor_id=vendor_id, vendor_name=vendor_name)


@app.route('/vendor_edit_product', methods=['GET', 'POST'])
def vendor_edit_product():
    vendor_id = session['id']
    vendor_name = get_vendor_name(vendor_id)
    if request.method == 'POST':
        product_id = request.form.get('product_id')
        product_description = request.form.get('product_description')
        origin_price = float(request.form.get('origin_price'))
        discount_checkbox = request.form.get('discount_checkbox')
        product_discount_status = 0
        if discount_checkbox == 'on':
            product_discount_status = 1
        current_price = float(request.form.get('current_price')) if discount_checkbox else origin_price
        discount_deadline = request.form.get('discount_deadline') if discount_checkbox else None

        edit_product(product_id, product_description, origin_price, product_discount_status, current_price,
                     discount_deadline)

        return redirect(url_for('vendor_index', vendor_id=vendor_id))
    else:
        product_id = request.args.get('product_id')
        product = get_product_by_id(product_id)
        if product:
            return render_template('vendor/edit_product.html', product=product, vendor_name=vendor_name)


@app.route('/vendor_delete_product/<product_id>')
def vendor_delete_product(product_id):
    vendor_id = session['id']
    delete_product(product_id)
    delete_product_order(product_id)
    delete_product_cart(product_id)

    return redirect(url_for('vendor_index', vendor_id=vendor_id))


if __name__ == '__main__':
    app.run(debug=True)
