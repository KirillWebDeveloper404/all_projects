# MasterYogaBot

## Python version
```
3.9
```

## Установка зависимостей
для работы необходимо установить все зависимости для питона (для работы с ботом используется фреймворк **Aiogram**)

    $pip install -r requirements.txt

## Настройка конфига

## Секретные данные
Секретны должны храниться в файле `.credentials.yml` в корне директории с такой структурой:
```
database:
  host: <имя хоста для бд>
  user: <имя пользователя бд>
  password: <пароль от пользователя бд>
  db: <имя базы данных>
  port: <порт базы данных>
bot:
  token: <токен бота от **@BotFather**>
  pay: <токен для платежей в телеграмм>
admin:
  tg: <телеграмм id администратора>
  phone: <телефон администратора, начиная с 9, например: 9501234567 (пропускаем +7 или 8)>
```

база данных **PostgreSQL**, для работы используется фреймворк **peewee**.

## Запуск

для запуска бота выполните

    $python3 Bot.py

для запуска бота

## Навигация

+ Admin - обрабатывает логику админки
+ BotCallbacks - обрабатывает нажатия на главную клавиатуру
+ BotKeyboards - хранит в себе клавиатури и их функции генераторы
+ Client - хранит обработчики для личного кабинета клиента
+ DataBase - хранит функии для работы с бд и классы таблиц
+ Help - обработка логики страницы поддержки
+ Login - авторизация при /start
+ Methods - вспомогательные методы типа валидации и генерации ключей
+ Payments - получение ссылок, оплата занятий
+ Seminar - обработка семинаров
+ Shop - все покупки внутри бота
+ Teachers - панель учителя
+ TimeTable - обработка календарей
+ Videos - видеотека и видеокурсы

## Code style
Code style checks are automated by a pre-commit hook
that executes such tools as `black` and `isort`.

The configs of the tools are:
- `.pre-commit-config.yaml` that describes the tools executed by a hook,
- `pyproject.toml` that configures `black` and `isort`,

## To configure a pre-hook for development
```sh
# install a git pre-commit hook
pre-commit install

# check by running
pre-commit run --all-files

# the desired output should look like this
# >> black............................................Passed
# >> isort............................................Passed

# to uninstall the hook in case it's needed
# pre-commit uninstall
```
