FROM python:3.9.13-buster

ARG APP_HOME=/app

WORKDIR ${APP_HOME}

COPY ./docker/production/flask/start /start
COPY . ${APP_HOME}

# Install depencies.
RUN pip3 install -r ${APP_HOME}/requirements/production.txt
RUN pip3 install -e ${APP_HOME}/src

# Make start script runnable.
RUN chmod +x /start
