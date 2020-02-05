FROM redis:5-alpine

RUN mkdir /etc/redis

## Copy our default nginx config
COPY ./conf/cache.conf /etc/redis/default.conf

# Define working directory.
WORKDIR /data

# Define default command.
CMD ["redis-server", "/etc/redis/default.conf"]
