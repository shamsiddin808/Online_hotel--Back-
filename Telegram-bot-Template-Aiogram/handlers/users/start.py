
from datetime import datetime
from random import random

import requests
from aiogram import types
from aiogram.bot import bot
from aiogram.dispatcher.filters import CommandStart
from aiogram import Bot
from loader import dp
from random import randint

import sqlite3


con = sqlite3.connect("../db.sqlite3")
cursor = con.cursor()


from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

inline_btn = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Profil👤", callback_data="profile"),
            InlineKeyboardButton(text="Mehmonhona Tanlash🏨",callback_data="choose_hotel" ),
        ],
    ],
    row_width=1
)


GET_USER = "http://0.0.0.0:8000/Users/get-tg-user/{user_id}/"
REGISTER_USER = "http://0.0.0.0:8000/Users/register-telegram/"
LOGIN_API = "http://0.0.0.0:8000/Users/login/"
API_URL = "http://0.0.0.0:8000/Users/get-user/{email}/"
GET_HOTEL = "http://0.0.0.0:8000/Users/get-hotel-data/"
BOOKING = "http://0.0.0.0:8000/Users/bookingroom/"
GET_ONE_HOTELDATA = "http://0.0.0.0:8000/Users/get-one-hotel/{hotel_id}/"
PRICING = "http://0.0.0.0:8000/Users/pricinghotel/"

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State


class UserStates(StatesGroup):
    login_email = State()
    login_passwd = State()
    register_name = State()
    register_email = State()
    register_passwd = State()
    menu_profile = State()

class HotelStates(StatesGroup):
    choose_hotel = State()
    checkout_time = State()
    room = State()




@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    user_id = message.from_user.id

    response = requests.get(GET_USER.format(user_id=user_id))


    if response.status_code == 200:
        await message.answer("Email kiriting📧")
        await UserStates.login_email.set()
    else:
        await message.answer("Registratsiya uchun ismingizni kiriting")
        await UserStates.register_name.set()


@dp.message_handler(state=UserStates.login_email)
async def login_user(message: types.Message):
    global email_login
    email_login = message.text
    domain = email_login.split("@")[-1]
    if domain == "gmail.com":
        await message.answer("email qabul qilindi parolni kiriting:")
        await UserStates.login_passwd.set()
    else:
        await message.answer("Emailni togti kiriting")


@dp.message_handler(state=UserStates.login_passwd)
async def login_passwd(message: types.Message, state: FSMContext):
    user_id = message.from_user.id

    json_data = {
        "email": email_login,
        "password": message.text
    }

    response = requests.post(LOGIN_API, json=json_data)

    if response.status_code == 200:
        response_data = response.json()
        last_value = list(response_data.values())[-1]
        last_word = last_value.split()[-1]
        await message.answer(f"{last_word} - Tizimga muvaffaqiyatli kirdingiz! ✅\nKerakli bolimlardan birini tanlang", reply_markup=inline_btn)
        check_user = cursor.execute("SELECT user_id FROM user_table WHERE user_id = ?", (user_id,)).fetchone()
        check_user_id = check_user[0]
        if check_user_id:
            pass
        else:
            cursor.execute("INSERT INTO user_table(user_id, email) VALUES(?,?)", (user_id, email_login))
        con.commit()
        await UserStates.menu_profile.set()
    else:
        await message.answer(
            "Login ma'lumotlari xato yoki foydalanuvchi topilmadi. ❌\nQaytadan <b><i>Email</i></b> yuboring.")
        await state.finish()
        await UserStates.login_email.set()

@dp.message_handler(state=UserStates.register_name)
async def register_name(message: types.Message):
    global name_register
    name_register = message.text
    await message.answer("Ismingiz qabul qilindi email yuboring:")
    await UserStates.register_email.set()

@dp.message_handler(state=UserStates.register_email)
async def register_passwd(message: types.Message, state: FSMContext):
    global email_register
    email_register = message.text
    domain = email_register.split("@")[-1]
    if domain == "gmail.com":
        await message.answer("email qabul qilindi parolni kiriting:")
        await UserStates.register_passwd.set()
    else:
        await message.answer("Emailni togti kiriting")

@dp.message_handler(state=UserStates.register_passwd)
async def register_passwd(message: types.Message, state: FSMContext):
    user_id = message.from_user.id

    json_data = {
        "name": name_register,
        "email": email_register,
        "password": message.text,
        "user_id": user_id
    }

    response = requests.post(REGISTER_USER, json=json_data)

    if response.status_code == 201:
        await message.answer("<b>Siz muvaffaqiyatli ro'yxatdan o'tdingiz! 🎉</b>", reply_markup=inline_btn)
        await state.finish()
        await UserStates.menu_profile.set()
    else:
        await message.answer("<b>Siz kiritgan email ayni paytda bizning bazamizda registratsiyadan otgan❌</b>\n\nMalumotlarni qaytadan kiriting")
        await state.finish()
        await UserStates.register_name.set()

@dp.callback_query_handler(state=UserStates.menu_profile)
async def menu_profile(call: types.CallbackQuery, state: FSMContext):
    if call.data == "profile":
        email = cursor.execute("SELECT email FROM user_table WHERE user_id = ?", [call.message.chat.id]).fetchone()
        if not email:
            await call.message.answer("Email topilmadi.")
            return

        email = email[0]

        response = requests.get(API_URL.format(email=email))


        if response.status_code == 200:
            try:
                data = response.json()
                await call.message.answer(f"👤 **Foydalanuvchi Ma'lumotlari** 👤\n\n"
                f"📧Email: {data.get('user_email',)}\n"
                f"🧑‍💼Ism: {data.get('user_name')}\n")
            except requests.exceptions.JSONDecodeError:
                await call.message.answer("Server noto'g'ri formatda javob qaytardi.")
                await state.finish()
        else:
            print("Status Code:", response.status_code, response.json())
            await call.message.answer("Xatolik yuz berdi: API noto'g'ri javob qaytardi.")
            await state.finish()
            await UserStates.menu_profile.set()
    elif call.data == "choose_hotel":
        response = requests.get(GET_HOTEL)
        if response.status_code == 200:
            data = response.json()

            # Mehmonxona nomlarini olish va inline keyboard yaratish
            inline_keyboard = InlineKeyboardMarkup(row_width=1)

            if 'message' in data:
                for hotel in data['message']:
                    hotel_id = hotel.get('id')
                    hotel_name = hotel.get('hotel_name')

                    inline_keyboard.add(
                        InlineKeyboardButton(
                            text=hotel_name,
                            callback_data=f"hotel_{hotel_id}"
                        )
                    )

                await call.message.answer("Mehmonxonalarni tanlang:", reply_markup=inline_keyboard)
                await HotelStates.choose_hotel.set()
            else:
                await call.message.answer("Mehmonxonalar topilmadi.")

        else:
            await call.message.answer(f"Xatolik: {response.status_code}")

@dp.callback_query_handler(state=HotelStates.choose_hotel)
async def choose_hotel(call: types.CallbackQuery):
    if "hotel_" in call.data:
        global hotel_idd
        hotel_idd = call.data.split("hotel_")[1]
        await call.message.answer("Nechinchi hona ekanligni kiriting")
        await HotelStates.room.set()

@dp.message_handler(state=HotelStates.room)
async def room(message: types.Message):
    global hotel_rooom
    hotel_rooom = message.text
    await message.answer("Mehmonhonamizda qachongacha qolmoqchisz\nQuyidagi korinishda yozing: 2024-12-15")
    await HotelStates.checkout_time.set()



@dp.message_handler(state=HotelStates.checkout_time)
async def checkout_time(message: types.Message, state: FSMContext):
    try:
        email = cursor.execute(
            "SELECT email FROM user_table WHERE user_id = ?",
            [message.chat.id]
        ).fetchone()

        if not email:
            await message.answer("Email topilmadi.")
            return

        email = email[0]

        response = requests.get(API_URL.format(email=email))
        if response.status_code != 200:
            await message.answer("Foydalanuvchi ma'lumotlari olinmadi.")
            return
        user_data = response.json()
        user_id = user_data['id']
        now = datetime.now()
        check_in = now.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        check_out = message.text

        try:
            check_out_parsed = datetime.strptime(check_out, "%Y-%m-%d")
            check_out_formatted = check_out_parsed.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        except ValueError:
            await message.answer("Sana formati noto'g'ri. Quyidagi formatda kiriting: 2024-12-15")
            return

        booking_payload = {
            "room_number": str(hotel_rooom),
            "check_in": check_in,
            "check_out": check_out_formatted,
            "user": user_id,
            "hotel": hotel_idd
        }

        booking_response = requests.post(BOOKING, json=booking_payload)
        json_data = {
            "hotel": hotel_idd,
            "check_in": check_in,
            "check_out": check_out_formatted,
        }

        if booking_response.status_code == 201:
            await message.answer("✅ Mehmonxona muvaffaqiyatli band qilindi!")
            response = requests.post(PRICING, json=json_data)
            print(response.json())
            total_price = response.json().get("total_price")
            response_2 = requests.get(GET_ONE_HOTELDATA.format(hotel_id=hotel_idd))
            hotel_name = response_2.json().get('hotel_name')
            location = response_2.json().get('hotel_location')
            longitude = response_2.json().get('longitude')
            latitude = response_2.json().get('latitude')
            images_1 = response_2.json().get('images_1')
            print(images_1)
            link = f"https://www.google.com/maps?q={latitude},{longitude}"
            txt = f"Mehmonhona nomi: {hotel_name}\n\nLakatsiya: {location}\nJami summa: {total_price}\n\nMehmonhona lakatsiyasinin korish uchun bosing {link}"
            await message.answer_photo(open(f'../{images_1}', 'rb'),caption=txt)





        else:
            await message.answer("❌ Xatolik yuz berdi\nMenimcha bu hona band\nQayta urinib ko'ring!")

        await state.finish()

    except Exception as e:
        await message.answer(f"Xatolik: {str(e)}")
        await state.finish()

