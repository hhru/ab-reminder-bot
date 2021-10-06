# AB Reminder bot

Бот создающий страницу wiki для AB и отправляющий напоминания о заполнении в slack 

## Как использовать 

Для запуска бота необходимо указать пути к нужным файлам/директориям в файле `docker-compose.yml` в разделе `volumes`.

Там нужно указать три пути для монтирования:
* Путь к директории, где будут храниться файлы кешей
* Путь к файлу с настройками авторизации, пример находится в `config.json.ex`
* Путь к файлу с основными настройками, пример находится в `bot_settings.py.ex`

После этого для запуска бота можно выполнить одну из команд:
* `docker-compose run ab-reminder-bot users` - получает и сохраняет в кеш информацию о командах и их участниках, 
  для которых необходимо подготовить wiki страницу и сделать напоминание
* `docker-compose run ab-reminder-bot page` - создает wiki страницу и отправляет сообщение в slack
* `docker-compose run ab-reminder-bot remind` - отправляет в slack напоминание о необходимости заполнить страницу юзерам 
не заполнившим её
* `docker-compose run ab-reminder-bot update` - забирает сообщения из slack треда, относящегося к сообщению созданному 
  на этапе `page`, и добавляет их на созданную wiki страницу
  
Для периодического запуска этих задач используется cron.

## Как выпустить новую версию

1. Узнать последнюю версию докер-образа на http://registry.pyn.ru:5000/v2/ab_reminder_bot/tags/list
2. Собрать образ со следующей версией и пометить его тегом latest
    ```
    docker build -t registry.pyn.ru/ab_reminder_bot:<version> -t registry.pyn.ru/ab_reminder_bot:latest -f ./docker/Dockerfile .
    ```
3. Запушить образ
    ```
    docker push registry.pyn.ru/ab_reminder_bot:<version> && docker push registry.pyn.ru/ab_reminder_bot:latest
    ```
   
