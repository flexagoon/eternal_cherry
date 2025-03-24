FROM python:latest

WORKDIR /app

COPY cherry.py /app

RUN pip install --no-cache-dir aiogram google-genai

ENV NAME Eternal Cherry

CMD ["python", "cherry.py"]
