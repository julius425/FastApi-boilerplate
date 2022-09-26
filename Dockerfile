FROM python:3.10

ENV PYTHONPATH "${PYTHONPATH}:/app/app"

EXPOSE 8000

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

COPY ./app /app
WORKDIR /app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--reload", "--reload-dir", "app"]
