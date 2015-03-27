# -*- coding: utf-8 -*-
import urllib
from flask import Flask, jsonify, request
from gensim.models import word2vec

from similar_pick.databases import session
# from sqlalchemy import text
# from similar_pick.models import Restaurant

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/word2vec')
def get_words():

    posi_words = get_arg_words('positive_words')
    nega_words = get_arg_words('negative_words')
    word_and_scores = get_similar_words(posi_words, nega_words)

    res = []
    for word_and_score in word_and_scores:
        obj = {}
        obj['word'] = word_and_score[0]
        obj['score'] = word_and_score[1]
        res.append(obj)

    response = jsonify({'results': res})
    response.status_code = 200
    return response


@app.route('/restaurants/', methods=['GET'])
def get_restrant_list():

    posi_words = get_arg_words('positive_words')
    nega_words = get_arg_words('negative_words')
    word_and_scores = get_similar_words(posi_words, nega_words)

    words = []
    for word_and_score in word_and_scores:
        words.append(word_and_score[0])

    restaurants = search_match_restrant(words)
    restaurant_list = []
    for restaurant in restaurants:
        restaurant_list.append({'name': restaurant.name,
                                'rank': restaurant.rank,
                                'address': restaurant.address,
                                'url': restaurant.url})

    response = jsonify({'results': restaurant_list})
    response.status_code = 200
    return response


def get_arg_words(arg_word):
    words = []
    word_org = request.args.get(arg_word)
    if word_org is not None:
        words = get_decode_word_list(word_org)

    return words


def get_decode_word_list(word_org):
    word_trans = urllib.parse.unquote(word_org)
    words = word_trans.split(',')

    return words


def get_similar_words(posi, nega):
    model = word2vec.Word2Vec.load('data/tabelog_baba.model')
    res = model.most_similar(positive=posi, negative=nega, topn=50)

    return res


def search_match_restrant(words):
    # TODO SQL直書きなのをORMに変更できないか？
    # TODO 単語をOR条件で当てているが、名寄なしでもっといい方法はないか？
    query_string = "SELECT name, address, rank, url FROM restaurant where "
    flag = True

    for word in words:
        print("word = " + word)
        if flag:
            query_string = query_string + "name like '" + word + "'"
            flag = False
        else:
            query_string = query_string + "or name like '" + word + "'"

    restaurants = session.execute(query_string)

    return restaurants


if __name__ == '__main__':
    app.run(debug=True)
    # app.run()
