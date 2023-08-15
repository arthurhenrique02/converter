# get build image to build docker
FROM python:3.10-slim-bullseye

# get python
RUN apt-get update \
    && apt-get install --no-install-recommends --no-install-suggests \
    build-essentials default-libmysqlclient-dev \ 
    && pip install --no-cache-dir --upgrade pip


WORKDIR /app

# copy requirements to app dir
COPY requirements.txt /app

# install requirements
RUN pip install --no-cache-dir --requirement /app/requirements.txt

# copy the rest of application
COPY . /app

# to run app on that port
EXPOSE 5000

# to run the application
CMD ["python", "manage.py", "runserver"]