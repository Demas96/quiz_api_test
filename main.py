import datetime
import sqlalchemy
import databases
import requests

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import desc
from asyncpg.exceptions import UniqueViolationError

from models.models import Questions
from config import HOST_DB, PORT_DB, USER_DB, NAME_DB, PASSWORD_DB


app = FastAPI()

DATABASE_URL = f"postgresql://{USER_DB}:{PASSWORD_DB}@{HOST_DB}:{PORT_DB}/{NAME_DB}"
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
    url = f"https://jservice.io/api/random?count={questions.questions_num}"
    response = requests.get(url)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Something is wrong")
    data = response.json()
    query = Questions.select().order_by(desc('id')).limit(1)
    last_questions = await database.fetch_all(query)
    for item in data:
        date = item['airdate'][:10]
        date = datetime.datetime.strptime(date, '%Y-%m-%d')
        try:
            query = Questions.insert().values(
                question_id=item['id'],
                question=item['question'],
                answer=item['answer'],
                date=date
            )
            await database.execute(query)
        except UniqueViolationError:
            url_rez = f"https://jservice.io/api/random?count=1"
            response = requests.get(url_rez)
            data.append(response.json()[0])

    return {'last_questions': last_questions}
