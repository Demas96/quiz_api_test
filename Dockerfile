FROM python:3

RUN mkdir /fastapi_app

WORKDIR /fastapi_app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

# CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0"]

