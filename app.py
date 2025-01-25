from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
import os
import logging
from marshmallow import Schema, fields, ValidationError

# Initialize Flask application
app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)

# Configure database
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///poolgame.db')
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

# Define the Player model
class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    table = db.Column(db.String(50), nullable=False)

# Create the database tables
def create_tables():
    try:
        db.create_all()
        logging.info("Tables created successfully.")
    except Exception as e:
        logging.error(f"Error creating tables: {e}")

# Schema for input validation
class PlayerSchema(Schema):
    name = fields.String(required=True)
    table = fields.String(required=True)

player_schema = PlayerSchema()

# Route to add a new player
@app.route('/players', methods=['POST'])
def add_player():
    data = request.get_json()
    
    # Validate input
    try:
        player_schema.load(data)
    except ValidationError as e:
        return jsonify({'message': 'Invalid input', 'errors': e.messages}), 400
    
    new_player = Player(name=data['name'], table=data['table'])
    
    try:
        db.session.add(new_player)
        db.session.commit()
        return jsonify({'message': 'Player added successfully!'}), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({'message': 'Player already exists!'}), 400
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error adding player: {e}")
        return jsonify({'message': 'An error occurred. Please try again later.'}), 500

# Route to get all players
@app.route('/players', methods=['GET'])
def get_players():
    players = Player.query.all()
    return jsonify([{'id': player.id, 'name': player.name, 'table': player.table} for player in players]), 200

# Start the application
if __name__ == '__main__':
    create_tables()
    app.run(host='0.0.0.0', port=5000)
