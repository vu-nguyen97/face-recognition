FROM python:3.12-slim

ENV DEBIAN_FRONTEND=noninteractive

# Cài đặt các gói cần thiết và thiết lập liên kết
RUN apt-get -y update \
    && apt-get -y install --no-install-recommends --no-install-suggests \
        apt-transport-https ca-certificates curl libaio-dev \
        unzip build-essential libssl-dev software-properties-common \
    && apt-get -y autoremove \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* 
      
# Cài đặt Oracle Instant Client
ADD https://download.oracle.com/otn_software/linux/instantclient/2111000/instantclient-basic-linux.x64-21.11.0.0.0dbru.zip /tmp/oracle-instantclient.zip
RUN mkdir -p /opt/oracle \
    && unzip /tmp/oracle-instantclient.zip -d /opt/oracle \
    && mv /opt/oracle/instantclient_* /opt/oracle/instantclient \
    && rm /tmp/oracle-instantclient.zip

# Cài đặt pip và các thư viện Python
ADD https://bootstrap.pypa.io/get-pip.py /tmp/get-pip.py
RUN python /tmp/get-pip.py \
    && pip install -U --no-cache-dir pip \
    && pip install cx_Oracle

# Cài đặt CMake
WORKDIR /tmp
RUN curl -OL https://github.com/Kitware/CMake/releases/download/v3.27.4/cmake-3.27.4.tar.gz \
    && tar -xzvf cmake-3.27.4.tar.gz \
    && cd cmake-3.27.4 \
    && ./bootstrap -- -DCMAKE_BUILD_TYPE:STRING=Release \
    && make -j4 \
    && make install \
    && cd .. \
    && rm -rf cmake-3.27.4*

# Cài đặt các yêu cầu từ requirements.txt
WORKDIR /app
COPY requirements.txt .
RUN pip install --ignore-installed -r requirements.txt

# Copy toàn bộ mã nguồn vào container
COPY . .

# Thiết lập biến môi trường và cổng
ENV LD_LIBRARY_PATH=/opt/oracle/instantclient:$LD_LIBRARY_PATH
EXPOSE 8000

CMD ["gunicorn"  , "-b", "0.0.0.0:8000", "app:app"]