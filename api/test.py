import requests

url = "https://heart-disease-predictor-8.onrender.com/chat"
uri="https://5fdd-41-155-62-9.ngrok-free.app/chat"
headers = {"Content-Type": "application/json"}
data = {
     "text": "What are the symptoms of heart disease?",
     "context": "The patient is a 57-year-old male with a history of smoking.",
     "session_id": "12345"
}

response = requests.post(uri, json=data, headers=headers)
print(response.json())