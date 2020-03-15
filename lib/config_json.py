from python_json_config import ConfigBuilder
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = BASE_DIR + '/banruo/config.json'


def save_config(**kwargs):
    builder = ConfigBuilder()
    config = builder.parse_config(CONFIG_PATH)
    for k in kwargs.keys():
        if kwargs[k] != None:
            for i in config.keys():
                if k in i:
                    config.update(i, kwargs[k])
    for i in config.keys():
        print(i.split('.')[-1])
    with open(CONFIG_PATH, "w") as f:
        f.write(config.to_json())
    #    print("加载入文件完成...")


def load_config(parm):
    builder = ConfigBuilder()
    global  config_parm
    config = builder.parse_config(CONFIG_PATH)
    for i in config.keys():
        if parm == i.split('.')[-1]:
            config_parm = config.get(i)
            break
    return config_parm

#fortify
fortify_path = load_config('fortify_path')
report_path = load_config('report_path')
filter_title = load_config('filter_title')


#MYSQL
MYSQL_HOST = load_config("MYSQL_HOST")
MYSQL_PORT = load_config("MYSQL_PORT")
MYSQL_DATABASE = load_config("MYSQL_DATABASE")
MYSQL_USER = load_config("MYSQL_USER")
MYSQL_PASSWORD = load_config("MYSQL_PASSWORD")



# SQLMAP
SQLMAP_LIMIT_RUN = load_config('SQLMAP_LIMIT_RUN')
SQLMAP_DBMS = load_config('SQLMAP_DBMS')
SQLMAP_PROXY = load_config('SQLMAP_PROXY')
SQLMAP_VERBOSE = load_config('SQLMAP_VERBOSE')
SQLMAP_REQUESTFILE_PATH = load_config('SQLMAP_REQUESTFILE_PATH')
SQLMAP_LEVEL = load_config('SQLMAP_LEVEL')
SQLMAP_RISK = load_config('SQLMAP_RISK')
SQLMAP_API_SERVER = load_config('SQLMAP_API_SERVER')
SQLMAP_PARMEXCLUDE = load_config('SQLMAP_PARMEXCLUDE')
SQLMAP_THREADS = load_config('SQLMAP_THREADS')
SQLMAP_RETRIES = load_config('SQLMAP_RETRIES')

# PROXY
PROXY_LISTEN_HOST = load_config('PROXY_LISTEN_HOST')
PROXY_LISTEN_PORT = load_config('PROXY_LISTEN_PORT')
PROXY_LISTEN_MODE = load_config('PROXY_LISTEN_MODE')
EXCLUDE_STATIC_FILE = load_config('EXCLUDE_STATIC_FILE')

#chaodao
OPENEDBY = load_config('OPENEDBY')
PRODUCT_ID = load_config('PRODUCT_ID')
CHANDAO_MYSQL_HOST = load_config('CHANDAO_MYSQL_HOST')
CHANDAO_MYSQL_USER = load_config('CHANDAO_MYSQL_USER')
CHANDAO_MYSQL_PASSWORD = load_config('CHANDAO_MYSQL_PASSWORD')
CHANDAO_MYSQL_DATABASE = load_config('CHANDAO_MYSQL_DATABASE')
CHANDAO_MYSQL_PORT = load_config('CHANDAO_MYSQL_PORT')
CHANDAO_ADDRESS = load_config("CHANDAO_ADDRESS")
EMAIL_RECEIVERS = load_config('EMAIL_RECEIVERS')

#email
MAIL_HOST = load_config('MAIL_HOST')
MAIL_USER = load_config('MAIL_USER')
MAIL_PASSWORD = load_config('MAIL_PASSWORD')

#GIT
GIT_PATH = load_config('GIT_PATH')
GIT_USERNAME = load_config('GIT_USERNAME')
GIT_PASSWORD = load_config('GIT_PASSWORD')
GIT_API_CHOICE = load_config('GIT_API_CHOICE')
GIT_ADDRESS = load_config('GIT_ADDRESS')
GIT_PARM = load_config("GIT_PARM")