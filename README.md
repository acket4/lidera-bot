# 🤖 Telegram-бот школы «ЛидерА» (@LiderAhelpbot)

Бот написан на современном фреймворке **Python 3.10+ / aiogram 3.x**.

## 📁 Структура файлов:
* `main.py` — основной код бота: интерактивные меню, ответы на вопросы, сбор заявок с номером телефона и пересылка администратору.
* `requirements.txt` — зависимости (`aiogram`, `python-dotenv`).
* `Procfile` — инструкция запуска для Railway (`worker: python main.py`).
* `.env.example` — образец переменных окружения.

---

## 🚀 Пошаговая инструкция: как залить на GitHub и запустить в Railway

### Шаг 1: Создай отдельную папку на компьютере
1. Создай у себя на ПК любую папку, например `lidera-telegram-bot`.
2. Скопируй туда 4 файла:
   - `main.py`
   - `requirements.txt`
   - `Procfile`
   - `.gitignore`

---

### Шаг 2: Загрузи на GitHub
1. Зайди на [GitHub](https://github.com/) и нажми **New repository** (назови, например, `lidera-help-bot`).
2. Загрузи файлы в репозиторий через Git или прямо кнопкой **«Upload files»** в браузере.

---

### Шаг 3: Деплой на Railway (работа 24/7 бесплатно/недорого)
1. Зайди на [Railway.app](https://railway.app/) и авторизуйся через свой GitHub.
2. Нажми **«+ New Project»** ➔ **«Deploy from GitHub repo»**.
3. Выбери репозиторий `lidera-help-bot`.
4. Перейди во вкладку **Variables** (переменные окружения проекта) и добавь:
   - `BOT_TOKEN` = `твой_токен_из_BotFather`
   - `ADMIN_CHAT_ID` = `твой_telegram_id` *(узнать свой ID можно в боте @userinfobot)*
5. Нажми **Deploy**.

Railway автоматически установит зависимости из `requirements.txt` и запустит бота по `Procfile`. Бот сразу начнет отвечать в Telegram 24/7!
