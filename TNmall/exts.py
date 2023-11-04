import mysql.connector
from models import Cart, Category, Customer, Feedback, Order, Product, Vendor

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

db = mysql.connector.connect(
    host='localhost',
    user='root',
    password='20010428',
    database='wad'
)
cursor = db.cursor()


# Login, register
def login_user(customer_email):
    cursor.execute("SELECT customer_password FROM `customer` WHERE customer_email = %s", (customer_email,))
    check_password = cursor.fetchone()
    if check_password:
        return check_password[0]
    else:
        return None


def register_user(customer):
    cursor.execute(
        "INSERT INTO `customer` (customer_name, customer_phone, customer_email, customer_address, customer_password) "
        "VALUES (%s,  %s, %s, %s, %s)",
        (customer.customer_name, customer.customer_phone, customer.customer_email, customer.customer_address,
         customer.customer_password))
    db.commit()


def get_customer_id(customer_email):
    cursor.execute("SELECT id FROM `customer` WHERE customer_email = %s", (customer_email,))
    customer_id = cursor.fetchone()
    return customer_id[0]


def get_customer_name(customer_email):
    cursor.execute("SELECT customer_name FROM `customer` WHERE customer_email = %s", (customer_email,))
    customer_name = cursor.fetchone()
    if customer_name:
      return customer_name[0]
    else:
      None


def login_vendor(vendor_email):
    cursor.execute("SELECT vendor_password FROM `vendor` WHERE vendor_email = %s", (vendor_email,))
    check_password = cursor.fetchone()
    if check_password:
        return check_password[0]
    else:
        return None


def register_vendor(vendor):
    cursor.execute(
        "INSERT INTO `vendor` (vendor_name, vendor_phone, vendor_email, vendor_address, vendor_password) "
        "VALUES (%s,  %s, %s, %s, %s)",
        (vendor.vendor_name, vendor.vendor_phone, vendor.vendor_email, vendor.vendor_address,
         vendor.vendor_password,))
    db.commit()


def get_vendor_id(vendor_email):
    cursor.execute("SELECT id FROM `vendor` WHERE vendor_email = %s", (vendor_email,))
    vendor_id = cursor.fetchone()
    if vendor_id is not None:
      return vendor_id[0]
    else:
      return None


def get_vendor_name(vendor_id):
    cursor.execute("SELECT vendor_name FROM `vendor` WHERE id = %s", (vendor_id,))
    vendor_name = cursor.fetchone()
    if vendor_name is not None:
      return vendor_name[0]
    else:
      return None


# index
def on_sales_product():
    cursor.execute("SELECT * FROM `product` WHERE product_discount_status = %s", (1,))
    discount_products = cursor.fetchall()

    discount_products_list = []
    for product in discount_products:
        product_dict = {
            'id': product[0],
            'category_id': product[1],
            'vendor_id': product[2],
            'product_name': product[3],
            'product_desc': product[4],
            'product_price': product[5],
            'product_img': product[6],
            'product_discount_status': product[7],
            'product_discount_price': product[8],
            'product_discount_deadline': product[9],
            'product_like': product[10],
            'product_dislike': product[11]
        }
        discount_products_list.append(product_dict)

    return discount_products_list


def get_products_by_category(category_id):
    cursor.execute("SELECT p.*, COALESCE(MAX(f.feedback_time), '1970-01-01') AS latest_feedback_time " 
                   "FROM product p LEFT JOIN feedback f ON p.id = f.product_id " 
                   "WHERE p.category_id = %s " 
                   "GROUP BY p.id " 
                   "ORDER BY latest_feedback_time DESC", (category_id,))
    products = cursor.fetchall()

    products_list = []
    for product in products:
        product_dict = {
            'id': product[0],
            'category_id': product[1],
            'vendor_id': product[2],
            'product_name': product[3],
            'product_desc': product[4],
            'product_price': product[5],
            'product_img': product[6],
            'product_discount_status': product[7],
            'product_discount_price': product[8],
            'product_discount_deadline': product[9],
            'product_dislike': product[10],
            'product_like': product[11]
        }
        products_list.append(product_dict)

    return products_list


def search_products(keyword):
    select_query = "SELECT p.*, COALESCE(MAX(f.feedback_time), '1970-01-01') AS latest_feedback_time " \
                   "FROM product p LEFT JOIN feedback f ON p.id = f.product_id " \
                   "WHERE p.product_name LIKE %s " \
                   "GROUP BY p.id " \
                   "ORDER BY latest_feedback_time DESC"
    keyword = f"%{keyword}%"
    cursor.execute(select_query, (keyword,))

    products = []
    for product_data in cursor.fetchall():
        product_dict = {
            'id': product_data[0],
            'category_id': product_data[1],
            'vendor_id': product_data[2],
            'product_name': product_data[3],
            'product_desc': product_data[4],
            'product_price': product_data[5],
            'product_img': product_data[6],
            'product_discount_status': product_data[7],
            'product_discount_price': product_data[8],
            'product_discount_deadline': product_data[9],
            'product_dislike': product_data[10],
            'product_like': product_data[11]
        }
        products.append(product_dict)

    return products


def add_to_cart_db(customer_id, product_id, product_amount):
    insert_query = "INSERT INTO cart (customer_id, product_id, product_amount) VALUES (%s, %s, %s)"
    cursor.execute(insert_query, (customer_id, product_id, product_amount))
    db.commit()


def get_user_cart_items(customer_id):
    select_query = "SELECT * FROM cart WHERE customer_id = %s"
    cursor.execute(select_query, (customer_id,))

    cart_items = []
    for cart_data in cursor.fetchall():
        cart_item = Cart(*cart_data)
        product_id = cart_item.product_id
        product = buy_get_product_by_id(product_id)
        if product['vendor_id']:
            vendor = buy_get_vendor_by_id(product['vendor_id'])
        else:
            vendor = None
        cart_item.product = product
        cart_item.vendor = vendor
        cart_items.append(cart_item)

    return cart_items


def buy_get_product_by_id(product_id):
    select_query = "SELECT p.*, CASE WHEN p.product_discount_status = 1 THEN p.product_discount_price " \
                   "ELSE p.product_price END AS price FROM product p WHERE p.id = %s"
    cursor.execute(select_query, (product_id,))

    product_data = cursor.fetchone()
    if product_data:
        product_dict = {
            'id': product_data[0],
            'category_id': product_data[1],
            'vendor_id': product_data[2],
            'product_name': product_data[3],
            'product_desc': product_data[4],
            'product_price': product_data[12],
            'product_img': product_data[6],
            'product_discount_status': product_data[7],
            'product_discount_price': product_data[8],
            'product_discount_deadline': product_data[9],
            'product_like': product_data[10],
            'product_dislike': product_data[11]
        }
    else:
        product_dict = None

    return product_dict


def buy_get_vendor_by_id(vendor_id):
    select_query = "SELECT * FROM vendor WHERE id = %s"
    cursor.execute(select_query, (vendor_id,))
    vendor_data = cursor.fetchone()
    if vendor_data:
        vendor_dict = {
            'id': vendor_data[0],
            'vendor_name': vendor_data[1],
            'vendor_address': vendor_data[2],
            'vendor_phone': vendor_data[3],
            'vendor_email': vendor_data[4]
        }
        return vendor_dict
    return None


def get_cart_item_by_id(customer_id, cart_item_id):
    select_query = "SELECT * FROM cart WHERE customer_id = %s AND id = %s"
    cursor.execute(select_query, (customer_id, cart_item_id))
    cart_item_data = cursor.fetchone()

    if cart_item_data:
        cart_item = Cart(
            id=cart_item_data[0],
            customer_id=cart_item_data[1],
            product_id=cart_item_data[2],
            product_amount=cart_item_data[3]
        )
        return cart_item

    return None


def create_order_db(order):
    insert_query = "INSERT INTO `order` (product_id, vendor_id, customer_id, product_amount, order_create_time, " \
                   "order_total, order_status) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    cursor.execute(insert_query, (
        order.product_id, order.vendor_id, order.customer_id, order.product_amount, order.order_create_time,
        order.order_total, order.order_status))
    db.commit()

    order_id = cursor.lastrowid

    return order_id


def delete_cart_item_db(customer_id, cart_item_id):
    delete_query = "DELETE FROM cart WHERE customer_id = %s AND id = %s"
    cursor.execute(delete_query, (customer_id, cart_item_id))
    db.commit()


def get_user_orders(customer_id):
    select_query = "SELECT * FROM `order` WHERE customer_id = %s"
    cursor.execute(select_query, (customer_id,))

    orders = []
    for order_data in cursor.fetchall():
        order = Order(*order_data)
        product_id = order.product_id
        vendor_id = order.vendor_id
        product = buy_get_product_by_id(product_id)
        vendor = buy_get_vendor_by_id(vendor_id)
        order.product = product
        order.vendor = vendor
        orders.append(order)

    return orders


def get_product_by_id(product_id):
    select_query = "SELECT p.*, c.category_name, v.vendor_name, " \
                   "CASE WHEN p.product_discount_status = 1 THEN p.product_discount_price " \
                   "ELSE p.product_price END AS product_current_price " \
                   "FROM product p " \
                   "INNER JOIN category c ON p.category_id = c.id " \
                   "INNER JOIN vendor v ON p.vendor_id = v.id " \
                   "WHERE p.id = %s"
    cursor.execute(select_query, (product_id,))

    product_data = cursor.fetchone()
    if product_data:
        product_dict = {
            'id': product_data[0],
            'category_id': product_data[1],
            'vendor_id': product_data[2],
            'product_name': product_data[3],
            'product_desc': product_data[4],
            'product_price': product_data[5],
            'product_img': product_data[6],
            'product_discount_status': product_data[7],
            'product_discount_price': product_data[8],
            'product_discount_deadline': product_data[9],
            'product_dislike': product_data[10],
            'product_like': product_data[11],
            'category_name': product_data[12],
            'vendor_name': product_data[13],
            'product_current_price': product_data[14],
        }
    else:
        product_dict = None

    return product_dict


def update_like_count(product_id):
    update_query = "UPDATE product SET product_like = product_like + 1 WHERE id = %s"
    cursor.execute(update_query, (product_id,))
    db.commit()


def update_dislike_count(product_id):
    update_query = "UPDATE product SET product_dislike = product_dislike + 1 WHERE id = %s"
    cursor.execute(update_query, (product_id,))
    db.commit()


def get_comment_by_id(product_id):
    select_query = "SELECT f.*, c.customer_name FROM feedback f INNER JOIN customer c " \
                   "ON f.customer_id = c.id WHERE f.product_id = %s ORDER BY f.feedback_time DESC"
    cursor.execute(select_query, (product_id,))

    feedbacks = cursor.fetchall()
    feedback_list = []
    for feedback in feedbacks:
        comment_dict = {
            'id': feedback[0],
            'product_id': feedback[1],
            'customer_id': feedback[2],
            'feedback_time': feedback[3],
            'feedback_content': feedback[4],
            'customer_name': feedback[5]
        }
        feedback_list.append(comment_dict)

    return feedback_list


def save_feedback(customer_id, product_id, feedback_time, feedback_content):
    insert_query = "INSERT INTO feedback (customer_id, product_id, feedback_time, feedback_content) " \
                   "VALUES (%s, %s, %s, %s)"
    values = (customer_id, product_id, feedback_time, feedback_content)
    cursor.execute(insert_query, values)

    db.commit()


def get_image_by_id(product_id):
    cursor.execute("SELECT product_img FROM product WHERE product_id = %s", (product_id,))
    img = cursor.fetchone()

    return img


# Vendor
def show_vendor_products(vendor_id):
    cursor.execute("SELECT product.*, category.category_name FROM product INNER JOIN category "
                   "ON product.category_id = category.id WHERE vendor_id = %s", (vendor_id,))
    products = cursor.fetchall()

    products_list = []
    for product in products:
        product_dict = {
            'id': product[0],
            'category_id': product[1],
            'vendor_id': product[2],
            'product_name': product[3],
            'product_desc': product[4],
            'product_price': product[5],
            'product_img': product[6],
            'product_discount_status': product[7],
            'product_discount_price': product[8],
            'product_discount_deadline': product[9],
            'product_like': product[10],
            'product_dislike': product[11],
            'category_name': product[12],
        }
        products_list.append(product_dict)

    return products_list


def get_category_id(category_name):
    cursor.execute("SELECT id FROM `category` WHERE category_name = %s", (category_name,))
    category_id = cursor.fetchone()
    if category_id is not None:
      return category_id[0]
    else:
      return None


def add_product(product):
    sql = '''
            INSERT INTO `product` (category_id, vendor_id, product_name, product_desc, product_price, 
                                  product_img, product_discount_status, product_discount_price, 
                                  product_discount_deadline, product_like, product_dislike)
            VALUES (%(category_id)s, %(vendor_id)s, %(product_name)s, %(product_desc)s, %(product_price)s, 
                    %(product_img)s, %(product_discount_status)s, %(product_discount_price)s, 
                    %(product_discount_deadline)s, %(product_like)s, %(product_dislike)s)
        '''

    product_data = {
        'category_id': product.category_id,
        'vendor_id': product.vendor_id,
        'product_name': product.product_name,
        'product_desc': product.product_desc,
        'product_price': product.product_price,
        'product_img': product.product_img,
        'product_discount_status': product.product_discount_status,
        'product_discount_price': product.product_discount_price,
        'product_discount_deadline': product.product_discount_deadline,
        'product_like': product.product_like,
        'product_dislike': product.product_dislike
    }
    cursor.execute(sql, product_data)
    db.commit()


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def edit_product(product_id, product_description, origin_price, product_discount_status, current_price,
                 discount_deadline):
    update_query = "UPDATE product SET product_desc=%s, product_price=%s, product_discount_status=%s, " \
                   "product_discount_price=%s, product_discount_deadline=%s WHERE id=%s"
    cursor.execute(update_query,
                   (product_description, origin_price, product_discount_status, current_price, discount_deadline,
                    product_id))
    db.commit()


def delete_product(product_id):
    cursor.execute("DELETE FROM `product` WHERE id = %s", (product_id,))
    db.commit()


def delete_product_cart(product_id):
    cursor.execute("DELETE FROM `cart` WHERE id = %s", (product_id,))
    db.commit()


def delete_product_order(product_id):
    cursor.execute("DELETE FROM `order` WHERE id = %s", (product_id,))
    db.commit()


# vendor's order
def get_orders_for_vendor(vendor_id):
    cursor.execute("SELECT `order`.*, customer.customer_name, customer.customer_phone, customer.customer_address, "
                   "product.product_name, product.product_img FROM `order` INNER JOIN customer "
                   "ON `order`.customer_id = customer.id INNER JOIN product ON `order`.product_id = product.id "
                   "WHERE `order`.vendor_id = %s", (vendor_id,))
    orders = cursor.fetchall()
    order_list = []
    for order in orders:
        order_dict = {
            'id': order[0],
            'product_id': order[1],
            'vendor_id': order[2],
            'customer_id': order[3],
            'product_amount': order[4],
            'order_create_time': order[5],
            'order_total': order[6],
            'order_status': order[7],
            'customer_name': order[8],
            'customer_phone': order[9],
            'customer_address': order[10],
            'product_name': order[11],
            'product_img': order[12]
        }
        order_list.append(order_dict)
    return order_list


def update_order_status(order_id, new_status):
    update_query = "UPDATE `order` SET order_status = %s WHERE id = %s"
    cursor.execute(update_query, (new_status, order_id))
    db.commit()


def get_pending_orders(vendor_id):
    select_query = "SELECT * FROM `order` WHERE vendor_id = %s AND order_status = 0"
    cursor.execute(select_query, (vendor_id,))
    orders = cursor.fetchall()
    return orders

