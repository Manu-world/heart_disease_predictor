from fastapi import FastAPI,Form,Response,Request
from pydantic import BaseModel
from chatbot import get_response
from model import model 
import pandas as pd
from dotenv import load_dotenv
import os
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()
app = FastAPI()
# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5501"], # Allow requests from your frontend's origin
    allow_credentials=True,
    allow_methods=["*"], # Allow all methods
    allow_headers=["*"], # Allow all headers
)
class Message(BaseModel):
    text: str
    context: str
    session_id: str

port = int(os.getenv("PORT", 9000))

@app.post('/check')
async def check_health_data(
    response: Response,
    age: int = Form(...),
    sex: int = Form(...),
    cp: int = Form(...),
    trestbps: int = Form(...),
    chol: int = Form(...),
    fbs: int = Form(...),
    restecg: int = Form(...),
    thalach: int = Form(...),
    exang: int = Form(...),
    oldpeak: float = Form(...),
    slope: int = Form(...),
    ca: int = Form(...),
    thal: int = Form(...)
):
    new_data = pd.DataFrame({
        "age": [age],
        "sex": [sex],
        "cp": [cp],
        "trestbps": [trestbps],
        "chol": [chol],
        "fbs": [fbs],
        "restecg": [restecg],
        "thalach": [thalach],
        "exang": [exang],
        "oldpeak": [oldpeak],
        "slope": [slope],
        "ca": [ca],
        "thal": [thal],
    }, index=[0])

    answer = model.predict(new_data)
    if answer == 1:
        response_text = "Status: You have heart disease"
    elif answer == 0:
        response_text = "Status: You not have heart disease"
    
    response.set_cookie(key="health_status", value=response_text, secure=False)
    return {"response": response_text}


@app.post("/chat")
async def chat_with_bot(message: Message):
    session_id = message.session_id
    context=message.context
    text=message.text
    response = get_response(context=context,message=text, session_id=session_id)
    output=("").join(response)

    return {"response": output}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=port)