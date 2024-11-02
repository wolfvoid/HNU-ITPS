from flask import Flask, request
from flask_cors import CORS
from app import app , admin

#处理查询用户请求
@app.route('/user', methods=['GET'])
def get_users():
    page = request.args.get('page')
    page = int(page)
    username = request.args.get('username')
    userid = request.args.get('userid')
    phonenumber = request.args.get('phonenumber')
    password = request.args.get('password')
#    print(username, userid, phonenumber, password)

    #构建 SQL 查询语句
    sql = "SELECT * FROM users WHERE 1=1"  #初始查询语句

    cur = admin.cursor()
    tsql = sql
    cur.execute(tsql)
    total = cur.rowcount
    cur.close()
#    print(total)
    is_all = True
    # 根据参数拼接条件
    if username:
        sql +=f" AND users.username='{username}'"
        is_all = True
    if userid:
        sql +=f" AND users.userid='{userid}'"
        is_all = True
    if phonenumber:
        sql +=f" AND users.phonenumber='{phonenumber}'"
        is_all = True
    if password:
        sql +=f" AND users.password='{password}'"
        is_all = True

# print(sql)
    limit = 20
    offset = limit * (page - 1)
    new_sql = f"{sql} LIMIT {limit} OFFSET {offset}"
    cur = admin.cursor()
    cur.execute(new_sql)
    if is_all:
        total = cur.rownumber
    # 获取所有列名
    columns = [desc[0] for desc in cur.description]
    #将元组列表转换为字典列表
    res = [dict(zip(columns, row)) for row in cur.fetchall()]
#    print(res)
    cur.close()
    return {
        "code": 200,
        "data": {
            "rows": res,
            "total": total
        }
    }

#处理添加用户请求
@app.route('/user', methods=['POST'])
def postuser():
    json_data = request.json
#    print(json_data)

    username = json_data["username"]
    userid = json_data["userid"]
    #password = json_data["password"]
    password ="123"
    phonenumber = json_data["phonenumber"]

    # json_data中的数据 就是 前端界面中按下添加按钮后出现的所有数据
    # 数据取你需要的即可
    # 将数据插入数据库
    #sql语句

    sql = "INSERT INTO users (username, userid, phonenumber,password) VALUES (%s, %s, %s, %s) "
    values = (username, userid, phonenumber, password)

    cur = admin.cursor()
    cur.execute(sql, values)
    #提交事物
    admin.commit()
    status = cur.rowcount
    cur.close()
    if status > 0:
        return {
            "code": 200,
            "data": True
        }
    else:
        return {
            "code": 500,
            "data": False,
            "msg":"添加失败"
        }



#处理删除用户请求
@app.route('/user', methods=['DELETE'])
def delete_user():
    username = request.args.get('username')
    userid = request.args.get('userid')
    # 以上为数据获取方法展示
    # delete请求 的参数获取方法和get请求一样
    # delete请求 中的数据 就是 前端页面上 delete 按钮所在行的数据

    sql = "DELETE FROM users WHERE username=%s AND userid=%s" # 根据数据确定sql语句
    values = (username, userid)
    cur = admin.cursor()
    cur.execute(sql,values)
    admin.commit()
    status = cur.rowcount
    cur.close()
    if status > 0:
        return {
            "code": 200,
            "data": True
        }
    else:
        return {
            "code": 500,
            "data": False,
            "msg":"删除失败"
        }


# 处理修改用户信息请求
@app.route('/user', methods=['PUT'])

def update_user():
    json_data = request.json
    #    print(json_data)

    old_phonenumber = json_data["oldData"]["phonenumber"]
    old_username = json_data["oldData"]["username"]
    old_userid = json_data["oldData"]["userid"]
    # 以上为数据获取方法展示
    # oldData 的所有数据 就是 前端界面按下编辑按钮前出现的所有选项（修改前的）
    new_phonenumber = json_data["newData"]["phonenumber"]
    #new_password =json_data["newData"]["password"]
    new_username = json_data["newData"]["username"]
    new_userid = json_data["newData"]["userid"]
    # 以上为数据获取方法展示
    # newData 的所有数据 就 前端界面按下编辑按钮后出现的所有选项（修改后的）
    # 新老数据取你需要的即可



    #sql = "SELECT * FROM users WHERE users.phonenumber= %s "  # 根据 oldData 确定需要修改的记录，并用新的数据替换之
    #values=(old_phonenumber)
    cur = admin.cursor()
    #cur.execute(sql, values)
    if old_phonenumber or old_username or old_userid:
        new_sql = "UPDATE users SET username=%s, userid=%s, phonenumber=%s WHERE username=%s AND userid=%s AND phonenumber=%s"
        values=(new_username, new_userid, new_phonenumber, old_username, old_userid, old_phonenumber)
        cur.execute(new_sql, values)
        admin.commit()

    status = cur.rowcount
    cur.close()
    if status > 0:
        return {
            "code": 200,
            "data": True
        }
    else:
        return {
            "code": 500,
            "data": False,
            "msg":"删除失败"
        }