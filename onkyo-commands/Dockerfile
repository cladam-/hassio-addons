ARG BUILD_FROM=ghcr.io/home-assistant/amd64-base:latest
FROM $BUILD_FROM

RUN apk add --no-cache python3 python3-dev git py3-pip py3-wheel py3-netifaces

WORKDIR /app
RUN git clone --branch 1.2.7 --depth 1 https://github.com/miracle2k/onkyo-eiscp .
RUN pip3 install --break-system-packages .
RUN pip3 install --break-system-packages paho-mqtt==2.1.0

COPY . .
CMD ["/app/run.sh"]
