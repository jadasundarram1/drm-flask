from flask import Flask

app = Flask(__name__)
app.debug = True

@app.route('/')
def hello():
    return 'Hello, World!'

