FROM python:3.12-slim

WORKDIR /SEADO_app

COPY . .

RUN pip install --upgrade pip && pip install -r requirements.txt

EXPOSE 8000

CMD ["gunicorn", "app:app", "-b", "0.0.0.0:5000", "-w", "4"]