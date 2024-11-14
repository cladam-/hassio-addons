FROM ghcr.io/home-assistant/amd64-base:latest
RUN apk update && apk add python3 python3-dev git py3-pip py3-wheel py3-netifaces

WORKDIR /app
RUN pip3 install paho-mqtt --break-system-packages
RUN pip3 install schedule --break-system-packages

COPY . .
CMD ["/app/run.sh"]
