import datetime

import sqlalchemy
from fastapi import FastAPI
import databases
import requests
import json
from pydantic import BaseModel
from sqlalchemy import desc

from models.models import Questions

app = FastAPI()

DATABASE_URL = "postgresql://postgres:postgres@pgdb:5432/quizdb"
database = databases.Database(DATABASE_URL)
engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)


class QuestValid(BaseModel):
    questions_num: int


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.post('/')
async def get_question(questions: QuestValid):
    q = json.loads(questions.json())
    url = f"https://jservice.io/api/random?count={q['questions_num']}"
    response = requests.get(url)
    data = response.json()
    try:
        query = Questions.select().order_by(desc('id')).limit(1)
        last_questions = await database.fetch_all(query)
    except:
        last_questions = None

    for item in data:
        date = item['airdate'][:10]
        date = datetime.datetime.strptime(date, '%Y-%m-%d')
        try:
            query = Questions.insert().values(question_id=item['id'], question=item['question'], answer=item['answer'],
                                              date=date)
            await database.execute(query)
        except:
            url_rez = f"https://jservice.io/api/random?count=1"
            response = requests.get(url_rez)
            data.append(response.json()[0])

    return {'last_questions': last_questions}
