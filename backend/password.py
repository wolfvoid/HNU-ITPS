from flask import Flask, request
from flask_cors import CORS
from app import app , admin

@app.route('/password/admin', methods=['PUT'])
def passwordadmin():
    data = request.json
#    print(data)
    daid = data["oldData"]["userid"]
    new_password = data["newData"]["password"]

    sql = "UPDATE administrator SET password = %s WHERE adid = %s"
    cur = admin.cursor()
    cur.execute(sql, (new_password,daid))
    admin.commit()
    status = cur.rowcount
    # 关闭游标
    cur.close()
    if status > 0:
#        print("插入成功")
        return {
            "code": 200,
            "data": True
        }
    else:
#        print("插入失败")
        return {
            "code": 201,
            "data": False,
            "msg":'修改失败'
        }
    

@app.route('/password/user', methods=['PUT'])
def passworduser():
    data = request.json
    userid = data["oldData"]["userid"]
    new_password = data["newData"]["password"]

    sql = "UPDATE users SET password = %s WHERE userid = %s"
    cur = admin.cursor()
    cur.execute(sql, (new_password,userid))
    admin.commit()
    status = cur.rowcount
    # 关闭游标
    cur.close()
    if status > 0:
#        print("插入成功")
        return {
            "code": 200,
            "data": True
        }
    else:
#        print("插入失败")
        return {
            "code": 201,
            "data": False,
            "msg":'修改失败'
        }