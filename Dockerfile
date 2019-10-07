FROM python:3.7

WORKDIR /usr/src/app
COPY . .

RUN pip install pipenv gunicorn
RUN pipenv run pip install pip==18.0
RUN pipenv install --system

CMD gunicorn --bind 0.0.0.0:$PORT wsgi 