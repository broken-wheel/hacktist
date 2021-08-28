FROM ubuntu:16.04
RUN apt-get update && apt-get upgrade -y
RUN apt-get install build-essential automake libtool gawk texinfo -y
RUN apt-get install gcc-4.7 g++-4.7 libreadline5 libncurses5 libncurses5-dev -y
RUN mkdir -p /hackt/src
RUN mkdir -p /hackt/deps
COPY ./install_hackt.sh /usr/bin
