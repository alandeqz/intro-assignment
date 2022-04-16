FROM django

WORKDIR /usr/src/app

COPY . /usr/src/app

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "8000"]
