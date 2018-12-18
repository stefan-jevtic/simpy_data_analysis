from flask import Flask, jsonify
from International.ProductInfo.Analysis import ProductAnalysis
from International.Keywords.Analysis import KeywordsAnalysis
app = Flask(__name__)


@app.route('/<type>/<country>/<id>', methods=['GET', 'POST'])
def index(type, country, id):
    if type == 'product':
        return product(country, id)
    elif type == 'kw':
        return keyword(country, id)
    elif type == 'cat':
        return categry(country, id)
    else:
        return 404


def product(country, id):
    a = ProductAnalysis(country, id, 'web')
    data = a.analyze()
    return jsonify(data)


def keyword(country, id):
    a = KeywordsAnalysis(country, id, 'web')
    data = a.analyze()
    return jsonify(data)


def categry(country, id):
    pass
