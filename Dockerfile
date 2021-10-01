FROM python:3.8.11
COPY requirements.txt /
RUN pip install -r /requirements.txt
COPY . /app
WORKDIR /app
RUN pytest
CMD [ "python3", "-m" , "flask", "db", "upgrade"]
CMD [ "python3", "-m" , "flask", "seed"]
ENTRYPOINT [ "gunicorn", "-b", "0.0.0.0:5000", "--log-level", "INFO", "serve:app" ]
