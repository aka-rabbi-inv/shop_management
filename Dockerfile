FROM python:3.8

WORKDIR /app

RUN pip install pipenv

COPY Pipfile Pipfile.lock ./

RUN pipenv install --system --deploy

COPY . .

RUN python manage.py migrate

ENTRYPOINT ["sh", "./scripts/create_superuser.sh"]

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
