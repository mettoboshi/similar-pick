import urllib
from flask import Flask, jsonify, request
from gensim.models import word2vec

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/restrants/', methods=['GET'])
def get_restrant_list():

    words = request.args.get('words')
    model = word2vec.Word2Vec.load('data/tabelog_baba.model')
    res = model.most_similar(positive=[urllib.parse.unquote(words)])

    response = jsonify({'results': res})
    response.status_code = 200
    return response

if __name__ == '__main__':
    app.run(debug=True)
    # app.run()
