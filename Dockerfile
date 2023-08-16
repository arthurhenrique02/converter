# get build image to build docker
FROM python:3.10.12-slim-bullseye

# make image lighter dont writing python byte code
ENV PYTHONDONTWRITEBYTECODE 1

# disable python buffer before sending somethings
ENV PYTHONUNBUFFERED 1

# change workspace directory
WORKDIR /app

# copy requirements to app dir
COPY requirements.txt /app

# copy the rest of application
COPY . /app
COPY scripts /scripts

# to run app on that port
EXPOSE 8000


# create venv on root
# upgrade pip
# get pkgconfig to MYSQL
# update
# install requirements
# create linux user with no password and home
# change user permissions
# make script files executable
RUN python -m venv /venv && \
    /venv/bin/pip install --upgrade pip && \
    apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y gcc default-libmysqlclient-dev pkg-config && \
    /venv/bin/pip install --no-cache-dir -r /app/requirements.txt && \
    adduser --gecos "" --disabled-password --no-create-home duser && \
    chown -R duser:duser /venv && \
    chmod -R +x /scripts



# add venv and scripts folder to path
ENV PATH="/scripts:/venv/bin:$PATH"

# change user
USER duser
# to run the application
CMD ["commands.sh"]