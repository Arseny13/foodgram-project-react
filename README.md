
<h1 align="center"> Foodgram</h1>


___
<h4>Автор:</h4>

**Изимов Арсений**  - студент Яндекс.Практикума Когорта 17+
https://github.com/Arseny13


<h4>Проект:</h4>

https://github.com/Arseny13/foodgram-project-react

Скачать: git@github.com:Arseny13/foodgram-project-react.git

<h4>Cайт</h4>

- сайт: arsenyxiii.ddns.net
- ip: 51.250.88.11

Cуперпользователь
{ "username": "admin", "password": "admin", "email": "admin@admin.ru }

<h4>Команды на сайте после исправлений</h4>

-   scp nginx.conf user@51.250.88.11:/home/user/foodgram/infra

-   docker-compose build --no-cache

-   docker-compose up --force-recreate

-   docker-compose exec backend python manage.py migrate

-   docker-compose exec backend python manage.py collectstatic --no-input 


<h2>Техническое описание проекта</h2>

Ваш дипломный проект — сайт Foodgram, «Продуктовый помощник». Вы напишете онлайн-сервис и API для него. На этом сервисе пользователи смогут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

<h2>Исходники</h2>

После того, как вы прочтёте уроки этой темы — вам станет доступен репозиторий ```foodgram-project-react```; в нём подготовлен фронтенд и структура приложения. Склонируйте этот репозиторий и делайте проект в нём.

-   В репозитории есть папки frontend, backend, infra, data и docs.
-   В папке frontend находятся файлы, необходимые для сборки фронтенда приложения.
-   В папке infra — заготовка инфраструктуры проекта: конфигурационный файл nginx и docker-compose.yml.-
-   В папке backend пусто, там вы будете с нуля разрабатывать бэкенд продуктового помощника.
-   В папке data подготовлен список ингредиентов с единицами измерения. Список сохранён в форматах JSON и CSV: данные из списка будет необходимо загрузить в базу. + (доступнта по команде 
```docker-compose exec backend python manage.py command ingredients```)
-   В папке docs — файлы спецификации API.

В репозитории нет ни базы данных, ни бекенда, однако сразу после клонирования репозитория вы можете запустить проект и увидеть спецификацию API. По этой спецификации вам предстоит написать API для проекта Foodgram.

<h2>Запуск проекта</h2>

В папке ```infra ``` выполните команду ```docker-compose up```.
При выполнении этой команде сервис frontend, описанный в docker-compose.yml подготовит файлы, необходимые для работы фронтенд-приложения, а затем прекратит свою работу. 
Проект запустится на адресе http://localhost, увидеть спецификацию API вы сможете по адресу http://localhost/api/docs/

На сервере скопируйте папку infra на свой сервер(+frontend и docs) и выполните ```docker-compose up -d```

Как будет выглядеть ваше приложение, можно посмотреть на ```Figma.com```

<h2>Чек-лист для самопроверки</h2>

<h3>Функциональность проекта</h3>

Проект доступен по IP или доменному имени.

Все сервисы и страницы доступны для пользователей в соответствии с их правами. 

Рецепты на всех страницах сортируются по дате публикации (новые — выше).

Работает фильтрация по тегам, в том числе на странице избранного и на странице рецептов одного автора).

Работает пагинатор (в том числе при фильтрации по тегам).

Исходные данные предзагружены; добавлены тестовые пользователи и рецепты.

<h3>Для авторизованных пользователей:</h3>

1.  Доступна главная страница. +
2.  Доступна страница другого пользователя. +
3.  Доступна страница отдельного рецепта. +
4.  Доступна страница «Мои подписки». + 

    1. Можно подписаться и отписаться на странице рецепта. +

    2. Можно подписаться и отписаться на странице автора. +

    3. При подписке рецепты автора добавляются на страницу «Мои подписки» и удаляются оттуда при отказе от подписки. +

5.  Доступна страница «Избранное». +

    1. На странице рецепта есть возможность добавить рецепт в список избранного и удалить его оттуда.

    2. На любой странице со списком рецептов есть возможность добавить рецепт в список избранного и удалить его оттуда.

6.  Доступна страница «Список покупок». +

    1. На странице рецепта есть возможность добавить рецепт в список покупок и удалить его оттуда.

    2. На любой странице со списком рецептов есть возможность добавить рецепт в список покупок и удалить его оттуда.

    3. Есть возможность выгрузить файл (.txt или .pdf) с перечнем и количеством необходимых ингредиентов для рецептов из «Списка покупок».

    4. Ингредиенты в выгружаемом списке не повторяются, корректно подсчитывается общее количество для каждого ингредиента.

7.  Доступна страница «Создать рецепт». +

    1. Есть возможность опубликовать свой рецепт.

    2. Есть возможность отредактировать и сохранить изменения в своём рецепте.

    3. Есть возможность удалить свой рецепт.

8.  Доступна и работает форма изменения пароля. +
9.  Доступна возможность выйти из системы (разлогиниться). +

<h3>Для неавторизованных пользователей</h3>

1.  Доступна главная страница. +
2.  Доступна страница отдельного рецепта. +
3.  Доступна и работает форма авторизации. +
4.  Доступна и работает система восстановления пароля. -
5.  Доступна и работает форма регистрации. +

<h3>Администратор и админ-зона</h3>

1.  Все модели выведены в админ-зону. +
2.  Для модели пользователей включена фильтрация по имени и email. +
3.  Для модели рецептов включена фильтрация по названию, автору и тегам. +
4.  На админ-странице рецепта отображается общее число добавлений этого рецепта в избранное. +
5.  Для модели ингредиентов включена фильтрация по названию. +

<h3>Инфраструктура</h3>

1.  Проект работает с СУБД PostgreSQL. +
2.  Проект запущен на сервере в Яндекс.Облаке в трёх контейнерах: nginx, PostgreSQL и Django+Gunicorn. Заготовленный контейнер с фронтендом используется для сборки файлов. +
3.  Контейнер с проектом обновляется на Docker Hub. +
4.  В nginx настроена раздача статики, запросы с фронтенда переадресуются в контейнер с Gunicorn. Джанго-админка работает напрямую через Gunicorn. +
5.  Данные сохраняются в volumes. +

<h2>шаблон env-файла</h2>

- SECRET_KEY=код приложения
- DB_ENGINE=django_db
- DB_NAME=имя_бд
- DB_HOST=бд
- DB_PORT=порт_бд





<h2>Техническая документация</h2>

Для того чтобы получить, описанные понятным языком эндпоинты и настройки, да ещё с примерами запросов, да ещё с образцами ответов! Читай ReDoc, документация в этом формате доступна по ссылке:

_http://arsenyxiii.ddns.net/api/docs/_


<h2>Используемые технологии</h2>

- Doker=20.10.22
- nginx=1.21.3
- Python 3.7.9
- asgiref==3.2.10
- Django==3.2.18
- django-filter==2.4.0
- djangorestframework==3.12.4
- djangorestframework-simplejwt==4.8.0
- gunicorn==20.0.4
- psycopg2-binary==2.8.6
- PyJWT==2.1.0
- pytz==2020.1
- sqlparse==0.3.1
- python-dotenv==0.21.0
- pytest==6.2.4
- pytest-django==4.4.0
- pytest-pythonpath==0.7.3
- django-utils-six==2.0
- webcolors==1.11.1