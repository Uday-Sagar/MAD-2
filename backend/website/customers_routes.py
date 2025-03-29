from . import db
from datetime import datetime
from .utils import role_required
from flask_cors import cross_origin
from flask import Blueprint, request, jsonify
from .models import Service_Professionals,Customers, Services, Service_Requests, Reviews
from flask_jwt_extended import jwt_required, get_jwt_identity


cust=Blueprint("cust",__name__)


# -------------------- Customer Routes --------------------


@cust.route('/get_service_types', methods=['GET'])
@cross_origin()
def get_service_types():
    try:
        services= Services.query.all() 
        services_list = [{
            'id': service.Service_id,
            'type': service.Service_type,
            'price_range': service.Price_range,
            'duration': service.Duration,
            'description': service.Description
        } for service in services]
        
        return jsonify({'success': True, 'services': services_list})
    except Exception as e:
        import traceback
        print("Error in get_service_types:", traceback.format_exc()) 
        return jsonify({'success': False, 'message': str(e)}), 500


@cust.route('/get_service_professionals_by_type', methods=['GET','OPTIONS'])
@cross_origin()
def get_service_professionals_by_type():
    try:
        service_type = request.args.get('serviceType')
        
        if not service_type:
            return jsonify({'success': False, 'message': 'Service type is required'}), 400
        service = Services.query.filter_by(Service_type=service_type).first()
        
        if not service:
            return jsonify({'success': False, 'message': 'Service type not found'}), 404
        professionals = Service_Professionals.query.filter_by(Service_Type=service.Service_id) \
            .filter(Service_Professionals.Is_Flagged == False, Service_Professionals.Status == True) \
            .all()

        professionals_list = [{
            'id': professional.Professional_id,
            'name': professional.Name,
            'email': professional.Email,
            'service_type': service.Service_type,  
            'experience': professional.Experience,
            'city': professional.City,
            'locality': professional.Locality,
            'contact': professional.Contact,
            'description': professional.Description
        } for professional in professionals]

        return jsonify({'success': True, 'professionals': professionals_list})
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
    

@cust.route('/get_professional_by_id', methods=['GET','OPTIONS'])
@cross_origin()
def get_professional_by_id():
    professional_id = request.args.get('professionalId')
    professional = Service_Professionals.query.filter_by(Professional_id=professional_id).first()
    return jsonify({
        "success": True,
        "professional": {
            "name": professional.Name,
            "email": professional.Email
        }
    })


@cust.route('/create_service_request',methods=['POST'])
@cross_origin()
def create_service_request():
    data = request.json
    try:
        start_date = datetime.strptime(data["startDate"], "%Y-%m-%d").date()
        end_date = datetime.strptime(data["endDate"], "%Y-%m-%d").date()
        new_request = Service_Requests(
            Customer_id=data["customerId"],
            Service_id=data["serviceType"],
            Professional_id=data["professionalId"],
            Address=data["location"],
            Start_date=start_date,
            End_date=end_date
        )
        db.session.add(new_request)
        db.session.commit()
        return jsonify({"success": True, "message": "Service request created successfully!"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
    

@cust.route('/get_service_requests_by_user/<int:user_id>', methods=['GET', 'OPTIONS'])
@cross_origin()
def get_service_requests_by_user(user_id):
        try:
            user_id = int(user_id)
        except ValueError:
            return jsonify({"success": False, "message": "Invalid User ID"}), 400
        service_requests = Service_Requests.query.filter_by(Customer_id=user_id).all()
        if not service_requests:
            return jsonify({"success": True, "serviceRequests": []})
        requests_list = []
        for req in service_requests:
            professional = Service_Professionals.query.filter_by(Professional_id=req.Professional_id).first()
            professional_name = professional.Name
            request_data = {
                "id": req.Request_id,
                "serviceType": req.Service_id,
                "professionalName": professional_name,
                "location": req.Address,
                "startDate": req.Start_date.strftime("%Y-%m-%d"),
                "endDate": req.End_date.strftime("%Y-%m-%d"),
                "status":req.Status,
                "action":req.Action
            }
            requests_list.append(request_data)
        if not requests_list:
            print("List is empty")
        else:
            return jsonify({"success": True, "serviceRequests": requests_list})



@cust.route('/get_service_request/<int:request_id>', methods=['GET','OPTIONS'])
@cross_origin()
def get_service_request(request_id):
    try:
        service_request = Service_Requests.query.filter_by(Request_id=request_id).first()
        if not service_request:
            return jsonify({'success': False, 'message': 'Service request not found'}), 404

        service_professional = Service_Professionals.query.filter_by(Professional_id=service_request.Professional_id).first()
        if not service_professional:
            return jsonify({'success': False, 'message': 'Professional not found'}), 404

        request_data = {
            'id': service_request.Request_id,
            'service_type': service_request.Service_id,
            'professional_name':service_professional.Name,
            'location':service_request.Address,
            'start_date': service_request.Start_date.strftime('%Y-%m-%d %H:%M:%S'),
            'end_date': service_request.End_date.strftime('%Y-%m-%d %H:%M:%S')
        }
        return jsonify({'success': True, 'service_request': request_data}), 200

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@cust.route('/update_service_request/<int:request_id>', methods=['PUT'])
@cross_origin()
def update_service_request(request_id):
    try:
        data = request.get_json()
        service_request = Service_Requests.query.filter_by(Request_id=request_id).first()
        if not service_request:
            return jsonify({'success': False, 'message': 'Service request not found'}), 404
        if 'location' in data:
            service_request.Address = data['location']
        if 'start_date' in data:
            start_date = datetime.strptime(data['start_date'], "%Y-%m-%d").date()
            service_request.Start_date = start_date
        if 'end_date' in data:
            end_date = datetime.strptime(data['end_date'], "%Y-%m-%d").date()
            service_request.End_date = end_date
        db.session.commit()
        return jsonify({'success': True, 'message': 'Service request updated successfully'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500


@cust.route('/update_request_action', methods=['POST'])
def update_request_action():
    try:
        data = request.get_json()
        request_id = data.get('request_id')
        action = data.get('action')

        # Validate input
        if not request_id or not action:
            return jsonify({"success": False, "message": "Missing request_id or action"}), 400

        # Find the request in the database
        service_request = Service_Requests.query.filter_by(Request_id=request_id).first()

        if not service_request:
            return jsonify({"success": False, "message": "Service request not found"}), 404

        # Update the action
        service_request.Action = action
        db.session.commit()

        return jsonify({"success": True, "message": "Action updated successfully"}), 200

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@cust.route('/get_completed_service_requests/<int:user_id>', methods=['GET'])
@cross_origin()
def get_completed_service_requests(user_id):
    try:
        user_id = int(user_id)
    except ValueError:
        return jsonify({"success": False, "message": "Invalid User ID"}), 400
    service_requests = Service_Requests.query.filter_by( Customer_id=user_id, Status="accepted", Action="closed").all()
    if not service_requests:
        return jsonify({"success": True, "serviceRequests": []}), 200

    requests_list = []
    for req in service_requests:
        professional = Service_Professionals.query.filter_by(Professional_id=req.Professional_id).first()
        professional_name = professional.Name if professional else "Unknown"

        service = Services.query.filter_by(Service_id=req.Service_id).first()
        service_name = service.Name if service else "Unknown"

        # Add request details
        request_data = {
            "id": req.Request_id,
            "serviceType": req.Service_id,
            "professionalName": professional_name,
            "endDate": req.End_date.strftime("%Y-%m-%d") if req.End_date else "N/A",
            "status": req.Status,
            "action": req.Action
        }
        requests_list.append(request_data)

    return jsonify({"success": True, "serviceRequests": requests_list}), 200


@cust.route('/get_service_details/<int:service_id>', methods=['GET'])
@cross_origin()
def get_service_details(service_id):
    service_request = Service_Requests.query.filter_by(Request_id=service_id).first()
    
    if not service_request:
        return jsonify({'success': False, 'message': 'Service request not found'}), 404

    professional = Service_Professionals.query.filter_by(Professional_id = service_request.Professional_id).first()

    if not professional:
        return jsonify({'success': False, 'message': 'Professional or service not found'}), 404

    return jsonify({
        'success': True,
        'service': {
            'request_id': service_request.Request_id,
            'customer_id': service_request.Customer_id,
            'professional_id': service_request.Professional_id,
            'serviceType': service_request.Service_id,
            'professionalName': professional.Name
        }
    })

@cust.route('/submit_service_rating', methods=['POST'])
@cross_origin()
def submit_service_rating():
    data = request.json
    user_id = data.get('user_id')
    service_id = data.get('service_id')
    rating = data.get('rating')
    comment = data.get('comment')

    if not (1 <= rating <= 5):
        return jsonify({'success': False, 'message': 'Invalid rating value'}), 400

    service_request = Service_Requests.query.filter_by(Request_id=service_id).first()
    if not service_request:
        return jsonify({'success': False, 'message': 'Service request not found'}), 404

    new_review = Reviews(
        Request_id=service_id,
        Customer_id=user_id,
        Professional_id=service_request.Professional_id,
        Ratings=rating,
        Comment=comment
    )
    db.session.add(new_review)
    db.session.commit()

    return jsonify({'success': True, 'message': 'Rating submitted successfully'})



@cust.route('/get_customer_profile/<int:user_id>', methods=['GET','OPTIONS'])
@cross_origin()
def get_customer_profile(user_id):
    try:
        customer = Customers.query.filter_by(User_id=user_id).first()
        if not customer:
            return jsonify({'success': False, 'message': 'Customer not found'}), 404
        customer_data = {
            'customer_id': customer.Customer_id,
            'name': customer.Name,
            'email': customer.Email,
            'contact': customer.Contact,
            'city': customer.City,
            'locality': customer.Locality
        }
        return jsonify({'success': True, 'data': customer_data}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@cust.route('/update_customer_profile/<int:userId>',methods=['PUT','OPTIONS'])
@cross_origin()
def update_customer_profile(userId):
    try:
        customer=Customers.query.filter_by(User_id=userId).first()
        if not customer:
            return jsonify({'success': False, 'message': 'Profile not found'}), 404
        data=request.get_json()
       
        customer.Name = data.get('name', customer.Name)
        customer.Email = data.get('email', customer.Email)
        customer.Contact = data.get('contact', customer.Contact)
        customer.City=data.get('city',customer.City)
        customer.Locality=data.get('locality',customer.Locality)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Profile updated successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

    