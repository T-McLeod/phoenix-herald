FROM alpine:latest
RUN apk add --no-cache py3-pip python3-dev gcc
RUN mkdir -p /app
COPY bot.py requirements.txt /app/
COPY phoenix /app/phoenix
RUN pip3 install -r /app/requirements.txt
ENTRYPOINT /app/bot.py
