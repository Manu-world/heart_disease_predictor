# import requests

# url = "https://heart-disease-predictor-7.onrender.com/chat"
# headers = {"Content-Type": "application/json"}
# data = {
#      "text": "What are the symptoms of heart disease?",
#      "context": "The patient is a 57-year-old male with a history of smoking.",
#      "session_id": "12345"
# }

# response = requests.post(url, json=data, headers=headers)
# print(response.json())

# @app.post('/check')
# async def check_health_data(
#     response: Response,
#     age: int = Form(...),
#     sex: int = Form(...),
#     cp: int = Form(...),
#     trestbps: int = Form(...),
#     chol: int = Form(...),
#     fbs: int = Form(...),
#     restecg: int = Form(...),
#     thalach: int = Form(...),
#     exang: int = Form(...),
#     oldpeak: float = Form(...),
#     slope: int = Form(...),
#     ca: int = Form(...),
#     thal: int = Form(...)
# ):
#     new_data = pd.DataFrame({
#         "age": [age],
#         "sex": [sex],
#         "cp": [cp],
#         "trestbps": [trestbps],
#         "chol": [chol],
#         "fbs": [fbs],
#         "restecg": [restecg],
#         "thalach": [thalach],
#         "exang": [exang],
#         "oldpeak": [oldpeak],
#         "slope": [slope],
#         "ca": [ca],
#         "thal": [thal],
#     }, index=[0])

#     answer = model.predict(new_data)
#     if answer == 1:
#         response_text = "Status: You have heart disease"
#     elif answer == 0:
#         response_text = "Status: You not have heart disease"
    
#     response.set_cookie(key="health_status", value=response_text, secure=False)
#     return {"response": response_text}

