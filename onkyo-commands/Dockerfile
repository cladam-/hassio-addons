FROM ghcr.io/home-assistant/amd64-base:latest
RUN apk update && apk add python3 python3-dev git py3-pip py3-wheel py3-netifaces

WORKDIR /app
RUN git clone https://github.com/miracle2k/onkyo-eiscp .
RUN pip3 install .
RUN pip3 install paho-mqtt

COPY . .
CMD ["/app/run.sh"]
