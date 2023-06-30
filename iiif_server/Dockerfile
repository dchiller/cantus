FROM debian:12

RUN apt-get update && apt-get install -y \
    default-jre \
    wget \ 
    unzip

RUN mkdir /opt/cantaloupe 
WORKDIR /opt/cantaloupe
RUN wget https://github.com/cantaloupe-project/cantaloupe/releases/download/v5.0.5/cantaloupe-5.0.5.zip \
    && unzip cantaloupe-5.0.5.zip \
    && rm cantaloupe-5.0.5.zip

COPY cantaloupe.properties /opt/cantaloupe/cantaloupe-5.0.5/cantaloupe.properties

EXPOSE 8182

WORKDIR /opt/cantaloupe/cantaloupe-5.0.5