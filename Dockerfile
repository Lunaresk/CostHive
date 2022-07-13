FROM python:3.10-slim

RUN useradd scan2kasse

WORKDIR /home/scan2kasse

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt

COPY app app
COPY migrations migrations
COPY run.py boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP run.py

RUN chown -R scan2kasse:scan2kasse ./
USER scan2kasse

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]