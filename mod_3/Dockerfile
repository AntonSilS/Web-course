FROM python:latest


WORKDIR /app

COPY . .

RUN pip install pipenv

RUN pipenv install


CMD ["pipenv", "run", "python", "personal_helper.py"]
