FROM python:3.8

WORKDIR /todoapi-k8s

COPY . /todoapi-k8s

RUN pip3 install -r requirements.txt

CMD python -m todoapp.main
