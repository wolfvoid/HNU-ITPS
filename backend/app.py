import psycopg2
from flask import Flask, request
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

admin = psycopg2.connect(dbname='postgres', user='postgres', password='020212', host='localhost')
user = psycopg2.connect(dbname='postgres', user='postgres', password='020212', host='localhost')



if __name__ == "__main__":
    print("hello world")
    # cur = admin.cursor()
    # sql = "SELECT getbooks();"
    # cur.execute(sql)
    # print(cur.fetchall())