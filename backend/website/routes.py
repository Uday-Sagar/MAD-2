from flask_cors import cross_origin
from flask import Blueprint, request, jsonify
from .models import Users
from flask_jwt_extended import jwt_required, get_jwt_identity


views=Blueprint("views",__name__)


@views.route('/get_user/<int:user_id>',methods=['GET','OPTIONS'])
@cross_origin()
def get_user(user_id):
        if not user_id:
            return jsonify({"success": False, "message": "User ID is required"}), 400
        try:
            user_id = int(user_id)
        except ValueError:
            return jsonify({"success": False, "message": "Invalid User ID"}), 400
        user = Users.query.filter_by(User_id=user_id).first()
        if not user:
            return jsonify({"success": False, "message": "User not found"}), 404
        return jsonify({
            "success": True,
            "user": {
                "id": user.User_id,
                "name": user.Name
            }
        })





