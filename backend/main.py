from flask import Flask, request
from flask_cors import CORS
import psycopg2
from administratorDeal import userManage
from app import app
import loginControl
import password
import pre
import realtime
import vision
from RealtimePredict import predict

if __name__ == '__main__':
    app.run(debug=True)



