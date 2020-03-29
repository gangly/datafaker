## 8 Precautions
English | [中文](zh_CN/注意事项.md)

#### 1. Construct mass data

If you need to construct a large amount of data, native Python will take a lot of time. Please use pypy to execute datafaker. For example:

```pypy -m datafaker hbase localhost:9090 PIGONE 50000 --meta hbase.txt```

Or multi thread execution, 8 threads generate data, and write PG 2000 pieces of data in batch each time:



```datafaker mysql postgresql+psycopg2://postgres:postgres@localhost/testpg pig_fnumbe_test 100000 --meta meta.txt --worker 8 --batch 2000```



#### 2. Write HBase and report broken pipe

Because the hbase.thrift.server.socket.read.timeout parameter set by HBase is too small, the default is 60 seconds

Therefore, add the configuration in conf/hbase-site.xml:

```

<property>

<name>hbase.thrift.server.socket.read.timeout</name>

<value>600000</value>

<description>eg:milisecond</description>

</property>

```

Restart HBase and thrift

### 3. Support relational database

Most of the examples show MySQL as an example.

Any relational database that supports sqlache can be used, such as PG, Oracle, tidb, redshift, etc.

But the type is RDB, for example:

```datafaker rdb postgresql+psycopg2://postgres:postgres@localhost/testpg pig_fnumbe_test 100000 --meta meta.txt --worker 8 --batch 2000```

Write to Oracle


```

datafaker rdb oracle://root:root@127.0.0.1:1521/helowin stu 10 --meta meta.txt

```

Sqlalchemy connection string must be Oracle: form



### 4. Test situation



|Operating system | Python version | test situation | remarks|
| -------- | -------- | ------ | ------- |
|Mac osx| python2.7 / 3.5 + | pass ||
|Linux | python2.7 | through ||
|Windows10 | python3.6 | via ||



### 5. Write the data I every certain time

You need to set the interval and batch parameters, for example:

```datafaker rdb postgresql+psycopg2://postgres:postgres@localhost/testpg pig_fnumbe_test 100000 --meta meta.txt --interval 0.5 --batch 1```




### XX. Other problems

If you need to write to other data sources, please give me the issue