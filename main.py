import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))  # DON'T CHANGE THIS !!!

from flask import Flask, jsonify
from src import db
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager

app = Flask(__name__)
CORS(app)

# Configuración de la base de datos MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///royalty_invest.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'super-secret')

db.init_app(app)
jwt = JWTManager(app)

# Import models
from src.models.user import User
from src.models.property import Property
from src.models.rental_listing import RentalListing
from src.models.sale_listing import SaleListing
from src.models.reservation import Reservation
from src.models.transaction import Transaction
from src.models.commission import Commission

# Create database tables
with app.app_context():
    db.create_all()

# Register routes
from src.routes import register_routes

register_routes(app)

@app.route('/')
def index():
    return app.send_static_file('index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
