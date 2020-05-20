
FROM debian:latest

#Install sumo
RUN apt-get update 
RUN apt-get -y install sumo sumo-tools sumo-doc
ENV SUMO_HOME /usr/share/sumo
#Other tools
RUN apt-get -y install iceweasel wget

WORKDIR /root/sumo-examples

