FROM python:3.11-alpine

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN ./compile.sh

EXPOSE 5005

CMD ["python", "main.py", "--host", "0.0.0.0", "--port", "5005"]