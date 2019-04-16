## 开源情况
datafaker是笔者开发的一个大批量测试数据和流测试数据生成工具，兼容python2.7和python3.4+，欢迎下载使用。github地址为：

https://github.com/gangly/datafaker

文档同步更新在github

## 工具产生背景


<font color=gray face="黑体">在软件开发测试过程，经常需要测试数据。这些场景包括：</font>
- 后端开发
新建表后，需要构造数据库测试数据，生成接口数据提供给前端使用。
- 数据库性能测试
生成大量测试数据，测试数据库性能
- 流数据测试
针对kafka流数据，需要不断定时生成测试数据写入kafka


经过调研，目前没有一个开源的测试数据生成工具，用来生成mysql 表结构相似的数据。常用方法是人工手动造几条数据写入数据库，这种方法带来的弊端是
- 浪费工时
针对表的不同数据类型的字段，需要构造不同数据
- 数据量小
如果需要构造大量数据，手动造数据无能为力
- 不够准确
比如需要构造邮箱（满足一定格式），电话号码（确定的数字位数），ip地址（固定格式），年龄（不能为负数，有大小范围）等。这些测试数据有一定的限制或规律，手工构造可能不能满足数据范围或一些格式要求而导致后端程序报错
- 多表关联
手动造的数据量较小，在多个表中用主键不一定能关联上，或者关联出来没数据
- 动态随机写入
比如针对流数据，需要随机每隔几秒钟写入kafka。或者动态随机插入mysql，手工操作相对麻烦，而且不好统计写入数据条数


**<font color=#6495ED face="黑体">针对目前这些痛点，datafaker应运而生。datafaker是一个多数据源测试数据构造工具，可以模拟产生大部分常用数据类型，轻松解决以上痛点。datafaker具有以下功能：</font>**


- 多种数据类型
包括常见数据库字段类型（整型、浮点型、字符型）、自定义类型（IP地址，邮箱，身份证号码等）
- 模拟多表关联数据
通过制定某些字段为枚举类型（从指定的数据列表里面随机选择），这样在数据量多的情况下能保证多表Join能关联上，查询到数据
- 支持批数据和流数据生成，可指定流数据间隔时间
- 支持多种数据输出方式，包括屏幕打印、文件和远程数据源
- 支持多种数据源。目前支持关系型数据库、Hive、Kafka、Hbase。后面将扩展到Mongo，ES等数据源
- 可指定输出格式，目前支持text，json



## 软件架构

datafaker是用python编写，支持python2.7，python3.4+。目前版本0.08，已经发布在pypi上。

![架构图](img/datafaker.png)

架构图完整的画出了工具的执行过程，从图可知工具经历了5个模块：
- 参数解析器。解析用户从终端命令行输入的命令。
- 元数据解析器。用户可以指定元数据来自本地文件或者远程数据库表。解析器获取到文件内容后按照规则将文本内容解析成表字段元数据和数据构造规则。
- 数据构造引擎。构造引擎根据元数据解析器产生的数据构造规则，模拟产生不同类型的数据。
- 数据路由。根据不同的数据输出类型，分成批量数据和流数据生成。流数据可指定产生频率。然后将数据转换成用户指定的格式输出到不同数据源中。
- 数据源适配器。适配不同数据源，将数据导入到数据源中。

## 安装流程

首先确保已经安装python和pip

1.下载安装。下载源码压缩包，解压后，执行：

```python setup.py install ```


2.直接安装

```pip install datafaker```

##使用举例
=========
$代表终端提示符
- 查看版本号，查看参数使用说明
---------
```
$ datafaker --version
0.0.8

$ datafaker --help
usage: datafaker [-h] [--meta [META]] [--interval INTERVAL] [--version]
                 [--outprint] [--outspliter OUTSPLITER] [--locale LOCALE]
                 [--outfile OUTFILE] [--format FORMAT]
                 [--withheader]
                 [dbtype] [connect] table [num]

Generates SQLAlchemy model code from an existing database.

positional arguments:
  dbtype                data source type
  connect               connect info to the database
  table                 table to process
  num                   number of records to generate

optional arguments:
  -h, --help            show this help message and exit
  --meta [META]         meta file path
  --interval INTERVAL   meta file path
  --version             print the version number and exit
  --outprint            print fake date to screen
  --outspliter OUTSPLITER
                        print data, to split columns
  --locale LOCALE       which country language
  --outfile OUTFILE     file to write output to (default: stdout)
  --format FORMAT       outprint and outfile format: json, text (default:
                        text)
```


- 从本地mysql的test数据库的stu表中读取表元数据，并构造10条数据写入stu表
---------
```
$ datafaker mysql mysql+mysqldb://root:root@localhost:3600/test stu 10
generated records : 10
saved records : 10
time used: 0.038 s
```
- 从本地文件meta.txt中读取元数据，以,,分隔符构造10条数据，打印在屏幕上
----------------
```
$ datafaker mysql mysql+mysqldb://root:root@localhost:3600/test stu 10 --outprint --meta meta.txt --outspliter ',,'
1,,鲍红,,人和中心,,高小王子,,3,,81,,55.6,,13197453222,,mwei@gmail.com,,192.100.224.255,,江苏省西宁市梁平朱路I座 944204
2,,刘东,,清华中学,,高小王子,,3,,31,,52.4,,15206198472,,lili@kong.cn,,203.0.190.6,,内蒙古自治区嘉禾市兴山呼和浩特街E座 706421
3,,匡静,,人和中心,,歌神,,9,,84,,72.51,,18944398099,,zouchao@gmail.com,,203.1.53.166,,安徽省永安市沈河惠州街x座 345415
4,,王宇,,猪场,,逗比,,6,,89,,19.3,,18628114285,,na58@cai.net,,169.4.126.215,,山西省梧州县朝阳何路y座 846430
5,,陆桂芝,,猪场,,逗比,,8,,99,,92.22,,13304570255,,na55@ti.cn,,168.136.127.200,,江苏省英县徐汇尹街C座 908240
6,,顾阳,,猪场,,歌神,,9,,32,,43.14,,18025578420,,linping@pr.net,,174.50.222.39,,黑龍江省惠州县梁平大冶街Z座 611736
7,,杨洁,,人和中心,,鬼泣,,6,,35,,81.25,,13654306263,,minzhong@xiaxia.cn,,100.57.79.2,,湖北省琳市沙湾汪街V座 544660
8,,申璐,,人和中心,,鬼泣,,6,,14,,73.61,,13866020503,,changxiulan@chaoxia.cn,,198.248.254.56,,陕西省合山县东丽宁德街Q座 810017
9,,申强,,广东中学,,逗比,,7,,48,,90.65,,13915915013,,ysun@chao.cn,,169.210.122.39,,甘肃省冬梅县城北六安街Z座 619755
10,,李丹丹,,旧大院,,鬼泣,,3,,67,,87.63,,18899812516,,xiulanmo@qin.cn,,192.52.218.133,,湖南省宜都县萧山澳门街E座 791911
generated records : 10
printed records : 10
time used: 0.458 s
```
这是个学生表描述。
其中meta.txt文件内容为：
```
id||int||自增id[:id]
name||varchar(20)||学生名字
school||varchar(20)||学校名字[:enum(file://names.txt)]
nickname||varchar(20)||学生小名[:enum(鬼泣, 高小王子, 歌神, 逗比)]
age||int||学生年龄
class_num||int||班级人数[:int(10, 100)]
score||decimal(4,2)||成绩[:decimal(4,2,1)]
phone||int(20)||电话号码[:phone_number]
email||varchar(64)||家庭网络邮箱[:email]
ip||varchar(32)||IP地址[:ipv4]
address||text||家庭地址[:address]
```
meta.txt文件中每行数据为元数据的一个字段描述，以||分割为三列
- 第一列：字段名
- 第二列：表字段类型
- 第三列：字段注释，其中包含构造规则标识

### 构造规则优先级：

解析器将优先选择第三列的带规则标记的字段注释进行解析，如果不带标记，则选择第二列的字段类型进行解析。

这种好处是：

1）对应已经创建的数据表，用户可以用desc tablename 或者show full columns from tablename，将表shema查询复制下来，对用字段类型构造数据不满足的情况下，在注释里面进行打标机进行特殊处理

2）对于新表，在create table创建表时直接在注释里面打上标记。这种情况不用指定元数据文件。

后面将详细介绍构造规则说明

其中学校名字[:enum(names.txt)]表示从本地文件names.txt中读取枚举数据，内容为，表示学校名称只能从下面这5所学校中随机产生。
```
清华中学
人和中心
广东中学
猪场
旧大院
```

- 从本地data/hive_meta.txt文件中读取元数据，产生1000条数据写入hive的test库，stu表中
```
datafaker hive hive://yarn@localhost:10000/test stu 1000 --meta data/hive_meta.txt
```

- 从meta.txt中读取元数据，产生10条json格式数据写入到/home目录out.txt中
--------------------

```
datafaker file /home out.txt 10 --meta meta.txt --format json
```


- 从本地meta.txt参数数据，以1秒间隔输出到kafka的topic hello中
------------------

```
$ datafaker kafka localhost:9092 hello 1 --meta meta.txt --outprint
{"school": "\u4eba\u548c\u4e2d\u5fc3", "name": "\u5218\u91d1\u51e4", "ip": "192.20.103.235", "age": 9, "email": "chaokang@gang.cn", "phone": "13256316424", "score": 3.45, "address": "\u5e7f\u4e1c\u7701\u5b81\u5fb7\u5e02\u6d54\u9633\u5468\u8defu\u5ea7 990262", "class_num": 24, "nickname": "\u9017\u6bd4", "id": 1}
{"school": "\u4eba\u548c\u4e2d\u5fc3", "name": "\u6768\u4e3d", "ip": "101.129.18.230", "age": 3, "email": "min60@hv.net", "phone": "18183286767", "score": 22.16, "address": "\u8fbd\u5b81\u7701\u592a\u539f\u5e02\u53cb\u597d\u6c55\u5c3e\u8defG\u5ea7 382777", "class_num": 30, "nickname": "\u6b4c\u795e", "id": 2}
{"school": "\u6e05\u534e\u4e2d\u5b66", "name": "\u8d75\u7ea2", "ip": "192.0.3.34", "age": 9, "email": "fxiao@gmail.com", "phone": "18002235094", "score": 48.32, "address": "\u5e7f\u897f\u58ee\u65cf\u81ea\u6cbb\u533a\u65ed\u5e02\u6c88\u5317\u65b0\u6731\u8defc\u5ea7 684262", "class_num": 63, "nickname": "\u6b4c\u795e", "id": 3}
{"school": "\u6e05\u534e\u4e2d\u5b66", "name": "\u5f20\u7389\u6885", "ip": "198.20.50.222", "age": 3, "email": "xiulanlei@cw.net", "phone": "15518698519", "score": 85.96, "address": "\u5b81\u590f\u56de\u65cf\u81ea\u6cbb\u533a\u6d69\u53bf\u767d\u4e91\u4e4c\u9c81\u6728\u9f50\u8857s\u5ea7 184967", "class_num": 18, "nickname": "\u9017\u6bd4", "id": 4}
{"school": "\u732a\u573a", "name": "\u674e\u6842\u5170", "ip": "192.52.195.184", "age": 8, "email": "fxiao@konggu.cn", "phone": "18051928254", "score": 97.87, "address": "\u9ed1\u9f8d\u6c5f\u7701\u54c8\u5c14\u6ee8\u53bf\u6c38\u5ddd\u6d2a\u8857E\u5ea7 335135", "class_num": 46, "nickname": "\u9ad8\u5c0f\u738b\u5b50", "id": 5}
{"school": "\u4eba\u548c\u4e2d\u5fc3", "name": "\u5434\u60f3", "ip": "192.42.234.178", "age": 3, "email": "uliang@yahoo.com", "phone": "14560810465", "score": 6.32, "address": "\u5b81\u590f\u56de\u65cf\u81ea\u6cbb\u533a\u516d\u76d8\u6c34\u5e02\u5357\u6eaa\u7f57\u8857M\u5ea7 852408", "class_num": 12, "nickname": "\u9b3c\u6ce3", "id": 6}
^Cgenerated records : 6
insert records : 6
time used: 6.285 s
```
消费端验证:

![数据消费](img/kafka.png)

- 数据写入hbase
---------------

```
datafaker hbase localhost:9090 test-table 10 --meta data/hbase.txt
```
需要开启hbase thrift服务,不能为thrift2
例子中，创建一张表test-table, 列族为Cf
元数据文件hbase.txt内容为

```
rowkey||varchar(20)||sdflll
Cf:name||varchar(20)||学生名字
Cf:age||int||学生名字[:age]
```

其中第一行必须为rowkey, 可带参数，rowkey(0,1,4)表示将rowkey值和后面第一列，第五列值用_连接

后面行为列族中的列名，可以创建多个列族


## 命令参数

datafaker参数包含4个必选参数和一些可选参数，如下表所示

| 参数名 | 含义 |  参数类型| 是否必选 | 默认值 | 备注 |
| ------ | ------ | ------ | ----- | ------| ---- |
|dbtype| 数据源类型 | string | 是 | 无 | 可选值为 mysql,hive, kafka, file |
| connect | 数据源连接信息 | string| 是 | 无 | 关系型数据库和hive为 sqlachemy的连接串<br>kafka为broker连接串<br>file为文件路径<br>hbase为thrift host和端口|
|table| 表名 | string | 是 |  无 | 将各种数据源操作单位都抽象为表，数据库中为表，kafka中为topic，file为文件名，hbase为表，mongo为集合|
| num | 数据条数 | int | 是 | 无 | 其中kafka必须为1
| meta | 元数据文件 | string | 否 | 无 | 若设定该参数，则忽略从数据源连接信息中读取远数据 |
| interval | 流数据产生间隔 | int | 否 | 1 | 单位秒|
| version | 显示版本号 | bool | 否 |  无 |  |
| outprint | 是否在屏幕打印 | bool | 否 |  false |  若设置屏幕打印，则数据不会写文件或数据源 |
| outspliter |  数据字段分割符 | string | 否 |  , | 屏幕打印，保存文件有效 |
| locale | 语言类型 | string | 否 | zh_CN | 支持多国语言，en_US， zh_CN|
| outfile | 输出到文件 | string | 否 |  无 |  |
| format | 数据格式 | string | 否 |  text |  kafka 默认为json|
| withheader | 打印和存储到文件是否带表头 | bool | 否 | False| |




## 数据构造规则

#### 1.数据库常用类型

这部分数据类型可以不用指定元数据文件
- 数值类型
支持大部分标准SQL数值数据类型。
这些类型包括严格数值数据类型( int、integer、smallint、decimal和numeric)，以 及近似数值数据类型(float、real和double, precision)
 - 日期和时间类型
    表示时间值的日期和时间类型为datetime、date、timestamp、time和year。

  - 字符串类型
    字符串类型指char、varchar、binary、varbinary、blob、text、enum和set。该节描述了这些类型如何工作以及如何在查询中使用这些类型。


#### 2.可变数据库类型
------------------
| 类型名 | 含义 | 默认值 | 备注|
| ---- | ---- | ---- | ---- |
| decimal(M,D, negative) | M指定总的数据位数，D指定小数位数,  negative指定正1负0 | 无 | decimal(4, 2, 1)指定4位数，2位小数的正浮点数，如78.23 |
| string(min, max) | min, max 指定字符串位数范围|无 | |
|date(start, end)| start, end 指定日期范围 | 无 | 如date(1990-01-01, 2019-12-12)|

**enum类型**
------

<font color=#6495ED face="黑体">
enum类型表示随机从列表里随机选取一个对象，例如：

enum(2, 4, 5, 18) 表示每次从2，4，5，8这四个整数中随机选择一个

如果enum数组中只有一个对象，则表示从文件读取数据列表，每行一个对象：

enum(file://data.txt) 表示从当前目录的data.txt文件中读取列表。

enum类型可用来构造多表关联，比如两个表的某些字段都用同一个enum数据列表产生数据。
</font>


**op类型**
-------

<font color=#6495ED face="黑体">
op类型表示从其他列中计算出值，例如：

op(c0+c3) 表示第一列值加上第四列值

op(c1*c4+c13) 表示第一列值乘上第五列值加上第十四列值

</font>


### 3.自定义扩展类型
-----------------

- address 地址


| 构造规则 |含义|举例 | 备注 |
| -------- | -------- | ------ | ------- |
| country| 国家名 |  中国 |  |
|province | 省份 | 河南 | |
| city | 城市名 | 郑州市 | |
| city_suffix | 城市的后缀 | 市 | 市或县 |
|address| 地址 | 河北省巢湖县怀柔南宁路f座 169812 |  |
|country_code | 国家编码 | AO | |
|district  | 区 | 普陀 | |
| latitude  | 地理坐标(纬度) | 68.0228435 | |
| longitude |地理坐标(经度) | 155.964341 | |
| postcode | 邮编 | 803511 |  |
|street_address | 街道地址 | 邯郸路W座 | |
|street_name |街道名 | 合肥路| |
| street_suffix | 街、路 | 街 | |

- 数值类型

| 构造规则 |含义|举例 | 备注 |
| -------- | -------- | ------ | ------- |
|random_digit | 0~9随机数| 1 | |
|random_digit_not_null |1~9的随机数| 9| |
|random_element | 随机字母| a | |
|random_int|随机数字| 44 |可设置范围，可以通过设置min,max来设置，默认0~9999，例如random_int(1,100)|
|random_letter| 随机字母| e | |
|random_number | 随机数字 | 参数digits设置生成的数字位数 |例如random_number(2)生成2为数数字 |
|boolean| True/False| False | |
|numerify| 三位随机数字| 934| |
| number | 一定数位的数字 | 44322 | number(digits=None, fix_len=0, positive=0)有三个参数，digits表示多少位数字，fix_len表示是否固定长度（1表示固定长度，否则为1到digits长度）positive表示是否为正数（1为正数，-1为负数，0正负都可能）。number(18, 1, 1) 产生18位数固定长度的正整数|


- 公司

| 构造规则 |含义|举例 | 备注 |
| -------- | -------- | ------ | ------- |
| bs | 公司服务名 | transition open-source content | |
| company | 公司名（长）| 天开信息有限公司 | |
| company_prefix | 公司名（短）| 浦华众城 | |
| company_suffix | 公司性质 | 传媒有限公司 | |
|job | 职位 | 项目执行/协调人员 | |

- 信用卡、货币

| 构造规则 |含义|举例 | 备注 |
| -------- | -------- | ------ | ------- |
|credit_card_expire | 信用卡到期日 | 05/19 | |
| credit_card_full | 完整信用卡信息 | JCB 16 digit 霞 张 3514193766205948 08/21CVC: 436 | |
| credit_card_number |信用卡号| 3500011993590161 | |
| credit_card_provider | 信用卡类型| American Express | |
| credit_card_security_code | 信用卡安全码| 190 | |
| currency_code | 货币编码 | HNL | |

- 日期、时间

| 构造规则 |含义|举例 | 备注 |
| -------- | -------- | ------ | ------- |
| am_pm | AM/PM | AM | |
| century | 世纪 | VII | |
| date | 随机日期 |2014-05-18 |date(start_date,end_date,format)<br>start_date表示从当前日期往前推的天数，默认值为-30y,前30年，<br>end_date表示从当前日期往后推的日期数,默认值为今天<br>format为日期格式,默认值为%Y-%m-%d<br>例如date(-30d, 20d, '%Y.%m.%d') |
| date_between| 指定范围内日期| 1997-08-29 |date_between(start_date,end_date,format)<br>start_date表示开始日期，必填<br>end_date表示结束日期，必填<br>format为日期格式,默认值为%Y-%m-%d<br>date_between(2017-01-01, 2019-12-02, '%Y%m%d')|
|date_this_month | 当前月份的日期 | 2019-03-13 | |
| date_this_year | 今年内的日期 | 2019-03-09 | |
| date_time |  时间|  2010-06-15 04:07:11 |（1970年1月1日至今）|
| date_time_between | 指定范围时间 |  2009-10-03 03:15:07  |用法同dates
| month | 随机月份| 05 | |
|month_name | 随机月份（英文）| December | |
| time() | 随机24小时时间| 18:52:55 | |
| timezone | 随机时区| Europe/Andorra| |
|unix_time |随机Unix时间| 203461583 | |
|year | 随机年份| 2017 | |

- internet

| 构造规则 |含义|举例 | 备注 |
| -------- | -------- | ------ | ------- |
|file_extension | 文件扩展名 | wav | |
| file_name | 文件名（包含扩展名，不包含路径）| werwe.jpg| |
|file_path | 文件路径（包含文件名，扩展名）| /home/| |
| mime_type | mime Type| video/x-flv| |
|company_email |公司邮箱 | jieyan@14.cn | |
| domain_name |  域名 | jq.cn | |
| email | 邮箱 | kren@wei.cn | |
|image_url | 随机URL地址 | https://www.lorempixel.com/470/178| |
|ipv4 | IP4地址 | 192.0.25.141 |  |
| ipv6 | IP6地址 | 206f:1ff0:374:2d5f:a6f8:69ef:4ba9:2d14 | |
| mac_address | MAC地址 | 65:02:ed:82:c6:98 | |
| tld | 网址域名后缀(.com,.net.cn,等等，不包括.) | cn | |
|uri | URI地址| http://24.cn/ | |
|url | URL地址| http://www.guiyinglei.cn/ | |
| user_name | 用户名| ping51 | |
|user_agent| 随机user_agent信息|  | |
|chrome | Chrome浏览器user_agent信息|Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/5342 (KHTML, like Gecko) Chrome/27.0.819.0 Safari/5342| |
| firefox | FireFox浏览器user_agent信息| | |
|internet_explorer | IE浏览器user_agent信息| | |
| opera | Opera浏览器user_agent | | |
| safari | Safari浏览器user_agent信息 | | |
| linux_platform_token | 随机Linux信息| X11; Linux i686| |
|isbn10 | 随机ISBN（10位）|1-02-136461-4| |
|isbn13 | 随机ISBN（13位）| 978-0-15-215169-0 | |

- 文本类型

| 构造规则 |含义|举例 | 备注 |
| -------- | -------- | ------ | ------- |
|paragraph | 随机生成一个段落| | |
|sentence | 随机生成一句话|  | |
|text |随机生成一篇文章|不要幻想着人工智能了，至今没完全看懂一句话是什么意思| |
|word |随机生成词语| hello | |
|locale | 随机生成语言/国际信息| niu_NZ | 各国本地化编码|
|md5 | 随机生成MD5| fd80f4681258a9ecb329ab12782dfbba | |
|password |随机生成密码| )we3JViVB1 |可选参数：length：密码长度；special_chars：是否能使用特殊字符；digits：是否包含数字；upper_case：是否包含大写字母；lower_case：是否包含小写字母|
|sha1| 随机SHA1| e9bb2fcd4b4089cc89c36636850ceafe779dbe58 | |
|sha256 |随机SHA256| dd119cb2aec9b3d5557e56bb497757d42f82b32486ea92126942821d3b657957 | |
|uuid4 | 随机UUID| 04aff886-8482-4069-9260-7917fd83982d | |


- 人物信息相关

| 构造规则 |含义|举例 | 备注 |
| -------- | -------- | ------ | ------- |
|name | 全名 | 单玉珍 | |
|name_female| 男性全名|  官平 | |
|name_male | 女性全名 |  许颖 | |
|first_name | 名 | 琴 | |
|last_name | 姓 | 潘 | |
| first_name_female |女名 |丽| |
| last_name_female | 女姓 |王| |
| first_name_male | 男名 | 强 | |
| last_name_male | 男姓 | 杨 | |
|age | 人年龄 | 23| 默认值 0-100 |
|ssn| 身份证号| 350526193807198690 | |
|phone_number |  手机号| 13926798387 | |
|phonenumber_prefix | 手机号段 | 157| |
|profile |  档案信息 || |
|simple_profile | 简单档案信息| {'username': u'kcui', 'name': u'\u5415\u67f3', 'birthdate': datetime.date(1993, 3, 28), 'sex': 'F', 'address': u'\u9752\u6d77\u7701\u4e0a\u6d77\u53bf\u6881\u5e73\u5174\u5b89\u76df\u8defQ\u5ea7 532381', 'mail': u'juanpan@hotmail.com'}| |




- 其他杂项

| 构造规则 |含义|举例 | 备注 |
| -------- | -------- | ------ | ------- |
|color_name| 随机颜色名 |Moccasin| |
|hex_color |随机HEX颜色| #7f7cb6 | |
|rgb_color | 随机RGB颜色| 210,85,105 | |




## 注意事项

#### 1.构造大批量数据
若需要构造大批量数据，原生python将耗费大量时间，请使用pypy执行datafaker，例如：

```pypy -m datafaker hbase localhost:9090 PIGONE 50000 --meta hbase.txt```

#### 2.写入Hbase报错Broken pipe
是由于hbase设置的hbase.thrift.server.socket.read.timeout参数过小，默认为60秒
因此在conf/hbase-site.xml中添加上配置即可：
```
<property>
         <name>hbase.thrift.server.socket.read.timeout</name>
         <value>600000</value>
         <description>eg:milisecond</description>
</property>
```
重启hbase, 重启thrift






















