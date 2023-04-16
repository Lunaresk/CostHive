FROM python@sha256:075fe10ae13ea0f081540bead850eeb7b6c71d07ed4766d75f8529abd0101c44
# python:3.10.10-slim-bullseye
RUN useradd costhive

WORKDIR /home/costhive

RUN apt update && apt -y upgrade
RUN apt install -y libpq-dev gcc g++ swig make

COPY boot.sh requirements.txt ./
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn
RUN chmod +x boot.sh

COPY backend backend

ENV FLASK_APP run.py

RUN chown -R costhive:costhive ./

USER costhive

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]