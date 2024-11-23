FROM python:3.10

WORKDIR /mack-etl

COPY ./requirements.txt .

RUN pip install -r requirements.txt

CMD ["/bin/bash"]
