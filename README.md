# Интернет-магазин игр на Django
Этот репозиторий содержит полнофункциональный игровой интернет-магазин, разработанный с использованием Django, одного из самых популярных фреймворков Python для веб-разработки. Этот проект предоставляет возможность создания и управления интернет-магазином для продажи видеоигр.

🌐  [Перейти на сайт магазина](https://gamestore-server.online/)

___

## Основные функции

- Регистрация и авторизация пользователей.
- Пагинация и фильтрация игр.
- Кеширование списка игр при помощи Redis
- Добавление и удаление продуктов в корзине.
- Изменение информации о пользователе и загрузка изображения в профиле.
- Просморт списка заказов и каждого заказа по отдельности.
- Оформление заказов и платежи с использованием интегрированной платежной системой Stripe.
- Панель администратора для управления играми, заказами и пользователями.
- Отправка электронных писем для подтверждения аккаунта и сброса пароля при помощи Celery.
  
___

## Установка и использование

Чтобы развернуть этот проект на своем локальном сервере, выполните следующие шаги:

1. Клонируйте репозиторий на свой локальный компьютер:
   
        git clone https://github.com/pavlechenk/GameStore.git

2. Перейдите в директорию проекта:
   
        cd GameStore

3. Создайте и активируйте виртуальное окружение (рекомендуется):
   
        python -m venv venv
        source venv/bin/activate  # Для Linux/Mac
        venv/Scripts/activate  # Для Windows

4. Установите зависимости:

        pip install -r requirements.txt

5. Скачайте и установите PostgreSQL с официального сайта:
   
       https://www.postgresql.org/download/
   
6. Создайте базу данных и роли в psql:

       CREATE DATABASE db_name;
       CREATE ROLE name with password 'password';
       ALTER ROLE "name" with LOGIN;
       GRANT ALL PRIVILEGES ON DATABESE "db_name" to name;
       ALTER USER name CREATEDB;

7. Создайте файл .env и установите в нем значения для следующих переменных:

        DEBUG=True
        SECRET_KEY=
        DOMAIN_NAME=http://127.0.0.1:8000
        
        REDIS_HOST=127.0.0.1
        REDIS_PORT=6379
        
        DATABASE_NAME=
        DATABASE_USER=
        DATABASE_PASSWORD=
        DATABASE_HOST=127.0.0.1
        DATABASE_PORT=5432
        
        EMAIL_HOST=smtp.gmail.com
        EMAIL_PORT=587
        EMAIL_HOST_USER=
        EMAIL_HOST_PASSWORD=
        EMAIL_USE_TLS=True
        
        STRIPE_PUBLIC_KEY=
        STRIPE_SECRET_KEY=
        STRIPE_WEBHOOK_SECRET=

8. Выполните миграции базы данных:
   
        python manage.py makemigrations
        python manage.py migrate
   
9. Загрузите фикстуры:

        python manage.py loaddata games/fixtures/genres.json # Для Linux/Mac
        python manage.py loaddata games/fixtures/games.json     

        python -Xutf8 manage.py loaddata games/fixtures/genres.json # Для Windows
        python -Xutf8 manage.py loaddata games/fixtures/games.json
   
10. Запустите Celery для асинхронной обработки задач:

        celery -A GameStore worker -l INFO

11. Зарегистрируйтесь на официальном сайте stripe и установите значения для переменных STRIPE_PUBLIC_KEY и STRIPE_SECRET_KEY в файле .env, которые можно взять из Dashboard после регистрации:

        Ссылка для регистрации - https://dashboard.stripe.com/register

12. Запустите webhook для Windows, используя stripe.exe и сохраните полученный webhook в переменной STRIPE_WEBHOOK_SECRET файла .env:
   
        stripe.exe webhook setup --listen-to http://127.0.0.1:8000/webhock/stripe/ 
        Инструкция по установке stripe - https://stripe.com/docs/payments/checkout/fulfill-orders

13. Запустите сервер разработки:
   
        python manage.py runserver

14. Откройте веб-браузер и перейдите по указанному ниже адресу для доступа к интернет-магазину:

        http://127.0.0.1:8000/

___

## Лицензия

Этот проект лицензируется в соответствии с [лицензией MIT](https://en.wikipedia.org/wiki/MIT_License). Подробности см. в файле [LICENSE](https://github.com/pavlechenk/GameStore/blob/main/LICENSE.txt).

___

## Вклад и обратная связь

Мы приветствуем ваш вклад в развитие проекта. Если у вас есть какие-либо вопросы или предложения, пожалуйста, создайте новый issue или отправьте pull request.

Давайте вместе сделаем этот игровой интернет-магазин лучше!
