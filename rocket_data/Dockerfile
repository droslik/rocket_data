FROM python:3.9

ENV PYTHONBUFFERED=1

WORKDIR /core

COPY Pipfile Pipfile.lock ./
RUN python -m pip install --upgrade pip
RUN pip install pipenv && pipenv install --dev --system --deploy

COPY ./electronics .

RUN chmod +x ./entrypoint.sh
RUN chmod +x ./run_celery.sh

CMD ["./entrypoint.sh"]