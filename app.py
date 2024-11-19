from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
   return 'Hello World! - 19/11/2024 update'
