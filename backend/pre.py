import psycopg2
from flask import Flask, request, jsonify
from flask_cors import CORS
from app import app, admin
import decimal
import json


# 自定义 JSON 编码器，用于处理 Decimal 类型
class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return float(obj)
        return super(CustomJSONEncoder, self).default(obj)


app.json_encoder = CustomJSONEncoder


@app.route('/pre', methods=['GET'])
def getPre():
    ID = request.args.get('ID')
    Date = request.args.get('Date')
    Time = request.args.get('Start_time')

    page = request.args.get('page', 1)
    page = int(page)

    # 初始化 SQL 查询语句
    sql = "SELECT * FROM xgbr1 WHERE 1=1"

    # 统计符合条件的总记录数
    count_sql = "SELECT COUNT(*) FROM xgbr1 WHERE 1=1"

    if ID:
        sql += f' AND xgbr1."ID" = \'{ID}\''
        count_sql += f' AND xgbr1."ID" = \'{ID}\''
    if Date:
        sql += f' AND xgbr1."Date" = \'{Date}\''
        count_sql += f' AND xgbr1."Date" = \'{Date}\''
    if Time:
        sql += f' AND xgbr1."Start_Time" = \'{Time}\''
        count_sql += f' AND xgbr1."Start_Time" = \'{Time}\''

    # 获取符合条件的总记录数
    cur = admin.cursor()
    cur.execute(count_sql)
    total = cur.fetchone()[0]  # 获取总记录数
    cur.close()

    # 分页处理
    limit = 20
    offset = limit * (page - 1)
    sql += f" LIMIT {limit} OFFSET {offset}"

    # 查询数据
    cur = admin.cursor()
    cur.execute(sql)

    columns = [desc[0] for desc in cur.description]
    res = [
        dict(zip(columns, [
            float(item) if isinstance(item, decimal.Decimal) else
            item  # 处理非Decimal类型的数据
            for item in row
        ]))
        for row in cur.fetchall()
    ]
    cur.close()

    # 构建响应数据
    response = {
        "code": 200,
        "data": {
            "rows": res,
            "total": total  # 返回总记录数
        }
    }

    # 打印响应数据（用于调试）
    print("Response data:", response)
    print("total:", total)
    print("sql:", sql)

    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)