FROM ubuntu:20.04

RUN apt update

WORKDIR /data

RUN apt-get install -y python3 python3-pip

COPY ./setup.sh /boot_scripts/setup.sh

RUN chmod 755 /boot_scripts/setup.sh

CMD ["/bin/bash", "/boot_scripts/setup.sh"]