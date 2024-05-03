import asyncio
import logging
import os
import sys

import asyncpg
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command, CommandObject, CommandStart
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')
bot = Bot(token=TOKEN)
dp = Dispatcher()
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_DB = os.getenv('POSTGRES_DB')
POSTGRES_HOST = os.getenv('POSTGRES_HOST')


async def create_pool():
    return await asyncpg.create_pool(
        user=POSTGRES_USER, password=POSTGRES_PASSWORD,
        database=POSTGRES_DB, host=POSTGRES_HOST
    )


async def create_table():
    pool = await create_pool()
    async with pool.acquire() as conn:
        async with conn.transaction():
            await conn.execute('''
                CREATE TABLE IF NOT EXISTS tasks (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER,
                    task TEXT
                )
            ''')
    await pool.close()


async def add_task(user_id, task):
    pool = await create_pool()
    async with pool.acquire() as conn:
        await conn.execute(
            'INSERT INTO tasks (user_id, task) VALUES ($1, $2)', user_id, task
        )
    await pool.close()


async def get_tasks(user_id):
    pool = await create_pool()
    async with pool.acquire() as conn:
        tasks = await conn.fetch(
            'SELECT task FROM tasks WHERE user_id = $1', user_id
        )
    await pool.close()
    return [task['task'] for task in tasks]


@dp.message(CommandStart())
async def command_start_handler(message: types.Message):
    await message.answer(
        f'Привет, {message.from_user.full_name}! '
        'Я бот для управления заданиями. '
        'Используй команду /add чтобы добавить задание и '
        '/tsk чтобы посмотреть все задания.'
    )


@dp.message(Command('add'))
async def command_add_task_handler(
    message: types.Message, command: CommandObject
):
    user_id = message.from_user.id
    task = command.args
    if not task:
        await message.answer(
            'Вы не ввели текст задания.\n'
            'Пример: "/add Написать бота"'
        )
        return
    await add_task(user_id, task)
    await message.answer('Задание успешно добавлено!')


@dp.message(Command('tsk'))
async def command_get_tasks_handler(message: types.Message):
    user_id = message.from_user.id
    tasks = await get_tasks(user_id)
    if tasks:
        tasks_str = '\n'.join(tasks)
        await message.answer(f'Ваши задания:\n{tasks_str}')
    else:
        await message.answer('У вас пока нет заданий.')


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO, stream=sys.stdout
    )
    asyncio.get_event_loop().run_until_complete(create_table())
    asyncio.run(main())
