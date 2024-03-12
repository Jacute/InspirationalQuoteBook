import asyncio
import logging
import sys
import os
import traceback
from dotenv import load_dotenv

from aiogram import F
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import Command

from cursor import dbConnect, selectQuery, updateQuery


load_dotenv()

TOKEN = os.getenv("TG_BOT_TOKEN")
ADMIN_ID = int(os.getenv("TG_ADMIN_ID"))

MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_PORT = os.getenv("MYSQL_PORT")

bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()


async def check_database():
    try:
        conn = dbConnect(MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE)
    except Exception as e:
        logging.critical(f'Unable to connect to database. Error: {traceback.format_exc()}')
        return

    try:
        query_result = await selectQuery(conn, "SELECT * FROM quotes WHERE status = 2")
        if query_result:
            for row in query_result:
                id = row[0]
                quote = row[1]
                author = row[2]
                categories = row[4]
                kb = [
                    [
                        types.InlineKeyboardButton(text="✅", callback_data=f"publicate_{id}"),
                        types.InlineKeyboardButton(text="❌", callback_data=f"not_publicate_{id}")
                    ]
                ]
                keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb)
                await bot.send_message(chat_id=ADMIN_ID, text=f"**Цитата**\n{quote}\n**Автор**\n{author}\n**Категории**\n{categories}\nОпубликовать?", reply_markup=keyboard)
    except Exception as e:
        logging.critical(f'Unable to connect to database. Error: {traceback.format_exc()}')
        await bot.send_message(chat_id=ADMIN_ID, text=f'Error: {traceback.format_exc()}')
    finally:
        conn.close()


@dp.callback_query(F.data.startswith("publicate_"))
async def publicate(call: types.CallbackQuery):
    call_data = call.data
    id = call_data.split('_')[-1]
    
    try:
        conn = dbConnect(MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE)
    except Exception as e:
        logging.critical(f'Unable to connect to database. Error: {traceback.format_exc()}')
        return

    try:
        await updateQuery(conn, f"UPDATE quotes SET status = 1 WHERE id = %s", (id,))
        await call.message.edit_text(f"Цитата id={id} опубликована!")
    except Exception as e:
        print(traceback.format_exc())
        await call.message.edit_text(f"Цитата id={id} не была опубликована")
    finally:
        conn.close()
    
    await call.answer()


@dp.callback_query(F.data.startswith("not_publicate_"))
async def not_publicate(call: types.CallbackQuery):
    call_data = call.data
    id = call_data.split('_')[-1]
    
    try:
        conn = dbConnect(MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE)
    except Exception as e:
        logging.critical(f'Unable to connect to database. Error: {traceback.format_exc()}')
        return
    
    try:
        await updateQuery(conn, f"UPDATE quotes SET status = 0 WHERE id = %s", (id,))
    except Exception as e:
        print(traceback.format_exc())
    finally:
        await call.message.edit_text(f"Цитата id={id} не опубликована!")
        conn.close()
    
    await call.answer()
    

@dp.message(Command(commands=['check']))
async def check_command(message: types.Message):
    await check_database()


async def scheduled_task():
    while True:
        await asyncio.sleep(60) # Проверка бд каждые 60 секунд
        await check_database()


async def main():
    task = asyncio.create_task(scheduled_task())
    await dp.start_polling(bot)



if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    file_handler = logging.FileHandler('logs/bot.log')
    file_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    logging.getLogger().addHandler(file_handler)

    asyncio.run(main())