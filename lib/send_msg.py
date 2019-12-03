import pymysql
import datetime
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from .config_json import *

mail_host = MAIL_HOST
mail_user = MAIL_USER
mail_pass = MAIL_PASSWORD
sender = mail_user
chaodao_receivers = EMAIL_RECEIVERS  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱


def send_sqlmap_email():

    html = """
    {% load static %}
<!DOCTYPE html>
<html lang="en">


<head>
    <meta charset="UTF-8">
    <title>更新认证</title>
    <script type="text/javascript" src={% static "lib/layui/layui.js" %} charset="utf-8"></script>
</head>

<body>
<pre>test</pre>
</body>
</html>
    
    """
    subject = 'SQLzhuru'
    message = MIMEText(html, 'html', 'utf-8')
    message['Subject'] = Header(subject, 'utf-8')
    smtpObj = smtplib.SMTP()
    smtpObj.connect(mail_host, 25)  # 25 为 SMTP 端口号
    smtpObj.login(mail_user, mail_pass)
    smtpObj.sendmail(sender, sender, message.as_string())



def send_chandao_email():
    now_time = datetime.datetime.now()
    now_time = str(now_time.strftime('%Y-%m-%d'))
    sql = '''
    SELECT bb.project as project_id,bb.name,COUNT(*) as total,IFNULL(d.new,0) ,GROUP_CONCAT(bb.id)as bug_id_list from
    (SELECT a.id,c.name 
     ,a.project from zt_bug a
     LEFT JOIN zt_project c on a.project = c.id
     WHERE a.status = 'active' and a.product = '%s' and a.openedDate  > '%s' )bb
    LEFT JOIN(select a.id,c.name 
     ,a.project,count(1) as new from zt_bug a
     LEFT JOIN zt_project c on a.project = c.id
     WHERE a.status = 'active' and a.product = '%s' and a.openedDate  > '%s' GROUP BY a.project) as d on d.name = bb.name  
    group by bb.name
        ''' % (PRODUCT_ID,now_time,PRODUCT_ID, now_time)

    conn = pymysql.connect(host=CHANDAO_MYSQL_HOST, user=CHANDAO_MYSQL_USER, passwd=CHANDAO_MYSQL_PASSWORD, db=CHANDAO_MYSQL_DATABASE, port=CHANDAO_MYSQL_PORT,
                           charset="utf8")
    cursor = conn.cursor()
    cursor.execute(sql)
    results = cursor.fetchall()
    td = ''
    for row in results:
        contend = ''
        try:
            chandao_id = row[4].split(',')
            for id in chandao_id:
                contend = contend + u'''<a href='{0}/bug-view-{1}.html'>{2}  </a>
        '''.format(CHANDAO_ADDRESS,id, id)
        except AttributeError:
            pass
        td = td + u'''   
    <tr>
              <td style="background:#e8eaeb,text-align:center"><a href="http://192.168.1.210:8888/zentao/project-bug-%s.html">%s</a></td>
              <td style="text-align:center">%s</td>
              <td style="text-align:center">%s</td>
              <td>%s</td>
            </tr>
    ''' % (row[0], row[1], row[2], row[3], contend)
    sql = '''
    SELECT bb.product,bb.name,bb.total,IFNULL(d.new,0),GROUP_CONCAT(d.id)as bug_id_list 
    from  (select a.product,c.name,count(*) as total from zt_bug a
             LEFT JOIN zt_product c on a.product = c.id
            WHERE a.status = 'active' and a.openedBy = '1' and a.product != '3' 
            group by a.product,c.name)bb
    left join (SELECT a.id,a.product,c.name,count(1) as new from zt_bug a
           LEFT JOIN zt_product c on a.product = c.id
          WHERE a.status = 'active' and a.openedBy = '1' and a.product != '3' and a.openedDate  > '%s'
           group by   a.product,c.name
          ) as d  on d.`name` = bb.`name` and d.product = bb.product
    group by bb.name
        ''' % now_time
    cursor.execute(sql)
    results = cursor.fetchall()
    testtd = ''
    for row in results:
        contend = ''
        try:
            chandao_id = row[4].split(',')
            for id in chandao_id:
                contend = contend + u'''<a href='http://test.com/index.php?m=bug&f=view&bugID={0}'>{1}  </a>
        '''.format(id, id)
        except AttributeError:
            pass
        testtd = testtd + u'''   
    <tr>
              <td style="background:#e8eaeb,text-align:center"><a href="http://test.com/index.php?m=bug&f=browse&productID=%s">%s</a></td>
              <td style="text-align:center">%s</td>
              <td style="text-align:center">%s</td>
              <td>%s</td>
            </tr>
    ''' % (row[0], row[1], row[2], row[3], contend)
    html = u'''
    <html>
    <head>
    </head>
    <body>
    <table border="1">
    <h2>代码审计项目</h2>
    <tr>
    <th>git项目</th>
    <th>总数</th>
    <th>新增数</th>
    <th>禅道ID</th>
    </tr>
    ''' + td + u'''
    </table>
    </br>
    <h2>渗透测试项目</h2>
    <table border="1">
    <tr>
    <th>测试项目</th>
    <th>总数</th>
    <th>新增数</th>
    <th>禅道ID</th>
    </tr>
    ''' + testtd + u'''
    </table>
    </br>
    <b>注意：代码审计的结果是基于github项目进行审计，每个项目的负责人我已经在禅道上面指派了。</b></br>
    <b>还有就是漏洞误报的问题，审计的结果是正确的，但是无法进行攻击。例如：发现了一个SQL注入的漏洞，但是由于这个查询仅供内部查询调用，即黑客无法在外部找到这个漏洞</b></br>
    <b>如果发现是误报，可以直接选择关闭，当然，你也可以按照我的修复建议进行修复，加强代码质量。</b></br>
    <b>如果你已经修复的话，请告诉你在那个分支修复了，以便我重新检测。（代码审计系统默认拉取master分支）</b></br>
    <b>谢谢各位的合作！！！</b>
    </body>
    </html>
    '''

    subject = '每天禅道安全审计结果'
    message = MIMEText(html, 'html', 'utf-8')
    message['From'] = Header("安全审计", 'utf-8')
    message['Subject'] = Header(subject, 'utf-8')
    smtpObj = smtplib.SMTP()
    smtpObj.connect(mail_host, 25)  # 25 为 SMTP 端口号
    smtpObj.login(mail_user, mail_pass)
    smtpObj.sendmail(sender, chaodao_receivers, message.as_string())
