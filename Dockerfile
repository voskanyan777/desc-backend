FROM python:3.10

WORKDIR /app

COPY . .

RUN pip install -r req.txt


CMD ["python", "backend/app/main.py"]
