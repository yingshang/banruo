# coding: utf-8
def information(title):
    infos = [
        {
        'vul_title':'SQL Injection',
        'describe':'''SQL注入就是通过把SQL命令插入到Web表单递交或输入域名或页面请求的查询字符串，最终达到欺骗服务器执行恶意的SQL命令。
具体来说，它是利用现有应用程序，将（恶意）的SQL命令注入到后台数据库引擎执行的能力，它可以通过在Web表单中输入（恶意）SQL语句得到一个存在安全漏洞的网站上的数据库，而不是按照设计者意图去执行SQL语句。''',
        'Recommendation':'''参数化查询是指在设计与数据库链接并访问数据时，在需要填入数值或数据的地方，使用参数来给值，这个方法目前已被视为最有效可预防SQL注入攻击的攻击手法的防御方式。
在使用参数化查询的情况下，数据库服务器不会将参数的内容视为SQL指令的一部份来处理，而是在数据库完成 SQL 指令的编译后，才套用参数运行，因此就算参数中含有恶意的指令，由于已经编译完成，就不会被数据库所运行。
有部份的开发人员可能会认为使用参数化查询，会让程序更不好维护，或者在实现部份功能上会非常不便，然而，使用参数化查询造成的额外开发成本，通常都远低于因为SQL注入攻击漏洞被发现而遭受攻击，所造成的重大损失。
        ''',
    },
        {
            'vul_title': 'Cross-Site Scripting: Reflected',
            'describe': '''
跨站脚本（XSS）漏洞发生在以下情况：
1.数据通过不受信任的来源进入Web应用程序。在反射XSS的情况下，不受信任的源通常是Web请求，而在Persisted（也称为Stored）XSS的情况下，它通常是数据库或其他后端数据存储。
2.数据包含在动态内容中，发送给Web用户，而不会对恶意代码进行验证。
发送到Web浏览器的恶意内容通常采用一段JavaScript的形式，但也可能包括HTML，Flash或浏览器可能执行的任何其他类型的代码。基于XSS的各种攻击几乎是无限的，但它们通常包括向攻击者传送私有数据（如Cookie或其他会话信息），将受害者重定向到受攻击者控制的Web内容，或在用户机器下执行其他恶意操作伪劣的脆弱网站。
示例1：以下JSP代码段从HTTP请求中读取员工ID,eid，并将其显示给用户。
<％String eid = request.getParameter（“eid”）; ％>
...
员工ID：<％= eid％>
如果eid仅包含标准字母数字文本，则此示例中的代码将正确运行。如果eid具有包含元字符或源代码的值，那么代码将在Web浏览器显示HTTP响应时执行。
最初这可能不是一个很大的漏洞。毕竟，为什么有人会输入一个导致恶意代码在自己的电脑上运行的URL？真正的危险是攻击者会创建恶意URL，然后使用电子邮件或社交工具技巧来诱骗受害者访问URL的链接。当受害者点击链接时，他们无意中将恶意内容通过易受攻击的Web应用程序反映回自己的计算机。这种利用易受攻击的Web应用程序的机制被称为反射XSS。
示例2：以下JSP代码段为具有给定ID的员工查询数据库，并打印相应的员工姓名。
<%... 
Statement stmt = conn.createStatement();
ResultSet rs = stmt.executeQuery("select * from emp where id="+eid);
if (rs != null) {
   rs.next();
   String name = rs.getString("name");
}
%>
Employee Name: <%= name %>
与示例1一样，当代码的值很好的时候，这个代码可以正常工作，但是如果没有这个名称，它就没有什么可以防止漏洞利用。同样，这个代码看起来不太危险，因为从数据库中读取名称的值，该数据库的内容显然由应用程序管理。但是，如果名称的值源自用户提供的数据，则数据库可能是恶意内容的通道。没有对存储在数据库中的所有数据进行适当的输入验证，攻击者可以在用户的​​Web浏览器中执行恶意命令。被称为持久（或存储）XSS的这种类型的漏洞尤其阴险，因为数据存储引起的间接使得识别威胁更加困难，并增加了攻击将影响多个用户的可能性。 XSS以这种形式开始，网站向访客提供了一个“留言簿”。攻击者将在其留言簿条目中包含JavaScript，并且访客留言页面的所有后续访问者都将执行恶意代码。
如示例所示，XSS漏洞是由HTTP响应中包含未验证数据的代码引起的。 XSS攻击有三个向量可以到达受害者：
- 与示例1一样，直接从HTTP请求中读取数据，并反映在HTTP响应中。当攻击者导致用户向易受攻击的Web应用程序提供危险内容时，会发生反映的XSS漏洞利用，然后将其反映回用户并由Web浏览器执行。传递恶意内容的最常见的机制是将其作为一个参数，将其公开发布或直接发送给受害者。以这种方式构建的URL构成了许多网络钓鱼方案的核心，攻击者说服受害者访问指向易受攻击的站点的URL。在站点将攻击者的内容反映给用户之后，执行内容并继续将诸如可以包括会话信息的cookie的私人信息从用户机器传送到攻击者或执行其他恶意活动。
- 与示例2一样，应用程序将危险数据存储在数据库或其他可信数据存储中。危险数据随后被读回应用程序并包含在动态内容中。持续的XSS漏洞发生在攻击者将危险内容注入到随后读取并包含在动态内容中的数据存储中时。从攻击者的角度来看，
''',
'Recommendation': '''
1. 自己写 filter 拦截来实现，但要注意的时，在WEB.XML 中配置 filter 的时候，请将这个 filter 放在第一位.
2. 采用开源的实现 ESAPI library ，参考网址: https://www.owasp.org/index.php/Category:OWASP_Enterprise_Security_API
3. 可以采用spring 里面提供的工具类来实现.
该方法来自：http://blog.csdn.net/liaozhongping/article/details/48649389
''',
        },
        {
            'vul_title': 'SQL Injection: MyBatis Mapper',
            'describe': '''SQL注入错误发生在：
1.数据从不受信任的来源进入程序。
2.数据用于动态构建SQL查询。
MyBatis Mapper XML文件允许您在SQL语句中指定动态参数，通常使用＃个字符定义，如下所示：
    <select id="getItems" parameterType="domain.company.MyParamClass" resultType="MyResultMap">
        SELECT *
        FROM items
        WHERE owner = #{userName}
    </select>
带有大括号的＃字符表示变量名称表示MyBatis将使用userName变量创建参数化查询。 但是，MyBatis还允许您使用$字符将变量直接连接到SQL语句，为SQL注入打开了攻击口。
示例1：以下代码动态构建并执行搜索与指定名称匹配的项的SQL查询。 该查询限制显示给所有者与当前验证的用户的用户名匹配的项目。
    <select id="getItems" parameterType="domain.company.MyParamClass" resultType="MyResultMap">
        SELECT *
        FROM items
        WHERE owner = #{userName}
        AND itemname = ${itemName}
    </select>
但是，由于查询是通过连接常量基本查询字符串和用户输入字符串动态构建的，所以如果itemName不包含单引号字符，则查询只能正确执行。 如果用户名为wiley的攻击者为itemName输入字符串“name”OR'a'='a“，则查询将成为以下内容：
SELECT * FROM items
    WHERE owner = 'wiley'
    AND itemname = 'name' OR 'a'='a';
OR'a'='a'条件的添加会导致WHERE子句始终为true，因此该查询在逻辑上等同于更简单的查询：SELECT * FROM items;
这种查询的简化允许攻击者绕过查询只应返回被认证的用户拥有的条目的要求。 查询现在返回存储在items表中的所有条目，而不管其指定的所有者如何。
示例2：此示例检查传递给示例1中构造和执行的查询的不同恶意值的影响。如果具有用户名wiley的攻击者输入字符串“name”; DELETE FROM items;“”for itemName，则 该查询成为以下两个查询：
 SELECT * FROM items
    WHERE owner = 'wiley'
    AND itemname = 'name';
    DELETE FROM items;
    --'
''',
            'Recommendation': '使用参数化查询',
        },
        {
            'vul_title': 'Access Control: Database',
            'describe': '''数据库访问控制错误发生在：
1、数据从不受信任的来源输入程序。
2、数据用于指定SQL查询中主键的值。
示例1：以下代码使用参数化语句，它转义元字符并防止SQL注入漏洞，构造并执行搜索与指定标识符匹配的发票的SQL查询。 从与当前认证的用户相关联的所有发票的列表中选择标识符。
...
id = Integer.decode(request.getParameter("invoiceID"));
String query = "SELECT * FROM invoices WHERE id = ?";
PreparedStatement stmt = conn.prepareStatement(query);
stmt.setInt(1, id);
ResultSet results = stmt.execute();
...
问题是开发人员未能考虑所有可能的id值。 虽然界面生成属于当前用户的发票标识符列表，但攻击者可能会绕过此界面以请求任何所需的发票。 由于本示例中的代码不检查以确保用户有权访问所请求的发票，所以它将显示任何发票，即使它不属于当前用户。
有些人认为，在移动世界中，传统的Web应用漏洞（如数据库访问控制错误）没有意义 - 用户为什么会攻击自己？ 但是，请记住，移动平台的本质是从各种源下载并在同一设备上并行运行的应用程序。 在银行应用程序旁边运行一个恶意软件的可能性很大，这需要扩展移动应用程序的攻击面，以包括进程间通信。
示例2：以下代码将示例1适配到Android平台:
...
        String id = this.getIntent().getExtras().getString("invoiceID");
        String query = "SELECT * FROM invoices WHERE id = ?";
        SQLiteDatabase db = this.openOrCreateDatabase("DB", MODE_PRIVATE, null);
        Cursor c = db.rawQuery(query, new Object[]{id});
...
''',
            'Recommendation': '''访问控制应该由应用程序和数据库层来处理，而不是依赖于表示层来限制用户提交的值。 在任何情况下，不允许用户在没有适当权限的情况下检索或修改数据库中的一行。 访问数据库的每个查询都应该强制执行此策略，这通常可以通过简单地将当前身份验证的用户名作为查询的一部分来实现。
示例3：以下代码实现与示例1相同的功能，但强加了一个附加约束，要求当前验证的用户具有对发票的具体访问权限。
...
userName = ctx.getAuthenticatedUserName();
id = Integer.decode(request.getParameter("invoiceID"));
String query ="SELECT * FROM invoices WHERE id = ? AND user = ?";
PreparedStatement stmt = conn.prepareStatement(query);
stmt.setInt(1, id);
stmt.setString(2, userName);
ResultSet results = stmt.execute();
...
安卓的查询代码
...
        PasswordAuthentication pa = authenticator.getPasswordAuthentication();
        String userName = pa.getUserName();
        String id = this.getIntent().getExtras().getString("invoiceID");
        String query = "SELECT * FROM invoices WHERE id = ? AND user = ?";
        SQLiteDatabase db = this.openOrCreateDatabase("DB", MODE_PRIVATE, null);
        Cursor c = db.rawQuery(query, new Object[]{id, userName});
...
''',
        },
        {
            'vul_title': 'Access Specifier Manipulation',
            'describe': '''
AccessibleObject API允许程序员绕过由Java访问说明符提供的访问控制检查。 特别地，它使程序员能够允许反射对象绕过Java访问控制，反过来改变私有域的值或调用私有方法，通常不允许的行为。''',
            'Recommendation': '''
访问说明符只能通过私有类的参数进行修改，这样攻击者就不能设置''',
        },
        {
            'vul_title': 'Unreleased Resource: Streams',
            'describe': '''
该程序可能无法释放系统资源。
资源泄漏至少有两个常见原因：
- 错误条件和其他特殊情况。
- 混淆程序的哪一部分负责释放资源。
大多数未发布的资源问题导致一般的软件可靠性问题，但是如果攻击者可以有意触发资源泄漏，则攻击者可能会通过耗尽资源池来启动拒绝服务攻击。
示例：以下方法从不关闭其打开的文件句柄。 FileInputStream的finalize（）方法最终会调用close（），但是不能保证在finalize（）方法被调用之前要花费多长时间。 在繁忙的环境中，这可能会导致JVM使用其所有文件句柄。
private void processFile(String fName) throws FileNotFoundException, IOException {
  FileInputStream fis = new FileInputStream(fName);
  int sz;
  byte[] byteArray = new byte[BLOCK_SIZE];
  while ((sz = fis.read(byteArray)) != -1) {
    processBytes(byteArray, sz);
  }
}
''',
            'Recommendation': '''
1.不要依赖finalize（）来回收资源。 为了调用对象的finalize（）方法，垃圾收集器必须确定该对象有资格进行垃圾回收。 因为垃圾收集器不需要运行，除非JVM内存不足，否则不能保证以方便的方式调用对象的finalize（）方法。 当垃圾收集器最终运行时，可能会导致大量资源在短时间内回收，这可能导致“突发”性能并降低整体系统吞吐量。 当系统负载增加时，这种效果变得更加显着。
最后，如果资源回收操作有可能挂起（例如，如果需要通过网络通信到数据库），则执行finalize（）方法的线程将挂起。
2.在最后的块中释放资源。 示例的代码应重写如下：
public void processFile(String fName) throws FileNotFoundException, IOException {
  FileInputStream fis;
  try {
    fis = new FileInputStream(fName);
    int sz;
    byte[] byteArray = new byte[BLOCK_SIZE];
    while ((sz = fis.read(byteArray)) != -1) {
      processBytes(byteArray, sz);
    }
  }
  finally {
    if (fis != null) {
      safeClose(fis);
    }
  }
}

public static void safeClose(FileInputStream fis) {
  if (fis != null) {
    try {
      fis.close();
    } catch (IOException e) {
      log(e);
    }
  }
}
此解决方案使用帮助函数来记录尝试关闭流可能发生的异常。 大概这个帮助函数将被重用，只要流需要关闭。
此外，processFile方法不会将fis对象初始化为null。 相反，它会检查以确保在调用safeClose（）之前fis不为空。 没有空检查，Java编译器报告fis可能没有被初始化。 这种选择充分利用了Java检测未初始化变量的能力。 如果fis在更复杂的方法中初始化为null，那么在不初始化的情况下使用fis的情况将不会被编译器检测到。
''',
        },
        {
            'vul_title': 'Unreleased Resource: Database',
            'describe': '''
该程序可能无法释放数据库资源。
资源泄漏至少有两个常见原因：
- 错误条件和其他特殊情况。
- 混淆程序的哪一部分负责释放资源。
大多数未发布的资源问题导致一般的软件可靠性问题，但是如果攻击者可以有意触发资源泄漏，则攻击者可能会通过耗尽资源池来启动拒绝服务攻击。
示例：在正常情况下，以下代码执行数据库查询，处理数据库返回的结果，并关闭已分配的语句对象。 但是，如果在执行SQL或处理结果时发生异常，则语句对象将不会被关闭。 如果这种情况经常发生，数据库将会耗尽可用的游标，而不能执行任何更多的SQL查询。
  Statement stmt = conn.createStatement();
  ResultSet rs = stmt.executeQuery(CXN_SQL);
  harvestResults(rs);
  stmt.close();
在这种情况下，存在不释放Statement的程序路径。
''',
            'Recommendation': '''
1.不要依赖finalize（）来回收资源。 为了调用对象的finalize（）方法，垃圾收集器必须确定该对象有资格进行垃圾回收。 因为垃圾收集器不需要运行，除非JVM内存不足，否则不能保证以方便的方式调用对象的finalize（）方法。 当垃圾收集器最终运行时，可能会导致大量资源在短时间内回收，这可能导致“突发”性能并降低整体系统吞吐量。 当系统负载增加时，这种效果变得更加显着。
最后，如果资源回收操作有可能挂起（例如，如果需要通过网络通信到数据库），则执行finalize（）方法的线程将挂起。
2.在最后的块中释放资源。 示例的代码应重写如下：
public void execCxnSql(Connection conn) {
    Statement stmt;
    try {
      stmt = conn.createStatement();
      ResultSet rs = stmt.executeQuery(CXN_SQL);
      ...
    }
    finally {
      if (stmt != null) {
        safeClose(stmt);
      }
    }
}

public static void safeClose(Statement stmt) {
  if (stmt != null) {
    try {
      stmt.close();
    } catch (SQLException e) {
      log(e);
    }
  }
}
此解决方案使用助手函数记录试图关闭语句时可能出现的异常。当语句需要关闭时，这个辅助函数将被重用。
同时，这个execCxnSql方法不能初始化stmt对象为空。相反，它检查以确保在调用safeclose()声明是无效的。没有null检查，java编译器报告stmt没有被初始化。这个选择是利用java的能力来检测未初始化的变量。如果为初始化为零的一个更复杂的方法，其中用地未经初始化不会被编译器检测到的。
''',
        },
        {
            'vul_title': 'Portability Flaw: Locale Dependent Comparison',
            'describe': '''
当比较可能与区域设置相关的数据时，应指定适当的区域设置。
示例1：以下示例尝试执行验证以确定用户输入是否包含<script>标记。
  ...
  public String tagProcessor(String tag){
    if (tag.toUpperCase().equals("SCRIPT")){
      return null;
    }
    //does not contain SCRIPT tag, keep processing input
    ...
  }
  ...
上述代码的问题是java.lang.String.toUpperCase（）在不带语言环境的情况下使用默认语言环境的规则。 使用土耳其语locale“title”.toUpperCase（）返回“T \ u0130TLE”，其中“\ u0130”是“我的上一个字母大写字母”。 这可能会导致意想不到的结果，例如在示例1中，这将阻止“验证”一词被该验证所捕获，这可能导致跨站点脚本漏洞。
''',
            'Recommendation': '''
要防止发生这种情况，请始终确保指定默认语言环境，或者使用接受它们的API（如toUpperCase（））指定语言环境。
示例2：以下将手动指定为toUpperCase（）的参数。
import java.util.Locale;
  ...
  public String tagProcessor(String tag){
    if (tag.toUpperCase(Locale.ENGLISH).equals("SCRIPT")){
      return null;
    }
    //does not contain SCRIPT tag, keep processing input
    ...
  }
  ...
示例3：以下使用java.lang.String.equalsIgnoreCase（）API函数来防止此问题。
 ...
  public String tagProcessor(String tag){
    if (tag.equalsIgnoreCase("SCRIPT")){
      return null;
    }
    //does not contain SCRIPT tag, keep processing input
    ...
  }
  ...
这样可以防止问题的发生，因为equalsIgnoreCase（）会改变与Character.toLowerCase（）和Character.toUpperCase（）类似的情况。 这涉及使用来自Unicode数据文件（由Unicode Consortium维护的Unicode字符数据库的一部分）的信息创建两个字符串的临时规范形式，即使这可能会导致它们读取不可读，也可以在没有 依赖于语言环境。
''',
        },
        {
            'vul_title': 'Often Misused: Boolean.getBoolean()',
            'describe': '''
在大多数情况下，对Boolean.getBoolean（）的调用经常被误用，因为它假定返回由指定的字符串参数表示的布尔值。 但是，如Javadoc Boolean.getBoolean（String）方法中所述“当且仅当由参数命名的系统属性存在且等于字符串”true“时返回true。
大多数开发人员打算使用的是调用Boolean.valueOf（String）或Boolean.parseBoolean（String）方法。
示例1：以下代码将不会按预期方式运行。 它将打印“FALSE”为Boolean.getBoolean（String）不会转换String原语。 它只能翻译系统属性。
 ...
 String isValid = "true";
 if ( Boolean.getBoolean(isValid) ) {
     System.out.println("TRUE");
 }
 else {
     System.out.println("FALSE");
 }
 ...

''',
            'Recommendation': '''
请确保您打算调用Boolean.getBoolean（String）方法，并且指定的字符串参数是系统属性。 否则，您最有可能寻找的方法调用是Boolean.valueOf（String）或Boolean.parseBoolean（String）。
''',
        },
        {
            'vul_title': 'Often Misused: Authentication',
            'describe': '''
许多DNS服务器易受欺骗攻击，因此您应该假定您的软件有一天会在受到破坏的DNS服务器的环境中运行。 如果允许攻击者进行DNS更新（有时称为DNS缓存中毒），则可以将网络流量路由到其机器，或者使其看起来好像其IP地址是您的域的一部分。 不要将系统的安全性置于DNS名称上。
示例：以下代码使用DNS查找来确定入站请求是否来自可信主机。 如果攻击者可以中毒DNS缓存，则可以获得可信任的状态。
 String ip = request.getRemoteAddr();
 InetAddress addr = InetAddress.getByName(ip);
 if (addr.getCanonicalHostName().endsWith("trustme.com")) {
 trusted = true;
 }
 IP地址比DNS名称更可靠，但也可能被欺骗。 攻击者可能会轻易伪造其发送的数据包的源IP地址，但响应数据包将返回伪造的IP地址。 要查看响应数据包，攻击者必须嗅探受害者机器和伪造的IP地址之间的流量。 为了完成所需的嗅探，攻击者通常会尝试将自己定位在与受害机器相同的子网上。 攻击者可以通过使用源路由来规避这一要求，但是源路由在当今的大部分互联网上被禁用。 总而言之，IP地址验证可以是认证方案的有用部分，但不应该是验证所需的单一因素。
''',
            'Recommendation': '''
如果您检查确保主机的前向和后向DNS条目匹配，您可以增加对域名查找的信心。攻击者将不能在不控制目标域的名称服务器的情况下欺骗正向和反向DNS条目。这不是一个愚蠢的方法：攻击者可能能够说服域名注册商将域名转换为恶意的域名服务器。基于DNS条目的身份认证只是一个冒险的命题。
虽然没有认证机制是万无一失的，但是有比基于主机的身份验证更好的选择。密码系统提供体面的安全性，但容易受到密码错误选择，密码传输不安全以及密码管理的影响。像SSL这样的加密方案是值得考虑的，但是这样的方案往往是非常复杂的，它们带来了重大实施错误的风险，而且关键的材料总是被偷走。在许多情况下，包括物理令牌的多因素身份验证提供了最合理的安全保障。
''',
        },
        {
            'vul_title': 'Null Dereference',
            'describe': '''
当一个或多个程序员的假设被违反时，通常会发生空指针异常。 当程序明确地将对象设置为null并在以后解除引用时，会发生解除引用存储后错误。 该错误通常是程序员在声明时将变量初始化为null的结果。
大多数空指针问题导致一般的软件可靠性问题，但是如果攻击者可以有意触发空指针解引用，则可以使用所产生的异常来绕过安全逻辑，或者使应用程序显示在规划后续攻击中有价值的调试信息。
示例：在下面的代码中，程序员显式地将变量foo设置为null。 之后，程序员在检查对象之前取消引用空值。
Foo foo = null;
...
foo.setBar(val);
...
}
''',
            'Recommendation': '''
在取消引用可能为null的对象之前，请仔细检查。 在可能的情况下，抽象的空值会检查代码中的包装器，以便操作资源，以确保在所有情况下应用它们，并尽可能减少出现错误的地方。    
    ''',
        },
        {
            'vul_title': 'Denial of Service: Regular Expression',
            'describe': '''
正则表达式求值程序和相关方法的实现中存在一个漏洞，当评估嵌套和重复正则表达式组的重复和交替重叠时，可能导致线程挂起。 此缺陷可用于执行拒绝服务（DoS）攻击。
例：
        (e+)+
        ([a-zA-Z]+)*
没有已知的正常表达式实现可以免受此漏洞的影响。 所有的平台和语言都容易受到这种攻击。
''',
            'Recommendation': '''
不允许不可信数据用作正则表达式模式。
''',
        },
        {
            'vul_title': 'Unchecked Return Value',
            'describe': '''
Java程序员误解read（）和许多java.io类的一部分的相关方法并不罕见。 Java中的大多数错误和异常事件导致抛出异常。 （这是Java对C语言的优点之一：异常使程序员更容易考虑可能出错的情况）但是，如果只有少量的数据，流和阅读器类不会被认为是异常或异常的 变得可用。 这些类只需将少量数据添加到返回缓冲区，并将返回值设置为读取的字节数或字符数。 不保证返回的数据量等于所请求的数据量。
这种行为使程序员重要的是从read（）和其他IO方法检查返回值，以确保他们收到他们期望的数据量。
示例：以下代码循环遍历一组用户，为每位用户读取私人数据文件。 程序员假定这些文件的大小始终都是1千字节，因此忽略了read（）的返回值。 如果攻击者可以创建一个较小的文件，该程序将回收前一个用户的其余数据，并将其处理为它属于攻击者。
FileInputStream fis;
byte[] byteArray = new byte[1024];
for (Iterator i=users.iterator(); i.hasNext();) {
    String userName = (String) i.next();
    String pFileName = PFILE_ROOT + "/" + userName;
    FileInputStream fis = new FileInputStream(pFileName);
    fis.read(byteArray); // the file is always 1k bytes
    fis.close();
    processPFile(userName, byteArray);
}
''',
            'Recommendation': '''
  FileInputStream fis;
  byte[] byteArray = new byte[1024];
  for (Iterator i=users.iterator(); i.hasNext();) {
    String userName = (String) i.next();
    String pFileName = PFILE_ROOT + "/" + userName;
    fis = new FileInputStream(pFileName);
    int bRead = 0;
    while (bRead < 1024) {
        int rd = fis.read(byteArray, bRead, 1024 - bRead);
        if (rd == -1) {
          throw new IOException("file is unusually small");
        }
        bRead += rd;
    }
    // could add check to see if file is too large here
    fis.close();
    processPFile(userName, byteArray);
  }
注意：由于此问题的修复相对复杂，您可能会尝试使用更简单的方法，例如在开始阅读之前检查文件的大小。 这种方法会使应用程序容易受到文件系统竞争条件的攻击，从而攻击者可以在文件大小检查和从文件读取数据的调用之间用恶意文件替换格式良好的文件。
''',
        },
        {
            'vul_title': 'Dead Code: Unused Method',
            'describe': '''
这个方法从来没有被调用过，也只能从其他死码中调用。
示例1：在下面的类中，doWork（）方法永远不能被调用。
public class Dead {
  private void doWork() {
    System.out.println("doing work");
  }
  public static void main(String[] args) {
    System.out.println("running Dead");
  }
}
示例2：在下面的类中，两个私有方法相互调用，但由于任何一个都不会被调用，所以它们都是死代码。
public class DoubleDead {
  private void doTweedledee() {
    doTweedledumb();
  }
  private void doTweedledumb() {
    doTweedledee();
  }
  public static void main(String[] args) {
    System.out.println("running DoubleDead");
  }
}
''',
            'Recommendation': '''
示例3：如果方法在包含以下分派方法的类中标记为死命名为getWitch（），则可能是由于复制和粘贴错误。 'w'case应该返回getWitch（）不是getMummy（）。
public ScaryThing getScaryThing(char st) {
  switch(st) {
    case 'm':
      return getMummy();
    case 'w':
      return getMummy();
    default:
      return getBlob();
  }
}
一般来说，您应该修复或删除死码。 要修复死码，请通过公共方法直接或间接执行死码。 死码导致额外的复杂性和维护负担，而不会对程序的功能做出贡献。
''',
        },
        {
            'vul_title': 'J2EE Bad Practices: getConnection() ',
            'describe': '''
J2EE标准要求应用程序使用容器的资源管理工具来获取与资源的连接。
例如，J2EE应用程序应获取数据库连接，如下所示：
ctx = new InitialContext();
datasource = (DataSource)ctx.lookup(DB_DATASRC_REF);
conn = datasource.getConnection();
并且应该避免以这种方式获得连接：
conn = DriverManager.getConnection(CONNECT_STRING);
每个主要的Web应用程序容器提供池化的数据库连接管理作为其资源管理框架的一部分。 在应用程序中复制此功能是困难和容易出错的，这是J2EE标准下禁止的一部分原因。
''',
            'Recommendation': '''
使用适当的连接工厂的JNDI查找替换对DriverManager.getConnection（）的直接调用，并从连接工厂获取连接。
''',
        },
        {
            'vul_title': 'Code Correctness: Class Does Not Implement equals',
            'describe': '''
在比较对象时，开发人员通常希望比较对象的属性。然而，在一个类调用equals()（或任何超类/接口），没有明确的实施equals()导致调用继承java.lang.Object的equals()方法。而不是比较的对象的成员字段或其他性质的对象。equals()比较两个对象实例是否相同。虽然有对象的合法使用。equals()，它往往是错误的代码指示。
例子1：
public class AccountGroup
{
	private int gid;

	public int getGid()
	{
		return gid;
	}

	public void setGid(int newGid)
	{
		gid = newGid;
	}
}
...
public class CompareGroup
{
	public boolean compareGroups(AccountGroup group1, AccountGroup group2)
	{
		return group1.equals(group2);   //equals() is not implemented in AccountGroup
	}
}
''',
            'Recommendation': '''
验证使用对象。equals()真的想要调用的方法。如果不实施equals()方法或使用不同的方法为比较对象。
例2：下面的代码添加equals()方法实例的解释部分
public class AccountGroup
{
	private int gid;

	public int getGid()
	{
		return gid;
	}

	public void setGid(int newGid)
	{
		gid = newGid;
	}

	public boolean equals(Object o)
	{
		if (!(o instanceof AccountGroup))
			return false;
		AccountGroup other = (AccountGroup) o;
		return (gid == other.getGid());
	}
}
...
public class CompareGroup
{
	public static boolean compareGroups(AccountGroup group1, AccountGroup group2)
	{
		return group1.equals(group2);
	}
}
''',
        },
        {
            'vul_title': 'Code Correctness: Constructor Invokes Overridable Function',
            'describe': '''
当构造函数调用重载函数，它可能允许攻击者访问这个引用被完全初始化的对象之前，它会导致一个漏洞。
示例1：下面调用可以重写的方法。
  ...
  class User {
    private String username;
    private boolean valid;
    public User(String username, String password){
      this.username = username;
      this.valid = validateUser(username, password);
    }
    public boolean validateUser(String username, String password){
      //validate user is real and can authenticate
      ...
    }
    public final boolean isValid(){
      return valid;
    }
  }
由于函数validateUser和类不是final，这意味着它们可以被覆盖，然后将变量初始化为覆盖此函数的子类将允许绕过validateUser功能。 例如：
  ...
  class Attacker extends User{
    public Attacker(String username, String password){
      super(username, password);
    }
    public boolean validateUser(String username, String password){
      return true;
    }
  }
  ...
  class MainClass{
    public static void main(String[] args){
      User hacker = new Attacker("Evil", "Hacker");
      if (hacker.isValid()){
        System.out.println("Attack successful!");
      }else{
        System.out.println("Attack failed");
      }
    }
  }
上述代码打印“攻击成功！”，因为Attacker类覆盖从超类User的构造函数调用的validateUser（）函数，Java将首先在子类中查找从构造函数调用的函数。
''',
            'Recommendation': '''
构造函数不应该调用可以被覆盖的函数，无论是将其指定为final还是将类指定为final。 或者，如果构造函数中仅需要该代码，则可以使用专用访问说明符，或者逻辑可以直接放置到超类的构造函数中。
示例2：以下内容使类final成为阻止函数在其他地方被覆盖的。
  ...
  final class User {
    private String username;
    private boolean valid;
    public User(String username, String password){
      this.username = username;
      this.valid = validateUser(username, password);
    }
    private boolean validateUser(String username, String password){
      //validate user is real and can authenticate
      ...
    }
    public final boolean isValid(){
      return valid;
    }
  }
此示例将该类指定为final，以使其不能被子类化，并将validateUser（）函数更改为private，因为在此应用程序中不需要它。 这是防御性的编程，因为在稍后的日期可能会决定User类需要进行子类化，如果validateUser（）函数未设置为private，则会导致此漏洞重新出现。
''',
        },
        {
            'vul_title': 'Code Correctness: Erroneous String Compare',
            'describe': '''
该程序使用==或！=来比较两个字符串的相等性，它将两个对象进行比较，而不是它们的值。 机会很好，两个参考文献永远不会相等。
示例1：以下分支将永远不会被占用。
  if (args[0] == STRING_CONSTANT) {
      logger.info("miracle");
  }
==和！=运算符只能用于比较对象中包含的字符串相等的字符串。 发生这种情况的最常见方法是将字符串进行实体化，从而将字符串添加到由String类维护的对象池中。 一旦字符串被实体化，该字符串的所有使用将使用相同的对象，并且等式运算符将按预期行为。 所有字符串文字和字符串值常量都是自动进行的。 其他字符串可以手动调用String.intern（），这将返回当前字符串的规范实例，如果需要，创建一个。
''',
            'Recommendation': '''
使用equals（）来比较字符串。
示例2：示例1中的代码可以通过以下方式重写：
  if (STRING_CONSTANT.equals(args[0])) {
      logger.info("could happen");
  }
''',
        },
        {
            'vul_title': 'Code Correctness: null Argument to equals()',
            'describe': '''
该程序使用equals（）方法将一个对象与null进行比较。 此比较将始终返回false，因为对象不为null。 （如果对象为空，程序将抛出NullPointerException）。
''',
            'Recommendation': '''
程序员可能要检查对象是否为空。而不是写obj.equals(null)。而是使用obj = = null
''',
        },
        {
            'vul_title': 'Dead Code: Expression is Always false',
            'describe': '''

''',
            'Recommendation': '''
这个表达式（或其一部分）将总是评估为false; 该程序可以以更简单的形式重写。 附近的代码可能存在用于调试目的，或者可能没有与程序的其余部分一起维护。 该表达式也可能指示方法中较早的错误。
示例1：在将其初始化为false后，以下方法将永远不会设置变量secondCall。 （变量firstCall被错误地使用了两次。）结果是表达式firstCall && secondCall将始终计算为false，因此setUpDualCall（）将永远不会被调用。
public void setUpCalls() {
  boolean firstCall = false;
  boolean secondCall = false;

  if (fCall > 0) {
    setUpFCall();
    firstCall = true;
  }
  if (sCall > 0) {
    setUpSCall();
    firstCall = true;
  }

  if (firstCall && secondCall) {
    setUpDualCall();
  }
}
示例2：以下方法从不将变量firstCall设置为true。 （在第一个条件语句之后，变量firstCall被错误地设置为false。）结果是表达式firstCall && secondCall的第一部分将始终计算为false。
public void setUpCalls() {
  boolean firstCall = false;
  boolean secondCall = false;

  if (fCall > 0) {
    setUpFCall();
    firstCall = false;
  }
  if (sCall > 0) {
    setUpSCall();
    secondCall = true;
  }

  if (firstCall || secondCall) {
    setUpForCall();
  }
}
''',
        },
        {
            'vul_title': 'Dead Code: Expression is Always true',
            'describe': '''
这个表达式（或者它的一部分）将总是评估为真; 该程序可以以更简单的形式重写。 附近的代码可能存在用于调试目的，或者可能没有与程序的其余部分一起维护。 该表达式也可能指示方法中较早的错误。
示例1：在将其初始化为true之后，以下方法将永远不会设置变量secondCall。 （变量firstCall被错误地使用了两次。）结果是表达式firstCall || secondCall将始终评估为true，因此将始终调用setUpForCall（）。
''',
            'Recommendation': '''
一般来说，您应该修复或删除未使用的代码。 它会导致额外的复杂性和维护负担，而不会影响程序的功能。
    ''',
        },
        {
            'vul_title': 'Dead Code: Unused Field',
            'describe': '''
此字段永远不会被访问，除非可能是死亡代码。 死码被定义为永远不会由公共方法直接或间接执行的代码。 这个字段很可能是简单的，但是未使用的字段也可能指出一个错误。
示例1：在下面的类中不使用名为glue的字段。 该类的作者不小心在字段名称上引用了引号，将其转换成字符串常量。
public class Dead {
  String glue;
  public String getGlue() {
    return "glue";
  }
}
示例2：名为glue的字段在以下类中使用，但仅用于从未调用的方法。
public class Dead {
  String glue;
  private String getGlue() {
    return glue;
  }
}
''',
            'Recommendation': '''
一般来说，您应该修复或删除死码。 要修复死码，请通过公共方法直接或间接执行死码。 死码导致额外的复杂性和维护负担，而不会对程序的功能做出贡献。
''',
        },
        {
            'vul_title': 'J2EE Bad Practices: getConnection()',
            'describe': '''
J2EE标准要求应用程序使用容器的资源管理工具来获取与资源的连接。
例如，J2EE应用程序应获取数据库连接，如下所示：
ctx = new InitialContext();
datasource = (DataSource)ctx.lookup(DB_DATASRC_REF);
conn = datasource.getConnection();
并且应该避免以这种方式获得连接：
conn = DriverManager.getConnection(CONNECT_STRING);
每个主要的Web应用程序容器提供池化的数据库连接管理作为其资源管理框架的一部分。 在应用程序中复制此功能是困难和容易出错的，这是J2EE标准下禁止的一部分原因。
    ''',
            'Recommendation': '''
使用适当的连接工厂的JNDI查找替换对DriverManager.getConnection（）的直接调用，并从连接工厂获取连接。
    ''',
        },
        {
            'vul_title': 'J2EE Bad Practices: Leftover Debug Code',
            'describe': '''
通常的开发实践是添加专门用于调试或测试目的的“后门”代码，这些代码并不意图与应用程序一起运送或部署。 当这种调试代码意外地留在应用程序中时，应用程序对于无意的交互模式是开放的。 这些后门进入点产生安全风险，因为它们在设计或测试期间不被考虑，并且不在应用程序的预期操作条件之外。
被遗忘的调试代码最常见的例子是出现在Web应用程序中的main（）方法。 虽然在产品开发过程中这是一个可以接受的做法，但是作为J2EE应用程序的一部分的类不应该定义一个main（）。
    ''',
            'Recommendation': '''
在部署应用程序的生产版本之前，请删除调试代码。 不管是否可以明确提出直接的安全威胁，在开发初期之后，这种守则不可能保留在申请中。
    ''',
        },
        {
            'vul_title': 'J2EE Misconfiguration: Excessive Session Timeout',
            'describe': '''
会话保持打开的时间越长，攻击者必须破坏用户帐户的机会越大。 当会话保持活动状态时，攻击者可能会暴力强制用户的密码，破解用户的无线加密密钥，或从打开的浏览器命令会话。 更长的会话超时也可以防止内存被释放，并且如果创建了足够数量的会话，则最终导致拒绝服务。
示例1：如果会话超时为零或小于零，则会话永不过期。 以下示例显示会话超时设置为-1，这将导致会话无限期地保持活动状态。
<session-config>
    <session-timeout>-1</session-timeout>
</session-config>
<session-timeout>标签定义了Web应用程序中所有会话的默认会话超时时间间隔。 如果缺少<session-timeout>标签，则容器将设置默认超时。
    ''',
            'Recommendation': '''
设置30分钟或更短的会话超时，这两者都允许用户在一段时间内与应用程序进行交互，并为攻击窗口提供合理的限制。
示例2：以下示例将会话超时设置为20分钟。
<session-config>
  <session-timeout>20</session-timeout>
</session-config>
    ''',
        },
        {
            'vul_title': 'J2EE Misconfiguration: Missing Error Handling',
            'describe': '''
当攻击者探索网站寻找漏洞时，网站提供的信息量对于任何企图攻击的最终成功或失败至关重要。 如果应用程序向攻击者显示堆栈跟踪，则它放弃使攻击者的工作显着更容易的信息。 例如，堆栈跟踪可能会向攻击者显示格式不正确的SQL查询字符串，正在使用的数据库的类型以及应用程序容器的版本。 此信息使攻击者能够定位这些组件中的已知漏洞。

应用程序配置应指定一个默认错误页面，以确保应用程序永远不会向错误消息发送错误消息。 处理标准的HTTP错误代码除了是一个很好的安全实践之外，还是很有用和用户友好的，而良好的配置也将定义一个最后一次机会错误处理程序，捕获可能被应用程序抛出的任何异常。
    ''',
            'Recommendation': '''
必须使用默认错误页面配置Web应用程序。 您的web.xml应至少包含以下条目：
<error-page>
   <exception-type>java.lang.Throwable</exception-type>
<location>/error.jsp</location>
</error-page>
<error-page>
   <error-code>404</error-code>
<location>/error.jsp</location>
</error-page>
<error-page>
   <error-code>500</error-code>
<location>/error.jsp</location>
</error-page>
    ''',
        },
        {
            'vul_title': 'J2EE Misconfiguration: Missing Filter Definition',
            'describe': '''
每个过滤器映射必须对应于有效的过滤器定义，以便将其应用。
示例1：以下示例显示了引用不存在的过滤器AuthenticationFilter的过滤器映射。 由于缺少定义，因此过滤器AuthenticationFilter将不会应用于指定的URL模式/ secure / *，并可能导致运行时异常。
<filter>
    <description>Compresses images to 64x64</description>
    <filter-name>ImageFilter</filter-name>
    <filter-class>com.ImageFilter</filter-class>
</filter>

<!-- AuthenticationFilter is not defined -->
<filter-mapping>
    <filter-name>AuthenticationFilter</filter-name>
    <url-pattern>/secure/*</url-pattern>
</filter-mapping>

<filter-mapping>
    <filter-name>ImageFilter</filter-name>
    <servlet-name>ImageServlet</servlet-name>
</filter-mapping>
    ''',
            'Recommendation': '''
确保每个过滤器映射指向有效的过滤器。
示例2：以下示例显示了每个过滤器映射表的适当过滤器定义
<filter>
    <description>An Authentication Filter</description>
    <filter-name>AuthenticationFilter</filter-name>
    <filter-class>com.AuthenticationFilter</filter-class>
</filter>

<filter>
    <description>Compresses images to 64x64</description>
    <filter-name>ImageFilter</filter-name>
    <filter-class>com.ImageFilter</filter-class>
</filter>

<filter-mapping>
    <filter-name>AuthenticationFilter</filter-name>
    <url-pattern>/secure/*</url-pattern>
</filter-mapping>

<filter-mapping>
    <filter-name>ImageFilter</filter-name>
    <servlet-name>ImageServlet</servlet-name>
</filter-mapping>
    ''',
        },
        {
            'vul_title': 'Obsolete',
            'describe': '''
随着编程语言的发展，方法有时会变得过时，原因如下：
- 语言进步
- 更好地了解操作如何有效和安全地执行
- 管理某些操作的惯例的变化
从语言中删除的方法通常由更新的同行替换，这些对象在一些不同的，希望更好的方式中执行相同的任务。
示例：以下代码从一个字节数组中构造一个字符串对象，一个值指定每个16位Unicode字符的前8位。
...
String name = new String(nameBytes, highByte);
...
在本示例中，构造函数可能无法正确地将字节转换为字符，具体取决于使用哪个字符集对由nameBytes表示的字符串进行编码。 由于用于编码字符串的字符集的演变，此构造函数已被弃用并替换为构造函数，构造函数接受用作编码转换字节的字符集名称作为其参数之一。
并非所有功能都被弃用或替换，因为它们具有安全隐患。 然而，过时功能的存在通常表明周围的代码被忽略，并且可能处于失修状态。 软件安全性并不是一个优先考虑，甚至是一个考虑。 如果程序使用不推荐使用或过时的功能，则会增加附近潜伏着安全问题的可能性。
''',
            'Recommendation': '''
不要使用已弃用或过时的功能。 不管直接的安全影响，将这些功能替换为现代同行。 当您遇到过时的功能时，请注意，其存在会提高周围代码包含安全风险的可能性。 考虑应用程序开发的安全相关假设。 它们是否仍然有效？ 特定过时功能的存在是否表示维护问题较大？
    ''',
        },
        {
            'vul_title': 'Poor Error Handling: Empty Catch Block',
            'describe': '''
关于软件系统的每一次严重攻击，都是以违反程序员的假设为由开始的。 攻击之后，程序员的假设看起来很脆弱，创立不成熟，但在攻击之前，许多程序员会在午餐结束后保卫自己的假设。
在代码中容易发现的两个可疑假设是“这种方法调用永远不会失败”，“这个调用失败也没关系”。 当程序员忽略异常时，它们隐含地表示它们在这些假设之一下运行。
示例1：以下代码摘录忽略了一个很少抛出的doExchange（）异常。
try {
  doExchange();
}
catch (RareException e) {
  // this can never happen
}
如果一个RareException被抛出，程序将继续执行，就好像没有发现异常。 该计划没有记录任何表明特殊情况的证据，可能会令任何后来企图解释该计划行为的企图失败。
    ''',
            'Recommendation': '''
至少，记录异常被抛出的事实，以便稍后再回来，并且对所得到的程序行为有所了解。 更好的是，中止当前的操作。 如果异常被忽略，因为调用者无法正确处理它，但上下文使调用者声明它抛出异常本身不方便或不可能，请考虑抛出一个RuntimeException或一个错误，这两个都是未检查的异常。 从JDK 1.4开始，RuntimeException具有一个构造函数，可以容易地包装另一个异常。
示例2：示例1中的代码可以通过以下方式重写：
try {
  doExchange();
}
catch (RareException e) {
  throw RuntimeException("This can never happen", e);
}
    ''',
        },
        {
            'vul_title': 'Poor Error Handling: Overly Broad Catch',
            'describe': '''
多个catch块可能会变得丑陋和重复，但是通过捕获像Exception这样的高级类来“缩小”catch块可能会遮挡应有特殊处理的异常，或者不应该在程序中被捕获。 捕捉过大范围的异常基本上击败了Java类型异常的目的，如果程序增加并开始引发新类型的异常，则可能会变得特别危险。 新的异常类型不会受到任何关注。
示例：以下代码摘录以相同的方式处理三种类型的异常。
  try {
    doExchange();
  }
  catch (IOException e) {
    logger.error("doExchange failed", e);
  }
  catch (InvocationTargetException e) {
    logger.error("doExchange failed", e);
  }
  catch (SQLException e) {
    logger.error("doExchange failed", e);
  }
乍看之下，在一个catch块中处理这些异常似乎比较可取，如下所示：
  try {
    doExchange();
  }
  catch (Exception e) {
    logger.error("doExchange failed", e);
  }
但是，如果doExchange（）被修改为抛出一种应该以某种不同种类的方式处理的新类型的异常，那么宽的catch块将阻止编译器指出这种情况。 此外，新的catch块现在也将处理从RuntimeException派生的异常，例如ClassCastException和NullPointerException，这不是程序员的意图。
''',
            'Recommendation': '''

    ''',
        },
        {
            'vul_title': 'Poor Error Handling: Overly Broad',
            'describe': '''

    ''',
            'Recommendation': '''

    ''',
        },
        {
            'vul_title': '',
            'describe': '''

    ''',
            'Recommendation': '''

    ''',
        },
        {
            'vul_title': '',
            'describe': '''

    ''',
            'Recommendation': '''

    ''',
        },
        {
            'vul_title': '',
            'describe': '''

    ''',
            'Recommendation': '''

    ''',
        },
        {
            'vul_title': '',
            'describe': '''

    ''',
            'Recommendation': '''

    ''',
        },
        {
            'vul_title': '',
            'describe': '''

    ''',
            'Recommendation': '''

    ''',
        },
        {
            'vul_title': '',
            'describe': '''

    ''',
            'Recommendation': '''

    ''',
        },
        {
            'vul_title': '',
            'describe': '''

    ''',
            'Recommendation': '''

    ''',
        },
        {
            'vul_title': '',
            'describe': '''

    ''',
            'Recommendation': '''

    ''',
        },

    ]
    for i in infos:
        if i['vul_title']==title:
            return i
    data = {'vul_title':title,
            'describe': '该漏洞详情和漏洞修复的方法还没添加，如果需要，请联系管理员添加，XXX@XXX.com',
            'Recommendation': '无',
            }
    return data
