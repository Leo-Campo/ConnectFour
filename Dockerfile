FROM python:3.9

COPY ./requirements.txt /tmp/requirements.txt
RUN python -m pip install --upgrade pip
RUN python -m pip install -r /tmp/requirements.txt
RUN python -m pip install black

RUN useradd -u 8877 --home-dir /home/leo --create-home --system --shell /bin/bash leo 
WORKDIR /home/connect-four

COPY --chown=leo ./.git ./.git
RUN chown -R leo .git/*
COPY --chown=leo ./app/ ./app/
COPY --chown=leo ./tests/ ./tests/

USER leo
CMD ["python", "-m", "app"]