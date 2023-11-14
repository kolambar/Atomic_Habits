# Atomic_Habits
Это веб-приложение. В нем пользователи могут создавать полезные привычки, которым хотят научиться. 
Сами привычки можно делать публичными, чтобы другие пользователи могли их заимствовать. 
Также у привычек могут быть поощерения, чтобы закреплять их было проще.
У приложения есть бот в телеграмме. Этот бот шлет уведомления, когда одну из привычек пользователю пора выполнять. Чтобы бот работал, нужно написать ему команду /start. 

# Инструкция по запуску проекта

Этот проект использует Docker Compose для запуска множества сервисов. Ниже приведены инструкции по запуску проекта.

## Требования

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Шаги по запуску

1. **Клонирование репозитория**

   ```bash
   git clone https://github.com/kolambar/Atomic_Habits
   cd Atomic_Habits
   ```
   
2. **Настройка окружения**
Создайте файл .env.docker в корне проекта и укажите необходимые переменные окружения. Пример:
   
   ```bash
   POSTGRES_DB=
   POSTGRES_USER=
   POSTGRES_PASSWORD=
   DEBUG=False
   SECRET_KEY=
   TELEGRAM_TOKEN=
   CELERY_BROKER_URL=redis://redis:6379/0
   CELERY_RESULT_BACKEND=redis://redis:6379/0
   HOST=db
   ```

3. **Запуск проекта**

   ```bash
   docker compose up --buile    
   ```
Это создаст и запустит все необходимые контейнеры, включая Redis, PostgreSQL, app и бота для телеграмма, Celery и Celery_beat.
   ```bash
  docker-compose down
   ```
Это остановит и удалит все созданные контейнеры

3. **Запуск проекта**

Для работы с вашим приложением посетите http://0.0.0.0:8001 в вашем веб-браузере.
