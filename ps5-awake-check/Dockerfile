FROM ghcr.io/home-assistant/amd64-base:3.13
RUN apk add mosquitto-clients
WORKDIR /app
COPY . .
CMD ["/app/run.sh"]
