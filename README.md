![Workflow status badge](https://github.com/berg96/tasks_bot_testtask_anverali/actions/workflows/main.yml/badge.svg)
# Тестовое задание для Python разработчика от Averali

## Описание задачи:
В рамках тестового задания написан телеграмм бот, который создает задачи по команде /add и добавляет их в БД PostgreSQL, а по команде /tsk он выводит список задач из БД для каждого пользователя.


[Tasks Averali (test task)](https://t.me/tasks_averali_testtask_bot) [@tasks_averali_testtask_bot](https://t.me/tasks_averali_testtask_bot)

### Автор Артём Куликов

tg: [@Berg1005](https://t.me/berg1005)

[GitHub](https://github.com/berg96)

## Используемые технологии 

Проект реализован на языке python c использованием следующих библиотек:

* aiogram (v 3.4.1)
* asyncpg (v 0.29.0)
* python-dotenv (v 1.0.1)

## Как запустить проект

Клонировать репозиторий:
```
git clone git@github.com:berg96/tasks_bot_testtask_anverali.git
```
Запустить Docker compose:
```
docker compose up -d
```
