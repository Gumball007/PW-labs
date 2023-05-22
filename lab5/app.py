import telebot

bot = telebot.TeleBot("6265105993:AAH37Vy19xNAs6k2ZjdAkGIwTFOSBAmDoSA")

@bot.message_handler(commands=['start'])
def send_welcome(message):
	bot.reply_to(message, "Say buna zîua to covrig_bot. Do u want some fake news? Here we go, fake covrigi")
	
@bot.message_handler(commands=['help'])
def send_welcome(message):
	bot.reply_to(message, "Pentru ajutor, sunați la 112")


@bot.message_handler(func=lambda message: True)
def echo_all(message):
	bot.reply_to(message, message.text)

bot.infinity_polling()