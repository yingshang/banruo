# 般若安全中心

## 安装教程
**该系统环境是python3.6运行的，3.7会显示错误**
具体安装过程就不一一说明，下面直接dockerfile,假如没有fortify，只是用里面渗透测试系统，可以直接注释掉那段fortify的配置。在banruo目录下有一个config.json文件，里面有所有的配置，在生成docker的时候，把config.json复制出来，修改里面的内容。
`````
#dockerfile
FROM centos:7
COPY fortify_linux /opt/fortify_linux


RUN yum update -y
RUN yum install epel-release -y
RUN yum install -y  git wget python36 gcc python36-libs python36-tools python36-devel   zlib-devel rpm-build openssl-devel python redis

#fortify
RUN cd /opt && git clone https://github.com/yingshang/banruo.git
RUN cd /opt/banruo && pip3 install -r requirements.txt
RUN mkdir /data && mkdir /data/fortify && mkdir /data/fortify/report && chmod 777 /data -R
RUN chmod 777 -R /opt/fortify_linux/ && ln -s /opt/fortify_linux/bin/sourceanalyzer /usr/local/bin/sourceanalyzer && ln -s /opt/fortify_linux/bin/ReportGenerator /usr/local/bin/ReportGenerator

#sqlmap
RUN mkdir /opt/taskid
RUN cd /opt && git clone https://github.com/sqlmapproject/sqlmap
RUN ln -s /opt/sqlmap/sqlmapapi.py /usr/bin/sqlmapapi

#config.json
COPY config.json /opt/banruo/banruo/

#ENTRYPOINT redis-server & && cd /opt/ && python3 manage.py celery -A banruo worker  -l info --beat & && python3 manage.py runserver 0.0.0.0:8000

```
config.json

```
{
  "setting": {
    "MYSQL": {
      "MYSQL_HOST": "127.0.0.1",
      "MYSQL_PORT": "3306",
      "MYSQL_DATABASE": "banruo",
      "MYSQL_USER": "root",
      "MYSQL_PASSWORD": "123456"
    },
    "SQLMAP": {
      "SQLMAP_LIMIT_RUN": 15,
      "SQLMAP_DBMS": "",
      "SQLMAP_REQUESTFILE_PATH": "/opt/taskid/",
      "SQLMAP_VERBOSE": 1,
      "SQLMAP_PROXY": "",
      "SQLMAP_LEVEL": 5,
      "SQLMAP_RISK": 3,
      "SQLMAP_THREADS": 1,
      "SQLMAP_PARMEXCLUDE": "Host,User-Agent,Accept-Language,Referer,Cookie",
      "SQLMAP_PROXYFILE": "",
      "SQLMAP_RETRIES": 5,
      "SQLMAP_API_SERVER": [
        "http://127.0.0.1:55000",
        "http://127.0.0.1:55001",
        "http://127.0.0.1:55002",
        "http://127.0.0.1:55003"
      ]
    },
    "PROXY": {
      "PROXY_LISTEN_HOST": "0.0.0.0",
      "PROXY_LISTEN_PORT": 9999,
      "PROXY_LISTEN_MODE": "regular",
      "EXCLUDE_STATIC_FILE": [
        ".js",
        ".txt",
        ".mp3",
        ".css",
        ".jpg",
        ".png",
        ".gif",
        ".woff",
        ".ico",
        ".pdf",
        ".mp4"
      ]
    },
    "FORTIFY": {
      "fortify_path": "/data/fortify/",
      "report_path": "/data/fortify/report/",
      "filter_title": [
        "Injection",
        "Cross-Site Scripting"
      ]
    },
    "GITLAB": {
      "GIT_PATH": "/opt/git-list",
      "GIT_USERNAME": "admin@example.com",
      "GIT_PASSWORD": "abc123456",
      "GIT_API_CHOICE": 1,
      "GIT_ADDRESS": [],
      "GIT_PARM": "giturl"
    },
    "CHANDAO": {
      "OPENEDBY": 1,
      "PRODUCT_ID": 1,
      "CHAODAO_MYSQL_HOST": "192.168.1.210",
      "CHAODAO_MYSQL_USER": "root",
      "CHAODAO_MYSQL_PASSWORD": "123456",
      "CHAODAO_MYSQL_DATABASE": "zendao",
      "CHAODAO_MYSQL_PORT": 3306,
      "EMAIL_RECEIVERS": [
        "xxx@163.com"
      ]
    },
    "EMAIL": {
      "MAIL_HOST": "smtp.163.com",
      "MAIL_USER": "w@163.com",
      "MAIL_PASSWORD": ""
    }
  }
}
```
# 配置说明
- mysql配置（忽略）
- sqlmap配置
1. 1. SQLMAP_LIMIT_RUN，限制sqlmap跑的进程数
2. SQLMAP_REQUESTFILE_PATH：保存数据包的位置
3. SQLMAP_PARMEXCLUDE：排除的参数（level3以上）
4. SQLMAP_API_SERVER：连接sqlmapapi，需要多开，因为sqlmap多了之后，一个api服务器跑不动，会死掉

- 代理配置
1. EXCLUDE_STATIC_FILE：排除静态文件
- fortify配置
1. fortify_path：保存源码位置
2. report_path：保存报告的位置
3. filter_title：过滤高危的漏洞，比如sql注入，xss
- gitlab配置
1. git_api_choice：有两种选择，1，本地文件，里面都写了要扫描的github地址（推荐）; 2,接口模式，请求网站获取扫描地址。
2. git_address：网址列表
3. GIT_PARM：模式2，json参数,例如{"giturl":[1,2,3,4]}
- 禅道配置
创建人ID
1. OPENEDBY：创建人ID
2. PRODUCT_ID：项目的ID
3. EMAIL_RECEIVERS：接受禅道提醒的邮箱

- 邮箱配置