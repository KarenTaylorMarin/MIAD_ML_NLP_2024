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
    title='API Prediccion Precio Vehiculos',
    description='API Prediccion Precio Vehiculos')

ns = api.namespace('Predicción', 
     description='Precio Vehiculos')

# Definición argumentos o parámetros de la API
parser = api.parser()
parser.add_argument(
    'Year', type=int, required=True, help='Year of the car', location='args')
parser.add_argument(
    'Mileage', type=int, required=True, help='Mileage of the car', location='args')
parser.add_argument(
    'Model', type=str, required=True, help='Model of the car', location='args')
parser.add_argument(
    'State', type=str, required=True, help='State of the car', location='args')

resource_fields = api.model('Resource', {
    'Price': fields.Float,
})

@ns.route('/')
class PricePrediction(Resource):

    @api.doc(parser=parser)
    @api.marshal_with(resource_fields)
    def get(self):
        args = parser.parse_args()
        
        return {
         "Price": mejor_modelo.predict(args['Year', 'Mileage', 'Model', 'State'])
        }, 200
    
    
if __name__ == '__main__':
    app.run(debug=True, use_reloader=False, host='0.0.0.0', port=5000)

