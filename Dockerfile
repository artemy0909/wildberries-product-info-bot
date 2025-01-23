FROM python:3.12.7

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip setuptools
RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "main:main_app", "--host", "127.0.0.1", "--port", "8000"]