FROM docker:dind as docker
FROM python:3.12.3

COPY --from=docker /usr/local/bin/docker /usr/local/bin/docker

COPY requirements.txt .
COPY source ./source/
COPY LICENSE .

RUN python3 -m pip install -r requirements.txt
WORKDIR source
CMD ["python3", "main.py"]