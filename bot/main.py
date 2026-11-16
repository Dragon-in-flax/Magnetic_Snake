import asyncio
import io
import csv
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.exceptions import TelegramBadRequest
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

import config
from keyboards import get_main_kb
import session as sess
import analytics

# Настройка логирования (записывает события в консоль)
logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
logger = logging.getLogger(__name__)

# Создание объекта бота. ParseMode.HTML позволяет использовать теги <b> для жирного текста
bot = Bot(token=config.TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
# Dispatcher — "мозг" бота, который распределяет входящие сообщения по функциям (хендлерам)
# MemoryStorage хранит состояния (FSM) в оперативной памяти
dp = Dispatcher(storage=MemoryStorage())

# --- МАШИНА СОСТОЯНИЙ (FSM) ---
# Нужна, чтобы бот понимал, чего он ждет от пользователя в данный момент
class BotState(StatesGroup):
    waiting_for_name = State()  # Ожидание ввода имени для проверки статистики
    waiting_for_file = State()  # Ожидание загрузки CSV-файла

# --- ФУНКЦИЯ АНТИФЛУДА (Редактирование экрана) ---
# Вместо отправки нового сообщения на каждое нажатие кнопки, эта функция изменяет (редактирует) уже существующее сообщение-экран.
async def show_screen(chat_id: int, user_id: int, text: str, kb=None):
    user_sess = sess.load_session(user_id)
    screen_id = user_sess.get("screen_id")
    
    # Если ID экрана уже сохранен в сессии пользователя
    if screen_id:
        try:
            # Пытается отредактировать текст и кнопки существующего сообщения
            await bot.edit_message_text(chat_id=chat_id, message_id=screen_id, text=text, reply_markup=kb)
            return
        except TelegramBadRequest as e:
            # Ошибка "message is not modified" возникает, если текст не изменился
            if "message is not modified" in str(e):
                return
            logger.warning(f"Не удалось изменить экран: {e}")
    
    # Если экрана нет (или он был удален), отправляет новое сообщение и запоминает его ID
    msg = await bot.send_message(chat_id, text, reply_markup=kb)
    user_sess["screen_id"] = msg.message_id
    sess.save_session(user_id, user_sess)

# --- ОБРАБОТЧИКИ КОМАНД И КНОПОК ---

# Обработка команды /start
@dp.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    await state.clear() # Сбрасывает все ожидания (FSM)
    user_id = message.from_user.id
    
    # Сбрасывает сохраненный ID экрана, чтобы бот отправил новое приветственное сообщение
    user_sess = sess.load_session(user_id)
    user_sess["screen_id"] = None 
    sess.save_session(user_id, user_sess)

    text = "🧲 Добро пожаловать в «Магнитный Дозор»!\nВыберите действие на клавиатуре ниже:"
    await show_screen(message.chat.id, user_id, text, get_main_kb())

# Обработка нажатия на кнопку "Топ-5 игроков"
@dp.callback_query(F.data == "top")
async def process_top(callback: CallbackQuery):
    await callback.answer() # Обязательный ответ, чтобы на кнопке не висели "часики"
    
    top_players = analytics.get_top() # Получает список кортежей (Имя, Очки) из модуля аналитики
    
    if not top_players:
        text = "🏆 <b>Топ-5 игроков:</b>\n\nПока нет записей в CSV."
    else:
        text = "🏆 <b>Топ-5 игроков:</b>\n\n"
        # Формирует красивый текст со списком
        for i, (name, score) in enumerate(top_players, 1):
            text += f"{i}. {name} — {score} очков\n"
            
    await show_screen(callback.message.chat.id, callback.from_user.id, text, get_main_kb())

# Обработка нажатия на кнопку "Моя статистика"
@dp.callback_query(F.data == "stats")
async def process_stats(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    # Переводит бота в состояние ожидания имени
    await state.set_state(BotState.waiting_for_name)
    text = "📊 Введите ваше имя (как вы его ввели в игре), чтобы найти ваш лучший результат:"
    await show_screen(callback.message.chat.id, callback.from_user.id, text)

# Обработка текста, когда бот находится в состоянии waiting_for_name
@dp.message(BotState.waiting_for_name)
async def handle_name_input(message: Message, state: FSMContext):
    name = message.text.strip() # Убирает лишние пробелы по краям
    best_score = analytics.get_stats(name) # Ищет результат в CSV
    
    if best_score is None or best_score == 0:
        text = f"❌ Игрок <b>{name}</b> не найден. Убедитесь, что имя верное, или сыграйте в игру."
    else:
        # Получает список ачивок на основе очков
        ach_list = analytics.get_achievements(best_score)
        ach_text = "\n".join(ach_list) if ach_list else "Пока нет наград"
        
        text = (f"📊 Статистика игрока <b>{name}</b>:\n\n"
                f"Максимальный результат: <b>{best_score}</b> очков.\n\n"
                f"🎖 <b>Награды:</b>\n{ach_text}")
        
    await state.clear() # Сбрасывает состояние ожидания
    await show_screen(message.chat.id, message.from_user.id, text, get_main_kb())

# Обработка нажатия на кнопку "Загрузить CSV"
@dp.callback_query(F.data == "upload")
async def process_upload(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    # Переводит бота в состояние ожидания файла
    await state.set_state(BotState.waiting_for_file)
    text = "📁 Отправьте мне CSV-файл с результатами (snake_records.csv):"
    await show_screen(callback.message.chat.id, callback.from_user.id, text)

# Обработка документа, когда бот ждет файл
@dp.message(BotState.waiting_for_file, F.document)
async def handle_file_upload(message: Message, state: FSMContext):
    document = message.document
    # Проверяет расширение файла
    if not document.file_name.endswith(".csv"):
        await message.answer("❌ Ошибка: это не CSV файл.")
        return

    # Скачивает файл в оперативную память (в байтовый буфер), чтобы не создавать лишние файлы на диске
    buffer = io.BytesIO()
    await bot.download(document, destination=buffer)
    
    try:
        # Декодирует байты в текст (utf-8-sig убирает невидимый BOM-символ, если он есть)
        text = buffer.getvalue().decode("utf-8-sig")
        # Читаем CSV из текста. Разделитель - точка с запятой
        reader = csv.reader(io.StringIO(text), delimiter=';')
        rows = list(reader)
        
        # Открывает наш главный файл в режиме 'a' (append - дописывание в конец)
        with open(config.CSV_FILE, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f, delimiter=';')
            for row in rows:
                # Пропускает строку с заголовками, если она есть в присланном файле
                if row and row[0] != "Имя": 
                    writer.writerow(row)
                    
        await state.clear()
        await message.answer("✅ Файл успешно загружен и обработан!", reply_markup=get_main_kb())
        
    except Exception as e:
        logger.error(f"Ошибка чтения файла: {e}")
        await message.answer("❌ Ошибка при чтении файла. Проверьте кодировку и формат.")
        await state.clear()

# --- ЗАПУСК БОТА ---
async def main():
    logger.info("Бот запущен!")
    # Запускает бесконечный цикл опроса серверов Telegram на наличие новых сообщений
    await dp.start_polling(bot)

# Точка входа. Код выполнится только если файл запущен напрямую
if __name__ == "__main__":
    asyncio.run(main())