FROM debian:stable

RUN apt-get update \
    && apt-get install -y --no-install-recommends python3-pip git ffmpeg \
    && rm -rf /var/lib/apt/lists/*

#RUN apt install python3 ffmpeg git gcc python3-pip
RUN pip3 install --upgrade pip

WORKDIR /music
RUN chmod 777 /music
COPY requirements.txt .
RUN pip3 install -U -r requirements.txt
COPY . .
CMD ["python3", "-m", "bot"]
