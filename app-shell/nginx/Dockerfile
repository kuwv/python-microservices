FROM node:lts-alpine AS build

WORKDIR /usr/local/src

COPY ./app-shell/package*.json /usr/local/src/

RUN apk add --no-cache --virtual .build-deps ;\
  npm install aurelia-cli -g ;\
  npm install

COPY ./app-shell /usr/local/src

RUN npm run build

FROM nginx:stable-alpine

WORKDIR /

COPY nginx.conf /etc/nginx/nginx.conf
COPY conf.d /etc/nginx/conf.d/
COPY --from=build /usr/local/src/dist /usr/share/nginx/html

EXPOSE 80 443
