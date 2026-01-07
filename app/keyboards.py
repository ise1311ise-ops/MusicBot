from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="💬 Чат"), KeyboardButton(text="🔔 Звук")],
        [KeyboardButton(text="🔗 Ссылка"), KeyboardButton(text="⛔ Стоп")],
    ],
    resize_keyboard=True
)
