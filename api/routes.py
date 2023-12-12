
from app import app, db
from flask import request, jsonify
from models import ChatbotFlow, UserInteraction
from flask_cors import CORS

CORS(app)

@app.route('/save-flow', methods=['POST'])
def save_flow():
    try:
        flow_data = request.json
        new_flow = ChatbotFlow(flow_data=flow_data)
        db.session.add(new_flow)
        db.session.commit()
        return jsonify({'message': 'Flow saved successfully'}), 200
    except Exception as e:
        # Rollback in case of error
        db.session.rollback()
        # Log the exception for debugging
        app.logger.error(f'Error saving flow: {str(e)}')
        return jsonify({'error': 'An error occurred while saving the flow'}), 500

@app.route('/get-flow', methods=['GET'])
def get_flow():
    try:
        # Fetching the latest flow from the database
        # Assuming that ChatbotFlow model has a column 'id' for ordering
        latest_flow = ChatbotFlow.query.order_by(ChatbotFlow.id.desc()).first()
        if latest_flow:
            return jsonify(latest_flow.flow_data), 200
        else:
            return jsonify({'error': 'No flow data found'}), 404
    except Exception as e:
        # Loging the exception for debugging
        app.logger.error(f'Error fetching flow: {str(e)}')
        return jsonify({'error': 'An error occurred while fetching the flow'}), 500
    
@app.route('/user-interaction', methods=['POST'])
def user_interaction():
    try:
        data = request.json
        if not data:
            raise ValueError("No data provided")

        phone_number = data.get('phone_number')
        if not phone_number:
            raise ValueError("Phone number is required")

        existing_user = UserInteraction.query.filter_by(phone_number=phone_number).first()
        if existing_user:
            existing_user.date = data['date']
            existing_user.time = data['time']
            existing_user.action = data['action']
        else:
            new_interaction = UserInteraction(
                whatsapp_user_name=data.get('whatsapp_user_name'),
                phone_number=phone_number,
                action=data.get('action'),
                date=data.get('date'),
                time=data.get('time')
            )
            db.session.add(new_interaction)
        db.session.commit()
        return jsonify({'message': 'Interaction recorded'}), 200
    except Exception as e:
        db.session.rollback()
        app.logger.error(f'Error in user_interaction: {str(e)}')
        return jsonify({'error': 'An error occurred'}), 500