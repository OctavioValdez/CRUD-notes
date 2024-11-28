FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ARG HOST
ARG USER
ARG PASSWORD
ARG NAME
ARG PORT
ARG BUCKET_NAME
ARG AWS_ACCESS_KEY_ID
ARG AWS_SECRET_ACCESS_KEY
ARG REGION

ENV HOST=$HOST
ENV USER=$USER
ENV PASSWORD=$PASSWORD
ENV NAME=$NAME
ENV PORT=$PORT
ENV BUCKET_NAME=$BUCKET_NAME
ENV AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID
ENV AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY
ENV REGION=$REGION

EXPOSE 5000

CMD ["python", "crud.py"]