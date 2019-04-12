FROM alpine:latest
RUN apk add --no-cache py3-pip python3-dev gcc
COPY *.py *.txt /app/
RUN pip3 install -r /app/requirements.txt
RUN mkdir -p /app
ENTRYPOINT /app/bot.py
