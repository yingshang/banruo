FROM centos:7
COPY fortify_linux /opt/fortify_linux


RUN yum update -y
RUN yum install epel-release -y
RUN yum install -y  git wget python36 gcc python36-libs python36-tools python36-devel   zlib-devel rpm-build openssl-devel python redis


#config.json
COPY config.json /opt/banruo/banruo/

#django
RUN cd /opt && git clone https://github.com/yingshang/banruo.git
RUN cd /opt/banruo && pip3 install -r requirements.txt
RUN cd /opt/banruo && python3 manage.py makemigrations && python3 manage.py migrate

#这个是fortify的运行程序
RUN mkdir /data && mkdir /data/fortify && mkdir /data/fortify/report && chmod 777 /data -R
RUN chmod 777 -R /opt/fortify_linux/ && ln -s /opt/fortify_linux/bin/sourceanalyzer /usr/local/bin/sourceanalyzer && ln -s /opt/fortify_linux/bin/ReportGenerator /usr/local/bin/ReportGenerator

#sqlmap
RUN mkdir /opt/taskid
RUN cd /opt && git clone https://github.com/sqlmapproject/sqlmap
RUN ln -s /opt/sqlmap/sqlmapapi.py /usr/bin/sqlmapapi &&  ln -s /opt/sqlmap/sqlmap.py /usr/bin/sqlmap




COPY run.sh /opt/run.sh
RUN chmod +x /opt/run.sh

ENTRYPOINT /opt/run.sh