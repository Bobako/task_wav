# Тестовое задание 2
## Веб-сервис преобразования wav->mp3

 ## Cборка образа
 Для сборки докер-образа запустите из корневой директориии проекта команду:
 ```
docker build -t task_wav .
 ```
 При этом для конфигурации образа будет использован Dockerfile из корневой директории проекта.

 ## Настройка проекта
 Во время разработки для настройки проекта может быть использован файл config.ini из корневой директории проекта.
 Когда проект контейнеризован, пересобирать его каждый раз для изменения конфигурации неудобно. Поэтому настройки так же можно передать в проект с помощью переменных окружения:
 ```
- USE_ENV=1
- DATABASE_URI=postgresql+psycopg2://postgres:postgrespw@postgres:5432
- SITE_PORT=5000
 ```
 Например, вот так это реализовано в файле docker-compose.yml.
 Переменная USE_ENV отвечает, будут использоваться переменные окружения или значения по умолчанию из config.ini.

## Запуск проекта
### Непосредственно на своей машине (например, во время разработки):
Подготовка окружения (выполнется один раз):
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirments.txt
```
Запуск:
```
python main.py
```
Все команды приведены для linux, выполняются из корневой директории проекта.
### В контейнере
```
docker run task_wav 
```
При необходимости можно передать переменные среды, например:
```
docker run task_wav SITE_PORT=80
```
### Docker-compose
В корневой директории проекта содержится файл docker-compose.yml, где заданы параметра проекта и контейнера с postgresql. Непосредственно сам образ проекта там подтягивается с докерхаба. Запустить оба контейнера можно с помощью команды
```
docker-compose up
```

## Подключение к базе данных
В качестве субд используется postgresql, контейнер с ней описан в docker-compose.yml.
Для подключения можно использовать URI.
```
DATABASE_URI=postgresql+psycopg2://postgres:postgrespw@postgres:5432
```

 ## На что следует обратить внимание
 Я сохраняю файлы .mp3 в отдельную директорию (или в volume, когда проект контейниризован), а в бд записываю лишь путь к ним. Полагаю, что составитель задания ожидает увидеть blob сохраненный непосредственно в бд. Но насколько я знаю, это не является best practice для таких задач. Надеюсь на ваше понимание)

 ## Примеры использования
 ```
alex@kuu:~/Downloads$ curl -X POST http://localhost:5000/create_user -H 'Content-Type: application/json' -d '{"username":"bobako"}'

{"token":"1c7c22ff-7f5c-48de-b413-8dc1855d346f","user_id":3}


alex@kuu:~/Downloads$ curl -X POST localhost:5000/create_audio -F user_data='{"user_id":3, "token":"1c7c22ff-7f5c-48de-b413-8dc1855d346f"}' -F file=@sample-3s.wav

http://localhost:5000/record?id=25eb1d5b-bf0c-41d1-b7be-7899f78129ca&user=3


alex@kuu:~/Downloads$ curl "http://localhost:5000/record?
id=25eb1d5b-bf0c-41d1-b7be-7899f78129ca&user=3" --output sample.mp3

  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100 52079  100 52079    0     0  3940k      0 --:--:-- --:--:-- --:--:-- 4238k
 ```


