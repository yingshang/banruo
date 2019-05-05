import requests
from threading import Thread


proxies = {
  'http': 'http://192.168.1.105:8888',
}

def get1():
    r = requests.get(url="http://192.168.1.105:8080/index.php?page=user-info.php&username=1&password=1&user-info-php-submit-button=View+Account+Details",
                     proxies=proxies
                     )
    print(len(r.text))



while True:

    ts1 = [Thread(target=get1) for i in range(1, 1000)]
    for t in ts1:
        t.start()
    for t in ts1:
        t.join()

