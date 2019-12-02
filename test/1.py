import json

data = '''POST http://192.168.1.105/index.php?tok2en=asdas&1token=SUD1 HTTP/1.1
Host:192.168.1.105
User-Agent:Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:66.0) Gecko/20100101 Firefox/66.0
Accept:text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language:en-US,en;q=0.5
Accept-Encoding:gzip, deflate
Referer:http://192.168.1.105/set-up-database.php
Connection:keep-alive
Cookie:12312312
Upgrade-Insecure-Requests:1


{"token":"home.php","id":1}'''


def is_json(value):
    try:
        json_object = json.loads(value)
    except ValueError:
        return "normal"
    return "json"


new_data = ""
status = is_json(data.split('\n')[-1])
method = data.split('\n')[0].split(' ')[0]
url = data.split('\n')[0].split(' ')[1]
if method == "GET":
    keys = url.split('?')[-1].split('&')
    for i in keys:
        if i.split('=')[0] == parm:
            value = i.split('=')[-1]
            new_data = data.replace(value, modify)
            break
elif method == 'POST':
    keys = url.split('?')[-1].split('&')
    for i in keys:
        if i.split('=')[0] == parm:
            value = i.split('=')[-1]
            t = 1
            break
        else:
            t = 0

    if t == 0:
        # token=asdasdas&id=1
        if status == "normal":
            values = data.split('\n')[-1].split('&')
            for i in values:
                if parm == i.split('=')[0]:
                    new_data = data.replace(i.split('=')[-1], modify)
                    break

        # {"token":"asdasdas","id":1}
        elif status == "json":
            json_data = json.loads(data.split('\n')[-1])
            for i in json_data:
                if parm == i:
                    new_data = data.replace(json_data[i],modify)
                    print(new_data)
                    break
    elif t == 1:
        new_data = data.replace(value, modify)
