from flask import Flask
import sqlite3
conn = sqlite3.connect('/database/htn2020.db')

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'




