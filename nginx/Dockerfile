FROM node:20.18 AS frontend
COPY ./public/node/frontend/package.json /code/frontend/
RUN npm install -g gulp

WORKDIR /code/frontend
RUN npm install
RUN mkdir -p ../static/fonts
RUN wget http://www.fawe.de/volpiano/volpiano51_web.zip
RUN unzip volpiano51_web.zip
RUN rm volpiano51_web.zip
RUN mv volpiano51_web/volpiano.woff ../static/fonts/volpiano.woff
COPY ./public/node/ /code/
RUN gulp build

FROM nginx:1.25
COPY ./nginx.conf /etc/nginx/nginx.conf
COPY --from=frontend /code/static /code/static
