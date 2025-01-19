import asyncio
from aiogram import Bot, Dispatcher, types, Router

dp = Dispatcher()

# Функция приёма заказов
@Router.message(func=lambda message: True)
async def receive_order(message):
    global orders
    orders.append(message)
    await dp.send_message("Ваш заказ принят!")

# Отображение всех заказов
@Router.message()
async def show_orders():
    if len(orders) > 0:
        for order in orders:
            await dp.send_message(order)
    else:
        await dp.send_message("Нет текущих заказов.")

# Уведомление пользователя при реакции
@Router.message(lambda message: message.reaction)
async def handle_reaction(message):
    user = message.from_user
    await dp.send_message(user, "Вы отреагировали!")

async def main() -> None:
    bot = Bot(token="7711719136:AAF2nw8_CLInKbO371tLuVf-HZICsHORX3A")

    await dp.start_polling()
# Запуск бота
if __name__ == '__main__':
   asyncio.run(main())
