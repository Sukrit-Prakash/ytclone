FROM python:3.8

WORKDIR /backend

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD [ "python","prev.py" ]
