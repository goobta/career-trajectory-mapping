FROM python:3-slim

RUN apt-get update \
    && apt-get -y install xvfb x11-utils unzip \
    && rm -rf /var/lib/apt/lists* \
    && apt-get -y autoremove --purge \
    && apt-get -y clean

RUN mkdir -p /work \ 
    mkdir -p /bin \
    mkdir -p /tmp \
    && cd \tmp \
    && wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && dpkg -i google-chrome-stable_current_amd64.deb

RUN wget -q https://chromedriver.storage.googleapis.com/89.0.4389.23/chromedriver_linux64.zip \
    && unzip chromedriver_linux64.zip \
    && mv chromedriver /bin/

COPY requirements.txt .

RUN pip install -r requirements.txt