FROM python:3.12.6

WORKDIR /app
COPY . /app

COPY requirements.txt ./

RUN pip install -r requirements.txt

CMD ["python", "main.py"]
