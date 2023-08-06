FROM python@sha256:21c9f0b22213295a13bd678c5b45aa587ff6cb01cd99b6cf0e6928f4c777006b
# python:3.11.4-slim-bullseye (arm/v7)
RUN useradd costhive

WORKDIR /home/costhive

RUN apt update && apt -y upgrade; \
    apt install -y libpq-dev gcc g++ swig make cmake m4; \
    rm -rf /var/lib/apt/lists

COPY boot.sh backend/requirements.txt ./
RUN python -m venv venv; \
    venv/bin/pip install --upgrade pip; \
    venv/bin/pip install wheel gunicorn; \
    venv/bin/pip install -r requirements.txt

COPY backend backend

ENV FLASK_APP run.py

RUN chmod +x boot.sh; \
    chown -R costhive:costhive .

USER costhive

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]