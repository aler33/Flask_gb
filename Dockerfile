FROM python:3.10-buster

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY wsgi.py wsgi.py
COPY blog ./blog

EXPOSE 5000

CMD ["flask", "init-db"]
CMD ["flask", "create-users"]
CMD ["python", "wsgi.py"]