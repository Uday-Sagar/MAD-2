from . import db
from flask_cors import cross_origin
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from .models import Users, Service_Professionals,Customers, Services, Service_Requests


admin=Blueprint("admin",__name__)


# --------------------- Admin Routes --------------------


@admin.route('/add_service', methods=['POST', 'OPTIONS'])
@cross_origin()
@jwt_required()
def add_service():
    claims = get_jwt()
    print(claims.get('role'))
    if claims.get("role") != "admin":
        return jsonify({'success': False, 'message': 'Unauthorized access'}), 403
    data = request.get_json()
    new_service = Services(
        Service_type=data.get('service_type'),  
        Price_range=data.get('price_range'),   
        Duration=data.get('duration'),       
        Description=data.get('description')   
    )
    db.session.add(new_service)
    db.session.commit()
    return jsonify({'success': True, 'message': 'Service added successfully'}), 201


@admin.route('/edit_service/<int:service_id>', methods=['GET'])
@cross_origin()
@jwt_required()
def edit_service(service_id):
    try:
        claims = get_jwt()
        if claims.get("role") != "admin":
            return jsonify({'success': False, 'message': 'Unauthorized access'}), 403
        service = Services.query.filter_by(Service_id=service_id).first()
        if not service:
            return jsonify({'success': False, 'message': 'Service not found'}), 404
        service_data = {
            'Service_id': service.Service_id,
            'Service_type': service.Service_type,
            'Price_range': service.Price_range,
            'Duration': service.Duration,
            'Description': service.Description
        }
        return jsonify({'success': True, 'service': service_data}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
    

@admin.route('/update_service/<int:service_id>', methods=['PUT'])
@cross_origin()
@jwt_required()
def update_service(service_id):
    try:
        claims = get_jwt()
        if claims.get("role") != "admin":
            return jsonify({'success': False, 'message': 'Unauthorized access'}), 403
    
        service = Services.query.filter_by(Service_id=service_id).first()
        if not service:
            return jsonify({'success': False, 'message': 'Service not found'}), 404

        data = request.get_json()

        service.Service_type = data.get('service_type', service.Service_type)  
        service.Price_range = data.get('price_range', service.Price_range)    
        service.Duration = data.get('duration', service.Duration)             
        service.Description = data.get('description', service.Description)    

        db.session.commit()
        return jsonify({'success': True, 'message': 'Service updated successfully'}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
    

@admin.route('/delete_service/<int:service_id>', methods=['DELETE', 'OPTIONS'])
@cross_origin()
@jwt_required()
def delete_service(service_id):
    claims = get_jwt()
    if claims.get("role") != "admin":
        return jsonify({'success': False, 'message': 'Unauthorized access'}), 403
    service = Services.query.filter_by(Service_id=service_id).first()
    if not service:
        return jsonify({'success': False, 'message': 'Service not found'}), 404
    db.session.delete(service)
    db.session.commit()
    return jsonify({'success': True, 'message': 'Service deleted successfully'}), 200


@admin.route('/get_services', methods=['GET', 'OPTIONS'])
@cross_origin()
@jwt_required()
def get_services():
    try:
        claims = get_jwt()
        if claims.get("role") != "admin":
            return jsonify({'success': False, 'message': 'Unauthorized access'}), 403
        services = Services.query.all()  
        services_list = [{
            'Service_id': service.Service_id,
            'Service_type': service.Service_type,
            'Price_range': service.Price_range,
            'Duration': service.Duration,
            'Description': service.Description,
        } for service in services]
        return jsonify({'success': True, 'services': services_list}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
    
# ----------------------------------------------------

@admin.route('/get_customers', methods=['GET','OPTIONS'])
@cross_origin()
@jwt_required()
def get_customers():
    try:
        claims = get_jwt()
        if claims.get("role") != "admin":
            return jsonify({'success': False, 'message': 'Unauthorized access'}), 403
        customers = Customers.query.all()
        if not customers:
            return jsonify({'success': False, 'message': 'No customers found'}), 404
        customers_list = [{
            'customer_id': customer.Customer_id, 
            'name': customer.Name,
            'email': customer.Email,
            'contact': customer.Contact,
            'is_flagged': customer.Is_Flagged  
        } for customer in customers]
        return jsonify({'success': True, 'customers': customers_list}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@admin.route('/flag_customer/<int:customer_id>', methods=['PUT','OPTIONS'])
@cross_origin()
@jwt_required()
def flag_customer(customer_id):
    try:
        claims = get_jwt()
        if claims.get("role") != "admin":
            return jsonify({'success': False, 'message': 'Unauthorized access'}), 403
        customer = Customers.query.filter_by(Customer_id=customer_id).first()
        data = request.get_json()
        is_flagged = data.get('is_flagged', None)
        if is_flagged is None:
            return jsonify({'success': False, 'message': 'Flag status not provided'}), 400
        customer.Is_Flagged = is_flagged
        db.session.commit()
        return jsonify({'success': True, 'message': 'Customer flag status updated'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

# ----------------------------------------------------

@admin.route('/get_service_professionals', methods=['GET','OPTIONS'])
@cross_origin()
@jwt_required()
def get_service_professionals():
    try:
        claims = get_jwt()
        if claims.get("role") != "admin":
            return jsonify({'success': False, 'message': 'Unauthorized access'}), 403
        professionals = Service_Professionals.query.all()
        if not professionals:
            return jsonify({'success': False, 'message': 'No professionals found'}), 404
        professionals_list = [{
            'professional_id': professional.Professional_id,  
            'name': professional.Name,
            'email': professional.Email,
            'service_type': professional.Service_Type,
            'contact': professional.Contact,
            'is_flagged': professional.Is_Flagged  
        } for professional in professionals]
        return jsonify({'success': True, 'professionals': professionals_list}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@admin.route('/flag_service_professionals/<int:professional_id>', methods=['PUT'])
@cross_origin()
@jwt_required()
def flag_service_professionals(professional_id):
    try:
        claims = get_jwt()
        if claims.get("role") != "admin":
            return jsonify({'success': False, 'message': 'Unauthorized access'}), 403
        professional = Service_Professionals.query.filter_by(Professional_id=professional_id).first()
        data = request.get_json()
        is_flagged = data.get('is_flagged', None)

        if is_flagged is None:
            return jsonify({'success': False, 'message': 'Flag status not provided'}), 400

        professional.Is_Flagged = is_flagged
        db.session.commit()
        return jsonify({'success': True, 'message': 'Customer flag status updated'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500
    

@admin.route('/get_professional_approval', methods=['GET','OPTIONS'])
@cross_origin()
@jwt_required()
def get_professional_approval():
    try:
        
        claims = get_jwt()
        if claims.get("role") != "admin":
            return jsonify({'success': False, 'message': 'Unauthorized access'}), 403

        professionals = Service_Professionals.query.filter_by(Status=False).all()
        if not professionals:
            return jsonify({'success': False, 'message': 'No pending professionals found'}), 404
        
        professionals_list = [{
            'professional_id': professional.Professional_id,  
            'name': professional.Name,
            'email': professional.Email,
            'service_type': professional.Service_Type,
            'experience': professional.Experience,
            'contact': professional.Contact,
            'city': professional.City,
            'locality': professional.Locality,
            'description': professional.Description,
        } for professional in professionals]

        return jsonify({'success': True, 'professionals': professionals_list}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@admin.route('/approve_professional/<int:professional_id>', methods=['PUT'])
@cross_origin()
@jwt_required()
def approve_professional(professional_id):
    try:
        claims = get_jwt()
        if claims.get("role") != "admin":
            return jsonify({'success': False, 'message': 'Unauthorized access'}), 403

        professional = Service_Professionals.query.filter_by(Professional_id=professional_id).first()
        if not professional:
            return jsonify({'success': False, 'message': 'Professional not found'}), 404

        professional.Status = True
        db.session.commit()
        return jsonify({'success': True, 'message': 'Professional approved'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500
    
