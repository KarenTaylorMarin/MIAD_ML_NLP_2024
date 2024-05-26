#!/usr/bin/python

from flask import Flask
from flask_restx import Api, Resource, fields, reqparse
from flask_cors import CORS
import joblib

app = Flask(__name__)
CORS(app)  # Habilitar CORS para todas las rutas y orígenes

api = Api(
    app, 
    version='1.0', 
    title='Movie Genres Prediction API',
    description='Movie Genres Prediction API')

ns = api.namespace('Predicción', description='Movie Classifier')

# Definir el analizador de argumentos
parser = reqparse.RequestParser()
parser.add_argument(
    'year', 
    type=int, 
    required=True, 
    help='Año de estreno de la película', 
    location='args')
parser.add_argument(
    'title', 
    type=str, 
    required=True, 
    help='Título de la película', 
    location='args')
parser.add_argument(
    'plot', 
    type=str, 
    required=True, 
    help='Argumento de la película', 
    location='args')

# Definir los campos de respuesta
resource_fields = api.model('Resource', {
    'Price': fields.Float,
})

@ns.route('/')
class MoviePrediction(Resource):

    @api.doc(parser=parser)
    @api.marshal_with(resource_fields)
    def get(self):
        args = parser.parse_args()
        
        # Lógica para predecir el precio
        prediction = mejor_modelo.predict(args['year', 'title', 'plot'])
        
        return {
            "Price": prediction
        }, 200
    
if __name__ == '__main__':
    app.run(debug=True, use_reloader=False, host='0.0.0.0', port=5000)

