FROM python:3.10

WORKDIR /app

COPY ./src /app/src
COPY ./requirements.txt .

RUN pip install -r requirements.txt

ENTRYPOINT ["python3", "-u", "/app/src/run.py"]