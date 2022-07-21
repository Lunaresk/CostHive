FROM python@sha256:38000b248a186dcae150fe2f64d23bd44a0730347d1e5e4d1faedd449a9a4913

RUN useradd scan2kasse

WORKDIR /home/scan2kasse

RUN apt update && apt upgrade
RUN apt install -y libpq-dev gcc g++

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn

COPY app app
COPY migrations migrations
COPY configs configs
COPY run.py boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP run.py

RUN chown -R scan2kasse:scan2kasse ./
USER scan2kasse

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]