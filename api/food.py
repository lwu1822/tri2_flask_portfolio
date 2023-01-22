
from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource # used for REST API building
from datetime import datetime

from model.users import User
from model.food import Food 

food_api = Blueprint('food_api', __name__,
                   url_prefix='/api/foods')

# API docs https://flask-restful.readthedocs.io/en/latest/api.html
api = Api(food_api)

class FoodAPI:        
    class _Create(Resource):
        def post(self):
            ''' Read data for json body '''
            body = request.get_json()
            
            ''' Avoid garbage in, error checking '''
            # validate name
            name = body.get('name')
            if name is None or len(name) < 1:
                return {'message': f'Name is missing'}, 210
            # validate uid
            category = body.get('category')
            if category is None or len(category) < 1:
                return {'message': f'Category is missing'}, 210
            # look for password and dob
            time = body.get('time')

            ''' #1: Key code block, setup USER OBJECT '''
            foodObj = Food(name=name, 
                      category=category,time=time)
        
            
            ''' #2: Key Code block to add user to database '''
            # create user in database
            food = foodObj.create()
            # success returns json of user
            if food:
                return jsonify(food.read())
            # failure returns error
            return {'message': f'Processed {name}, either a format error or User ID {uid} is duplicate'}, 210

    class _Read(Resource):
        def get(self):
            foods = Food.query.all()    # read/extract all users from database
            json_ready = [food.read() for food in foods]  # prepare output in json
            return jsonify(json_ready)  # jsonify creates Flask response object, more specific to APIs than json.dumps

    # building RESTapi endpoint
    api.add_resource(_Create, '/create')
    api.add_resource(_Read, '/')