FROM python:3.8.7-slim-buster
COPY . /app
WORKDIR /app
ENV PYTHONPATH /app
ENV PYTHONBUFFERED=1

RUN apt-get update
RUN apt-get install vim -y

RUN pip install pip==21.2.4 && \
	pip install -r requirements.txt

CMD ["uvicorn","main:app","--reload","--host=0.0.0.0","--port=8000"]