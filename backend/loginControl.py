import psycopg2
from flask import Flask, request
from flask_cors import CORS
from app import app,admin

@app.route('/login', methods=['POST'])
def postLogin():
    jdata = request.json
    print(jdata)
    _type = jdata["type"]
    _username = jdata["username"]
    _userid = jdata["userid"]
    _password = jdata["password"]

    cur = admin.cursor()
    if(_type == 0):  
        sql = f"SELECT * FROM administrator WHERE adid = '{_userid}' AND password = '{_password}'"
        cur.execute(sql)
        res = cur.fetchall()
        if res:
            name = res[0][1]
            id = res[0][0]
            cur.close()
            return {
                "code":200,
                "data":{
                    "type":_type,
                    "username": name,
                    "userid":id,
                    }
            }
        else:
            cur.close()
            return{
                "code":401,
                "msg":"密码输入错误或没有创建账户",
                "data":None
            }
    else:
        sql = f"SELECT * FROM users WHERE userid = '{_userid}' AND password = '{_password}'"
        cur.execute(sql)
        res = cur.fetchall()
        print('here',res)
        if res:
            name = res[0][0]
            id = res[0][1]
            cur.close()
#            print(name)
            return {
                "code":200,
                "data":{
                    "type":_type,
                    "username": name,
                    "userid":id,
                    }
                }
        else:
            cur.close()
            return{
                "code":401,
                "msg":"密码输入错误或没有创建账户",
                "data":None
            }