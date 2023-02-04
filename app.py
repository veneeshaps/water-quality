
# 1. Library imports
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
import pickle
import pandas as pd

# 2. Create the app object
app = FastAPI()
pickle_in = open("./static/random-forest-water.sav", "rb")
classifier = pickle.load(pickle_in)


# 3. Index route, opens automatically on http://127.0.0.1:8000
@app.get('/')
def index():
    return {'message': 'Welcome to water quality prediction API'}

@app.get('/inputs')
def Inputs_to_api():
    return {"Provide json data for ph,Hardness,Solids,Chloramines,Sulfate,Conductivity,Organic_carbon,Trihalomethanes,Turbidity"}



# 4. Route with a single parameter, returns the parameter within a message
#    Located at: http://127.0.0.1:8000/AnyNameHere
class Pollutants(BaseModel):
    ph: float
    Hardness: float
    Solids: float
    Chloramines: float
    Sulfate: float
    Conductivity: float
    Organic_carbon: float
    Trihalomethanes: float
    Turbidity: float

# 3. Expose the prediction functionality, make a prediction from the passed
#    JSON data and return the predicted Bank Note with the confidence
@app.post('/predict')
def Predict_level_of_pollution(data: Pollutants):
    print(data)
    data = data.dict()
    print(data)
    ph = data['ph']
    Hardness = data['Hardness']
    Solids = data['Solids']
    Chloramines = data['Chloramines']
    Sulfate = data['Sulfate']
    Conductivity = data['Conductivity']
    Organic_carbon = data['Organic_carbon']
    Trihalomethanes = data['Trihalomethanes']
    Turbidity = data['Turbidity']


    prediction = classifier.predict([[ph,Hardness,Solids,Chloramines,Sulfate,Conductivity,Organic_carbon,Trihalomethanes,Turbidity]])
    prediction = prediction.tolist()
    return {
        'potability': prediction[0],
        'Result' : 'Potable' if prediction[0]==1 else 'Not Potable'
    }
# @app.get('/{name}')
# def get_name(name: str):
#     return {'Welcome To Krish Youtube Channel': f'{name}'}


# 5. Run the API with uvicorn
# #    Will run on http://127.0.0.1:8000
# if __name__ == '__main__':
#     uvicorn.run(app, host='127.0.0.1', port=8000)

# uvicorn app:app --reload
