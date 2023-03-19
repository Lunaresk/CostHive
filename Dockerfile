FROM python@sha256:53da4973924b6b3da6eb34f98e4e9dffdaf1cc05b468da73c69e3a862c36ee19
# python:3.10.10-slim-bullseye
RUN useradd costhive

WORKDIR /home/costhive

RUN apt update && apt -y upgrade
RUN apt install -y libpq-dev gcc g++

RUN python -m pip install pipenv

COPY boot.sh ./
RUN chmod +x boot.sh

COPY backend backend

ENV FLASK_APP run.py

RUN chown -R costhive:costhive ./
USER costhive

RUN cd backend && pipenv install && pipenv install gunicorn && cd ..

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]