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
    config = builder.parse_config(CONFIG_PATH)
    for i in config.keys():
        if parm == i.split('.')[-1]:
            record = config.get(i)
            break
    return record


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
PROXY_CACER_DIR = load_config('PROXY_CACER_DIR')
EXCLUDE_STATIC_FILE = load_config('EXCLUDE_STATIC_FILE')

#chaodao
OPENEDBY = load_config('OPENEDBY')
PRODUCT_ID = load_config('PRODUCT_ID')
CHAODAO_MYSQL_HOST = load_config('CHAODAO_MYSQL_HOST')
CHAODAO_MYSQL_USER = load_config('CHAODAO_MYSQL_USER')
CHAODAO_MYSQL_PASSWORD = load_config('CHAODAO_MYSQL_PASSWORD')
CHAODAO_MYSQL_DATABASE = load_config('CHAODAO_MYSQL_DATABASE')
CHAODAO_MYSQL_PORT = load_config('CHAODAO_MYSQL_PORT')
EMAIL_RECEIVERS = load_config('EMAIL_RECEIVERS')

#email
MAIL_HOST = load_config('MAIL_HOST')
MAIL_USER = load_config('MAIL_USER')
MAIL_PASSWORD = load_config('MAIL_PASSWORD')
