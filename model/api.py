from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import pandas as pd
from chatbot import get_response


from model import model  # Import your model class from the model module

load_dotenv()

app = FastAPI()



# Add CORS middleware with specific configurations
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
    "http://172.20.10.2:3001","http://localhost:3001"
],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Content-Type", "Authorization"],
)


port = int(os.getenv("PORT", 9000))


class HealthData(BaseModel):
    age: int
    sex: int
    cp: int
    trestbps: int
    chol: int
    fbs: int
    restecg: int
    thalach: int
    exang: int
    oldpeak: float
    slope: int
    ca: int
    thal: int

class Message(BaseModel):
    text: str
    context: dict
    session_id: str



@app.post("/chat")
async def chat_with_bot(message: Message):
    session_id = message.session_id
    context=message.context
    text=message.text
    response = get_response(context=context, message=text, session_id=session_id)
    output=("").join(response)

    return {"response": output}


@app.post('/prediction')
async def check_health_data(data: HealthData):
    try:
        # Create a DataFrame from the received data
        new_data = pd.DataFrame(data.dict(), index=[0])

        # Use your model to make predictions
        answer = model.predict(new_data)
        
        # Define parameter meanings
        parameter_meanings = {
            "age": "Age in years",
            "sex": "Sex (0: female, 1: male)",
            "cp": "Chest pain type (0-3)",
            "trestbps": "Resting blood pressure (mm Hg)",
            "chol": "Serum cholesterol (mg/dl)",
            "fbs": "Fasting blood sugar > 120 mg/dl (1: true, 0: false)",
            "restecg": "Resting electrocardiographic results (0-2)",
            "thalach": "Maximum heart rate achieved",
            "exang": "Exercise induced angina (1: yes, 0: no)",
            "oldpeak": "ST depression induced by exercise relative to rest",
            "slope": "Slope of the peak exercise ST segment",
            "ca": "Number of major vessels (0-3) colored by fluoroscopy",
            "thal": "Thalassemia type (0-3)"
        }
        
        # Prepare the response JSON
        response_data = {parameter_meanings[key]: value for key, value in data.dict().items()}
        response_data["Status"] = "You have heart disease" if answer == 1 else "You do not have heart disease"
        response_data["Prediction"]=1 if answer==1 else 0
        return {"response": response_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=port)
