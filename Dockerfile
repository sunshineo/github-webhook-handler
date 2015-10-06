FROM python:2.7.10

WORKDIR /root

EXPOSE 80

ENV USE_PROXYFIX true
ENV SERVICE_ID "Replace me"

COPY requirements.txt /root/requirements.txt
RUN pip install -r requirements.txt

COPY index.py /root/index.py

ENTRYPOINT /usr/local/bin/python /root/index.py
