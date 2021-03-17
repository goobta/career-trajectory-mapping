FROM selenium/standalone-chrome:88.0

USER root
RUN apt-get update \
    && apt install -y python3-pip python3.9-dev \
    && rm -rf /var/lib/apt/lists* \
    && apt-get -y autoremove --purge \
    && apt-get -y clean

COPY requirements.txt .
RUN python3.9 -m pip install -r requirements.txt