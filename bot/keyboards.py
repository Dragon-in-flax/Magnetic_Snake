from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_main_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🏆 Топ-5 игроков", callback_data="top")],
        [InlineKeyboardButton(text="📊 Моя статистика", callback_data="stats")],
        [InlineKeyboardButton(text="🎖 Мои награды", callback_data="achievements")],
        [InlineKeyboardButton(text="📁 Загрузить CSV с результатами", callback_data="upload")]
    ])