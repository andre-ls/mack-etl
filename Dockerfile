FROM python:3.10

WORKDIR /mack-etl

COPY . .

RUN pip install -r requirements.txt

CMD ["python","./code/main.py"]
