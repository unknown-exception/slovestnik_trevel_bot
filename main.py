from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import numpy as np
import config, utils, tours


SUBSCRIBERS = utils.read_users()
bot = Bot(token=config.HTTP_API_TOCKEN)
dp = Dispatcher(bot)
tmp_order = {}
kb = [
    [
        types.KeyboardButton(text="Aвтобусные туры"),
        types.KeyboardButton(text="Vylety со Словестником"),
        types.KeyboardButton(text="Походы")
    ],
]
MAIN_KEYBOARD = types.ReplyKeyboardMarkup(keyboard=kb)

print("hello world")

def print_tours(trs: [tours.Tour]):
    urlkb = InlineKeyboardMarkup(row_width=2)
    for t in trs:
        urlButton1 = InlineKeyboardButton(text=t.head, callback_data="order_tour_"+t.id)
        urlButton2 = InlineKeyboardButton(text='Подробнее', url=t.url)
        urlkb.add(urlButton1,urlButton2 )
    return urlkb

@dp.message_handler(content_types=["new_chat_members"])
async def new_member(message: types.Message):
    await message.reply("Приветствуем, на какие мероприятия вы хотите записаться?", reply_markup=MAIN_KEYBOARD)


@dp.callback_query_handler()
async def check_button(call: types.CallbackQuery):
    print(call.data)
    user_id = call.from_user.id
    tour = call.data.split("_")[2]
    tmp_order[user_id] = tour
    await call.message.answer(f"""Вы хотите записаться на [{tours.get_tour_by_id(tour).head}]
пожалуйста напишите ФИО, количество человек/из них детей, контактная информация.""")
    await call.answer()

@dp.message_handler(commands=["order"])
async def order_command(message: types.Message):
    user_id = message.chat.id
    tour = tmp_order[user_id]
    tour_name = tours.get_tour_by_id(tour).head
    del tmp_order[user_id]
    reply = f"""Вы записались на поездку [{tour_name}]!
    
    Тебе приходит сообщение/письмо 'пользователь {message.from_user.id} {message.from_user.url} {message.from_user.username} записался на {tour_name}, [{message.text.replace("/order","")}]
    """
    
    await message.reply(reply, reply_markup=MAIN_KEYBOARD)


@dp.message_handler(commands=["push"])
async def push_command(message: types.Message):
    arg = utils.extract_arg(message.text)
    if arg[0] != config.ADMIN_PWD:
        print("ALARM")
    else:
        await message.reply("Got this")


@dp.message_handler(commands=["start"])
async def send_welcome(message: types.Message):
    utils.add_user(message.chat.id, SUBSCRIBERS)
    # await bot.send_message(chat_id="1289285297", text="hohoho")
    print("sent")
    await message.reply(
        """Привет! Я бот Поездок со Словестником!
Нажмите кнопку для выбора экскурсий""",
         reply_markup=MAIN_KEYBOARD
    )

@dp.message_handler(regexp="Походы")
async def hiking_list(message: types.Message):
    markup = print_tours( tours.get_bus())
    await message.answer(f"""Расписание по запросу {message.text}
Левая кнопка - записаться на поездку, правая - посмотреть подробную информацию"""
                         , reply_markup=markup)

@dp.message_handler(regexp="Vylety со Словестником")
async def tours_list(message: types.Message):
    markup = print_tours( tours.get_tours())
    await message.answer(f"""Расписание по запросу {message.text}
Левая кнопка - записаться на поездку, правая - посмотреть подробную информацию"""
                         , reply_markup=markup)


@dp.message_handler()
async def echo123(message: types.Message):
    if not tmp_order[message.chat.id]:
        await message.answer("Я не знаю такой команды, извините", reply_markup=MAIN_KEYBOARD)
    else:
        await order_command(message)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
