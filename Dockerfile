FROM ubuntu:20.04

RUN apt-get update
RUN apt-get install -y python3.8 python3-pip
RUN pip3 install flask db-sqlite3 jwt 

COPY src /data
WORKDIR /data

RUN ["chmod", "+x", "/data/run.sh"]
ENTRYPOINT [ "/data/run.sh" ]


EXPOSE 5000 3000