#配置文件
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


#SQLMAP的配置
SQLMAP_DBMS =  ""
SQLMAP_REQUESTFILE = os.path.join(BASE_DIR, 'taskid')
SQLMAP_LEVEL = 1
SQLMAP_RISK = 1
SQLMAP_API_SERVER = "http://127.0.0.1:8775"
#代理的配置
PROXY_LISTEN_PORT = 8888
PROXY_LISTEN_MODE = "regular"
PROXY_CACER_DIR = "./ssl/"
EXCLUDE_STATIC_FILE = ['.js', '.txt', '.mp3', '.css', '.jpg', '.png', '.gif', '.woff', '.ico', '.pdf', '.mp4']


#fortify的配置路径
fortify_path = "/data/fortify/"
report_path = "/data/fortify/report/"

#GitAPI配置,1为文档，2为web-api
git_username = 'admin@example.com'
git_password = 'abc123456'
git_api_choice = 1
git_api_adress = "http://127.0.0.1:8000/aduit/api_test"
parm = "gitlab_url"
git_filepath = "/opt/git-list"

#过滤fortify的高危漏洞到禅道数据表里面
filter_title = ['Injection', 'Cross-Site Scripting']

#发送禅道的设置，不使用禅道的接口，直接写入数据库
openedBy = '1' #创建人ID
product = '3' #项目的ID
MYSQL_HOST = '192.168.1.210'
MYSQL_USER = 'root'
MYSQL_PASSWORD = '123456'
MYSQL_DATABASE = 'zentao'
MYSQL_PORT = 3307

#邮件设置
MAIL_HOST = "smtp.163.com"
MAIL_USER = "xxx@163.com"
MAIL_PASSWORD = ""

