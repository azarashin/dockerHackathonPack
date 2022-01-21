FROM ubuntu:20.04

RUN apt update

WORKDIR /data

RUN apt install -y python3 python3-pip vim nano \
	mysql-client libmysqlclient-dev \
	cron systemctl

COPY ./setup.sh /boot_scripts/setup.sh
COPY ./requirements.txt /boot_scripts/requirements.txt
COPY ./daily_task.sh /boot_scripts/daily_task.sh

# https://qiita.com/iganari/items/5a61ec93d989f7c77a2c
COPY ./crontabs_root.txt /var/spool/cron/crontabs/root

COPY ./preseed.txt /boot_scripts/preseed.txt
RUN debconf-set-selections /boot_scripts/preseed.txt

RUN pip install -r /boot_scripts/requirements.txt

RUN chmod 755 /boot_scripts/setup.sh /boot_scripts/daily_task.sh

RUN chmod 600 /var/spool/cron/crontabs/root
RUN chown root.crontab /var/spool/cron/crontabs/root

CMD ["/bin/bash", "/boot_scripts/setup.sh"]
