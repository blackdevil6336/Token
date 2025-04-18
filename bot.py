from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

TOKEN = "7236669739:AAETs2xNl8jCidGBjVaOoQ09_lNxL3ppyKY"

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# 🛍 Menyu tugmalarini yaratish
menu_buttons = [
    [KeyboardButton("1. Ustki kiyimlar"), KeyboardButton("2. Ichki kiyimlar")],
    [KeyboardButton("3. Savol va murojaatlar"), KeyboardButton("4. Do‘kon manzili va kontaktlar")]
]
menu = ReplyKeyboardMarkup(menu_buttons, resize_keyboard=True)

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.reply("Assalomu alaykum! MONICA ayollar kiyimlari do‘koniga xush kelibsiz!", reply_markup=menu)

executor.start_polling(dp)

import json

# JSON fayldan mahsulotlarni yuklash
def yuklash_mahsulotlar():
    with open("mahsulotlar.json", "r", encoding="utf-8") as fayl:
        mahsulotlar = json.load(fayl)
    return mahsulotlar

# Mahsulotlarni ekranga chiqarish
mahsulotlar = yuklash_mahsulotlar()
for mahsulot in mahsulotlar:
    print(f"Kod: {mahsulot['kod']}, Nomi: {mahsulot['nomi']}, Narxi: {mahsulot['narxi']}")

# Mahsulot qo‘shish
def mahsulot_qoshish(kod, nomi, narx, rasm):
    mahsulotlar = yuklash_mahsulotlar()
    mahsulotlar.append({"kod": kod, "nomi": nomi, "narxi": narx, "rasm": rasm})

    with open("mahsulotlar.json", "w", encoding="utf-8") as fayl:
        json.dump(mahsulotlar, fayl, ensure_ascii=False, indent=4)

# Mahsulot qo‘shish uchun misol
mahsulot_qoshish("103", "Yangi kofta", "180,000 so'm", "https://example.com/kofta.jpg")
print("✅ Mahsulot qo‘shildi!")

# Mahsulot narxini yangilash
def mahsulot_yangilash(kod, yangi_narx):
    mahsulotlar = yuklash_mahsulotlar()
    for mahsulot in mahsulotlar:
        if mahsulot["kod"] == kod:
            mahsulot["narxi"] = yangi_narx

    with open("mahsulotlar.json", "w", encoding="utf-8") as fayl:
        json.dump(mahsulotlar, fayl, ensure_ascii=False, indent=4)

# Narxni o‘zgartirish misoli
mahsulot_yangilash("102", "160,000 so'm")
print("✅ Narx yangilandi!")

# Mahsulot o‘chirish
def mahsulot_ochirish(kod):
    mahsulotlar = yuklash_mahsulotlar()
    mahsulotlar = [mahsulot for mahsulot in mahsulotlar if mahsulot["kod"] != kod]

    with open("mahsulotlar.json", "w", encoding="utf-8") as fayl:
        json.dump(mahsulotlar, fayl, ensure_ascii=False, indent=4)

# Mahsulotni o‘chirish misoli
mahsulot_ochirish("101")
print("✅ Mahsulot o‘chirildi!")

ADMIN_CHAT_ID = 5806807500  # Adminning Telegram ID'si

@dp.message_handler(lambda message: message.text == "3. Savol va murojaatlar")
async def anonim_chat(message: types.Message):
    await bot.send_message(ADMIN_CHAT_ID, f"📩 Yangi anonim suhbat boshlandi!\nMijoz: @{message.from_user.username}")
    await message.reply("Savolingizni yozing, u to‘g‘ridan-to‘g‘ri adminga jo‘natiladi.")

@dp.message_handler()
async def mijoz_xabari(message: types.Message):
    if message.reply_to_message and message.reply_to_message.text == "Savolingizni yozing, u to‘g‘ridan-to‘g‘ri adminga jo‘natiladi.":
        await bot.send_message(ADMIN_CHAT_ID, f"✉️ Anonim mijozdan: {message.text}")
        await message.reply("Savolingiz adminga yuborildi!")

@dp.message_handler(lambda message: message.chat.id == ADMIN_CHAT_ID and message.text.startswith("Javob:"))
async def admin_javobi(message: types.Message):
    malumot = message.text.split(" ", 2)  # Xabarni bo‘lish

    if len(malumot) == 3:  # >= 3 emas, == 3 bo‘lishi kerak
        username = malumot[1].replace("@", "")  # Mijoz username ni ajratish
        javob_matni = malumot[2]  # Admin javobi

        # Mijozga javob yuborish
        await bot.send_message(message.chat.id, f"✅ Javob yuborildi: {javob_matni}")
        await bot.send_message(f"@{username}", f"👤 Admin javobi: {javob_matni}")

@dp.message_handler(lambda message: message.text.lower() == "boshqa savolim yo'q")
async def tugatish_xabari(message: types.Message):
    await bot.send_message(ADMIN_CHAT_ID, f"🚫 Mijoz (@{message.from_user.username}) suhbatni yakunladi.")
    await message.reply("✅ Suhbat tugatildi! Rahmat.")

import json

# Do‘kon ma’lumotlarini yuklash
def yuklash_dokon():
    with open("dokonan.json", "r", encoding="utf-8") as fayl:
        return json.load(fayl)

@dp.message_handler(lambda message: message.text == "4. Do‘kon manzili va kontaktlar")
async def manzil_va_kontakt(message: types.Message):
    dokonan = yuklash_dokon()
    lokatsiya = dokonan["lokatsiya"]
    telefonlar = "\n".join(dokonan["telefonlar"])

    await bot.send_location(message.chat.id, lokatsiya["latitude"], lokatsiya["longitude"])
    await message.reply(f"📞 Kontaktlar:\n{telefonlar}")
# Do‘kon ma’lumotlarini yangilash
def dokon_yangilash(yangi_lat, yangi_long, yangi_telefonlar):
    dokonan = {"lokatsiya": {"latitude": yangi_lat, "longitude": yangi_long}, "telefonlar": yangi_telefonlar}

    with open("dokonan.json", "w", encoding="utf-8") as fayl:
        json.dump(dokonan, fayl, ensure_ascii=False, indent=4)

@dp.message_handler(lambda message: message.chat.id == ADMIN_CHAT_ID and message.text.startswith("/yangilash"))
async def admin_yangilash(message: types.Message):
    malumot = message.text.split(";")
    if len(malumot) >= 3:
        lat = float(malumot[1])
        long = float(malumot[2])
        telefonlar = malumot[3].split(",")

        dokon_yangilash(lat, long, telefonlar)
        await message.reply("✅ Lokatsiya va telefon raqamlar yangilandi!")
/yangilash 41.315000; 69.250000; +998901112233, +998933445566
