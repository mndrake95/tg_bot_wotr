from dotenv import load_dotenv
import os
import telebot
import random
import time

COOLDOWN_SECONDS = 300

chat_cooldowns = {}

TRIGGER_WORDS = ['наруто', 'naruto', 'злой', 'хороший']

PHRASES = [
    "Ты не злой ты не злой, ты хороший ты хороший!",
    "ДАТТЕБАЙО!",
    "Это мой путь ниндзя!",
    "Я стану Хокаге!"
]

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

@bot.message_handler(func=lambda message: True) 
def handle_trigger_phrases(message):
    chat_id = message.chat.id
    current_time = time.time()
    message_text = message.text.lower() 

    if not any(word in message_text for word in TRIGGER_WORDS):
        return 

    if chat_id in chat_cooldowns:
        time_passed = current_time - chat_cooldowns[chat_id]
        if time_passed < COOLDOWN_SECONDS:
            print(f"Cooldown active in chat {chat_id}")
            return 
    
    print(f"Triggered in chat {chat_id}")
    
    delete_last_bot_message(chat_id) 

    response = random.choice(PHRASES)
    sent_message = bot.send_message(chat_id, response)

    last_bot_messages[chat_id] = sent_message.message_id
    
    chat_cooldowns[chat_id] = current_time

bot.infinity_polling()
