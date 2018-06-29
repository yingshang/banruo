FROM ubuntu:16.04

COPY run.sh /opt/run.sh
COPY sources.list /etc/apt/sources.list

COPY fortify_linux /opt/fortify_linux

ENV DEBIAN_FRONTEND noninteractive   
RUN chmod 777 /opt/run.sh
RUN apt-get update -y \
  && apt-get install -y mysql-server mysql-client libmysqlclient-dev --no-install-recommends \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
RUN apt-get update -y
RUN apt-get install -y redis-server  unzip python3-pip wget vim git libffi-dev libssl-dev  libjpeg8-dev zlib1g-dev libxml2-dev libxslt-dev libyaml-cpp-dev 
RUN pip3 install django
RUN pip3 install  mitmproxy==0.18.2 
RUN pip3 install django-celery redis pymysql
RUN pip3 install typing

RUN cd /opt && git clone https://github.com/yingshang/banruo.git
RUN service mysql start && mysql -e "create  database banruo DEFAULT CHARSET utf8 COLLATE utf8_general_ci; " && mysql -e "set password for 'root'@'localhost' =password('123456');"
RUN service mysql start &&  cd /opt/banruo && python3 manage.py makemigrations && python3 manage.py migrate
RUN mkdir /data && mkdir /data/fortify && mkdir /data/fortify/report && chmod 777 /data -R
#这个是fortify的运行程序
#RUN chmod 777 -R /opt/fortify_linux/ && ln -s /opt/fortify_linux/bin/sourceanalyzer /usr/local/bin/sourceanalyzer && ln -s /opt/fortify_linux/bin/ReportGenerator /usr/local/bin/ReportGenerator
EXPOSE 8000

ENTRYPOINT /opt/run.sh

