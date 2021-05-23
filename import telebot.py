import telebot

bot = telebot.TeleBot("1734494822:AAEV57FXwoqyBRYFWarnJoQgNMl-ILLqZlk")

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Howdy, how are you doing?")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
	bot.reply_to(message, message.text)

bot.polling()

print('test')