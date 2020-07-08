# syntax=docker/dockerfile:experimental
FROM registry.pyn.ru/python3.7-ubuntu18-building:2019.07.30

WORKDIR /home/hh/ab-reminder-bot
COPY . .

RUN mkdir -p -m 0600 ~/.ssh && ssh-keyscan github.com >> ~/.ssh/known_hosts
RUN pip3 install -r ./requirements.txt

ENTRYPOINT ["python","./run.py"]
