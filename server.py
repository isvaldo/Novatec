#!flask/bin/python
import json
from flask import Flask, jsonify
from scrapy_novatec import ScrapyNovatec

app = Flask(__name__)

scrapy = ScrapyNovatec()


@app.route('/book/launch', methods=['GET'])
def launch():
    books = scrapy.get_launch_books()
    json_string = json.dumps(books)

    return json_string


@app.route('/book/next_launch', methods=['GET'])
def next_launch():
    books = scrapy.get_next_launch()
    json_string = json.dumps(books)
    return json_string


@app.route('/book/category/<id>/<page>', methods=['GET'])
def category(id, page=0):
    books = scrapy.get_by_category(id, page)
    json_string = json.dumps(books)
    return json_string


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
