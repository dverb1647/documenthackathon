FROM python:3.7-slim
COPY . /app
WORKDIR /app
RUN pip install --upgrade pip && pip install -r requirements.txt
CMD FLASK_APP=server.py flask run -p 7001