#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate
from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)


# Add view to get earthquake by id
@app.route('/earthquakes/<int:id>')
def get_earthquake_by_id(id):
    # Query the database for the earthquake with the given id
    earthquake = Earthquake.query.filter_by(id=id).first()
    
    # If earthquake is found, return JSON with earthquake data
    if earthquake:
        body = {
            'id': earthquake.id,
            'location': earthquake.location,
            'magnitude': earthquake.magnitude,
            'year': earthquake.year
        }
        return make_response(jsonify(body), 200)
    
    # If earthquake is not found, return 404 error
    else:
        body = {
            'message': f'Earthquake {id} not found.'
        }
        return make_response(jsonify(body), 404)


# Add view to get earthquakes by minimum magnitude
@app.route('/earthquakes/magnitude/<float:magnitude>')
def get_earthquakes_by_magnitude(magnitude):
    # Query the database for all earthquakes with magnitude >= parameter
    earthquakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()
    
    # Build list of earthquake dictionaries
    quakes = []
    for earthquake in earthquakes:
        quake_dict = {
            'id': earthquake.id,
            'location': earthquake.location,
            'magnitude': earthquake.magnitude,
            'year': earthquake.year
        }
        quakes.append(quake_dict)
    
    # Return JSON response with count and list of earthquakes
    body = {
        'count': len(quakes),
        'quakes': quakes
    }
    return make_response(jsonify(body), 200)


if __name__ == '__main__':
    app.run(port=5555, debug=True)