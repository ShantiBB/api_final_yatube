Как запустить проект:
Клонировать репозиторий и перейти в него в командной строке:

git clone https://github.com/ShantiBB/api_final_yatube/tree/master
Cоздать и активировать виртуальное окружение:

python3 -m venv env
source env/bin/activate
Установить зависимости из файла requirements.txt:

python3 -m pip install --upgrade pip
pip install -r requirements.txt
Выполнить миграции:

python3 manage.py migrate
Запустить проект:

python3 manage.py runserver

Основные возможности API:
1. CRUD операции для постов.
2. CRUD операции для комментариев к постам.
3. Функциональность подписок и фильтрация по подпискам.
4. Пагинация для постов.

Примеры запросов к API есть в документации данного проекта по адресу: http://127.0.0.1:8000/redoc/
