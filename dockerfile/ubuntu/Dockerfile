FROM ubuntu:20.04

RUN apt update

WORKDIR /data

COPY ./setup.sh /boot_scripts/setup.sh

RUN chmod 755 /boot_scripts/setup.sh

CMD ["/bin/bash", "/boot_scripts/setup.sh"]