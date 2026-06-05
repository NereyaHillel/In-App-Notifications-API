from flask import Blueprint, request, jsonify
from DB_Connector import DBConnector


in_app_notifications_bp = Blueprint('in_app_notifications_bp', __name__)

@in_app_notifications_bp.route('/h/api/v1/sdk/device/register', methods=['POST'])
def register_device():
    """Register a device for in-app notifications
    ---
    tags:
      - In-App Notifications - Device Registration
    parameters:
      - name: device_info
        in: body
        required: true
        description: Device information for registration
        schema:
          type: object
          required:
            - device_id
            - user_id
          properties:
            device_id:
              type: string
              description: Unique identifier for the device
            user_id:
              type: string
              description: Identifier for the user associated with the device
    responses:
        200:
            description: Device registered successfully
        400:
            description: Invalid input
        500:
            description: Internal server error
    """
    # Logic to register a device for in-app notifications
    data = request.get_json()
    db = DBConnector.get_db()
    
    if db is None:
        return jsonify({"error": "Database connection failed"}), 500
    
    if not data:
        return jsonify({"error": "Invalid input, JSON data is required"}), 400
    
    if not isinstance(data['device_id'], str) or not isinstance(data['user_id'], str):
        return jsonify({"error": "Invalid input types: device_id and user_id must be strings"}), 400
    
    device_id = data.get('device_id')
    user_id = data.get('user_id')
    
    db.registered_devices.insert_one({
        "device_id": device_id,
        "user_id": user_id
    })
    
    return jsonify({"message": "Device registered successfully", "device": {
        "device_id": device_id,
        "user_id": user_id
    }}), 200
    
    
    

@in_app_notifications_bp.route('/api/v1/sdk/notifications', methods=['GET'])
def get_notifications():
    """Get in-app notifications for a user
    ---
    tags:
      - In-App Notifications - Get Notifications
    parameters:
      - name: user_id
        in: query
        required: true
        description: Identifier for the user to retrieve notifications for
        schema:
          type: string
    responses:
        200:
            description: Notifications retrieved successfully
        400:
            description: Invalid input
        500:
            description: Internal server error
    """
    # Logic to retrieve in-app notifications for a user
    user_id = request.args.get('user_id')
    db = DBConnector.get_db()
    
    if db is None:
        return jsonify({"error": "Database connection failed"}), 500
    
    if not user_id:
        return jsonify({"error": "Invalid input, user_id is required"}), 400
    
    notifications = list(db.notifications.find({"user_id": user_id}))
    
    return jsonify({"message": "Notifications retrieved successfully", "notifications": notifications}), 200
  
  
@in_app_notifications_bp.route('/api/v1/sdk/sync', methods=['POST'])
def sync_notifications():
    """Sync in-app notifications for a user
    ---
    tags:
      - In-App Notifications - Sync Notifications
    parameters:
      - name: user_id
        in: body
        required: true
        description: Identifier for the user to sync notifications for
        schema:
          type: object
          required:
            - user_id
          properties:
            user_id:
              type: string
              description: Identifier for the user to sync notifications for
    responses:
        200:
            description: Notifications synced successfully
        400:
            description: Invalid input
        500:
            description: Internal server error
    """
    # Logic to sync in-app notifications for a user
    data = request.get_json()
    db = DBConnector.get_db()
    
    if db is None:
        return jsonify({"error": "Database connection failed"}), 500
    
    if not data:
        return jsonify({"error": "Invalid input, JSON data is required"}), 400
    
    if not isinstance(data['user_id'], str):
        return jsonify({"error": "Invalid input type: user_id must be a string"}), 400
    
    user_id = data.get('user_id')
    
    # Logic to sync notifications for the user (e.g., mark as read, fetch new notifications, etc.)
    
    return jsonify({"message": "Notifications synced successfully", "user_id": user_id}), 200
  
  
@in_app_notifications_bp.route('/api/v1/sdk/crash-report', methods=['POST'])
def report_crash():
    """Report a crash for in-app notifications
    ---
    tags:
      - In-App Notifications - Crash Reporting 
    parameters:
      - name: crash_info
        in: body
        required: true
        description: Crash information for reporting
        schema:
          type: object
          required:
            - user_id
            - crash_details
          properties:
            user_id:
              type: string
              description: Identifier for the user who experienced the crash
            crash_details:
              type: string
              description: Details about the crash (e.g., error message, stack trace, etc.)
    responses:
        200:
            description: Crash reported successfully
        400:
            description: Invalid input
        500:
            description: Internal server error
    """
    # Logic to report a crash for in-app notifications
    data = request.get_json()
    db = DBConnector.get_db()
    
    if db is None:
        return jsonify({"error": "Database connection failed"}), 500
    
    if not data:
        return jsonify({"error": "Invalid input, JSON data is required"}), 400
    
    if not isinstance(data['user_id'], str) or not isinstance(data['crash_details'], str):
        return jsonify({"error": "Invalid input types: user_id and crash_details must be strings"}), 400
    
    user_id = data.get('user_id')
    crash_details = data.get('crash_details')
    
    db.crash_reports.insert_one({
        "user_id": user_id,
        "crash_details": crash_details
    })
    
    return jsonify({"message": "Crash reported successfully", "crash_report": {
        "user_id": user_id,
        "crash_details": crash_details
    }}), 200
    
@in_app_notifications_bp.route('/api/v1/admin/campaigns', methods=['GET'])
def get_campaigns():
    """Get all in-app notification campaigns
    ---
    tags:
      - In-App Notifications - Campaign Management
    responses:
        200:
            description: Campaigns retrieved successfully
        500:
            description: Internal server error
    """
    # Logic to retrieve all in-app notification campaigns
    db = DBConnector.get_db()
    
    if db is None:
        return jsonify({"error": "Database connection failed"}), 500
    
    campaigns = list(db.campaigns.find())
    
    return jsonify({"message": "Campaigns retrieved successfully", "campaigns": campaigns}), 200
  
@in_app_notifications_bp.route('/api/v1/admin/campaigns', methods=['POST'])
def create_campaign():
    """Create a new in-app notification campaign
    ---
    tags:
      - In-App Notifications - Campaign Management
    parameters:
      - name: campaign_info
        in: body
        required: true
        description: Information for creating a new campaign
        schema:
          type: object
          required:
            - name
            - message
          properties:
            name:
              type: string
              description: Name of the campaign
            message:
              type: string
              description: Message content for the campaign
    responses:
        200:
            description: Campaign created successfully
        400:
            description: Invalid input
        500:
            description: Internal server error
    """
    # Logic to create a new in-app notification campaign
    data = request.get_json()
    db = DBConnector.get_db()
    
    if db is None:
        return jsonify({"error": "Database connection failed"}), 500
    
    if not data:
        return jsonify({"error": "Invalid input, JSON data is required"}), 400
    
    if not isinstance(data['name'], str) or not isinstance(data['message'], str):
        return jsonify({"error": "Invalid input types: name and message must be strings"}), 400
    
    name = data.get('name')
    message = data.get('message')
    
    db.campaigns.insert_one({
        "name": name,
        "message": message
    })
    
    return jsonify({"message": "Campaign created successfully", "campaign": {
        "name": name,
        "message": message
    }}), 200
    
@in_app_notifications_bp.route('/api/v1/admin/campaigns/<campaign_id>', methods=['DELETE'])
def delete_campaign(campaign_id):
    """Delete an in-app notification campaign
    ---
    tags:
      - In-App Notifications - Campaign Management
    parameters:
      - name: campaign_id
        in: path
        required: true
        description: Identifier for the campaign to delete
        schema:
          type: string
    responses:
        200:
            description: Campaign deleted successfully
        400:
            description: Invalid input
        500:
            description: Internal server error
    """
    # Logic to delete an in-app notification campaign
    db = DBConnector.get_db()
    
    if db is None:
        return jsonify({"error": "Database connection failed"}), 500
    
    if not campaign_id:
        return jsonify({"error": "Invalid input, campaign_id is required"}), 400
    
    result = db.campaigns.delete_one({"_id": campaign_id})
    
    if result.deleted_count == 0:
        return jsonify({"error": "Campaign not found"}), 404
    
    return jsonify({"message": "Campaign deleted successfully", "campaign_id": campaign_id}), 200
  
@in_app_notifications_bp.route('/api/v1/admin/campaigns/<campaign_id>/status', methods=['PATCH'])
def update_campaign_status(campaign_id):
    """Update the status of an in-app notification campaign
    ---
    tags:
      - In-App Notifications - Campaign Management
    parameters:
      - name: campaign_id
        in: path
        required: true
        description: Identifier for the campaign to update
        schema:
          type: string
      - name: status
        in: body
        required: true
        description: New status for the campaign
        schema:
          type: object
          required:
            - status
          properties:
            status:
              type: string
              description: New status for the campaign (e.g., active, paused, etc.)
    responses:
        200:
            description: Campaign status updated successfully
        400:
            description: Invalid input
        500:
            description: Internal server error
    """
    # Logic to update the status of an in-app notification campaign
    data = request.get_json()
    db = DBConnector.get_db()
    
    if db is None:
        return jsonify({"error": "Database connection failed"}), 500
    
    if not data:
        return jsonify({"error": "Invalid input, JSON data is required"}), 400
    
    if not isinstance(data['status'], str):
        return jsonify({"error": "Invalid input type: status must be a string"}), 400
    
    status = data.get('status')
    
    result = db.campaigns.update_one({"_id": campaign_id}, {"$set": {"status": status}})
    
    if result.matched_count == 0:
        return jsonify({"error": "Campaign not found"}), 404
    
    return jsonify({"message": "Campaign status updated successfully", "campaign_id": campaign_id, "new_status": status}), 200
  
@in_app_notifications_bp.route('/api/v1/admin/campaigns/test-push', methods=['POST'])
def send_test_push():
    """Send a test push notification for an in-app notification campaign
    ---
    tags:
      - In-App Notifications - Campaign Management
    parameters:
      - name: test_push_info
        in: body
        required: true
        description: Information for sending a test push notification
        schema:
          type: object
          required:
            - campaign_id
            - user_id
          properties:
            campaign_id:
              type: string
              description: Identifier for the campaign to test
            user_id:
              type: string
              description: Identifier for the user to receive the test push notification
    responses:
        200:
            description: Test push notification sent successfully
        400:
            description: Invalid input
        500:
            description: Internal server error
    """ 
    # Logic to send a test push notification for an in-app notification campaign
    data = request.get_json()
    db = DBConnector.get_db()
    
    if db is None:
        return jsonify({"error": "Database connection failed"}), 500
    
    if not data:
        return jsonify({"error": "Invalid input, JSON data is required"}), 400
    
    if not isinstance(data['campaign_id'], str) or not isinstance(data['user_id'], str):
        return jsonify({"error": "Invalid input types: campaign_id and user_id must be strings"}), 400
    
    campaign_id = data.get('campaign_id')
    user_id = data.get('user_id')
    
    # Logic to send a test push notification to the user for the specified campaign
    
    return jsonify({"message": "Test push notification sent successfully", "test_push_info": {
        "campaign_id": campaign_id,
        "user_id": user_id
    }}), 200
    
@in_app_notifications_bp.route('/api/v1/admin/stats/overview', methods=['GET'])
def get_overview_stats():
    """Get overview statistics for in-app notifications
    ---
    tags:
      - In-App Notifications - Analytics and Reporting
    responses:
        200:
            description: Overview statistics retrieved successfully
        500:
            description: Internal server error 
    """
    # Logic to retrieve overview statistics for in-app notifications (e.g., total notifications sent, total active campaigns, etc.)
    db = DBConnector.get_db()
    
    if db is None:
        return jsonify({"error": "Database connection failed"}), 500
    
    stats = {
        "total_notifications_sent": db.notifications.count_documents({}),
        "total_active_campaigns": db.campaigns.count_documents({"status": "active"}),
        # Add more statistics as needed
    }
    
    return jsonify({"message": "Overview statistics retrieved successfully", "stats": stats}), 200
  
@in_app_notifications_bp.route('/api/v1/admin/stats/campaign/<campaign_id>', methods=['GET'])
def get_campaign_stats(campaign_id):
    """Get statistics for a specific in-app notification campaign
    ---
    tags:
      - In-App Notifications - Analytics and Reporting
    parameters:
      - name: campaign_id
        in: path
        required: true
        description: Identifier for the campaign to retrieve statistics for
        schema:
          type: string
    responses:
        200:
            description: Campaign statistics retrieved successfully
        400:
            description: Invalid input
        500:
            description: Internal server error
    """
    # Logic to retrieve statistics for a specific in-app notification campaign (e.g., total notifications sent for the campaign, total clicks, etc.)
    db = DBConnector.get_db()
    
    if db is None:
        return jsonify({"error": "Database connection failed"}), 500
    
    if not campaign_id:
        return jsonify({"error": "Invalid input, campaign_id is required"}), 400
    
    stats = {
        "total_notifications_sent": db.notifications.count_documents({"campaign_id": campaign_id}),
        "total_clicks": db.notifications.count_documents({"campaign_id": campaign_id, "clicked": True}),
        # Add more statistics as needed
    }
    
    return jsonify({"message": "Campaign statistics retrieved successfully", "campaign_id": campaign_id, "stats": stats}), 200.
  
  