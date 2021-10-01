FROM python:3.8.11
RUN pip install --upgrade pip
COPY requirements.txt /
RUN pip install -r /requirements.txt
COPY . /app
WORKDIR /app
RUN pytest
EXPOSE 5000
ENTRYPOINT [ "docker-entrypoint.sh" ]
