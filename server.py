#!flask/bin/python
import json
from flask import Flask, jsonify
from scrapy_novatec import Scrapy_novatec

app = Flask(__name__)

scrapy = Scrapy_novatec()

@app.route('/book/lancamento', methods=['GET'])
def lancamento():
    books = scrapy.getLancamentoBooks()
    json_string = json.dumps([ob.__dict__ for ob in books])

    return json_string


@app.route('/book/proximos', methods=['GET'])
def proximo():
    books = scrapy.getEmBreve()
    json_string = json.dumps([ob.__dict__ for ob in books])
    return json_string



@app.route('/book/categoria', methods=['GET'])
def categoria():
    books = scrapy.getByCategory()
    json_string = json.dumps(books)
    return json_string



if __name__ == '__main__':
    app.run(debug=True)
