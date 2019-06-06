# 北京大学软件工程课程第一组项目

## Demo 地址

[demo](http://222.29.159.164:10018/)

## 文档

+ 见`/doc/最终提交文档`

## 部署

### 后端

```sh
$ git clone

$ conda install --file requirement.txt

$ mysql -u root -p
mysql> CREATE DATABASE SoftwareEngineeringProject;
mysql> ALTER DATABASE SoftwareEngineeringProject CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
mysql> QUIT;

$ vim src/backend/server/settings.py
把 src/backend/server/settings.py 里面第 93-94 行的 DATABASES 设置里的 USER 和 PASSWORD 改为对应的 MySQL 设置

$ python3 src/backend/manage.py makemigrations City User Travel Message

$ python3 src/backend/manage.py migrate

$ python3 src/backend/manage.py shell
>>> from apps.db.City.models import City
>>> City.objects.create(city_id=1, country_name='未设置', province_name='未设置', city_name='未设置', latitude=0, longitude=0)
>>> exit()

$ python3 src/backend/manage.py runserver 127.0.0.1:port
```

### 前端

```sh
$ cd src/frontend/src
$ npm install # 需要预先安装 node, 具体参见 nodejs.org
$ npm run serve
```
