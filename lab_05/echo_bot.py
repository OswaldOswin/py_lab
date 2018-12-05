import telebot
import config
import random
bot = telebot.TeleBot(config.token)

@bot.message_handler(content_types=['text'])
def echo(message):
    bot.send_message(message.chat.id, random.choice(["саня пидор", "соси", "ты приемный", "верни сотку"]))

if __name__ == '__main__':
    bot.polling(none_stop=True)
