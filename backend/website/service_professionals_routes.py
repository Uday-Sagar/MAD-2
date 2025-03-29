from . import db
from datetime import datetime
from flask_cors import cross_origin
from flask import Blueprint, request, jsonify
from .utils import role_required
from .models import Users, Service_Professionals,Customers, Services, Service_Requests
from flask_jwt_extended import jwt_required, get_jwt_identity


prof=Blueprint("prof",__name__)


# -------------------- Service Professional Routes --------------------


@prof.route('/get_my_requests/<int:user_id>',methods=['GET','OPTIONS'])
@cross_origin()
def get_my_services(user_id):
    
    service_professional = Service_Professionals.query.filter_by(User_id=user_id).first()
    if not service_professional:
        return jsonify({'success': False, 'message': 'Professional not found'}), 404

    service_requests = Service_Requests.query.filter_by(Professional_id=service_professional.Professional_id).all()
    if not service_requests:
        return jsonify({'success': False, 'message': 'No services found'}), 404
    # for req in service_requests:
    #     print(f"Customer ID: {type(req.Customer_id)}")
    #     print(f"Customer ID: {req.Customer_id}")

    try:
        request_list = []
        for req in service_requests:
            request_list.append({
                'request_id': req.Request_id,
                'customer_name': 'Unknown',
                'address': req.Address,
                'start_date': req.Start_date.strftime('%Y-%m-%d'),
                'end_date': req.End_date.strftime('%Y-%m-%d'),
                'status': req.Status,
                'action': req.Action
            })

        return jsonify({'success': True, 'requests': request_list}), 200

    except Exception as e:
        print(f"Error fetching service requests: {e}")  # Log error for debugging
        return jsonify({'success': False, 'message': str(e)}), 500


@prof.route('/update_request_status', methods=['POST'])
@cross_origin()
def update_request_status():
    try:
        data = request.get_json()
        print("Received Data:", data)

        request_id = data.get('request_id')
        status = data.get('status')

        if not request_id or not status:
            return jsonify({"success": False, "message": "Invalid data provided"}), 400

        service_request = Service_Requests.query.filter_by(Request_id=request_id).first()
        if not service_request:
            return jsonify({"success": False, "message": "Request not found"}), 404

        service_request.Status = status
        db.session.commit()

        return jsonify({"success": True, "message": f"Request status updated to {status}"})
    except Exception as e:
        db.session.rollback()
        print(f"Error updating request status: {e}")
        return jsonify({"success": False, "message": str(e)}), 500


@prof.route('/update_request_action', methods=['POST', 'OPTIONS'])
@cross_origin()
def update_request_action():
    try:
        data = request.get_json()
        request_id = data.get('request_id')
        action_status = data.get('action')

        if not request_id or not action_status:
            return jsonify({'success': False, 'message': 'Missing request ID or action status'}), 400

        # Find the service request in the database
        service_request = Service_Requests.query.filter_by(Request_id=request_id).first()

        if not service_request:
            return jsonify({'success': False, 'message': 'Service request not found'}), 404

        # Update the action status
        service_request.Action = action_status
        db.session.commit()

        return jsonify({'success': True, 'message': 'Action updated successfully'}), 200

    except Exception as e:
        print(f"Error updating request action: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500


@prof.route('/get_professional_profile/<int:user_id>', methods=['GET'])
@cross_origin()
def get_professional_profile(user_id):

    professional = Service_Professionals.query.filter_by(User_id=user_id).first()
    if not professional:
        return jsonify({'success': False, 'message': 'Professional profile not found'}), 404
    service = Services.query.filter_by(Service_id=professional.Service_Type).first()
    service_name = service.Service_type if service else "Unknown Service"
    professional_data = {
        'user_id': professional.User_id,
        'name': professional.Name,
        'email': professional.Email,
        'service_type': service_name,
        'experience': professional.Experience,
        'contact': professional.Contact,
        'city':professional.City,
        'locality': professional.Locality,
        'description': professional.Description,
    }
    return jsonify({'success': True, 'data': professional_data}), 200


@prof.route('/get_professional_services', methods=['GET'])
@cross_origin()
def get_professional_services():
    try:
        services = Services.query.with_entities(Services.Service_id, Services.Service_type).all()
        return jsonify({"success": True, "services": [{"id": s.Service_id, "name": s.Service_type} for s in services]}), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@prof.route('/update_professional_profile/<int:user_id>', methods=['PUT', 'OPTIONS'])
@cross_origin()
def update_professional_profile(user_id):
    try:
        profile = Service_Professionals.query.filter_by(User_id=user_id).first()
        if not profile:
            return jsonify({'success': False, 'message': 'Profile not found'}), 404
        data = request.get_json()
        service_name = data.get('service_type')
        if service_name:
            service = Services.query.filter_by(Service_type=service_name).first()
            if not service:
                return jsonify({'success': False, 'message': 'Invalid service type'}), 400
            profile.Service_id = service.Service_id  
        profile.Name = data.get('name', profile.Name)
        profile.Email = data.get('email', profile.Email)
        profile.Experience = data.get('experience', profile.Experience)
        profile.Contact = data.get('contact', profile.Contact)
        profile.City = data.get('city', profile.City)
        profile.Locality = data.get('locality', profile.Locality)
        profile.Description = data.get('description', profile.Description)

        db.session.commit()
        return jsonify({'success': True, 'message': 'Profile updated successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500
