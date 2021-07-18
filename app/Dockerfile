FROM python:3.8-slim

WORKDIR /usr/src/app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

# more suitable for production
# CMD ["gunicorn", "--bind", ":5000", "--workers", "3", "app:app"]

# for development, debugging
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]