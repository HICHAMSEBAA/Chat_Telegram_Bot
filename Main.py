#! /usr/bin/python3
from telebot import types, util
import telebot
import os
from dotenv import load_dotenv
from googletrans import Translator
import json

load_dotenv()
TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(token=TOKEN)

Bot_Data = {
    "name": ["Hicham", "hicham", "bot"]
}

commands = {
    "translate": ["translate", "trans"]
}

text_list = {
    "offensive": ["cat", "dog", "fox"]
}


def bad_word(message: types):
    id = str(message.from_user.id)
    name = message.from_user.first_name
    username = message.from_user.username
    print(message.from_user)
    with open("user_data.json", "r") as file:
        data = json.load(file)
    if id in data["users"].keys():
        data["users"][id]["counter"] -= 1
    else:
        data["users"][id] = {"counter": 5}
        data["users"][id]["username"] = username
        data["users"][id]["name"] = name
    if data["users"][id]["counter"] <= 0:
        bot.kick_chat_member(chat_id=message.chat.id, user_id=message.from_user.id)
        bot.send_message(chat_id=message.chat.id, text=f"🔴 {message.from_user.first_name} He kicked because break the rule 🔴")
        del data["users"][id]
    else:
        count = data["users"][id]["counter"]
        bot.send_message(chat_id=message.chat.id, text=f"❌ {message.from_user.first_name} you are say bad words ❌ \n you have {count} Chance 😡 ")
    with open("user_data.json", "w") as file:
        json.dump(data, file, indent=2)

    return bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)


@bot.message_handler(commands=["start", "help"])
def startBot(message: types):
    chat_id = message.chat.id
    first_name = message.from_user.first_name
    bot.send_message(chat_id, f"{first_name} Welcome to Hicham Bot  😀")


@bot.chat_member_handler()
def handleUpdate(message: types.ChatMemberUpdated):
    newResponse = message.new_chat_member
    chat_id = message.chat.id
    first_name = message.from_user.first_name
    print(message.from_user)
    print(message)
    if newResponse.status == "member":
        bot.send_message(chat_id=chat_id, text=f"{first_name} Welcome to Our Group 😀 ")
    elif newResponse.status == "left":
        bot.send_message(chat_id=chat_id, text=f"{first_name} He is Left The Group 😢 ")


@bot.my_chat_member_handler()
def leave(message: types.ChatMemberUpdated):
    update = message.new_chat_member
    if update.status == "member":
        bot.send_message(message.chat.id, "I am sorry \n This is Not My Chat Group Good Bay 🖐")
        bot.leave_chat(message.chat.id)


@bot.message_handler(func=lambda m: True)
def reply(message: types.Message):
    words = message.text.split()
    print(words)
    for word in words:
        if word in text_list["offensive"]:
            bad_word(message=message)
    if words[0] in Bot_Data["name"]:
        bot.reply_to(message=message, text="How I can Help You ? 😀")
    elif words[0] in commands["translate"]:
        translator = Translator(service_urls=[
            'translate.google.com',
            'translate.google.co.kr',
        ])
        print(" ".join(words[1:]))
        print(type(" ".join(words[1:])))
        translation = translator.translate(text=" ".join(words[1:]), dest="ar")
        bot.reply_to(message=message, text=translation.text)


bot.infinity_polling(allowed_updates=util.update_types)
