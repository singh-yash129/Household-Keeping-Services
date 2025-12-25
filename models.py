from config import *
from datetime import datetime

class User(db.Model,UserMixin):
    __tablename__ = 'users'
    username = db.Column(db.String, primary_key=True, nullable=False, unique=True)
    email_id = db.Column(db.String, nullable=False, unique=True)
    department = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    services_code = db.Column(db.String, nullable=False)
    gstin_no = db.Column(db.String, default='xxxx-xxxx-xxxx')
    uan_no = db.Column(db.String, default='xxxx-xxxx-xxxx')
    identification_pic = db.Column(db.String)
    account_creation_date = db.Column(db.String, nullable=False, default=datetime.utcnow)
    two_factor_authentication = db.Column(db.Integer,default='False')
    visibilty=db.Column(db.String,default=True)
    activity=db.Column(db.String,default='offline',nullable=False)
    admin_data=db.Column(db.String)
    passcode=db.Column(db.Integer,default=0)
    rating = db.Column(db.Integer)
    services = db.relationship('Service_request', backref='user', lazy=True)
    notifications = db.relationship('Notify', backref='user', lazy=True)
    orders = db.relationship('Order', backref='user', lazy=True)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def get_id(self):
        return self.username 
    


class Notify(db.Model):
    __tablename__ = 'notification'
    noti_id = db.Column(db.String, primary_key=True, nullable=False, unique=True)
    noti_data = db.Column(db.String, nullable=False)
    user_id = db.Column(db.String, db.ForeignKey('users.username'), nullable=False)
    noti_markdown = db.Column(db.DateTime, default=datetime.utcnow)

class Order(db.Model):
    __tablename__ = 'orders'
    order_id = db.Column(db.String, primary_key=True, nullable=False)
    user_id = db.Column(db.String, db.ForeignKey('users.username'), nullable=False)
    service_id = db.Column(db.String, db.ForeignKey('service_request_form.request_id'), nullable=False)
    address_id = db.Column(db.String, db.ForeignKey('address.address_id'), nullable=False)   
    rating = db.Column(db.Integer)
    order_status = db.Column(db.String, nullable=False)
    feedback = db.Column(db.String)
    tracks = db.relationship("Track", back_populates="order", cascade="all, delete-orphan")
    

    service_request = db.relationship("Service_request", back_populates="orders")
    address = db.relationship("Address", back_populates="orders") 

class Payments(db.Model):
    __tablename__ = 'payments'
    transaction_id = db.Column(db.String, primary_key=True, nullable=False)
    user_id = db.Column(db.String, db.ForeignKey('users.username'), nullable=False)
    order_id = db.Column(db.String, db.ForeignKey('orders.order_id'), nullable=False)
    payment_mode = db.Column(db.String, nullable=False)
    payment_amount = db.Column(db.Float, nullable=False)
    payment_status = db.Column(db.String, nullable=False)
    payment_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    

class Help(db.Model):
    __tablename__ = 'help'
    email_id = db.Column(db.String, db.ForeignKey('users.email_id'), nullable=False)
    Name = db.Column(db.String, nullable=False)
    problem = db.Column(db.String, nullable=False)
    subject = db.Column(db.String, nullable=False)
    status = db.Column(db.String, nullable=False)
    help_date = db.Column(db.DateTime, default=datetime.utcnow)
    issue_id = db.Column(db.String, primary_key=True, nullable=False, unique=True)

class CartItem(db.Model):
    __tablename__ = 'cart_items'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    item_id = db.Column(db.String, nullable=False, unique=True)
    cart_id = db.Column(db.String,  nullable=False)
    user_id = db.Column(db.String, db.ForeignKey('users.username'), nullable=False)
    price = db.Column(db.String, nullable=False)



class Address(db.Model):
    __tablename__ = 'address'
    address_count_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    address_id = db.Column(db.String, nullable=False, unique=True)
    pincode = db.Column(db.String, nullable=False)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    address_description = db.Column(db.String, nullable=False)
    landmark = db.Column(db.String, nullable=False)
    user_id = db.Column(db.String, db.ForeignKey('users.username'), nullable=False)
    contact_num = db.Column(db.String)
    alternate_num = db.Column(db.String)
    city = db.Column(db.String)
    state = db.Column(db.String)
    country = db.Column(db.String)

    user = db.relationship('User', backref=db.backref('addresses', lazy=True)) 
    orders = db.relationship("Order", back_populates="address") 


class ProfileUpdate(db.Model):
    __tablename__ = 'profile_update'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    owner_name = db.Column(db.String)
    manager_name = db.Column(db.String)
    mobile_number = db.Column(db.String, nullable=False)
    alternate_number = db.Column(db.String, nullable=True)
    street_address = db.Column(db.String, nullable=False)
    city = db.Column(db.String, nullable=False)
    state = db.Column(db.String, nullable=False)
    country = db.Column(db.String, nullable=False)
    pincode = db.Column(db.String, nullable=False)
    landmarks = db.Column(db.String, nullable=True)
    user_id = db.Column(db.String, db.ForeignKey('users.username'), nullable=False)

    user = db.relationship('User', backref=db.backref('profile_updates', lazy=True))

    def __repr__(self):
        return f'<ProfileUpdate {self.id}>'
class VerifyAccount(db.Model):
    __tablename__ = 'verify_account'
    user_id = db.Column(db.String, db.ForeignKey('users.username'), nullable=False)
    user = db.relationship('User', backref=db.backref('verify_accounts', lazy=True))  
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    gst_file = db.Column(db.String)
    uan_file = db.Column(db.String)
    business_reg_file = db.Column(db.String)
    income_tax_file = db.Column(db.String)
    status=db.Column(db.String())

class Track(db.Model):
    __tablename__ = 'track_update'

    id = db.Column(db.Integer, primary_key=True)  
    order_id = db.Column(db.String, db.ForeignKey('orders.order_id'), nullable=False)  
    helper_contact = db.Column(db.String(15))  
    helper_name = db.Column(db.String(255))  
    status = db.Column(db.String(255)) 
    address = db.Column(db.String(255)) 
    estimated_time = db.Column(db.String)  
    transaction_id = db.Column(db.String(255))  


    order = db.relationship("Order", back_populates="tracks")

class Rate(db.Model):
    __tablename__='rating'
  
    rate=db.Column(db.Integer)
    feedback=db.Column(db.String)
    id=db.Column(db.Integer,autoincrement=True,primary_key=True)
    item_id = db.Column(db.String, db.ForeignKey('service_request_form.service_providing_code'))



class Service_request(db.Model):
    __tablename__ = 'service_request_form'
    service_name = db.Column(db.String, nullable=False, unique=True)
    request_id = db.Column(db.String, primary_key=True, nullable=False, unique=True)
    service_description = db.Column(db.String, nullable=False)
    servicable_pincode = db.Column(db.String, nullable=False)
    contact_email = db.Column(db.String, nullable=False)
    contact_phone = db.Column(db.String, nullable=False)
    service_category = db.Column(db.String, nullable=False)
    status = db.Column(db.String)
    brand_logo = db.Column(db.String)
    pricing = db.Column(db.String)
    prev_Work_images = db.Column(db.String)
    currency = db.Column(db.String)
    country_code = db.Column(db.String)
    request_date = db.Column(db.DateTime, default=datetime.utcnow)
    service_providing_code = db.Column(db.String)
    avg_rate=db.Column(db.String)
    user_id = db.Column(db.String, db.ForeignKey('users.username'), nullable=False)
    orders = db.relationship("Order", back_populates="service_request")



