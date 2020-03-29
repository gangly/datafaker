## 6、command parameters
English | [中文](docs/zh_CN/命令参数.md)


The datafaker parameter contains 4 mandatory parameters and some optional parameters, as shown in the following table.

| parameter name | meaning |  type | required | Defaults | note |
| ------ | ------ | ------ | ----- | ------| ---- |
| dbtype| Data source type | string | Yes | None | The optional value is rdb, hive, kafka, hbase, es, file |
| connect | connection information | string| Yes | None | sqlachemy string for relational database and hive. <br>broker string for kafka<br>file path for file type<br>thrift host and port for hbase|
| table| table name | string | Yes |  None | Abstract various data source operation units are abstracted into tables, tables in the database, topics in kafka, file names, hbase columns, mongos as collections|
| num | records number | int | Yes | None | must be 1 for kafka |
| auth | account and password | string | No | None | split by `:`, such as admin:12334 |
| meta | meta data file | string | No | None |  |
| interval | interval | float | No | 1 | second unit |
| version | Display version number | bool | No |  None |  |
| outprint | Whether to print on the screen | bool | No |  false | If the screen is set to print, the data will not be written to a file or data source. |
| outspliter | Data field spliter | string | No | comma | Screen printing and save to files is valid |
| locale | Language type | string | No | zh_CN | support for en_US and zh_CN|
| format | data format | string | No |  text |  json for kafka|
| withheader | Print and store to file with header | bool | No | False| |
| batch | the size for batch write to data source | int | No | 1000 |  |
| workers | the parallel threads for generating data | int | No | 4 |  |