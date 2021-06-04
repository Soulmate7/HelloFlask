# Python FLask框架入门学习

> 本项目用于学习使用Flask框架搭建不同功能的网页,仅供参考，欢迎交流

- [简介](#简介)
- [HelloFlask](#HelloFlask)
- [Flask框架之模版](#Flask框架之模版)
- [添加人脸识别系统](#添加人脸识别系统)
- [Flask框架之数据库](#Flask框架之数据库)
    - [连接数据库](#连接数据库)
        - [flask_sqlalchemy](#flask_sqlalchemy)
        - [pymysql](#pymysql)
- [参考资料](#参考资料)

## 简介
Flask支持各种关系数据库，也支持图数据库Neo4J，扩展功能交友给第三方开发
若你不仅仅只是想编辑代码文档，而是开发出一款集成软件，那么Flask就是一个好的选择

- 安装

`pip install flask`

---

## HelloFlask

在认识了FLask后，我们先来写一个简单的flask程序
``` python
#1
from flask import Flask
app=Flask(__name__)
#2
@app.route('/')
def index():
    return '<h1>Hello Flask!</h1>'
#3
if __name__=='__main__':
    app.run(debug=True)
```
 #1第一部分**初始化**：所有的Flask都必须创建程序实例，web服务器使用wsgi协议，把客户端所有的请求都转发给这个程序实例,程序实例是Flask的对象，一般情况下用如下方法实例化Flask类只有一个必须指定的参数，即程序主模块或者包的名字，__name__是系统变量，该变量指的是本py文件的文件名"""
 
 #2第二部分**路由和视图函数**：客户端发送url给web服务器，web服务器将url转发给flask程序实例，程序实例需要知道对于每一个url请求启动那一部分代码，所以保存了一个url和python函数的映射关系。处理url和函数之间关系的程序，称为路由在flask中，定义路由最简便的方式，是使用程序实例的app.route装饰器，把装饰的函数注册为路由,在访问网页时，也要添加相应的路径。'/'则是根目录。

 #3第三部分**程序实例用run方法启动flask集成的开发web服务器**：__name__ == '__main__'是python常用的方法，表示只有直接启动本脚本时候，才用app.run方法如果是其他脚本调用本脚本，程序假定父级脚本会启用不同的服务器，因此不用执行app.run()服务器启动后，会启动轮询，等待并处理请求。轮询会一直请求，直到程序停止。值得注意的是，run()可以添加参数`debug=True`,它能够在代码出错时及时将错误返回到网页上

在了解了代码的基本框架后，我们运行py文件，打开链接，发现Hello Flask被打印在页面上
![hello](image/hello.png)

这是因为Flask调用**视图函数**后，会将其返回值作为**响应内容**，作为**HHTML页面**返回客户端

---

## Flask框架之模版
`import render_template`

模版包括相应文本的文件，用真值替换变量，返回响应字符串，过程即渲染

我们在目录下建立一个**templates**子目录，在这里我们存放我们的模版

尝试编辑一个index.html

``` html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Jinja2模版</title>
</head>
<body>
<h1>Hello,{{name}}!</h1>
</body>
</html>
```

然后在py文件中修改index()
``` python
def index():
    return render_template('index.html',name='Flask')
```

这样，我们就得到了和之前一样的效果
其中{{name}}表示一个变量，从渲染模版的数据中取值

- 条件控制语句
```
{% if user %}
Hello, {{ user }}!
{% else %}
Hello, Stranger!
{% endif %}

<ul>
{% for comment in comments %}
<li>{{ comment }}</li>
{% endfor %}
</ul>
```

---

## 添加人脸识别功能

在学习了flask的基础框架和开发后，我们来尝试将人脸识别功能加入到flask中运行

[人脸识别的入门学习](http://47.93.252.206/%e4%ba%ba%e8%84%b8%e8%af%86%e5%88%ab%e7%9a%84%e5%85%a5%e9%97%a8%e5%ad%a6%e4%b9%a0/)

在index.py中，添加人脸识别函数detect()，并返回一张识别并处理过后的图片。
在函数index()，我们传入原始图片（这个操作也可以由用户在网页端实现，这里按下不表）并返回处理后的图片，将其传入模版之中，然后将其作为响应内容，显示为HTML页面返回客户端

``` python
from flask import Flask,render_template
import cv2

app=Flask(__name__)

@app.route('/')
def index():
    outname=detect('static/101.png')
    return render_template('index.html',outname=outname)

def detect(filename):
    face_cascade = cv2.CascadeClassifier('/Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/cv2/data/haarcascade_frontalface_default.xml')

    img = cv2.imread(filename)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        img = cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
    outname='static/101.png'
    cv2.imwrite(outname,img)
    return outname


if __name__=='__main__':
    app.run()
```

``` html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>媒体大数据</title>
</head>
<body>
我的老婆赖小七，亲亲抱抱举高高
<img src="{{outname}}" />
</body>
</html>
```

- 效果

![face](image/face.png)

可以看到，我们利用flask实现了一个简单的人脸识别，当然在这里仅仅只是将返回值打印在了页面上，我们依然可以去优化程序，可以让用户来上传或者拍摄图片，然后对图片进行人脸识别，接着和数据库的人脸进行匹配，最后返回匹配结果到页面。

---

## Flask框架之数据库

- 模块安装

``` bash
pip install flask_sqlalchemy
pip install pymysql
```

Flask-SQLAlchemy 是一个 Flask 扩展， 它简化了在 Flask 应用程序中对SQLAlchemy的使用。

### 连接数据库

#### flask_sqlalchemy

``` python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)

app.config['SECRET_KEY']='yoursecret'
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:yoursecret@127.0.0.1:3306/DataVisual'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN']=True
db=SQLAlchemy(app)
#用户名:root
#密码:yoursecret
#IP地址:127.0.0.1
#端口:3306
#数据库名:DataVisual
```

- 创建数据表
``` python
#创建数据表roles
class Role(db.Model):
    __tablename__='roles'
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(64),unique=True)
    users=db.relationship('User',backref='role',lazy='dynamic')

    def __repr__(self):#显示一个可读字符串
        return '<Role %r>' %self.name

#创建数据表users
class User(db.Model):
    __tablename__='users'
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(64),unique=True,index=True)
    role_id=db.Column(db.Integer,db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>'%self.username

#执行数据库
if __name__=='__main__':
    db.drop_all()
    db.create_all()
    app.run()
```

- 增删改查
``` python
#增
admin_role=Role(name='Admin')
user_role=Role(name='User')
user_cuc=User(username='cuc',role=admin_role)
user_dviz=User(username='dviz',role=user_role)
db.session.add_all([admin_role,user_role,user_cuc,user_dviz])
#提交会话到数据库
db.session.commit()

#改
admin_role.name='Administrator'
db.session.add(admin_role)
db.session.commit()

#删
db.session.delete(user_role)#从数据库中删除'user'角色
db.session.commit()

#查
print(user_role)
print(admin_role)
print(User.query.filter_by(role=user_role).all())
```

#### pymysql

现在我们再来使用pymysql模块来进行对数据库的操作
``` python
import pymysql
from flask import Flask,render_template,request

app=Flask(__name__)

@app.route('/search')
#由于route改变，此时我们的路径就发生了变化:http://127.0.0.1:5000/search
def search():#查询函数
    wanted=request.args.get("wanted",type=str)
    #从模块获取查询单词
    if wanted == None:
        wanted='pineapple'#默认单词

    db=pymysql.connect(host='localhost',user='root',passwd="z1012194891",db="DataVisual",charset="utf8")
    #链接数据库，注意参数一定要按照顺序显示，前面添加参数名
    cursor=db.cursor()
    try:
        sql="SELECT * FROM DataVisual.map_enword where english like '%"+wanted+"%'"
        #执行sql语句
        cursor.execute(sql)
        #返回结果
        rs=cursor.fetchall()
        rs=list(rs)
        print(rs)
    except:
        #错误处理
        rs='db-error'
        print('py-db-error')
    #断开数据库连接
    db.close()
    #将结果返回到模版中渲染，并传入查询结果
    return render_template('english.html',rs=rs)

if __name__=='__main__':
    app.run(debug=True)
```

- 效果

查询含有tion的单词

![单词查询](image/english.png)

---

后续待更新...

---

##参考资料
https://www.cnblogs.com/chaojiyingxiong/p/9549987.html