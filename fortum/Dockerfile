FROM ghcr.io/home-assistant/amd64-base:3.19
RUN apk add nodejs npm 
WORKDIR /app
COPY . .
RUN npm i
RUN npm run build
EXPOSE 4321
CMD ["npm", "run", "serve"]
