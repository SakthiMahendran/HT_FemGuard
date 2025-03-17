import os
import json
import joblib
import torch
import numpy as np
from dotenv import load_dotenv
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from twilio.rest import Client
from .ai_handler import AIHandler
from .preditions import RiskSafetyPredictor, RiskSafetyNN

# Load environment variables
load_dotenv()

# Twilio setup
ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_NUMBER = os.getenv("TWILIO_NUMBER")
TO_NUMBER = os.getenv("TO_NUMBER")

client = Client(ACCOUNT_SID, AUTH_TOKEN)

# Initialize AIHandler
ai_handler = AIHandler()

# Load preprocessing objects
try:
    scaler = joblib.load("scaler.pkl")
    label_encoders = joblib.load("label_encoders.pkl")
    y_encoder = joblib.load("y_encoder.pkl")
    print("Successfully loaded scaler, label encoders, and y_encoder.")
except FileNotFoundError:
    print("Warning: Missing scaler or encoders! Creating new ones dynamically.")
    scaler = None
    label_encoders = {}
    y_encoder = None

# Load trained model
model_path = "risk_safety_nn.pth"
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
checkpoint = torch.load(model_path, map_location=device)
input_dim = checkpoint["fc1.weight"].shape[1]
output_dim = checkpoint["fc4.weight"].shape[0]

predictor = RiskSafetyPredictor(
    model=RiskSafetyNN(input_dim, output_dim).to(device),
    scaler=scaler,
    label_encoders=label_encoders,
    y_encoder=y_encoder,
    device=device
)

print("RiskSafetyPredictor instance created successfully.")

@csrf_exempt
def send_location_sms(request):
    if request.method == "POST":
        location_link = "https://maps.app.goo.gl/T395Dph1VWyo7MnU8"
        message_body = f"Your contact is traveling in a danger zone. Track their location here: {location_link}"
        try:
            message = client.messages.create(body=message_body, from_=TWILIO_NUMBER, to=TO_NUMBER)
            with open("emergency_alert.txt", "w") as file:
                file.write("Emergency Alert: User is in a danger zone!\n")
            return JsonResponse({"status": "success", "message_sid": message.sid})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)
    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=400)

@csrf_exempt
def make_emergency_call(request):
    if request.method == "POST":
        try:
            call = client.calls.create(
                twiml='<Response><Say>Your emergency contact has initiated an emergency call. Please check on them.</Say></Response>',
                to=TO_NUMBER,
                from_=TWILIO_NUMBER
            )
            with open("emergency_alert.txt", "w") as file:
                file.write("Emergency Alert: Emergency call initiated!\n")
            return JsonResponse({"status": "success", "call_sid": call.sid})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)
    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=400)

@csrf_exempt
def chat_with_ai(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            prompt = data.get("prompt", "")
            if not prompt:
                return JsonResponse({"error": "No prompt provided"}, status=400)
            response = ai_handler.process_prompt(prompt)
            return JsonResponse({"response": response}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)
    return JsonResponse({"error": "Only POST requests are allowed"}, status=405)

@csrf_exempt
def predict_safety_rating(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            latitude = data.get("latitude")
            longitude = data.get("longitude")
            if latitude is None or longitude is None:
                return JsonResponse({"error": "Latitude and Longitude required"}, status=400)
            
            prediction_result = predictor.predict(latitude, longitude)
            return JsonResponse(prediction_result, status=200)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)
    return JsonResponse({"error": "Only POST requests are allowed"}, status=405)

@csrf_exempt
def sos_alert(request):
    """
    Triggers both an SMS and an emergency call simultaneously.
    """
    if request.method == "POST":
        location_link = "https://maps.app.goo.gl/T395Dph1VWyo7MnU8"
        message_body = f"Emergency Alert! Your contact is in danger. Track their location here: {location_link}"
        try:
            # Send SMS
            message = client.messages.create(body=message_body, from_=TWILIO_NUMBER, to=TO_NUMBER)
            
            # Make Emergency Call
            call = client.calls.create(
                twiml='<Response><Say>Emergency Alert! Please check on your contact immediately.</Say></Response>',
                to=TO_NUMBER,
                from_=TWILIO_NUMBER
            )
            
            with open("emergency_alert.txt", "w") as file:
                file.write("Emergency Alert: SOS triggered!\n")
            
            return JsonResponse({
                "status": "success",
                "message_sid": message.sid,
                "call_sid": call.sid
            })
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)
    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=400)
