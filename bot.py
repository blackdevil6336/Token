import asyncio
import json
from aiogram import Bot, Dispatcher, Router, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

TOKEN = "7236669739:AAETs2xNl8jCidGBjVaOoQ09_lNxL3ppyKY"
ADMIN_CHAT_ID = 5806807500  # Adminning Telegram ID'si

bot = Bot(token=TOKEN)
dp = Dispatcher()
router = Router()
dp.include_router(router)

# 🛍 Menyu tugmalarini yaratish
menu_buttons = [
    [KeyboardButton(text="1. Ustki kiyimlar"), KeyboardButton(text="2. Ichki kiyimlar")],
    [KeyboardButton(text="3. Savol va murojaatlar"), KeyboardButton(text="4. Do‘kon manzili va kontaktlar")]
]
menu = ReplyKeyboardMarkup(keyboard=menu_buttons, resize_keyboard=True)

@router.message(Command("start"))  # 🔹 commands=['start'] o'rniga Command("start") ishlatiladi
async def start_command(message: types.Message):
    await message.answer("Assalomu alaykum! MONICA ayollar kiyimlari do‘koniga xush kelibsiz!", reply_markup=menu)

# 🗣 Anonim chat (Admin bilan mijoz)
@router.message(lambda message: message.text == "3. Savol va murojaatlar")
async def anonim_chat(message: types.Message):
    await bot.send_message(ADMIN_CHAT_ID, f"📩 Yangi anonim suhbat boshlandi!\nMijoz: @{message.from_user.username}")
    await message.answer("Savolingizni yozing, u to‘g‘ridan-to‘g‘ri adminga jo‘natiladi.")

@router.message()
async def mijoz_xabari(message: types.Message):
    if message.reply_to_message and message.reply_to_message.text == "Savolingizni yozing, u to‘g‘ridan-to‘g‘ri adminga jo‘natiladi.":
        await bot.send_message(ADMIN_CHAT_ID, f"✉️ Anonim mijozdan: {message.text}")
        await message.answer("Savolingiz adminga yuborildi!")

@router.message(lambda message: message.chat.id == ADMIN_CHAT_ID and message.text.startswith("Javob:"))
async def admin_javobi(message: types.Message):
    malumot = message.text.split(" ", 2)
    if len(malumot) == 3:
        username = malumot[1].replace("@", "")
        javob_matni = malumot[2]
        await bot.send_message(message.chat.id, f"✅ Javob yuborildi: {javob_matni}")
        await bot.send_message(f"@{username}", f"👤 Admin javobi: {javob_matni}")

@router.message(lambda message: message.text.lower() == "boshqa savolim yo'q")
async def tugatish_xabari(message: types.Message):
    await bot.send_message(ADMIN_CHAT_ID, f"🚫 Mijoz (@{message.from_user.username}) suhbatni yakunladi.")
    await message.answer("✅ Suhbat tugatildi! Rahmat.")

# 🚀 **Botni boshlash**
async def main():
    await dp.start_polling(bot)

asyncio.run(main())  # executor o'rniga asyncio ishlatish
