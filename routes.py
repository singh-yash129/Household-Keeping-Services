from models import *
import os

@login_manager.user_loader
def load_user(username):
    return User.query.get(username)

def save_file(file):
    if file:
        filename = file.filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        return filepath
    else:
        return None

@app.route("/logout")
@login_required
def logout():
    user=User.query.filter_by(username=current_user.username).first()
    user.activity='offline'
    db.session.commit()
    logout_user() 
    session.pop('user_id', None)
    return redirect(url_for('login'))

def send_otp(email, otp):
    msg = Message('OTP-Verification', recipients=[email])
    msg.body = f'Your verification code is: {otp}. Please enter this code on the website to confirm your identity. This code will expire in 10 minutes. For security, never share this code with anyone.'
    mail.send(msg)


@app.route('/')
def home_page():
    return render_template('home.html')


def is_strong_password(password):
    return (len(password) >= 8 and 
            re.search(r"[A-Za-z]", password) and 
            re.search(r"\d", password) and 
            re.search(r"[!@#$%^&*(),.?\":{}|<>]", password))


@app.route("/login", methods=['GET', 'POST'])
def login():
    login_manager.login_view = 'login'
    if request.method == 'POST':
        username = request.form['uname']
        password = request.form['psw']
        slider_value = request.form['slider_value']
        user_admin_value = request.form['user_admin_value']
        
        user = User.query.filter((User.username == username) | (User.email_id == username)).first()
        if user_admin_value.lower() == 'admin':
            if username == os.getenv('ADMIN_USERNAME') and password == os.getenv('ADMIN_PASSWORD'):
                return redirect(url_for('admin_dashboard'))
            else:
                return jsonify({"error": "!! Invalid Credential !!"}), 400

        elif user_admin_value.lower() == 'user':
            if user and user.check_password(password) and slider_value.lower() == user.department:
                if user.admin_data == 'deactivate':
                    return jsonify({"error": "Your account is temporarily banned by Admin"}), 400

                if user.two_factor_authentication == 'True':
                    if 'inp-1' in request.form:
                        verify_2fa = ''.join(request.form.get(f'inp-{i}', '') for i in range(1, 7))
                        if int(verify_2fa) == user.passcode:
                            login_user(user)
                            user.activity = 'online'
                            db.session.commit()
                            return redirect(url_for(f'{slider_value.lower()}_dashboard', user=user.username))
                        else:
                            return jsonify({"error": "Invalid 2FA code!"}), 400
                    else:
                        return render_template("login.html", user=user)
                else:
                    login_user(user)
                    user.activity = 'online'
                    db.session.commit()
                    return redirect(url_for(f'{slider_value.lower()}_dashboard', user=user.username))
            else:
                return jsonify({"error": "!! Invalid Credential !!"}), 400

    return render_template("login.html", user=current_user)

@app.route('/admin_dashboard')
def admin_dashboard():
    service=Service_request.query.all()
    return render_template('admin_dashboard.html',service=service)

@app.route('/registration/<string:data>', methods=['GET', 'POST'])
def registration(data):
    if request.method == "POST":
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        cnf_password = request.form.get('cnf-password')
        gst_in = request.form.get('gstin') if data == 'professional' else None
        uan = request.form.get('uan_no') if data == 'professional' else None

    
        if not re.fullmatch(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$', password):
            return jsonify({"error": "Password must be at least 8 characters, include letters, numbers, and special characters."}), 400


        if password != cnf_password:
            return jsonify({"error": "Passwords do not match."}), 400

       
        if User.query.filter_by(email_id=email.lower()).first():
            return jsonify({"error": "Email is already registered."}), 400
        if User.query.filter_by(username=username).first():
            return jsonify({"error": "Username is already taken."}), 400
        if gst_in and User.query.filter_by(gstin_no=gst_in).first():
            return jsonify({"error": "GST number is already registered."}), 400
        if uan and User.query.filter_by(uan_no=uan).first():
            return jsonify({"error": "UAN number is already registered."}), 400

     
        otp = ''.join(random.choices('0123456789', k=6))
        send_otp(email, otp)

        session['new_user'] = {
            'username': username,
            'email_id': email.lower(),
            'department': 'professional' if data == 'professional' else 'customer',
            'password':password,
            'gstin_no': gst_in,
            'uan_no': uan,
            'services_code': str(uuid.uuid4()),
            'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        print(session['new_user'])
        session['otp'] = otp
        session['otp_time'] = datetime.now()

        return redirect(url_for('otp_verification'))

    return render_template("sign-up.html")

@app.route("/otp-verification", methods=['GET', 'POST'])
def otp_verification():
    if request.method == 'POST':
        entered_otp = ''.join(request.form.get(f'otp{i}', '') for i in range(1, 7))
        otp = session.get('otp')
        otp_time = session.get('otp_time')

        if entered_otp == otp:
            otp_time = otp_time.replace(tzinfo=pytz.utc)
            current_time = datetime.now(pytz.utc)
            elapsed_time = current_time - otp_time
            if elapsed_time > timedelta(minutes=10):
                return render_template("otp.html")

            session.pop('otp', None)
            session.pop('otp_time', None)

       
            new_user_data = session.get('new_user')
            print(new_user_data)
            user = User(
                account_creation_date=new_user_data['created_at'],
                username=new_user_data['username'],
                email_id=new_user_data['email_id'],
                department=new_user_data['department'],
                gstin_no=new_user_data['gstin_no'],
                uan_no=new_user_data['uan_no'],
                services_code=new_user_data['services_code']
            )
            user.set_password(new_user_data['password'])
            db.session.add(user)
            db.session.commit()


            print("User successfully added to the database.")
            return redirect(url_for('login'))

        print("Invalid OTP entered.")
        return render_template("otp.html")

    return render_template("otp.html")




def allowed_file(filename):
    """Check if the file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']



@app.route('/<username>/service_form', methods=["GET", "POST"])
@login_required
def service_form(username):
    if request.method == 'POST':
        
        service_name = request.form['service-name']
        service_description = request.form['service-description']
        servicable_pincodes = request.form['servicable-pincode'].split(',')       
        pricing = request.form['pricing']
        contact_email = request.form['contact-email']
        contact_phone = request.form['contact-phone']
        service_category = request.form['service-category']
        country_code = request.form['countryCode']
        currency = request.form['currency']
        createdAt = datetime.utcnow()

        brand_logo = request.files.get('brand-logo')
        if brand_logo and allowed_file(brand_logo.filename):
            brand_logo_filename = secure_filename(brand_logo.filename)
            brand_logo.save(os.path.join(app.config['UPLOAD_FOLDER'], brand_logo_filename))
        else:
            flash('Invalid brand logo file', 'error')
            return redirect(request.url)

        prev_work_images = []
        if 'work-images' in request.files:
            for file in request.files.getlist('work-images'):
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    prev_work_images.append(filename)

        servicable_pincodes_str = ','.join(servicable_pincodes)  
        prev_work_images_str = ','.join(prev_work_images)  

        serve_req = Service_request(
            service_name=service_name,
            request_id=str(uuid.uuid4()),
            servicable_pincode=servicable_pincodes_str,  
            contact_email=contact_email,
            contact_phone=contact_phone,
            service_category=service_category,
            status='pending',
            brand_logo=brand_logo_filename,
            prev_Work_images=prev_work_images_str,  
            currency=currency,
            country_code=country_code,
            service_description=service_description,
            request_date=createdAt,
            user_id=username,
            pricing=pricing,
            service_providing_code=str(uuid.uuid4())
        )

        db.session.add(serve_req)
        db.session.commit()

        flash('Service request submitted successfully', 'success')
        return render_template('service_form.html', username=username)
    
    return render_template('service_form.html', username=username)




@app.route('/<username>/add_to_cart/<service_providing_code>',methods=['GET','POST'])
@login_required
def add_to_cart(service_providing_code,username):
    item = Service_request.query.filter_by(service_providing_code=service_providing_code).filter_by(status='approved').first()
    cart_item_addition=CartItem(
        item_id = item.service_providing_code,
        user_id=username,
        price=item.pricing,
        cart_id=str(uuid.uuid4())
    )
    db.session.add(cart_item_addition)
    db.session.commit()
    return redirect(url_for('cart',username=username))


@app.route('/<item_id>/<user_id>/<cart_id>/remove',methods=['GET',"POST"])
@login_required
def remove_cart_item(item_id,user_id,cart_id):
    item_data=CartItem.query.filter_by(item_id=item_id).filter_by(user_id=user_id).filter_by(cart_id=cart_id).first()
    db.session.delete(item_data)
    db.session.commit()
    return redirect(url_for('cart',username=user_id))
@app.route('/add_new_address/<user>',methods=['GET',"POST"])
@login_required
def add_new_address(user):
    if request.method == 'POST':

        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        mobile_number = request.form['mobileNumber']
        alternate_number = request.form.get('alternateNumber')
        street_address = request.form['streetAddress']
        city = request.form['city']
        state = request.form['state']
        country = request.form['country']
        pincode = request.form['pincode']
        landmarks = request.form.get('landmarks')

        add=Address(
            first_name=first_name,
            last_name=last_name,
            address_id=str(uuid.uuid4()),
            contact_num=mobile_number,
            alternate_num=alternate_number,
            address_description=street_address,
            city=city,
            state=state,
            country=country,
            pincode=pincode,
            landmark=landmarks, 
            user_id=user 
        )
    db.session.add(add)
    db.session.commit()
    return redirect(url_for('cart',username=user))    
@app.route('/<cart_id>/<user_id>/transaction', methods=['POST','GET'])
@login_required
def transaction_data(cart_id, user_id):
    if request.method =='POST':
        selected_item_ids = request.form.get('selected_items')
        address = request.form.get('address_1')
        total = request.form.get('total')
        payment_mode = request.form.get('c-dmode','cod')
        print(selected_item_ids,address,total,payment_mode)
        if not selected_item_ids or not address or not total or not payment_mode:
            flash('All fields are required.', 'error')
            return redirect(request.referrer)
    
        for item_id in selected_item_ids.split(','):
            print(item_id)
            order = Order(
                order_id=str(uuid.uuid4()),
                user_id=user_id,
                service_id=item_id,
                address_id=address,
                order_status='pending'
            )
            payment = Payments(
                transaction_id=str(uuid.uuid4()),
                user_id=user_id,
                order_id=order.order_id,
                payment_amount=total,
                payment_mode=payment_mode,
                payment_status='pending' if payment_mode == 'cod' else 'paid',
                payment_date=datetime.utcnow()
            )
            cart_item = CartItem.query.filter_by(user_id=user_id, item_id=item_id).first()
            print(cart_item)
            db.session.delete(cart_item)
            db.session.add_all([order, payment])
        db.session.commit()
        return redirect(url_for('customer_dashboard', user=user_id))

@app.route('/help', methods=["GET", "POST"]) 
def help():
    if request.method == 'POST':
        email = request.form['email']
        description = request.form['description']
        issue = request.form['issue']
        name = request.form['name']
    

        help_entry = Help(
            issue_id = str(uuid.uuid4()),
            problem=description,
            email_id=email,
            help_date=datetime.utcnow(),
            Name=name,
            subject=issue,
            status='pending'
        )
        db.session.add(help_entry)
        db.session.commit()
        return render_template('success.html', data='Your request has been generated. We will fix it soon.', id=help_entry.issue_id)
    return render_template('help.html')


@app.route('/about')
def about():
    return render_template('about.html')
@app.route('/privacy_policy')
def privacy_policy():
    return render_template('privacy.html')
@app.route('/learn')
def learn():
    return render_template('learn.html')
@app.route('/customer_dashboard/<user>',methods=['GET',"POST"])
@login_required
def customer_dashboard(user):
    inf=User.query.filter_by(username=user).first()
    data = ProfileUpdate.query.filter_by(user_id=user).first()
    print(inf)
    if request.method == "POST":
        if 'visibility' in request.form:
            visibility = request.form['visibility']
            inf.visibility = visibility
            db.session.commit()
            flash('Profile visibility updated successfully', 'success')   

        elif 'setup' in request.form:
            print('clicked')
            passcode = ''.join(request.form.get(f'inp_{i}', '') for i in range(1, 7))
            cnf_passcode = ''.join(request.form.get(f'inp_{i}', '') for i in range(7, 13))
            if passcode == cnf_passcode:
                inf.two_factor_authentication = 'True'
                inf.passcode = int(passcode)
                db.session.commit()
                flash('Two-factor authentication enabled successfully.', 'success')
            else:
                flash('Passcodes do not match. Please try again.', 'danger')
        elif 'disable' in request.form:
            old_passcode = ''.join(request.form.get(f'inp_{i}', '') for i in range(13, 19))
            if int(old_passcode) == inf.passcode:
                inf.two_factor_authentication = 'False'
                inf.passcode = 0
                db.session.commit()
                flash('Two-factor authentication disabled successfully.', 'success')
            else:
                flash('Incorrect passcode. Please try again.', 'danger') 
        elif 'deactivate' in request.form:
            inf.activity='offline'
            db.session.commit()        
    service=Service_request.query.filter_by(status='approved').all()        

           
    return render_template('customer_dashboard.html',inf=inf,data=data,service=service)
@app.route('/customer_dashboard')
def customer_dashboard_explore():
    service=Service_request.query.all()            
    return render_template('explore.html',service=service)
@app.route('/home/book_now')
def book_now():
    if(current_user):
        return redirect(url_for('customer_dashboard',user=current_user))
    else:
        return redirect(url_for('login'))


@app.route('/<username>/order_tracking',methods=['GET',"POST"])
@login_required
def order_tracking(username):
    order= db.session.query(Order, Payments, Service_request, Address,Track) \
    .join(Payments, Payments.order_id == Order.order_id) \
    .join(Service_request, Service_request.service_providing_code == Order.service_id) \
    .join(Address, Address.address_id == Order.address_id) \
    .join(Track, Track.order_id == Order.order_id) \
    .filter(Order.user_id == username) \
    .all()
    print(order)
    return render_template('tracking.html',order=order)

@app.route('/cart/<username>',methods=['GET','POST'])
def cart(username):
    cart_item=db.session.query(Service_request,CartItem).join(CartItem,CartItem.item_id == Service_request.service_providing_code ).filter(CartItem.user_id ==username).all()
    cart=CartItem.query.filter_by(user_id=username).first()
    address=Address.query.filter_by(user_id=username).all()
   
    return render_template('cart.html',cart_item=cart_item,address=address,cart=cart)

@app.route("/account")
def account():
    try:
        return redirect(url_for(f'{current_user.role}_dashboard', user_1=current_user.username))
    except Exception as e:
        return render_template('error.html', error_1='Unexpected error occurred: !! Pls login to Continue !!')
    

@app.route('/delete_account/<string:user>',methods=['GET','POST'])
def delete_account(user):
    users=User.query.filter_by(username=user).first()
    email_id=request.form['email']
    if email_id==users.email_id:
        db.session.delete(users)
        db.session.commit()
        return redirect(url_for('login'))
    return redirect(url_for(''))

@app.route('/change-password/<string:user>',methods=['GET','POST'])
def change_password(user):
    user_2=User.query.filter_by(username=user).first()
    old_pass=request.form['old_pass']
    new_pass=request.form['new_pass']
    cnf_pass=request.form['cnf_pass']
    if user_2.check_password(old_pass):
        if new_pass == cnf_pass:
            user_2.set_password(new_pass)
            db.session.commit()
            return redirect(url_for('customer_dashboard'))
    return redirect(url_for('customer_dashboard',user=current_user.username))




@app.route('/forgot', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        data = request.get_json()
        action = data.get('action')

        if action == 'verifyEmail':
            email_1 = data.get('email')
            user = User.query.filter_by(email_id=email_1).first()
            if user:
                session['email'] = email_1
                return jsonify({'exists': True})
            else:
                return jsonify({'exists': False})

        elif action == 'requestOTP':
            email_1 = session.get('email')
            user = User.query.filter_by(email_id=email_1).first()
            new_pass = data.get('newPassword')
            if user:
                otp = ''.join(random.choices('0123456789', k=6))
                send_otp(user.email_id, otp)
                session['otp'] = otp
                session['new_password'] = new_pass
                return jsonify({'status': 'otp_sent'})
            else:
                return jsonify({'status': 'email_not_found'})

        elif action == 'setPassword':
            email_1 = session.get('email')
            user = User.query.filter_by(email_id=email_1).first()
            new_pass = session.get('new_password')
            passcode = data.get('passcode')

            if user and passcode == session.get('otp'):
                user.set_password(new_pass) 
                db.session.commit()
                return jsonify({'success': True})
            else:
                return jsonify({'success': False, 'message': 'Invalid passcode or user'})

    return render_template('forgot.html') 


@app.route('/list_filter/<data_filter>',methods=['GET','POST'])
@login_required
def list_filter(data_filter):
    service=Service_request.query.filter_by(service_category=data_filter).all()
    return render_template('list_filter_service.html',service=service)





@app.route('/professional_dashboard/<user>',methods=['GET','POST'])
def professional_dashboard(user):
    ver=VerifyAccount.query.filter_by(user_id=user).first()
    pro=User.query.filter_by(username=user).first()
    data=ProfileUpdate.query.filter_by(user_id=user).first()
    service=Service_request.query.filter_by(status='approved').all() 
    if request.method == "POST":
        if 'visibility' in request.form:
            visibility = request.form['visibility']
            pro.visibility = visibility
            db.session.commit()
            flash('Profile visibility updated successfully', 'success')   

        elif 'setup' in request.form:
            print('clicked')
            passcode = ''.join(request.form.get(f'inp_{i}', '') for i in range(1, 7))
            cnf_passcode = ''.join(request.form.get(f'inp_{i}', '') for i in range(7, 13))
            if passcode == cnf_passcode:
                pro.two_factor_authentication = 'True'
                pro.passcode = int(passcode)
                db.session.commit()
                flash('Two-factor authentication enabled successfully.', 'success')
            else:
                flash('Passcodes do not match. Please try again.', 'danger')
        elif 'disable' in request.form:
            old_passcode = ''.join(request.form.get(f'inp_{i}', '') for i in range(13, 19))
            if int(old_passcode) == pro.passcode:
                pro.two_factor_authentication = 'False'
                pro.passcode = 0
                db.session.commit()
                flash('Two-factor authentication disabled successfully.', 'success')
            else:
                flash('Incorrect passcode. Please try again.', 'danger') 
        elif 'deactivate' in request.form:
            pro.activity='offline'
            db.session.commit()        
    return render_template('professional_dashboard.html',pro=pro,service=service,data=data,ver=ver)





@app.route('/submit_profile_update/<user>', methods=["POST",'GET'])
def submit_profile_update(user):
    user=User.query.filter_by(username=user).first()
    if request.method == 'POST':
        owner_name = request.form.get('ownerName','customer')
        manager_name = request.form.get('managerName','customer')
        first_name = request.form.get('firstName','professional')
        last_name = request.form.get('lastName','professional')
        mobile_number = request.form['mobileNumber']
        alternate_number = request.form.get('alternateNumber')
        street_address = request.form['streetAddress']
        city = request.form['city']
        state = request.form['state']
        country = request.form['country']
        pincode = request.form['pincode']
        landmarks = request.form.get('landmarks')

        if(user):
            user.first_name=first_name,
            user.last_name=last_name,
            user.owner_name=owner_name,
            user.manager_name=manager_name,
            user.mobile_number=mobile_number,
            user.alternate_number=alternate_number,
            user.street_address=street_address,
            user.city=city,
            user.state=state,
            user.country=country,
            user.pincode=pincode,
            user.landmarks=landmarks,  
                  
        else:
            profile_update = ProfileUpdate(
            first_name=first_name,
            last_name=last_name,
            owner_name=owner_name,
            manager_name=manager_name,
            mobile_number=mobile_number,
            alternate_number=alternate_number,
            street_address=street_address,
            city=city,
            state=state,
            country=country,
            pincode=pincode,
            landmarks=landmarks,
            user_id=user.username,  
        )
            db.session.add(profile_update)

        db.session.commit()

        flash('Profile updated successfully!', 'success')
        return redirect(url_for(f"{user.department}_dashboard",user=current_user.username )) 

    return redirect(url_for(f"{user.department}_dashboard",user=current_user.username )) 


@app.route('/verify_account/<user>',methods=['GET','POST'])
def verify_account(user):
    if request.method == 'POST':
        gst_file = request.files.get('gst_file') 
        uan_file = request.files.get('uan_file') 
        business_reg_file = request.files.get('bussiness_file') 
        income_tax_file = request.files.get('income_file') 
        if gst_file and allowed_file(gst_file.filename):
             gst_filename = secure_filename(gst_file.filename) 
             gst_file.save(os.path.join(app.config['UPLOAD_FOLDER'], gst_filename)) 
        if uan_file and allowed_file(uan_file.filename): 
            uan_filename = secure_filename(uan_file.filename) 
            uan_file.save(os.path.join(app.config['UPLOAD_FOLDER'], uan_filename))
        if business_reg_file and allowed_file(business_reg_file.filename): 
            business_reg_filename = secure_filename(business_reg_file.filename) 
            business_reg_file.save(os.path.join(app.config['UPLOAD_FOLDER'], business_reg_filename)) 
        if income_tax_file and allowed_file(income_tax_file.filename): 
            income_tax_filename = secure_filename(income_tax_file.filename) 
            income_tax_file.save(os.path.join(app.config['UPLOAD_FOLDER'], income_tax_filename)) 
        verified = VerifyAccount( gst_file=gst_filename,
                                uan_file=uan_filename,
                                 business_reg_file=business_reg_filename, 
                                 status='pending',
                                 income_tax_file=income_tax_filename, 
                                 user_id=user )
        db.session.add(verified) 
        db.session.commit() 
        return redirect(request.referrer)
    return redirect(request.referrer)


@app.route('/view_service/<service_>')
def view_service(service_):
    service=Service_request.query.filter_by(service_providing_code=service_).first()
    return render_template('view.html',service=service)


@app.route('/admin/list',methods=['GET','POST'])
def admin_list():
    user=User.query.all()
    service=Service_request.query.all()
    adds = db.session.query(User, VerifyAccount).join(VerifyAccount, User.username == VerifyAccount.user_id).all()
    return render_template('admin_list.html',camp=service,user=user,verified=adds) 


@app.route('/admin/<userId>/<action>',methods=['GET','POST'])
def admin_action(userId,action):
    user=User.query.filter_by(username=userId).first()
    if action == 'delete':
        db.session.delete(user)
        db.session.commit()
    elif action =='deactivate':
        user.admin_data='deactivate'
        db.session.commit()
    elif action =='mav'   :
        user.admin_data='View'
        db.session.commit()
    elif action =='activate'  :
        user.admin_data='activate'  
        db.session.commit()
    elif action == 'unview':
        user.admin_data='unview'
        db.session.commit()    
    return jsonify({"message": f"Action {action} performed for user {userId}"}) 

@app.route('/verify_professioanal',methods=["GET","POST"])
def verify_professioanal():
    professional_data = db.session.query(User, VerifyAccount).join(
            VerifyAccount, User.username == VerifyAccount.user_id
        ).filter(User.department == 'professional', VerifyAccount.status == 'pending').all()

    pending_services = db.session.query(User, Service_request).join(
            Service_request, User.username == Service_request.user_id).filter(Service_request.status == 'pending').all()
    
    return render_template(
            'admin_search.html',
            verification_data=professional_data,
            service_data=pending_services
        )


@app.route('/verify_user', methods=['POST'])
def verify_user():
    try:
       
        data = request.get_json()
        username = data['username']

        verify_account = db.session.query(VerifyAccount).join(User).filter(User.username == username).first()
        if verify_account:
            verify_account.status = 'Verified'  
            db.session.commit()
            return jsonify({'message': 'User verified successfully!'})
        else:
            return jsonify({'message': 'User not found!'}), 404
    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500



@app.route('/process_service', methods=['POST'])
def process_service():
    try:
     
        data = request.get_json()
        service_id = data['service_id']


        service_request = db.session.query(Service_request).filter(Service_request.request_id == service_id).first()
        if service_request:
            service_request.status = 'approved' 
            db.session.commit()
            return jsonify({'message': 'Service request processed successfully!'})
        else:
            return jsonify({'message': 'Service request not found!'}), 404
    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500




@app.route('/admin/payments',methods=['GET','POST'])
def payments():
    order = Order.query.all()
    payments=Payments.query.all()
    return render_template('admin_pay.html',order=order,payments=payments)

@app.route('/api/help/solve', methods=['POST'])
def solve_help_request():
    data = request.json
    issue_id = data.get('issue_id')
    solution = data.get('solution')

    help_request = Help.query.filter_by(issue_id=issue_id).first()
    if help_request:
        help_request.status = 'Solved'
        db.session.commit()

        send_solution_email(help_request.email_id, solution)

        return jsonify({'message': 'Help request solved and email sent!'}), 200
    else:
        return jsonify({'message': 'Help request not found'}), 404

def send_solution_email(email, solution):
    msg = Message('Solution to your issue',recipients=[email])
    msg.body = f"Dear user,\n\nHere is the solution to your problem:\n\n{solution}\n\nBest regards,\nSupport Team"
    mail.send(msg)

@app.route('/admin_help_solns',methods=['GET','POST'])
def help_request():
    helps=Help.query.all()
    return render_template('admin_help_sol.html',helps=helps)



@app.route('/service_edit_form/<request_id>', methods=['POST'])
def service_edit_form(request_id):
   
    service = Service_request.query.filter_by(request_id=request_id).first()

    if not service:
        flash("Service request not found!", "error")
        return redirect(url_for('professional_dashboard',user=current_user.username)) 

    
    service_name = request.form.get('service-name')
    service_description = request.form.get('service-description')
    servicable_pincode = request.form.get('services-pincode')
    contact_email = request.form.get('contact-email')
    contact_phone = request.form.get('contact-phone')
    service_category = request.form.get('service-category')
    pricing = request.form.get('pricing')
    currency = request.form.get('currency')
    country_code = request.form.get('countryCode')
    
    
    service.service_name = service_name
    service.service_description = service_description
    service.servicable_pincode = servicable_pincode
    service.contact_email = contact_email
    service.contact_phone = contact_phone
    service.service_category = service_category
    service.pricing = pricing
    service.currency = currency
    service.country_code = country_code
    
    
    try:
        db.session.commit()
        flash("Service request updated successfully!", "success")
    except Exception as e:
        db.session.rollback()
        flash("An error occurred while updating the service request.", "error")
        return redirect(url_for('professional_dashboard',user=current_user.username))  


    return redirect(url_for('view_service', service_=service.service_providing_code))  

@app.route('/get_service_data/<request_id>', methods=['GET'])
def get_service_data(request_id):
    service = Service_request.query.filter_by(request_id=request_id).first()
    
    if not service:
        return jsonify({'error': 'Service not found'}), 404
    
    return jsonify({
        'service_providing_code': service.service_providing_code,
        'service_name': service.service_name,
        'service_description': service.service_description,
        'servicable_pincode': service.servicable_pincode,  
        'pricing': service.pricing,
        'contact_email': service.contact_email,
        'contact_phone': service.contact_phone,
        'service_category': service.service_category,
        'currency': service.currency,
        'country_code': service.country_code
    })



@app.route('/delete_service/<request_id>',methods=['GET',"POST"])
@login_required
def dele(request_id):
    
    ser = Service_request.query.filter_by(request_id=request_id).first()
    db.session.delete(ser)
    db.session.commit()
    return redirect(url_for('professional_dashboard',user=current_user.username))  


@app.route('/track_update',methods=['GET','POST'])
@login_required
def track():
    orders = db.session.query(Order, Service_request) \
    .join(Service_request, Service_request.service_providing_code == Order.service_id) \
    .filter(Service_request.user_id == current_user.username) \
    .all()
    return render_template('track_update.html',orders=orders)



@app.route('/update_tracking', methods=['POST'])
def update_tracking():
    order_id = request.form['order_id']
    status = request.form['status']
    help_name = request.form['help_name']
    help_contact = request.form['help_contact']
    estimated_time = request.form.get('estimated_time')
    transaction_id = request.form.get('transaction_id')

   
    pay=Payments.query.filter_by(order_id=order_id).first()
    ord = Order.query.filter_by(order_id=order_id).first()

 
    if not ord:
        return jsonify({"error": "Order not found"}), 404

    track = Track.query.filter_by(order_id=order_id).first()

    if track:
 
        track.status = status
        track.helper_name = help_name
        track.helper_contact = help_contact
        track.estimated_time = estimated_time
        track.transaction_id = pay.transaction_id
        ord.order_status= status
    
    else:
        new_track = Track(
            order_id=order_id,
            status=status,
            helper_name=help_name,
            helper_contact=help_contact,
            estimated_time=estimated_time,
            transaction_id=transaction_id
        )
        ord.order_status= status
 
        db.session.add(new_track)  

  
    db.session.commit()

    return jsonify({"message": "Tracking updated successfully"}), 200
@app.route('/order/<order_id>/track', methods=['GET'])
def track_order(order_id):
  
    order = Order.query.filter_by(order_id=order_id).first()
    if not order:
        return jsonify({"error": "Order not found"}), 404

 
    address = Address.query.filter_by(address_id=order.address_id).first()
    if not address:
        return jsonify({"error": "Address not found"}), 404

   
    service = Service_request.query.filter_by(service_providing_code=order.service_id).first()
    if not service:
        return jsonify({"error": "Service not found"}), 404


    track = Track.query.filter_by(order_id=order_id).first()

    
    tracking_data = {
        "helper_name": track.helper_name if track else None,
        "helper_contact": track.helper_contact if track else None,
        "estimated_time": track.estimated_time if track else None,
        "transaction_id": track.transaction_id if track else None,
    }

    order_data = {
        'order_id': order.order_id,
        'address': f"{address.address_description}, {address.city}, {address.state} - {address.pincode}",
        'service_name': service.service_name,
        'order_status': order.order_status,
        'tracking': tracking_data
    }

    return jsonify(order_data)




@app.route('/delete_address/<address_id>',methods=['GET','POST'])
@login_required
def delete_address(address_id):
    if request.form == 'POST':
        delete_= Address.query.filter_by(request_id=address_id).first()
        db.session.delete(delete_)
        db.session.commit()
        flash('Address Deletion Success')
        return redirect(request.referrer)
    return redirect(request.referrer)





@app.route('/rate/<order_id>', methods=['GET', 'POST'])
@login_required
def rate(order_id):
    if request.method == 'POST':
        rate = request.form.get('rate')
        feedback = request.form.get('feedback')


        order = Order.query.filter_by(order_id=order_id).first()

        if not order:
            flash("Order not found.", "error")
            return redirect(request.referrer)

      
        if order.user_id != current_user.username:
            flash("You are not authorized to rate this order.", "error")
            return redirect(request.referrer)

        order.rating = rate
        order.feedback = feedback
        rt=Rate(
            item_id=order.service_id,
            rate=rate,
            feedback=feedback
        )
        db.session.add(rt)
        db.session.commit()
        flash("Feedback submitted successfully!", "success")
    
    return redirect(request.referrer)





@app.route('/search', methods=['GET'])
def search_service_requests():
    try:
        service_name = request.args.get('service_name', '').strip()
        category = request.args.getlist('service_category')  
        sort_by = request.args.get('sort', 'name_asc')  
        rating_filter = request.args.get('min_rating', 0, type=float) 
        pincode = request.args.get('servicable_pincode')

    
        query = Service_request.query.filter(Service_request.status == 'approved')

        
        if 'all' not in category and category:
            query = query.filter(Service_request.service_category.in_(category))

    
        if service_name:
            query = query.filter(Service_request.service_name.ilike(f"%{service_name}%"))
        if pincode:
            query = query.filter(Service_request.servicable_pincode == pincode)
        if rating_filter > 0:
            query = query.filter(Service_request.avg_rate >= rating_filter)

        
        if sort_by == 'name_asc':
            query = query.order_by(Service_request.service_name.asc())
        elif sort_by == 'name_desc':
            query = query.order_by(Service_request.service_name.desc())
        elif sort_by == 'price_low_high':
            query = query.order_by(Service_request.pricing.asc())
        elif sort_by == 'price_high_low':
            query = query.order_by(Service_request.pricing.desc())
        elif sort_by == 'rating_high_low':
            query = query.order_by(Service_request.avg_rate.desc())
        elif sort_by == 'rating_low_high':
            query = query.order_by(Service_request.avg_rate.asc())

    
        services = query.all()

    
        response = [
            {
                "service_name": service.service_name,
                "service_category": service.service_category,
                "pricing": service.pricing,
                "rating": service.avg_rate,
                "logo": url_for('uploads', filename=service.brand_logo),
                "service_code": service.service_providing_code,
            } for service in services
        ]
        return jsonify(response), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500





@app.route('/decline/<order_id>',methods=['GET',"POST"])
@login_required
def decline(order_id):
    if request.method == "POST":
        order=Order.query.filter_by(order_id=order_id).first()
        payment=Payments.query.filter_by(order_id=order_id).first()
        print(order)
        print(payment)
        order.order_status = 'declined'
        payment.payment_status = 'refunded'
        db.session.commit()
        return redirect(request.referrer)
    return redirect(request.referrer)










@app.route('/unverify/<request_id>',methods=['GET','POST'])

def unverify(request_id):
    if request.method =='POST':
        ser=Service_request.query.filter_by(request_id=request_id).first()
        ser.status='pending'
        db.session.commit()
        return redirect(request.referrer)
    return redirect(request.referrer)



@app.route('/chart-data')
def chart_data():
    
    customers = User.query.filter_by(department="customer").count()
    professionals = User.query.filter_by(department="professional").count()

    service_confirmed = Order.query.filter_by(order_status="Service Confirmed").count()
    on_the_way = Order.query.filter_by(order_status="On the Way").count()
    work_completed = Order.query.filter_by(order_status="Work Completed").count()
    payment_done = Order.query.filter_by(order_status="Payment Done").count()
    pending_orders = Order.query.filter_by(order_status="Pending").count()


    return jsonify({
        "orderData": {
            "labels": ["Service Confirmed", "On the Way", "Work Completed", "Payment Done", "Pending"],
            "data": [service_confirmed, on_the_way, work_completed, payment_done, pending_orders]
        },

        "sponsorData": {
            "labels": ["Customers", "Professionals"],
            "data": [customers, professionals]
        }
    })

@app.route('/paymented')
def show_user_payments():
   
    payments_data = (
        db.session.query(Payments, Service_request, Order)
        .join(Order, Payments.order_id == Order.order_id)
        .join(Service_request, Order.service_id == Service_request.service_providing_code)
        .filter(Service_request.user_id == current_user.username)
        .all()
    )

    return render_template('payments.html', payments_data=payments_data)







