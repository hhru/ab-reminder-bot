# syntax=docker/dockerfile:experimental
FROM registry.pyn.ru/python3.7-ubuntu18-building:2019.07.30

WORKDIR /home/hh/ab-reminder-bot
COPY ab-reminder-bot ab-reminder-bot

RUN mkdir -p -m 0600 ~/.ssh && ssh-keyscan github.com >> ~/.ssh/known_hosts
RUN --mount=type=ssh pip3 install -r ./ab-reminder-bot/requirements.txt

ENTRYPOINT ["python","./ab-reminder-bot/run.py"]
