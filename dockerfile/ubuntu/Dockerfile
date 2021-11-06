FROM ubuntu:20.04

RUN apt update

WORKDIR /data

RUN apt-get install -y python3 python3-pip vim nano

COPY ./setup.sh /boot_scripts/setup.sh
COPY ./requirements.txt /boot_scripts/requirements.txt

RUN pip install -r /boot_scripts/requirements.txt

RUN chmod 755 /boot_scripts/setup.sh

CMD ["/bin/bash", "/boot_scripts/setup.sh"]