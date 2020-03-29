## 7 Data construction rule
English | [中文](docs/zh_CN/数据构造规则.md)

#### 1. Common types of databases

This part of the data type can be used without specifying a metadata file.

- Numerical type
supports most standard SQL numeric data types.
These types include strict numeric data types ( int, integer, smallint, decimal, and numeric), as well as approximate numeric data types (float, real, and double, precision).

- Date and time type
The date and time types that represent time values ​​are datetime, date, timestamp, time, and year.

- String type
String types refer to char, varchar, binary, varbinary, blob, text, enum, and set. This section describes how these types work and how to use them in queries.


#### 2.Variable database type
------------------
| Type name | description | Defaults | note |
| ---- | ---- | ---- | ---- |
| decimal(M,D, negative) | M specifies the total number of data bits, D specifies the number of decimal places, negative specifies positive 1 negative 0 | None | Decimal (4, 2, 1) specifies a 4-digit, 2-digit fractional positive floating point number, such as 78.23 |
| string(min, max) | Min, max specifies the range of string digits | None | |
|date(start, end)| Start, end specifies the date range |  None | Such as date (1990-01-01, 2019-12-12) |


**auto increment type**
------
<font color=#6495ED face="黑体">
inc(mark, start, step)

mark: variable name

start: start value, default value is 1

step: increment step，default value is 1

inc(id) means that the column ID will grow by 1 every time starting from 1. It can be used for MySQL's auto increase primary key

inc(score, 100, 2), means that the column score increase by 2 from 100



</font>

**enum**
------

<font color=#6495ED face="黑体">
The enum type means randomly picking an object randomly from the list, for example:
enum(2, 4, 5, 18) means that one of the four integers 2, 4, 5, 8 is randomly selected each time.

If there is only one object in the enum array, it means that the data list is read from the file, one object per line:
enum(file://data.txt) means to read the list from the data.txt file in the current directory.

The enum type can be used to construct multi-table associations. For example, some fields of two tables use the same enum data list to generate data.
</font>


**order_enum**
-------
Usage same as enum type.

The difference is that it is used to generate enumeration values in cyclic order. It is often used to generate values in associated multiple columns. For example, one column is city code and the other column is city name. The city code needs to correspond to the city name one by one. The number of enumeration values should be the same for the associated multiple columns.

Note: due to multithreading, it is not guaranteed that the sequence is generated in strict accordance with the enumeration value list. But it can ensure that multiple related columns correspond one by one

Please search for issues for details

**op**
-------

<font color=#6495ED face="黑体">
The op type indicates that values are calculated from other columns, such as:

Op (C0 + C3) means the first column value plus the fourth column value

Op (C1 * C4 + C13) means the value of the first column multiplied by the value of the fifth column plus the value of the fourteenth column

</font>


### 3.Custom extension type
-----------------

- address


| rule mark | description |Example | note |
| -------- | -------- | ------ | ------- |
| country| Country name |  China |  |
|province | province | Henan | |
| city | city | Zhengzhou City | |
| city_suffix | City suffix | city | City or county |
|address| address | Block F, Nanning Road, Huairou, Chaohu County, Hebei Province, China 169812 |  |
|country_code | National code | AO | |
|district  | Area | Putuo | |
| latitude  | Geographic coordinates (latitude) | 68.0228435 | |
| longitude | Geographical coordinates (longitude) | 155.964341 | |
| postcode | Zip code | 803511 |  |
|street_address | Street address | Kushiro W | |
|street_name | Street name | Hefei Road| |
| street_suffix | Street, road | street | |

- Numerical type

| rule mark | description |Example | note |
| -------- | -------- | ------ | ------- |
|random_digit | 0~9 random number| 1 | |
|random_digit_not_null |1~9 random number| 9| |
|random_element | Random letter | a | |
|random_int|Random number| 44 |The range can be set, which can be set by setting min, max. The default is 0~9999, for example, random_int(1,100)|
|random_letter| Random letter| e | |
|random_number | Random number | For example, random_number(2) generates 2 as a number |
|boolean| True/False| False | |
|numerify| Three random numbers | 934| |
| number | A certain number | 44322 | number(digits=None, fix_len=0, positive=0)有三个参数，digits表示多少位数字，fix_len表示是否固定长度（1表示固定长度，否则为1到digits长度）positive表示是否为正数（1为正数，-1为负数，0正负都可能）。number(18, 1, 1) 产生18位数固定长度的正整数 Number (digits = none, fix? Len = 0, position = 0) has three parameters. Digits indicates the number of digits, fix? Len indicates whether the length is fixed (1 indicates fixed length, otherwise 1 to digits length). Position indicates whether the length is positive (1 is positive, - 1 is negative, 0 can be positive or negative). Number (18, 1, 1) produces a positive integer with a fixed length of 18 digits|

- company

|Construction rule | meaning | example | remarks|
| -------- | -------- | ------ | ------- |
|BS company service name transition open source content|
|Company name (long) Tiankai Information Co., Ltd|
|Company | prefix | company name (short) | Puhua Zhongcheng ||
|Company | suffix | company nature | Media Co., Ltd. ||
|Job | position | Project Executive / Coordinator ||



- Credit card, currency

|Construction rule | meaning | example | remarks|
| -------- | -------- | ------ | ------- |
|Credit card expiry date 05 / 19|
|Credit card full credit card information JCB 16 digital 3514193766205948 08 / 21cvc: 436|
|Credit card number 3500011993590161|
|Credit card provider American Express|
|Credit card security code 190|
|Currency code HNL|

- Date, time

|Construction rule | meaning | example | remarks|
| -------- | -------- | ------ | ------- |
| am_pm | AM/PM | AM | |
|Century VII|
|Date | random date | 2014-05-18 | date (start | date, end | date, format) < br > start | date means the number of days pushed forward from the current date, the default value is - 30y, the first 30 years, < br > end | date means the number of days pushed back from the current date, the default value is today | br > format is the date grid, the default value is% Y -% m -% d < br > for example, date (- 30d, + 20d,% y.% M.% d)|
|Date | between | within the specified range | 1997-08-29 | date | between (start | date, end | date, format) < br > start | date means start date, required < br > end | date, required < br > format is date format, default value is% Y -% m -% d < br > date | between (2017-01-01, 2019-12-02,% Y% m% d)|
|Date | this | month | date of current month | March 13, 2019 ||
|Date | this year | March 9, 2019|
|Date | time / datetime | (January 1, 1970 to now) time | can be datetime without parameter, or datetime with parameter (0) random time, datetime (1,% Y -% m -% d% H:% m) data generation time 2010-06-15 04:07 | datetime (now, format): now (whether 0,1 uses the current time, 0 represents the random event by default, 1 is the current time), Format (default time format is%Y-%m-%d%H:%M:%S)|
|Date | time | specified range time | 2009-10-03 03:15:07 | use the same as dates
|Month | random month | 05 ||
|Month| name | random month | December ||
|Time | random 24-hour time | 18:52:55 ||
|Timezone | random time zone | Europe / Andorra ||
|UNIX time random UNIX time 203461583|
|Timestamp | random UNIX time | timestamp / timestamp (0) random timestamp, timestamp (1) the current data generates a timestamp | with a parameter default of 0|
|Year | random year | 2017 ||

- Internet

|Construction rule | meaning | example | remarks|
| -------- | -------- | ------ | ------- |
|File extension file extension wav|
|File | name | filename (including extension, excluding path) | werwe.jpg |)|
|File path file path (including file name, extension) | / home / ||
| mime_type | mime Type| video/x-flv| |
|Company email: company email: jieyan@14.cn|
|Domain name domain jq.cn|
|Email | email | kren@wei.cn ||
|Image | URL | random URL address | https://www.lorempixel.com/470/178||
|IPv4 | IP4 address | 192.0.25.141 ||
|IPv6 | IP6 address | 206F: 1ff0:374:2d5f: a6f8:69ef: 4ba9:2d14 ||
|MAC address MAC address 65:02: ED: 82: c6:98|
|TLD domain name suffix (. Com,. Net. CN, etc., excluding.)|
|URI | URI address | http://24.cn/ ||
|URL | URL address | http://www.guiyinglei.cn/ ||
|User | name | user name | ping51 ||
|User agent random user agent information|
|Chrome browser user agent information Mozilla / 5.0 (X11; Linux x86) applewebkit / 5342 (KHTML, like gecko) Chrome / 27.0.819.0 Safari / 5342|
|Firefox browser user agent information|
|Internet Explorer IE browser user agent information|
|Opera browser user agent|
|Safari browser user agent information|
|Linux | platform | token | random Linux information | X11; Linux i686 ||
|Isbn10 | random ISBN (10 bits) | 1-02-136461-4 ||
|Isbn13 | random ISBN (13 bits) | 978-0-15-215169-0 ||

- Text type

|Construction rule | meaning | example | remarks|
| -------- | -------- | ------ | ------- |
|Paragraph | randomly generates a paragraph ||
|Sentence randomly generates a sentence|
|Text | randomly generate an article | don't fantasize about artificial intelligence, so far you haven't fully understood the meaning of a sentence ||
|Word | randomly generate word | Hello ||
|Locale | randomly generated language / international information | Niu | NZ | national localization code|
|MD5 | randomly generate MD5 | fd80f4681258a9ecb329ab12782dfbba ||
|Password | randomly generate password |) we3jvivb1 | optional parameters: length: password length; special_chars: whether special characters can be used; digits: whether numbers are included; upper_case: whether uppercase letters are included; lower_case: whether lowercase letters are included|
|SHA1 | random SHA1 | e9bb2fcd4b4089cc89c366850ceafe779dbe58 ||
|Sha256 | random sha256 | dd119cb2aec9b3d5557e56bb497757d42f82b32486ea92126942821d3b657957 ||
|Uuid4 | random UUID | 04aff886-8482-4069-9260-7917fd83982d ||


- Character information related

|Construction rule | meaning | example | remarks|
| -------- | -------- | ------ | ------- |
|Name | full name | Dan Yuzhen|

- Text type

|Construction rule | meaning | example | remarks|
| -------- | -------- | ------ | ------- |
|Paragraph | randomly generates a paragraph ||
|Sentence randomly generates a sentence|
|Text | randomly generate an article | don't fantasize about artificial intelligence, so far you haven't fully understood the meaning of a sentence ||
|Word | randomly generate word | Hello ||
|Locale | randomly generated language / international information | Niu | NZ | national localization code|
|MD5 | randomly generate MD5 | fd80f4681258a9ecb329ab12782dfbba ||
|Password | randomly generate password |) we3jvivb1 | optional parameters: length: password length; special_chars: whether special characters can be used; digits: whether numbers are included; upper_case: whether uppercase letters are included; lower_case: whether lowercase letters are included|
|SHA1 | random SHA1 | e9bb2fcd4b4089cc89c366850ceafe779dbe58 ||
|Sha256 | random sha256 | dd119cb2aec9b3d5557e56bb497757d42f82b32486ea92126942821d3b657957 ||
|Uuid4 | random UUID | 04aff886-8482-4069-9260-7917fd83982d ||

- Character information related

|Construction rule | meaning | example | remarks|
| -------- | -------- | ------ | ------- |
|Name full name Dan Yuzhen|
|Name | female | male full name | official ||
|Name | male | female full name | Xu Ying|
|First name|
|Last| name | surname | pan ||
|First|name|female||
|Last | name | female | surname | Wang ||
|First | name | male | name | strong ||
|Last | name | male | surname | Yang ||
|Age | person age | 23 | default value 0-100|
|Ssn| ID card No. | 350526193807198690||
|Phone number mobile number 13926798387|
|Phonenumber | prefix | mobile number segment | 157 ||
|Profile information||: u'juanpan@hotmail.com '}||

- Miscellaneous

|Construction rule | meaning | example | remarks|
| -------- | -------- | ------ | ------- |
|Color|name|random color name|moccasin||
|Hex color random hex color 7f7cb6|
|RGB color random RGB color 210,85105|