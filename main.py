import telebot
from telebot import types
import os


bot = telebot.TeleBot('')

orders = []
user_orders = {}
ORDERS_FILE = "orders.txt"
last_message_id = {}    
waiting_for_order = {}    
waiting_for_delete = {}    

def load_orders():

    if os.path.exists(ORDERS_FILE):
        with open(ORDERS_FILE, "r", encoding="utf-8") as file:
            for line in file:
                user_id, username, order_text = line.strip().split("|")
                user_id = int(user_id)
                orders.append({"user_id": user_id, "username": username, "order_text": order_text})
                if user_id not in user_orders:
                    user_orders[user_id] = []
                user_orders[user_id].append(order_text)


def save_orders():

    with open(ORDERS_FILE, "w", encoding="utf-8") as file:
        for order in orders:
            file.write(f"{order['user_id']}|{order['username']}|{order['order_text']}\n")

def delete_previous_message(chat_id):

    if chat_id in last_message_id:
        try:
            bot.delete_message(chat_id, last_message_id[chat_id])
        except Exception as e:
            print(f"Не удалось удалить сообщение: {e}")
    last_message_id[chat_id] = None

def main_menu():

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Создать заказ")
    btn2 = types.KeyboardButton("Доска объявлений")
    btn3 = types.KeyboardButton("Мои объявления")
    btn4 = types.KeyboardButton("Удалить заказ")
    markup.add(btn1, btn2, btn3, btn4)
    return markup


@bot.message_handler(commands=['start'])
def start(message):

    delete_previous_message(message.chat.id)
    msg = bot.send_message(message.chat.id, 'Приветствую, я ТГ-бот сервис: Guzlobot.\nСпособен принимать заказы от вас и выставлять их на доску объявлений.',\
                            reply_markup=main_menu())
    last_message_id[message.chat.id] = msg.message_id

@bot.message_handler(func=lambda message: message.text == "Создать заказ")
def create_order(message):

    delete_previous_message(message.chat.id)
    msg = bot.send_message(message.chat.id, "Введите текст заказа:")
    last_message_id[message.chat.id] = msg.message_id
    waiting_for_order[message.chat.id] = True

@bot.message_handler(func=lambda message: waiting_for_order.get(message.chat.id, False))
def save_order(message):

    user_id = message.from_user.id
    username = message.from_user.username
    order_text = message.text

    orders.append({"user_id": user_id, "username": username, "order_text": order_text})
    if user_id not in user_orders:
        user_orders[user_id] = []
    user_orders[user_id].append(order_text)

    save_orders()

    delete_previous_message(message.chat.id)
    msg = bot.send_message(message.chat.id, "Ваш заказ сохранён!", reply_markup=main_menu())
    last_message_id[message.chat.id] = msg.message_id
    waiting_for_order[message.chat.id] = False 


@bot.message_handler(func=lambda message: message.text == "Доска объявлений")
def show_all_orders(message):

    delete_previous_message(message.chat.id)
    if not orders:
        msg = bot.send_message(message.chat.id, "Пока нет заказов.", reply_markup=main_menu())
    else:
        response = "Все заказы:\n"
        for order in orders:
            response += f"@{order['username']}: {order['order_text']}\n"
        msg = bot.send_message(message.chat.id, response, reply_markup=main_menu())
    last_message_id[message.chat.id] = msg.message_id

@bot.message_handler(func=lambda message: message.text == "Мои объявления")
def show_my_orders(message):

    delete_previous_message(message.chat.id)
    user_id = message.from_user.id
    if user_id not in user_orders or not user_orders[user_id]:
        msg = bot.send_message(message.chat.id, "У вас пока нет заказов.", reply_markup=main_menu())
    else:
        response = "Ваши заказы:\n"
        for i, order in enumerate(user_orders[user_id], 1):
            response += f"{i}. {order}\n"
        msg = bot.send_message(message.chat.id, response, reply_markup=main_menu())
    last_message_id[message.chat.id] = msg.message_id

@bot.message_handler(func=lambda message: message.text == "Удалить заказ")
def delete_order_prompt(message):

    delete_previous_message(message.chat.id)
    user_id = message.from_user.id
    if user_id not in user_orders or not user_orders[user_id]:
        msg = bot.send_message(message.chat.id, "У вас пока нет заказов для удаления.", reply_markup=main_menu())
    else:
        response = "Ваши заказы:\n"
        for i, order in enumerate(user_orders[user_id], 1):
            response += f"{i}. {order}\n"
        response += "Введите номер заказа, который хотите удалить:"
        msg = bot.send_message(message.chat.id, response)
        last_message_id[message.chat.id] = msg.message_id
        waiting_for_delete[message.chat.id] = True

@bot.message_handler(func=lambda message: waiting_for_delete.get(message.chat.id, False))
def delete_order(message):

    user_id = message.from_user.id
    try:
        order_number = int(message.text) - 1
        if 0 <= order_number < len(user_orders[user_id]):

            deleted_order = user_orders[user_id].pop(order_number)

            orders[:] = [order for order in orders if not (order["user_id"] == user_id and order["order_text"] == deleted_order)]

            save_orders()
            delete_previous_message(message.chat.id)
            msg = bot.send_message(message.chat.id, f"Заказ '{deleted_order}' удалён.", reply_markup=main_menu())
        else:
            delete_previous_message(message.chat.id)
            msg = bot.send_message(message.chat.id, "Неверный номер заказа.", reply_markup=main_menu())
    except ValueError:
        delete_previous_message(message.chat.id)
        msg = bot.send_message(message.chat.id, "Пожалуйста, введите номер заказа числом.", reply_markup=main_menu())
    last_message_id[message.chat.id] = msg.message_id
    waiting_for_delete[message.chat.id] = False

load_orders()


if __name__ == "__main__":
    print("Бот запущен...")
    bot.infinity_polling()