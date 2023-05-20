from datetime import datetime

from sqlalchemy import MetaData, Table, Column, Integer, String, Date

metadata = MetaData()

Questions = Table(
    'questions',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('question_id', Integer, nullable=False),
    Column('question', String, nullable=False, unique=True),
    Column('answer', String, nullable=False),
    Column('date', Date, nullable=False)
)
