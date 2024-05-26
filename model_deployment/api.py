#!/usr/bin/python

from flask import Flask
from flask_restx import Api, Resource, fields
import joblib
from m09_model_deployment import predict_proba
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes and origins

api = Api(
    app, 
    version='1.0', 
    title='Movie Genres Prediction API',
    description='Movie Genres Prediction API')

ns = api.namespace('Predicción', 
     description='Movie Classifier')

parser = api.parser()
parser.add_argument(
    'year', 
    type=int, 
    required=True, 
    help='Año de estreno de la pelicula', 
    location='args')
parser.add_argument(
    'title', 
    type=str, 
    required=True, 
    help='Año de estreno de la pelicula', 
    location='args')
parser.add_argument(
    'plot', 
    type=str, 
    required=True, 
    help='Año de estreno de la pelicula', 
    location='args')

@ns.route('/')
class MoviePrediction(Resource):

    @api.doc(parser=parser)
    @api.marshal_with(resource_fields)
    def get(self):
        args = parser.parse_args()

        prediction = modelo.predict(args['year', 'title', 'plot'])
        
        return {
         "Pelicula": prediction
        }, 200
    
    
if __name__ == '__main__':
    app.run(debug=True, use_reloader=False, host='0.0.0.0', port=5000)

