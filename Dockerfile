FROM python:3.9.12

ENV HOME /root
WORKDIR /root

COPY . .

RUN pip3 install -r requirements.txt

CMD python app.py