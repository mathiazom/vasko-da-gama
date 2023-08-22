FROM python:3.10.9-bullseye

RUN apt update && apt -y install cron

# Set local timezone (for cron)
RUN ln -sf /usr/share/zoneinfo/Europe/Amsterdam /etc/localtime

WORKDIR /app

RUN curl -sSL https://install.python-poetry.org | python3 - -y --version 1.6.1

RUN /root/.local/bin/poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock ./

RUN /root/.local/bin/poetry install --only main

COPY . .

COPY docker/runner.sh /

RUN chmod 0744 /runner.sh

CMD ["sh", "/runner.sh"]
