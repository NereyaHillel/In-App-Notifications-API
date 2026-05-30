from flask import Blueprint, request, jsonify
from DB_Connector import DBConnector


in_app_notifications_bp = Blueprint('in_app_notifications_bp', __name__)

@in_app_notifications_bp.route('/in-app-notifications', methods=['POST'])
def create_notification():
    """Create a new in-app notification
    ---    
    tags:
      - In-App Notifications
    parameters:
      - name: in_app_notification
        in: body
        required: true
        description: Notification details to be created
        schema:
          type: object
          id: InAppNotification
          required:
            - user_id
            - message
            - start_date
            - end_date
            - status
          properties:
            user_id:
              type: string
              description: ID of the user to receive the notification
            message:
              type: string
              description: Notification message content
            start_date:
              type: string
              format: date-time
              description: Start date and time for the notification
            end_date:
              type: string
              format: date-time
              description: End date and time for the notification
            status:
              type: string
              description: Status of the notification
    responses:
        201:
            description: Notification created successfully
        400:
            description: Invalid input
        500:
            description: Internal server error
        """
    # Logic to create a new in-app notification
    data = request.get_json()
    db = DBConnector.get_db()
    
    if db is None:
        return jsonify({"error": "Database connection failed"}), 500
    
    if not data:
        return jsonify({"error": "Invalid input, JSON data is required"}), 400
    
    if not all(key in data for key in ['user_id', 'message', 'start_date', 'end_date', 'status']):
        return jsonify({"error": "Missing required fields: user_id, message, start_date, end_date, status"}), 400
    
    if not isinstance(data['user_id'], str) or not isinstance(data['message'], str) or not isinstance(data['status'], str):
        return jsonify({"error": "Invalid input types: user_id, message, and status must be strings"}), 400
    
    if not isinstance(data['start_date'], str) or not isinstance(data['end_date'], str):
        return jsonify({"error": "Invalid input types: start_date and end_date must be strings in date-time format"}), 400
    
    if data['status'] not in ['active', 'inactive']:
        return jsonify({"error": "Invalid status value: must be 'active' or 'inactive'"}), 400
    
    if data['start_date'] >= data['end_date']:
        return jsonify({"error": "Invalid date range: start_date must be before end_date"}), 400
            
    
    user_id = data.get('user_id')
    message = data.get('message')
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    status = data.get('status')
