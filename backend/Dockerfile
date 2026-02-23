FROM python:3.11-slim

# Ставим пакеты, нужные для Oracle Instant Client, и сразу качаем его
RUN apt-get update && \
    apt-get install -y wget unzip libaio-dev && \
    # чиним libaio.so.1
    ln -s /usr/lib/x86_64-linux-gnu/libaio.so /usr/lib/x86_64-linux-gnu/libaio.so.1 || true && \
    # скачиваем и распаковываем Instant Client
    mkdir -p /opt/oracle && \
    wget https://download.oracle.com/otn_software/linux/instantclient/1919000/instantclient-basic-linux.x64-19.19.0.0.0dbru.zip && \
    unzip instantclient-basic-linux.x64-19.19.0.0.0dbru.zip -d /opt/oracle/ && \
    rm instantclient-basic-linux.x64-19.19.0.0.0dbru.zip && \
    mv /opt/oracle/instantclient_19_19 /opt/oracle/instantclient && \
    rm -rf /var/lib/apt/lists/*

ENV LD_LIBRARY_PATH=/opt/oracle/instantclient

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY templates ./templates
COPY static ./static

EXPOSE 5000

CMD ["python", "app.py"]
