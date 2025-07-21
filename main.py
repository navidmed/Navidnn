import os  
import requests  
from flask import Flask, request, abort  

app = Flask(__name__)  

TOKEN = os.environ.get("BOT_TOKEN")  
if not TOKEN:  
    raise RuntimeError("BOT_TOKEN environment variable not set")  

TELEGRAM_API_URL = f"https://api.telegram.org/bot{TOKEN}"  

@app.route('/', methods=['GET'])  
def index():  
    return "NavidMed bot is running.", 200  

@app.route('/webhook', methods=['POST'])  
def telegram_webhook():  
    update = request.get_json(force=True)
    if not update or "message" not in update:
        return "No message", 200

    chat_id = update["message"]["chat"]["id"]  
    text = update["message"].get("text", "")  

    if text.strip().lower().startswith("/start"):  
        send_message(chat_id, "سلام! به ربات پزشکی نویدمد خوش آمدید. لطفا علائم بیماری خود را شرح دهید.")  
    else:
        send_message(chat_id, "پیام شما دریافت شد: " + text)

    return "OK", 200  

def send_message(chat_id, text):  
    requests.post(f"{TELEGRAM_API_URL}/sendMessage", json={"chat_id": chat_id, "text": text})  

if __name__ == "__main__":  
    port = int(os.environ.get("PORT", 5000))  
    app.run(host="0.0.0.0", port=port)
