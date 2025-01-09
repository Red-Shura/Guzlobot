'''Главный файл бота'''

import asyncio
from telebot.async_telebot import AsyncTeleBot
import telebot
from telebot import types

API_TOKEN = '7711719136:AAF2nw8_CLInKbO371tLuVf-HZICsHORX3A'
bot = AsyncTeleBot(API_TOKEN)


@bot.message_handler(commands=['start'])
async def handle_keyboard(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item = types.KeyboardButton("Мои заказы")
    markup.add(item)
    item = types.KeyboardButton("Мои объявления")
    markup.add(item)
    item = types.KeyboardButton("Доска объявлений")
    markup.add(item)
    item = types.KeyboardButton("Добавить заказ")
    markup.add(item)

    await bot.send_message(message.chat.id, "Выберите опцию:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "Добавить заказ")
async def say_order(message):
    await bot.reply_to(message, "Описание заказа:")
async def set_order(message):
    order_range = message.text
    order_author = message.chat.id
    await bot.send_message(message.chat.id, order_author, order_range)

asyncio.run(bot.polling())