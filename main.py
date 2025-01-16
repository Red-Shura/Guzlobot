'''Главный файл бота'''

import asyncio
from telebot.async_telebot import AsyncTeleBot
import telebot
from telebot import types

API_TOKEN = '7711719136:AAF2nw8_CLInKbO371tLuVf-HZICsHORX3A'
bot = AsyncTeleBot(API_TOKEN)
order_list = []


@bot.message_handler(commands=['start'])
async def hello_message(message):
    bot.reply_to(message, 'Приветствую, я ТГ-бот сервис: Guzlobot.\n Способен принимать заказы от вас и выставлять их на доску объявлений.')
async def handle_mainkeyboard(message):
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
'''Обработка команды добавление заказа'''
@bot.message_handler(func=lambda message: message.text == "Добавить заказ") 
async def receive_order(message):
    await bot.reply_to(message, "Описание заказа:")
    global orders
    orders.append(message)
    await bot.send_message("Ваш заказ принят!")
    handle_mainkeyboard()
    
'''Обработка команды доска объявлений'''
@bot.message_handler(func=lambda message: message.text == "Доска объявлений")
async def show_orders():
    if len(orders) > 0:
        for order in orders:
            await bot.send_message(order)
    else:
        await bot.send_message("Нет текущих заказов.")
    handle_mainkeyboard()

'''Обработка команды'''



'''Обработка команды'''

asyncio.run(bot.polling())