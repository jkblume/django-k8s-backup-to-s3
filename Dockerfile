FROM python:3.7

WORKDIR /app

# install python requirements
ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt

# install kubernetes
RUN curl -LO https://storage.googleapis.com/kubernetes-release/release/v1.9.0/bin/linux/amd64/kubectl
RUN chmod +x kubectl
RUN mv kubectl /usr/local/bin/kubectl

ADD . .

ENV AWS_ACCESS_KEY_ID ""
ENV AWS_SECRET_ACCESS_KEY ""
ENV POD_ID ""
ENV PROJECT_NAME ""
ENV S3_BUCKET_NAME ""
ENV DUMPDATA_EXCLUDE ""
ENV MEDIA_DIRECTORY ""
