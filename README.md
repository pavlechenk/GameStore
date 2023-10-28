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
- Отправка электронных писем для подтверждения аккаунта при помощи Celery.
  
___

## Установка и использование

Чтобы развернуть этот проект на своем локальном сервере, выполните следующие шаги:

1. Клонируйте репозиторий на свой локальный компьютер:
   
        git clone https://github.com/your-username/game-store.git

2. Перейдите в директорию проекта:
   
        cd GameStore

3. Создайте и активируйте виртуальное окружение (рекомендуется):
   
        python -m venv venv
        source venv/bin/activate  # Для Linux/Mac
        venv/Scripts/activate  # Для Windows

4. Установите зависимости:

        pip install -r requirements.txt

5. Выполните миграции базы данных:
   
        python manage.py makemigrations
        python manage.py migrate
   
7. Загрузите фикстуры:

        python manage.py loaddata games/fixtures/genres.json # Для Linux/Mac
        python manage.py loaddata games/fixtures/games.json     

        python -Xutf8 manage.py loaddata games/fixtures/genres.json # Для Windows
        python -Xutf8 manage.py loaddata games/fixtures/games.json
   
9. Запустите Celery для асинхронной обработки задач:

        celery -A GameStore worker -l INFO

10. Запустите webhook для Windows, используя stripe.exe:
   
        stripe.exe webhook setup --listen-to http://127.0.0.1:8000/webhook/stripe  
        Инструкция по установке stripe - https://stripe.com/docs/payments/checkout/fulfill-orders#go-live

11. Запустите сервер разработки:
   
        python manage.py runserver

12. Откройте веб-браузер и перейдите по указанному ниже адресу для доступа к интернет-магазину:

        http://127.0.0.1:8000/

___

## Лицензия

Этот проект лицензируется в соответствии с [лицензией MIT](https://en.wikipedia.org/wiki/MIT_License). Подробности см. в файле [LICENSE](https://github.com/pavlechenk/GameStore/blob/main/LICENSE.txt).

___

## Вклад и обратная связь

Мы приветствуем ваш вклад в развитие проекта. Если у вас есть какие-либо вопросы или предложения, пожалуйста, создайте новый issue или отправьте pull request.

Давайте вместе сделаем этот игровой интернет-магазин лучше!
