# The first instruction is what image we want to base our container on
# We Use an official Python runtime as a parent image
FROM python:3.8-slim
LABEL maintainer="alpha@example.com"

# set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update \
    && apt-get -y upgrade 
    # \
    # && apt-get install -y build-essential \
    # && apt-get install -y python-dev \
    # && apt-get install -y git

# create root directory for our project in the container
RUN mkdir /home/docker/ \
    && mkdir /home/docker/alpha/ \
    && mkdir /home/docker/alpha/multi
# Copy the current directory contents into the container 
# at /home/docker/alpha/multi
COPY . /home/docker/alpha/multi

# Set the working directory to /home/docker/alpha/multi
WORKDIR /home/docker/alpha/multi/src

# allow access to postgres wait script
RUN chmod +x /home/docker/alpha/multi/src/start_app_local.sh \
    && chmod +x /home/docker/alpha/multi/src/start_worker.sh \
    && chmod +x /home/docker/alpha/multi/src/start_scheduler.sh \
    && chmod +x /home/docker/alpha/multi/src/start_api.sh \
    && chmod +x /home/docker/alpha/multi/src/start_monitor.sh

RUN useradd -N -M -u 1037 --system -s /bin/bash docker \
    && groupadd docker \
    && usermod -a -G docker docker

RUN chown -R docker:docker /home/docker

# celery daemon
ADD ./celeryd.sh /etc/init.d/celeryd
ADD ./conf/celeryd.conf /etc/default/celeryd

# allow access to celery scripts
RUN chmod 755 /etc/init.d/celeryd \
    && chmod 640 /etc/default/celeryd \
    && chown root:root /etc/init.d/celeryd \
    && chown root:root /etc/default/celeryd

# celery beat daemon
ADD ./celerybeat.sh /etc/init.d/celerybeat

# allow access to celery scripts
RUN chmod 755 /etc/init.d/celerybeat \
    && chown root:root /etc/init.d/celerybeat

RUN mkdir /var/run/celery \
    && mkdir /var/log/celery \
    && chown docker:docker /var/run/celery/ \
    && chown docker:docker /var/log/celery/ 

# ENV LOCALCERTDIR /usr/local/share/ca-certificates
RUN pip install --upgrade pip \
    && pip install -r /home/docker/alpha/multi/dep/requirements.txt

CMD ["/home/docker/alpha/multi/src/start_app.sh"]