import json
from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/test/')
def hello_test():
    data = '{"b": "test"}'

    print(data)
    print(json.dumps(data))
    return 'Hello World!'

if __name__ == '__main__':
    # app.run(debug=True)
    app.run()
