FROM python:3.11-alpine

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 80

COPY ./app* ./app/

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]