import re
from . import db
from flask_cors import cross_origin
from .models import Users, Service_Professionals,Customers
from flask import Blueprint, request, jsonify, make_response
from flask_jwt_extended import create_access_token, set_access_cookies
from werkzeug.security import generate_password_hash, check_password_hash


auth=Blueprint("auth",__name__)


@auth.route("/signup", methods=['POST'])
def signup():
    data = request.json
    name = data.get('name', '')
    email = data.get('email', '')
    password = data.get('password', '')
    confirm_password = data.get('confirmPassword', '')
    role = data.get('role', '')
    contact = data.get('contact', '')
    city = data.get('city', '')
    locality = data.get('locality', '')

    # Unique fields for service professionals
    service_type = data.get('service_type')
    experience = data.get('experience', '0')
    description = data.get('description', '')

    email_regex = r'^[a-zA-Z0-9._%+-]+@gmail\.com$'
    def is_valid_email(mail):
        return bool(re.match(email_regex, mail))

    if not is_valid_email(email):
        return jsonify({'success': False, 'message': 'Invalid Email Address'}), 400

    if Users.query.filter_by(Email=email).first():
        return jsonify({'success': False, 'message': 'Email already exists'}), 400

    if len(password) < 8:
        return jsonify({'success': False, 'message': 'Password should be at least 8 characters'}), 400

    hashed_password = generate_password_hash(password)

    new_user = Users(Name=name, Email=email, Password=hashed_password, Role=role)
    db.session.add(new_user)
    db.session.flush()  

    if role == 'service_professional':
        new_professional = Service_Professionals(
            User_id=new_user.User_id,
            Name=name,
            Email=email,
            Service_Type=service_type,
            Experience=experience,
            Contact=contact,
            City=city,
            Locality=locality,
            Description=description
        )
        db.session.add(new_professional)

    elif role == 'customer':
        new_customer = Customers(
            User_id=new_user.User_id,
            Name=name,
            Email=email,
            Contact=contact,
            City=city,
            Locality=locality
        )
        db.session.add(new_customer)
    db.session.commit()
    return jsonify({'success': True, 'message': 'User registered successfully', 'redirect': '/login'}), 201


@auth.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({'success': False, 'message': 'Invalid request format, expected JSON'}), 400  # ✅ Explicit error

    data = request.get_json()
    print("Received Data:", data)  # ✅ Debug print

    if not data:
        return jsonify({'success': False, 'message': 'No data received'}), 400

    email = data.get('email')
    password = data.get('password')
    print(email, password)

    if not email or not password:
        return jsonify({'success': False, 'message': 'Email and Password are required'}), 400

    user = Users.query.filter_by(Email=email).first()

    if not user or not check_password_hash(user.Password, password):
        return jsonify({'success': False, 'message': 'Invalid email or password'}), 401
    
    print(user, "- User Exists !!!")
    # Role checks
    if user.Role == 'service_professional':
        professional = Service_Professionals.query.filter_by(User_id=user.User_id).first()
        if professional:
            if professional.Is_Flagged:
                return jsonify({'success': False, 'message': 'Your profile has been flagged, cannot enter'}), 403
            if not professional.Status:
                return jsonify({'success': False, 'message': 'Your profile has been rejected'}), 403

    if user.Role == 'customer':
        customer = Customers.query.filter_by(User_id=user.User_id).first()
        if customer and customer.Is_Flagged:
            return jsonify({'success': False, 'message': 'Your profile has been flagged, cannot enter'}), 403

    role_redirects = {
        'admin': '/admin_home',
        'customer': f'/customer_home/{user.User_id}',
        'service_professional': f'/professional_home/{user.User_id}'
    }

    access_token = create_access_token(identity=user.User_id, additional_claims={"role": user.Role})

    print('Access_token: ', access_token)
    # Create response and set secure HTTP-only JWT cookie
    response = jsonify({
        'success': True,
        'message': 'Login successful',
        'redirect': role_redirects.get(user.Role, '/')
    })  
    print("RESPONSE: ", response)
    
    print("Before setting cookies:", response.headers)
    set_access_cookies(response, access_token)
    print("After setting cookies:", response.headers)

    return response



@auth.route('/logout', methods=['POST'])
def logout():
    return jsonify({'success': True, 'message': 'Logout successful'}), 200