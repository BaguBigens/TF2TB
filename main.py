import telebot
import random
from telebot import types
import json


def get_class(data, name):
    for cls in data:
        if cls["class"] == name:
            return cls


def photo(call_message_chat_id, link, text=""):
    bot.send_photo(call_message_chat_id, link, text)


def keyboard(buttonNameList, callbackDataList):
    markup = types.InlineKeyboardMarkup()
    for i in range(len(buttonNameList)):
        button = types.InlineKeyboardButton(buttonNameList[i], callback_data=callbackDataList[i])
        markup.add(button)
    return markup


def second_menu(id):
    buttons = "продолжить", "вернуться в меню"
    markup = keyboard(buttons, buttons)
    bot.send_photo(id, "https://cdn.cloudflare.steamstatic.com/steam/apps/440/header.jpg?t=1659929900", "Что дальше?",
                   reply_markup=markup)


def main_menu(id):
    buttons = classes + ["Случайный"]
    markup = keyboard(buttons, buttons)
    bot.send_photo(id, "https://i.ytimg.com/vi/MWQVwTctaL4/maxresdefault.jpg", "Какой класс ты выберешь?",
                   reply_markup=markup)


def generate_loadout(id, cls):
    # сообщение что за класс
    bot.send_message(id, cls["class"])
    slot1 = random.choice(cls["slot1"])
    photo(id, slot1["url"], slot1["text"])
    slot2 = random.choice(cls["slot2"])
    photo(id, slot2["url"], slot2["text"])
    slot3 = random.choice(cls["slot3"])
    photo(id, slot3["url"], slot3["text"])
    if "slot4" in cls:
        slot4 = random.choice(cls["slot4"])
        photo(id, slot4["url"], slot4["text"])


def second_menu(id, callback_data):
    markup = keyboard(["Повторить", "Вернуться в меню"], [callback_data, "Menu"])
    bot.send_photo(id, "https://cdn.cloudflare.steamstatic.com/steam/apps/440/header.jpg?t=1659929900", "Что дальше?",
                   reply_markup=markup)


with open("data2.json", "rt", encoding='utf-8') as f:
    data = f.read()
    data = json.loads(data)

classes = []
for item in data:
    classes.append(item["class"])

bot_token = "5779297053:AAGIHx6jlLnGTPwcv6FQZsHqJ3ZQ1O1QFUc"

bot = telebot.TeleBot(bot_token)


@bot.message_handler(commands=["start", "language"])
def Start(message):
    id = message.chat.id
    if message.text == "/start":
        main_menu(id)
        # markup1 = keyboard(["Случайный"], ["Случайный"])
        # bot.send_message(id, ".", reply_markup=markup1)
    # if message.text == "/language":
    #     main_menu(id)


@bot.callback_query_handler(func=lambda call: True)
def call(call):
    id = call.message.chat.id
    if call.data == "Menu":
        main_menu(id)
    if call.data == "Случайный":
        random_cls = get_class(data, random.choice(classes))
        generate_loadout(id, random_cls)
        second_menu(id, call.data)

    if call.data in classes:
        cls = get_class(data, call.data)
        generate_loadout(id, cls)
        second_menu(id, call.data)
    # сообщение с менюшкой продолжить или вернуться в меню


bot.infinity_polling()