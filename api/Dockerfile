FROM python:3.10
WORKDIR /python-docker

COPY ./requirements.txt /python-docker

RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

ENV FASTAPI_APP=app.py

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5000"]