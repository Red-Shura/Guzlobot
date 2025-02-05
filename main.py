'''Главный файл бота'''

import telebot
from telebot import types, custom_filters
from telebot.storage import StateMemoryStorage
from telebot.handler_backends import State, StatesGroup

stage_storage = StateMemoryStorage()

API_TOKEN = '7711719136:AAF2nw8_CLInKbO371tLuVf-HZICsHORX3A'
bot = telebot.TeleBot(API_TOKEN, state_storage=stage_storage)

orders = []


class MyStates(StatesGroup):
    
    AddOrder = State()
    OrderBoard = State()
    MyAds = State()
    Menu = State()


def handle_mainkeyboard(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    
    item = types.KeyboardButton("Главная")
    markup.add(item)

    item = types.KeyboardButton("Мои объявления")
    markup.add(item)

    item = types.KeyboardButton("Доска объявлений")
    markup.add(item)

    item = types.KeyboardButton("Добавить заказ")
    markup.add(item)
    
    bot.send_message(message.chat.id, "Выберите опцию:", reply_markup=markup)

'''Обработка команды start'''
@bot.message_handler(commands=['start'])
def hello_message(message):
    bot.reply_to(message, 'Приветствую, я ТГ-бот сервис: Guzlobot.\nСпособен принимать заказы от вас и выставлять их на доску объявлений.')
    bot.set_state(message.from_user.id, MyStates.Menu, message.chat.id)
    handle_mainkeyboard(message)
'''Функция главного меню'''
@bot.message_handler(state=MyStates.Menu, func=lambda message: message.text == 'Главная')

def main_menu(msg):

    bot.send_message(msg.chat.id, 'Вы хотите:\nДобавить заказ\nВзять заказ\nПосмотреть ваши объявления')
    bot.set_state(msg.from_user.id, MyStates.Menu, msg.chat.id)

    handle_mainkeyboard(msg)


'''Обработка команды добавление заказа'''
@bot.message_handler(func=lambda message: message.text == 'Добавить заказ')
    
def set_state_addord(msg):
    
    bot.reply_to(msg, "Описание заказа:")
    bot.set_state(msg.from_user.id, MyStates.AddOrder, msg.chat.id)

@bot.message_handler(state=MyStates.AddOrder) 

def add_order(message):
    
    global orders
    orders.append([message.from_user.id, message.text])
    bot.send_message(message.chat.id, "Ваш заказ принят!")

    main_menu(message)


'''Обработка команды доска объявлений'''
@bot.message_handler(func=lambda message: message.text == 'Доска объявлений')

def set_state_OrderBoard(msg):

    bot.set_state(msg.from_user.id, MyStates.OrderBoard)
    show_orders(msg)

@bot.message_handler(state=MyStates.OrderBoard)

def show_orders(message):

    if len(orders) > 0:
        for order in orders:
            bot.send_message(message.chat.id, f'------------------------\n{order}\n------------------------')

    else:
        bot.send_message(message.chat.id, "------------------------\nНет текущих заказов.\n------------------------")
    
    bot.set_state(message.from_user.id, MyStates.Menu, message.chat.id)


'''Обработка команды Мои объявления'''
@bot.message_handler(func=lambda message: message.text == 'Мои объявления')

def set_state_MyAds(msg):

    bot.set_state(msg.from_user.id, MyStates.MyAds, msg.chat.id)
    my_ads(msg)

@bot.message_handler(state=MyStates.MyAds)

def my_ads(message):
    
    author = message.from_user.id

    bot.send_message(message.chat.id,
     '\n'.join([order for order in orders if message.from_user.id
                 == order[author]]))

    bot.set_state(message.from_user.id, MyStates.Menu, message.chat.id)


bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.infinity_polling()