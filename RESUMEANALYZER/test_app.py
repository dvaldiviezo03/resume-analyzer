# test_app.py
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    print(">>> Hello route hit")
    return "Hello World!"

if __name__ == '__main__':
    print(">>> Starting minimal app")
    app.run(debug=True)
