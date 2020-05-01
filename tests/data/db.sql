create table stu (
	id int unsigned auto_increment primary key COMMENT '自增id',
	name varchar(20) not null comment '学生名字',
	school varchar(20) not null comment '学校名字',
	nickname varchar(20) not null comment '学生小名',
	age int not null comment '学生年龄',
	class_num int not null comment '班级人数',
	score decimal(4,2) not null comment '成绩',
	phone int(20) not null comment '电话号码',
	email varchar(64) comment '家庭网络邮箱',
	ip varchar(32) comment 'IP地址',
	address text comment '家庭地址'
) engine=InnoDB default charset=utf8;

