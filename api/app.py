from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_talisman import Talisman
from flask_limiter import Limiter
from werkzeug.exceptions import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from config import Config

app = Flask(__name__)
app.config.from_object(Config)


db = SQLAlchemy(app)
CORS(app)

talisman = Talisman(
    app, 
    content_security_policy=Config.TALISMAN_CSP,
    force_https=Config.TALISMAN_FORCE_HTTPS,
    frame_options=Config.TALISMAN_FRAME_OPTIONS
)
limiter = Limiter(app, default_limits=["200000 per day", "5000 per hour"])


from routes import *

# General Exception Handler
@app.errorhandler(Exception)
def handle_exception(e):
    app.logger.error(f'An unexpected error occurred: {str(e)}')
    return jsonify({'error': 'An unexpected error occurred'}), 500

# HTTP Exception Handlers
@app.errorhandler(404)
def handle_404(e):
    return jsonify({'error': 'Resource not found'}), 404

@app.errorhandler(405)
def handle_405(e):
    return jsonify({'error': 'Method not allowed'}), 405

# Database Error Handler
@app.errorhandler(SQLAlchemyError)
def handle_sqlalchemy_error(e):
    # Rollback the session in case of database errors
    db.session.rollback()
    app.logger.error(f'Database error: {str(e)}')
    return jsonify({'error': 'A database error occurred'}), 500

# Other specific HTTP exception handlers can be added here

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)