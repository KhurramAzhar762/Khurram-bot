from flask import Flask, request
import requests
import os
app = Flask(__name__)
VERIFY_TOKEN = "khurram123"
ACCESS_TOKEN = os.environ.get("WHATSAPP_TOKEN", "EAAWHB7ra2I8BSIfD6Hlp6Vj85J3F4ESA6DULvpp7o9MkUgfWhm3twB9RJI")
PHONE_NUMBER_ID = "1360556050475485"
@app.route("/")
def home():
    return "WhatsApp Bot is Live!"
@app.route("/webhook", methods=["GET"])
def verify_webhook():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    if mode == "subscribe" and token == VERIFY_TOKEN:
        return challenge, 200
    return "Verification failed", 403
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    try:
        if data["object"] == "whatsapp_business_account":
            for entry in data["entry"]:
                for change in entry["changes"]:
                    if "messages" in change["value"]:
                        msg = change["value"]["messages"][0]
                        from_number = msg["from"]
                        text = msg["text"]["body"]
                        send_message(from_number, f"Hello! You said: {text} - Bot is working!")
    except Exception as e:
        print(e)
    return "OK", 200
def send_message(to, text):
    url = f"https://graph.facebook.com/v20.0/{PHONE_NUMBER_ID}/messages"
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}", "Content-Type": "application/json"}
    data = {"messaging_product": "whatsapp", "to": to, "type": "text", "text": {"body": text}}
    requests.post(url, headers=headers, json=data)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
