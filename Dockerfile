FROM python:3.8-slim-buster

RUN apt-get update \
    && apt-get install -y --no-install-recommends python3-pip git \
    && rm -rf /var/lib/apt/lists/*
RUN pip3 install --upgrade pip

WORKDIR /music
RUN chmod 777 /music
COPY requirements.txt .
RUN pip3 install --no-cache-dir -U -r requirements.txt
COPY . .
CMD ["python3", "-m", "mbot"]
