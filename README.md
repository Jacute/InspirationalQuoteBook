# InspirationalQuoteBook

InspirationalQuoteBook - это проект для создания и управления сборником вдохновляющих цитат. Проект использует несколько технологий, таких как Python и Docker, для обеспечения его работы. Проект содержит в себе сайт и телеграм бота для модерации пользовательских цитат.

## Оглавление

1. [Требования](#требования)
2. [Установка](#установка)
3. [Запуск проекта](#запуск-проекта)

## Требования

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

## Установка

1. Склонируйте репозиторий:
    ```bash
   git clone https://github.com/Jacute/InspirationalQuoteBook.git
   ```

2. Внесите данные БД в .env_mysql, данные веб-приложения в .env_production_app, данные телеграм бота в bot/.env

## Запуск проекта

1. Запустите контейнеры с помощью Docker Compose:
   ```bash
   docker compose up --build
   ```

2. Откройте браузер и перейдите по адресу:
   ```
   http://127.0.0.1
   ```

## Внешний вид

- Сайт

![alt text](img/site.png)
