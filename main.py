
import os
from flask import Flask, request
import requests
BOT_TOKEN= os.getenv("BOT_TOKEN")

app = Flask(__name__)

BOT_TOKEN = "7492991149:AAEXvqQzkrOTlCUf28siqXp7jQa2kKtWidM"
API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

user_data = {}

def predict_next_round(history):
    if len(history) < 10:
        return "Enter 10 rounds first."
    avg = sum(history[-10:]) / 10
    prediction = round(avg * 1.15, 2)
    confidence = "High" if prediction > 9 else "Medium"
    return f"🎯 Predicted Next Round: {prediction}x\nConfidence: {confidence}"

@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    data = request.get_json()
    message = data.get("message", {})
    text = message.get("text", "")
    chat_id = message.get("chat", {}).get("id")

    if not chat_id or not text:
        return {"ok": True}

    if chat_id not in user_data:
        user_data[chat_id] = []

    if text.startswith("/start"):
        reply = "Welcome to Selihana Aviator Predictor!\nSend rounds using /round <value> (e.g. /round 2.34)."
    elif text.startswith("/round"):
        try:
            val = float(text.split()[1])
            user_data[chat_id].append(val)
            reply = f"✅ Logged: {val}x\n" + predict_next_round(user_data[chat_id])
        except:
            reply = "Please send a valid number like /round 2.34"
    elif text.startswith("/status"):
        reply = "Bot is online and listening for your rounds."
    else:
        reply = "Unknown command. Use /round <value> to log rounds."

    requests.post(API_URL, json={"chat_id": chat_id, "text": reply})
    return {"ok": True}

@app.route("/", methods=["GET"])
def index():
    return "Bot is running."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
