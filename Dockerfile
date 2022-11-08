FROM python:3.10

ENV HOME /root
WORKDIR /root

COPY . .

RUN pip3 install -r requirements.txt

CMD python3 -m app