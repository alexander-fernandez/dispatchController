# docker pull python:3.11-slim-bullseye
FROM python:3.11-slim-bullseye
EXPOSE 5000
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD python main.py


