import asyncio
import logging
import os
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)

# Загружаем переменные окружения (.env)
load_dotenv()

# Поддержка всех возможных вариантов названий переменных
BOT_TOKEN = (
    os.getenv("BOT_TOKEN")
    or os.getenv("TELEGRAM_BOT_TOKEN")
    or os.getenv("TELEGRAM_TOKEN")
    or os.getenv("TOKEN")
)

ADMIN_CHAT_ID = (
    os.getenv("ADMIN_CHAT_ID")
    or os.getenv("ADMIN_ID")
    or os.getenv("CHAT_ID")
    or os.getenv("TELEGRAM_ADMIN_ID")
    or os.getenv("ADMIN")
)

# Дополнительные настраиваемые переменные (по желанию)
SITE_URL = os.getenv("SITE_URL", "https://ais-dev-cdlf3ezhuvi7anp6qx2pxp-417559399269.europe-west2.run.app").strip().strip('"\'')
ADMIN_PHONE = os.getenv("ADMIN_PHONE", "+7 (900) 000-00-00").strip().strip('"\'')

# Очистка токена от возможных пробелов и кавычек при копировании в Railway
if BOT_TOKEN:
    BOT_TOKEN = BOT_TOKEN.strip().strip('"\'')

if ADMIN_CHAT_ID:
    ADMIN_CHAT_ID = ADMIN_CHAT_ID.strip().strip('"\'')

if not BOT_TOKEN:
    raise ValueError(
        "ОШИБКА: Токен бота не задан! "
        "В Railway во вкладке Variables добавьте переменную BOT_TOKEN (или TELEGRAM_BOT_TOKEN) со значением токена от @BotFather."
    )

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# FSM машина состояний для записи на пробное занятие
class BookingState(StatesGroup):
    waiting_for_name = State()
    waiting_for_phone = State()
    waiting_for_direction = State()

# Главное меню (Inline-кнопки)
def get_main_menu():
    keyboard = [
        [
            InlineKeyboardButton(text="👶 Дошкольникам (5-7 лет)", callback_data="cat_preschool"),
            InlineKeyboardButton(text="🎒 Школьникам (ВПР, ОГЭ, ЕГЭ)", callback_data="cat_school")
        ],
        [
            InlineKeyboardButton(text="🧠 Психолог и Эмоции", callback_data="cat_psychology"),
            InlineKeyboardButton(text="🗣️ Логопед-дефектолог", callback_data="cat_speech")
        ],
        [
            InlineKeyboardButton(text="💰 Цены и абонементы", callback_data="info_prices"),
            InlineKeyboardButton(text="📍 Адрес и контакты", callback_data="info_contacts")
        ],
        [
            InlineKeyboardButton(text="✍️ Записаться на пробное", callback_data="start_booking")
        ],
        [
            InlineKeyboardButton(text="🌐 Наш сайт", url=SITE_URL)
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_back_button():
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="◀️ Назад в меню", callback_data="main_menu")]]
    )

# Старт бота
@dp.message(CommandStart())
async def cmd_start(message: types.Message, state: FSMContext):
    await state.clear()
    welcome_text = (
        f"👋 Здравствуйте, <b>{message.from_user.first_name}</b>!\n\n"
        "Добро пожаловать в официальный бот школы детского развития <b>«ЛидерА»</b> (г. Ангарск)!\n\n"
        "Я помогу вам узнать о направлениях, ценах, расписании и записаться на первое пробное занятие.\n\n"
        "Выберите интересующий пункт меню ниже 👇"
    )
    await message.answer(welcome_text, reply_markup=get_main_menu(), parse_mode="HTML")

# Возврат в главное меню
@dp.callback_query(F.data == "main_menu")
async def back_to_menu(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text(
        "Главное меню школы детского развития <b>«ЛидерА»</b>:\nВыберите интересующий раздел 👇",
        reply_markup=get_main_menu(),
        parse_mode="HTML"
    )
    await callback.answer()

# Категория: Дошкольникам
@dp.callback_query(F.data == "cat_preschool")
async def cat_preschool(callback: types.CallbackQuery):
    text = (
        "👶 <b>Направления для дошкольников (5–7 лет):</b>\n\n"
        "1️⃣ <b>Комплексная подготовка к школе:</b>\n"
        "• Обучение чтению, письму, математике и счету\n"
        "• Развитие логики, внимания, памяти и мелкой моторики\n"
        "• Умение слушать педагога и взаимодействовать в коллективе\n\n"
        "2️⃣ <b>Легоконструирование и ИЗО-студия</b>\n"
        "3️⃣ <b>Английский для малышей в игровой форме</b>\n\n"
        "👥 Занятия проходят в мини-группах (до 6 детей) или индивидуально."
    )
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✍️ Записаться на подготовку", callback_data="book_preschool")],
        [InlineKeyboardButton(text="◀️ В главное меню", callback_data="main_menu")]
    ])
    await callback.message.edit_text(text, reply_markup=kb, parse_mode="HTML")
    await callback.answer()

# Категория: Школьникам
@dp.callback_query(F.data == "cat_school")
async def cat_school(callback: types.CallbackQuery):
    text = (
        "🎒 <b>Для школьников (1–11 классы):</b>\n\n"
        "• <b>Подготовка к ВПР, ОГЭ и ЕГЭ:</b> русский язык, математика, обществознание\n"
        "• <b>Устранение пробелов в программе:</b> помощь с домашними заданиями\n"
        "• <b>Английский язык:</b> разговорная практика, грамматика, снятие языкового барьера\n"
        "• <b>Скорочтение и каллиграфия:</b> красивый почерк и быстрое усвоение текста"
    )
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✍️ Записаться школьнику", callback_data="book_school")],
        [InlineKeyboardButton(text="◀️ В главное меню", callback_data="main_menu")]
    ])
    await callback.message.edit_text(text, reply_markup=kb, parse_mode="HTML")
    await callback.answer()

# Категория: Психология
@dp.callback_query(F.data == "cat_psychology")
async def cat_psychology(callback: types.CallbackQuery):
    text = (
        "🧠 <b>Психологическое развитие:</b>\n\n"
        "🌟 <b>Код Эмоций (6–9 лет):</b>\n"
        "Курс развития эмоционального интеллекта. Учимся справляться со страхами, управлять гневом, уверенно находить друзей и обходиться без капризов.\n\n"
        "🚀 <b>Teen Club LiderA (11–17 лет):</b>\n"
        "Подростковый клуб: лидерские качества, профориентация, преодоление стеснительности, ораторское мастерство."
    )
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✍️ Записаться на курс", callback_data="book_psychology")],
        [InlineKeyboardButton(text="◀️ В главное меню", callback_data="main_menu")]
    ])
    await callback.message.edit_text(text, reply_markup=kb, parse_mode="HTML")
    await callback.answer()

# Категория: Логопед
@dp.callback_query(F.data == "cat_speech")
async def cat_speech(callback: types.CallbackQuery):
    text = (
        "🗣️ <b>Логопед-дефектолог:</b>\n\n"
        "• Диагностика речевого аппарата\n"
        "• Постановка и автоматизация звуков (Р, Л, шипящие)\n"
        "• Запуск речи у неговорящих детей\n"
        "• Коррекция дисграфии и дислексии\n\n"
        "Индивидуальные занятия с бережным подходом к каждому ребенку."
    )
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✍️ Записаться к логопеду", callback_data="book_speech")],
        [InlineKeyboardButton(text="◀️ В главное меню", callback_data="main_menu")]
    ])
    await callback.message.edit_text(text, reply_markup=kb, parse_mode="HTML")
    await callback.answer()

# Цены
@dp.callback_query(F.data == "info_prices")
async def info_prices(callback: types.CallbackQuery):
    text = (
        "💰 <b>Стоимость занятий:</b>\n\n"
        "• <b>Мини-группы (до 6 человек):</b> от 550 ₽ за занятие (от 4 400 ₽ за 8 занятий)\n"
        "• <b>Индивидуальные занятия:</b> от 800 ₽\n"
        "• <b>Логопед-дефектолог:</b> индивидуально по результатам первичной диагностики\n\n"
        "🎁 <i>При покупке абонемента в день пробного занятия действуют специальные условия!</i>"
    )
    await callback.message.edit_text(text, reply_markup=get_back_button(), parse_mode="HTML")
    await callback.answer()

# Адрес и контакты
@dp.callback_query(F.data == "info_contacts")
async def info_contacts(callback: types.CallbackQuery):
    text = (
        "📍 <b>Контакты и адрес школы «ЛидерА»:</b>\n\n"
        "🏢 <b>Адрес:</b> г. Ангарск, 92/93 квартал, дом 19\n"
        "⏰ <b>График работы:</b> Ежедневно с 08:00 до 20:30 (без выходных)\n"
        f"📞 <b>Телефон администратора:</b> {ADMIN_PHONE}\n"
        "💬 <b>Мы всегда на связи!</b>"
    )
    await callback.message.edit_text(text, reply_markup=get_back_button(), parse_mode="HTML")
    await callback.answer()

# Запись на занятие (FSM)
@dp.callback_query(F.data.startswith("book_") | (F.data == "start_booking"))
async def start_booking(callback: types.CallbackQuery, state: FSMContext):
    direction_map = {
        "book_preschool": "Подготовка к школе (дошкольники)",
        "book_school": "Школьные предметы / ВПР / ОГЭ / ЕГЭ",
        "book_psychology": "Психология / Код Эмоций / Teen Club",
        "book_speech": "Логопед-дефектолог",
        "start_booking": "Не выбрано (уточнить по телефону)"
    }
    direction = direction_map.get(callback.data, "Общее направление")
    await state.update_data(direction=direction)

    await state.set_state(BookingState.waiting_for_name)
    await callback.message.answer(
        "✍️ <b>Запись на пробное занятие</b>\n\n"
        "Как вас зовут (и имя ребенка, если есть)? Напишите ответ в чат:",
        parse_mode="HTML"
    )
    await callback.answer()

@dp.message(BookingState.waiting_for_name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text.strip())
    await state.set_state(BookingState.waiting_for_phone)
    
    # Кнопка отправки номера телефона
    kb = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="📱 Поделиться номером телефона", request_contact=True)]],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await message.answer(
        "Отлично! Теперь укажите ваш номер телефона для связи (или нажмите кнопку внизу):",
        reply_markup=kb
    )

@dp.message(BookingState.waiting_for_phone)
async def process_phone(message: types.Message, state: FSMContext):
    phone = message.contact.phone_number if message.contact else message.text.strip()
    user_data = await state.get_data()
    name = user_data.get("name", "Не указано")
    direction = user_data.get("direction", "Не выбрано")

    await state.clear()

    # Сообщение клиенту
    await message.answer(
        "🎉 <b>Спасибо! Заявка успешно принята!</b>\n\n"
        f"👤 <b>Имя:</b> {name}\n"
        f"📞 <b>Телефон:</b> {phone}\n"
        f"🎯 <b>Направление:</b> {direction}\n\n"
        "Администратор школы «ЛидерА» свяжется с вами в течение 10-15 минут в рабочее время для согласования даты и времени занятия.",
        reply_markup=ReplyKeyboardRemove(),
        parse_mode="HTML"
    )

    # Уведомление администратору (если задан ADMIN_CHAT_ID)
    if ADMIN_CHAT_ID:
        try:
            target_chat_id = int(ADMIN_CHAT_ID) if ADMIN_CHAT_ID.lstrip('-').isdigit() else ADMIN_CHAT_ID
            admin_msg = (
                "🔔 <b>НОВАЯ ЗАЯВКА С TELEGRAM-БОТА!</b>\n\n"
                f"👤 <b>Имя:</b> {name}\n"
                f"📞 <b>Телефон:</b> {phone}\n"
                f"🎯 <b>Направление:</b> {direction}\n"
                f"💬 <b>Telegram:</b> @{message.from_user.username or 'нет юзернейма'} (id: {message.from_user.id})"
            )
            await bot.send_message(chat_id=target_chat_id, text=admin_msg, parse_mode="HTML")
        except Exception as e:
            logging.error(f"Не удалось отправить уведомление админу: {e}")

async def main():
    print("Бот @LiderAhelpbot успешно запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
