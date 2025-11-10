from dotenv import load_dotenv
import os
import telebot



load_dotenv('token.env') 

BOT_TOKEN = os.environ.get('BOT_TOKEN')

bot = telebot.TeleBot(BOT_TOKEN)

last_bot_messages = {}

def delete_last_bot_message(chat_id: int):
    """Удаляет последнее отправленное ботом сообщение в указанном чате, если оно есть."""
    if chat_id in last_bot_messages:
        try:
            bot.delete_message(chat_id=chat_id, message_id=last_bot_messages[chat_id])
            # Удаляем из словаря, чтобы не пытаться удалить сообщение снова
            del last_bot_messages[chat_id]
        except telebot.apihelper.ApiTelegramException as e:
            print(f"Failed to delete message: {e}")

@bot.message_handler(commands=['start','hello'])
def send_welcome(message):
    delete_last_bot_message(message.chat.id)
    sent_message = bot.send_message(message.chat.id, "Здарова, датебайо")
    last_bot_messages[message.chat.id] = sent_message.message_id

@bot.message_handler(commands=['naruto'])
def echo_all(message):
    delete_last_bot_message(message.chat.id)
    sent_message = bot.send_message(message.chat.id, "Ты не злой ты не злой, ты хороший ты хороший!")
    last_bot_messages[message.chat.id] = sent_message.message_id
    bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)


bot.infinity_polling()
