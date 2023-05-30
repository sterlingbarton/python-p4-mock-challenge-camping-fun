#!/usr/bin/env python3

from models import db, Activity, Camper, Signup
from flask_restful import Api, Resource
from flask_migrate import Migrate
from flask import Flask, make_response, jsonify, request
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'instance/app.db')}")


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)


@app.route('/')
def home():
    return ''


class Campers(Resource):

    def get(self):
        campers = [camper.to_dict() for camper in Camper.query.all()]
        return make_response(jsonify(campers), 200)

    def post(self):
        try:
            new_camper = Camper(
                name=request.get_json()['name'],
                age=request.get_json()['age'],
            )

            db.session.add(new_camper)
            db.session.commit()

            return make_response(new_camper.to_dict(), 201)
        except:
            return make_response({"error": "Post new camper failed."}, 400)


api.add_resource(Campers, '/campers')


class CampersById(Resource):

    def get(self, id):
        try:
            camper = Camper.query.filter(Camper.id == id).first()
            return make_response(jsonify(camper.to_dict()), 200)
        except:
            return make_response({"error": "Camper not found."}, 404)


api.add_resource(CampersById, '/campers/<int:id>')


class Activities(Resource):

    def get(self):
        activities = [activity.to_dict() for activity in Activity.query.all()]
        return make_response(jsonify(activities), 200)


api.add_resource(Activities, '/activities')


class ActivitiesById(Resource):

    def delete(self, id):
        activity = Activity.query.filter(Activity.id == id).first()

        if activity is None:
            return make_response({"error": "Activity not found."}, 404)

        db.session.delete(activity)
        db.session.commit()

        return make_response("", 204)


api.add_resource(ActivitiesById, '/activities/<int:id>')


class Signups(Resource):

    def post(self):
        try:
            new_signup = Signup(
                time=request.get_json()['time'],
                camper_id=request.get_json()['camper_id'],
                activity_id=request.get_json()['activity_id'],
            )
            db.session.add(new_signup)
            db.session.commit()
            return make_response(new_signup.to_dict(), 201)

        except:
            return make_response({"error": "Post signup failed."}, 400)


api.add_resource(Signups, '/signups')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
