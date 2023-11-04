class Cart:
    def __init__(self, id, customer_id, product_id, product_amount):
        self.id = id
        self.customer_id = customer_id
        self.product_id = product_id
        self.product_amount = product_amount


class Category:
    def __init__(self, id, category_name):
        self.id = id
        self.category_name = category_name


class Customer:
    def __init__(self, id, customer_name, customer_phone, customer_email, customer_address, customer_password):
        self.id = id
        self.customer_name = customer_name
        self.customer_phone = customer_phone
        self.customer_email = customer_email
        self.customer_address = customer_address
        self.customer_password = customer_password


class Feedback:
    def __init__(self, id, customer_id, product_id, feedback_time, feedback_content):
        self.id = id
        self.customer_id = customer_id
        self.product_id = product_id
        self.feedback_time = feedback_time
        self.feedback_content = feedback_content


class Order:
    def __init__(self, id, product_id, vendor_id, customer_id, product_amount, order_create_time, order_total,
                 order_status):
        self.id = id
        self.product_id = product_id
        self.vendor_id = vendor_id
        self.customer_id = customer_id
        self.product_amount = product_amount
        self.order_create_time = order_create_time
        self.order_total = order_total
        self.order_status = order_status


class Product:
    def __init__(self, id, category_id, vendor_id, product_name, product_desc, product_price, product_img,
                 product_discount_status, product_discount_price, product_discount_deadline, product_like,
                 product_dislike):
        self.id = id
        self.category_id = category_id
        self.vendor_id = vendor_id
        self.product_name = product_name
        self.product_desc = product_desc
        self.product_price = product_price
        self.product_img = product_img
        self.product_discount_status = product_discount_status
        self.product_discount_price = product_discount_price
        self.product_discount_deadline = product_discount_deadline
        self.product_like = product_like
        self.product_dislike = product_dislike


class Vendor:
    def __init__(self, id, vendor_name, vendor_phone, vendor_email, vendor_address, vendor_password):
        self.id = id
        self.vendor_name = vendor_name
        self.vendor_phone = vendor_phone
        self.vendor_email = vendor_email
        self.vendor_address = vendor_address
        self.vendor_password = vendor_password

