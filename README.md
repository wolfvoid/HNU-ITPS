# HNU-ITPS
HNU - Intelligent Transportation Prediction System (2024Summer for a Course Project)

## 1 简介

HNU21大三专业综合设计课设。

实现的是一个前端+后端的可视化分析平台，能实现数据采集，预测，呈现

具体实现效果请参考
[文字报告地址](https://blog.csdn.net/qq_39480177/article/details/143454509)

小组成员

- @甘晴void
- @Earnshawn
- @一只快活小散仙
- @想开一点
- @Y++

技术栈

- 前端：java+vue框架
- 后端：python
- 数据库：PostgreSQL

## 2 环境配置

### 2.1 前端

配置前端依赖

```bash
npm install
npm cache clean --force
```

如果报错，请检查node，npm版本是否太低，自行解决。

node版本22.11.0是可以的，但是16不行

npm版本10.9.0是可以的

### 2.2 后端

后端使用python，请确保python版本不要过低，

python 3.11.3是可以的

### 2.3 数据库

请自行配置好PostgreSQL（注意不是MySQL）

需要使用到的SQL文件放在主目录下的data.sql，直接导入即可（若导入出现问题极有可能是因为数据库不对）

## 3 运行

### 3.1 前端

（可以使用vscode等打开）

```bash
npm run server
```

终端会跳出链接，本地浏览器可见。一般是http://localhost:5173/

### 3.2 后端

（可以使用PyCharm等打开）

找到main文件右击运行即可。

## 4 其他

- reference为中间文件，可以提供思路参考
- step_data.txt输入数据，以期待得到预测结果

如果本项目帮到你了，麻烦点个小星星与关注。
