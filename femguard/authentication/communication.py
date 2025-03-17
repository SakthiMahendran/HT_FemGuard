import os
from dotenv import load_dotenv
from twilio.rest import Client

def communication_page():
    # Load environment variables
    load_dotenv()
    
    # Twilio setup
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    twilio_number = os.getenv("TWILIO_NUMBER")
    to_number = os.getenv("TO_NUMBER")

    client = Client(account_sid, auth_token)

    def send_location_sms():
        location_link = "https://maps.app.goo.gl/CZj1QCrL8Uy6ZB5g8"
        message_body = f"Your contact is traveling in a danger zone. Track their location here: {location_link}"
        
        try:
            # Sending SMS using Twilio client
            message = client.messages.create(
                body=message_body,
                from_=twilio_number,
                to=to_number
            )
            print(f"SMS sent: {message.sid}")
            
            # Write to the emergency alert file
            with open("emergency_alert.txt", "w") as file:
                file.write("Emergency Alert: User is in a danger zone!\n")
                
            return {"status": "success", "message_sid": message.sid}
        except Exception as e:
            print(f"Error sending SMS: {e}")
            return {"status": "error", "message": str(e)}

    def make_emergency_call():
        try:
            call = client.calls.create(
                twiml='<Response><Say>Your emergency contact has initiated an emergency call. Please check on them.</Say></Response>',
                to=to_number,
                from_=twilio_number
            )
            print(f"Call initiated: {call.sid}")
            
            # Write to the emergency alert file
            with open("emergency_alert.txt", "w") as file:
                file.write("Emergency Alert: Emergency call initiated!\n")
                
            return {"status": "success", "call_sid": call.sid}
        except Exception as e:
            print(f"Error initiating call: {e}")
            return {"status": "error", "message": str(e)}