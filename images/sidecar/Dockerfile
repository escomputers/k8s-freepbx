FROM alpine:3.18

RUN apk update && apk add bash curl jq openssl python3 py3-pip && \
  python3 -m pip install fastapi uuid uvicorn

COPY get-freepbx-credentials.sh /usr/local/bin/get-freepbx-credentials.sh
COPY main.py  /usr/local/bin/main.py

CMD ["bash", "/usr/local/bin/get-freepbx-credentials.sh"]
