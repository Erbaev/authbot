from database_functions import *
import asyncio
import yaml
import telebot
from telebot import async_telebot, asyncio_filters, types
from telebot.async_telebot import AsyncTeleBot
from telebot.asyncio_storage import StateMemoryStorage
from telebot.states import State, StatesGroup
from telebot.states.asyncio.context import StateContext
from telebot.types import ReplyParameters
from telebot.states.asyncio.middleware import StateMiddleware

with open("config.yaml", "r", encoding="utf-8") as file:
    config = yaml.safe_load(file)

with open("bot_messages.yaml", "r", encoding="utf-8") as file:
	msg = yaml.safe_load(file)


state_storage = StateMemoryStorage()
bot = AsyncTeleBot(config['authbot']['token'], state_storage=state_storage)

class MyStates(StatesGroup):
	welcome = State()
	register = State()
	waiting_for_nickname = State()
	waiting_for_phone = State()
	waiting_for_name = State()
	waiting_for_birthday = State()
	waiting_for_gender = State()





@bot.callback_query_handler()
async def callback_handler(callback, state: StateContext):
	if callback.data == 'startRegister':
		await state.set(MyStates.waiting_for_nickname)
		await bot.send_message(callback.message.chat.id, msg['register_starts'])







async def reg_pnum(message):
	keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
	button_contact = telebot.typesKeyboardButton(text='Поделиться контактом', request_contact=True)
	keyboard.add(button_contact)
	await bot.send_message(chat_id, msg['register_pnum'], reply_markup=keyboard)
	await bot.register_next_step_handler(message, handle_contact)

@bot.message_handler(content_types=['contact'])
async def handle_contact(message):
	phone_number = message.contact.phone_number
	user_id_sent = message.contack.user_id
	if user_id_sent == message.from_user.id:
		markup = telebot.types.ReplyKeyboardRemove()
		reg_data.append(phone_number)
	else:
		await bot.send_message('Это не твой номер телефона. Попробуй еще раз')
		await reg_pnum(message)

async def reg_check(message: types.Message):
	tg_id = message.from_user.id
	reg = telebot.types.InlineKeyboardMarkup()
	ConfirmBtn = telebot.types.InlineKeyboardButton('Да', callback_data='startRegister')
	DeclineBtn = telebot.types.InlineKeyboardButton('Нет', callback_data='cancelRegister')
	reg.row(ConfirmBtn, DeclineBtn)
	response = await find_reg(tg_id)
	if response == False:
		await bot.send_message(tg_id, msg['register_not_found'], reply_markup=reg)




@bot.message_handler(commands=["start"])
async def start_ex(message: types.Message, state: StateContext):
    await state.set(MyStates.welcome)
    await bot.send_message(
        message.chat.id,
        msg['hello'],
        reply_parameters=ReplyParameters(message_id=message.message_id),
    )
    await reg_check(message)




bot.setup_middleware(StateMiddleware(bot))
asyncio.run(bot.polling())
