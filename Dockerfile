FROM python:3.11.2-bullseye
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . /app
WORKDIR /app/to_do_app/to_do_app
CMD ["python3","manage.py","runserver","0.0.0.0:8000"]
