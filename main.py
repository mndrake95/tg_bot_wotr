# Импортируем нужные функции
from dotenv import load_dotenv
import os
import telebot



# Загружаем переменные из файла token.env
load_dotenv('token.env') 

# Получаем токен из переменных окружения
BOT_TOKEN = os.environ.get('BOT_TOKEN')

# Юзаем эту переменную для инициализации бота
bot = telebot.TeleBot(BOT_TOKEN)

# Словарь для хранения последнего сообщения бота в каждом чате
last_bot_messages = {}

@bot.message_handler(commands=['start','hello'])
def send_welcome(message):
    chat_id = message.chat.id
    if chat_id in last_bot_messages:
        try:
            bot.delete_message(chat_id=chat_id, message_id=last_bot_messages[chat_id])
        except telebot.apihelper.ApiTelegramException as e:
            print(f"Failed to delete message: {e}")

    sent_message = bot.send_message(chat_id, "Здарова, датебайо")
    last_bot_messages[chat_id] = sent_message.message_id

@bot.message_handler(commands=['naruto'])
def echo_all(message):
    chat_id = message.chat.id
    if chat_id in last_bot_messages:
        try:
            bot.delete_message(chat_id=chat_id, message_id=last_bot_messages[chat_id])
        except telebot.apihelper.ApiTelegramException as e:
            print(f"Failed to delete message: {e}")

    sent_message = bot.send_message(chat_id, "Ты не злой ты не злой, ты хороший ты хороший!")
    last_bot_messages[chat_id] = sent_message.message_id
    bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)


bot.infinity_polling()
