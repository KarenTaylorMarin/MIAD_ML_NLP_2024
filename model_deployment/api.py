#!/usr/bin/python

import pandas as pd
import numpy as np
from flask import Flask
from flask_restx import Api, Resource, fields
import joblib
from m09_model_deployment import predict_proba
from flask_cors import CORS

dataTraining = pd.read_csv('https://raw.githubusercontent.com/davidzarruk/MIAD_ML_NLP_2023/main/datasets/dataTrain_carListings.zip')
X_train = dataTraining.drop(['Make', 'State', 'Model', 'Price'], axis=1).join(pd.get_dummies(dataTraining['Model'], prefix='M'))

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes and origins

api = Api(
    app, 
    version='1.0', 
    title='API Prediccion Precio Vehiculos',
    description='API Prediccion Precio Vehiculos')

ns = api.namespace('Predicción', 
     description='Precio Vehiculos')
   
parser = api.parser()
parser.add_argument(
    'Year', type=int, required=True, help='Year of the car', location='args')
parser.add_argument(
    'Mileage', type=int, required=True, help='Mileage of the car', location='args')

columnas_modelo = True

if columnas_modelo:
    for col in X_train.columns:
        if col.startswith('M_'):
            parser.add_argument(col, type=float, required=False, help=f'{col} value', location='args')

resource_fields = api.model('Resource', {
    'Price': fields.Float,
})

@ns.route('/')
class PricePrediction(Resource):

    @api.doc(parser=parser)
    @api.marshal_with(resource_fields)
    def get(self):
        args = parser.parse_args()
        year = args['Year']
        mileage = args['Mileage']
        modelo_diligenciado = None

        for col in X_train.columns:
            if col.startswith('M_') and args.get(col) is not None:
                modelo_diligenciado = args[col]
                break

        total_columnas = [[year, mileage, modelo_diligenciado]]
        pred_precio = grid_search_xgb.predict(total_columnas)

        return {
         "Precio": float(pred_precio[0])}, 200
    
    
if __name__ == '__main__':
    app.run(debug=True, use_reloader=False, host='0.0.0.0', port=5000)
