# Quiz Question Collector

Данный API собирает вопросы для викторины с сервиса https://jservice.io

## Основной стек

* FastAPI
* PostgreSQL

## Запуск

Скачать репозиторий и выполнить команду

    docker-compose up

# REST API
 Автоматическую документацию можно посмотреть по ссылке  http://127.0.0.1:8000/docs

REST API описан ниже

## Получение вопросов

### Request

    curl -X 'POST' \
    'http://127.0.0.1:8000/' \
    -H 'accept: application/json' \
    -H 'Content-Type: application/json' \
    -d '{
    "questions_num": 2
    }'


### Response
Ответом на запрос будет предыдущий сохранённый вопрос для викторины (если в бд ничего не было записано, 
возвращаается Null).

    {
    "last_questions": [
        {
          "id": {id},
          "question_id": {question_id},
          "question": {question},
          "answer": {answer},
          "date": {date}
        }
      ]
    }
##