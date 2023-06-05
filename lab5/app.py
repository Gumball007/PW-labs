import telebot
from flask import Flask, request
import os

bot = telebot.TeleBot("6265105993:AAH37Vy19xNAs6k2ZjdAkGIwTFOSBAmDoSA")
server = Flask(__name__)

TOKEN = "6265105993:AAH37Vy19xNAs6k2ZjdAkGIwTFOSBAmDoSA"
WEBHOOK_URL = "https://covrig.fly.dev"

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Say buna zîua to covrig_bot. Do u want some fake news? Here we go, fake covrigi")
    
@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.reply_to(message, "Pentru ajutor, sunați la 112")


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)

@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates(
        [telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200

@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL + "/" + TOKEN)
    return "!", 200


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))