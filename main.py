'''Главный файл бота'''

import asyncio
from telebot.async_telebot import AsyncTeleBot
import telebot
from telebot import types, custom_filters
from telebot.storage import StateMemoryStorage
from telebot.asyncio_handler_backends import State, StatesGroup

stage_storage = StateMemoryStorage()

API_TOKEN = '7711719136:AAF2nw8_CLInKbO371tLuVf-HZICsHORX3A'
bot = AsyncTeleBot(API_TOKEN, state_storage=stage_storage)

orders = []


class MyStates(StatesGroup):
    
    MyOrders = State()
    AddOrder = State()
    OrderBoard = State()
    MyAds = State()
    Menu = State()


async def handle_mainkeyboard(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    
    item = types.KeyboardButton("Главная")
    markup.add(item)

    item = types.KeyboardButton("Мои заказы")
    markup.add(item)

    item = types.KeyboardButton("Мои объявления")
    markup.add(item)

    item = types.KeyboardButton("Доска объявлений")
    markup.add(item)

    item = types.KeyboardButton("Добавить заказ")
    markup.add(item)
    
    await bot.send_message(message.chat.id, "Выберите опцию:", reply_markup=markup)


'''Обработка команды start'''
@bot.message_handler(commands=['start'])

async def hello_message(message):

    await bot.reply_to(message, 'Приветствую, я ТГ-бот сервис: Guzlobot.\n Способен принимать заказы от вас и выставлять их на доску объявлений.')
    await bot.set_state(message.from_user.id, MyStates.Menu, message.chat.id)

'''Функция главного меню'''
@bot.message_handler(state=MyStates.Menu, commands=['Главная'])

async def main_menu(msg):

    await bot.send_message(msg.chat.id, 'Вы хотите: Добавить заказ\nВзять заказ\nПосмотреть ваши объявления')
    await bot.set_state(msg.from_user.id, MyStates.Menu, msg.chat.id)
    await handle_mainkeyboard()


'''Обработка команды добавление заказа'''
@bot.message_handler(state=MyStates.AddOrder) 

async def add_order(message):
    
    global orders
    await bot.reply_to(message, "Описание заказа:")
    orders.append(message)
    await bot.send_message(message.chat.id, "Ваш заказ принят!")

    await handle_mainkeyboard()


'''Обработка команды доска объявлений'''
@bot.message_handler(state=MyStates.OrderBoard)

async def show_orders(message):

    if len(orders) > 0:
        for order in orders:
            await bot.send_message(message.chat.id, order)
    else:
        await bot.send_message(message.chat.id, "Нет текущих заказов.")

    await handle_mainkeyboard()


'''Обработка команды Мои объявления'''
@bot.message_handler(state=MyStates.MyAds)

async def my_ads(message):

    await bot.send_message(message.chat.id, '\n'.join([order for order in orders if message.from_user.id == order['author']]))

    await handle_mainkeyboard()


'''Обработка команды Мои заказы'''
@bot.message_handler(state=MyStates.MyOrders)

async def my_orders(message):

    await bot.send_message(message.chat.id, '\n'.join([order for order in orders if message.from_user.id in order['reactions']]))

    await handle_mainkeyboard()


bot.add_custom_filter()

asyncio.run(bot.polling())