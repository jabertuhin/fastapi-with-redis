FROM python:3.9-slim-buster

RUN apt-get update \
    && apt-get upgrade \
    && rm -rf /var/lib/apt/lists/*


WORKDIR /app

RUN pip install --upgrade pip
COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . ./

EXPOSE 8080

CMD [ "make", "server" ]