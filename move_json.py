import os
import sys

import requests
from flask import Flask, request, make_response

import json
import math
from urllib.request import urlopen
from urllib.parse import urlencode
from datetime import datetime
from datetime import timedelta


class BoxOffice(object):
    base_url = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/' \
               'searchDailyBoxOfficeList.json'

    def __init__(self, api_key):
        self.api_key = api_key

    def get_movies(self):
        target_dt = datetime.now() - timedelta(days=1)
        target_dt_str = target_dt.strftime('%Y%m%d')
        query_url = '{}?key={}&targetDt={}'.format(self.base_url, self.api_key, target_dt_str)
        with urlopen(query_url) as fin:
            return json.loads(fin.read().decode('utf-8'))

    def simplify(self, result):
        return [
            {
                'rank': entry.get('rank'),
                'name': entry.get('movieNm'),
                'code': entry.get('movieCd')
            }
            for entry in result.get('boxOfficeResult').get('dailyBoxOfficeList')
        ]


app = Flask(__name__)

@app.route('/', methods=['POST'])
def get_movie():
    data = request.get_json()

    if data["messenger user id"]:
        res = make_response(movie_info())
        res.headers['Content-Type'] = 'application/json'

    return res


def movie_info():
    box_office = BoxOffice("7d1ea7cad554680a8378ef94a52f29d7")
    movies = box_office.simplify(box_office.get_movies())
    rank_message = ', '.join(['{}. {}'.format(m['rank'], m['name']) for m in movies])

    message = '현재 박스오피스 순위: \n{}'.format(rank_message)

    data = json.dumps({
        "messages": [
            {"text": message},
        ]}, ensure_ascii=False)

    return data


if __name__ == "__main__":
    app.run()
