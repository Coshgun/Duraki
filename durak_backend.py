from flask import Flask, jsonify, request
from flask_cors import CORS
import telegram

app = Flask(__name__)
CORS(app)

players = {
    # user_id: {"name": "User", "cards": ["6♠", "9♥", ...]}
}
TELEGRAM_BOT_TOKEN = "7912617632:AAHNXUxYYp2QhT6hq4_3kFEFsR16KHTwFhQ"
GROUP_CHAT_ID = "-1002471042754"  # və ya -1001234567890
bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)

@app.route("/api/cards/<int:user_id>")
def get_cards(user_id):
    if user_id not in players:
        return jsonify([])
    return jsonify(players[user_id]['cards'])

@app.route("/api/play", methods=['POST'])
def play_card():
    data = request.get_json()
    user_id = int(data['user_id'])
    card = data['card']

    if user_id in players and card in players[user_id]['cards']:
        players[user_id]['cards'].remove(card)
        user_name = players[user_id]['name']
        text = f"{user_name} kart oynadı: {card}"
        bot.send_message(chat_id=GROUP_CHAT_ID, text=text)
        return jsonify({"status": "ok"})

    return jsonify({"error": "Kart tapılmadı"}), 400

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
