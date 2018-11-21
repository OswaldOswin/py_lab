import requests
import datetime
import time
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
from pprint import pprint as pp
from config import config
from collections import Counter
from igraph import Graph, plot
import numpy as np


user_id = int(input('Enter id: '))

plotly.tools.set_credentials_file(username=config.get('plotly_username'), api_key=config.get('plotly_api_key'))


def get(url: str, params={}, timeout=5, max_retries=5, backoff_factor=0.3) -> dict:
    for i in range(max_retries):
        try:
            response = requests.get(url, params=params)
            return response
        except requests.RequestException:
            time.sleep(timeout)
            timeout = backoff_factor * (2 ** i)


def get_friends(user_id: int, fields = '') -> dict:

    assert isinstance(user_id, int), "user_id must be positive integer"
    assert isinstance(fields, str), "fields must be string"
    assert user_id > 0, "user_id must be positive integer"

    query_params = {
    'domain': config.get('domain'),
    'access_token': config.get('access_token'),
    'v': config.get('v'),
    'user_id': user_id,
    'fields': fields
    }

    query = "{domain}/friends.get?access_token={access_token}&user_id={user_id}&fields={fields}&v={v}".format(**query_params)
    response = get(query)
    return response.json()


def age_predict(user_id: str) -> int:

    assert isinstance(user_id, int), "user_id must be positive integer"
    assert user_id > 0, "user_id must be positive integer"

    #получаем список дат рождения
    dates = []
    ages = []
    data = get_friends(user_id, 'bdate')
    for i in data['response']['items']:
        if i.get('bdate'):
            dates.append(i['bdate'])
    #учитываем только даты с годом
    new = []
    for elem in dates:
        if len(elem) in range(8, 11):
            new.append(elem)
    dates = new
    #считаем возраст друзей
    for elem in dates:
        a = list(map(int, elem.split('.')))
        data = datetime.date(a[2], a[1], a[0])
        age = (datetime.date.today() - data) // 365
        ages.append(age.days)
    #считаем медиану
    if ages:
        ages.sort()
        if len(ages) % 2 == 1:
            return ages[len(ages) // 2]
        else:
            return int((ages[len(ages) // 2 - 1] + ages[len(ages) // 2]) / 2)
    else:
        return 0


def messages_get_history(user_id: int, offset=0, count=200) -> dict:

    assert isinstance(user_id, int), "user_id must be positive integer"
    assert user_id > 0, "user_id must be positive integer"
    assert isinstance(offset, int), "offset must be positive integer"
    assert offset >= 0, "user_id must be positive integer"
    assert count >= 0, "user_id must be positive integer"
    max_count = 200

    query_params = {
    'domain': config.get('domain'),
    'access_token': config.get('access_token'),
    'v': config.get('v'),
    'user_id': user_id,
    'offset': offset,
    'count': min(count, max_count)
    }

    query = "{domain}/messages.getHistory?access_token={access_token}&user_id={user_id}&offset={offset}&count={count}&v={v}".format(**query_params)
    response = get(query)
    data = response.json()
    count = data['response']['count']
    messages = []
    while count > 0:
        query2 = "{domain}/messages.getHistory?access_token={access_token}&user_id={user_id}&offset={offset}&count={count}&v={v}".format(**query_params)
        response2 = get(query2)
        data2 = response2.json()
        messages.extend(data2['response']['items'])
        count -= min(count, max_count)
        query_params['offset'] += 200
        query_params['count'] = min(count, max_count)
        time.sleep(0.3333333334)
    return messages


def count_dates_from_messages(messages: dict) -> list:
    dates = []
    for message in messages:
        dates.append(message['date'])
    for i in range(len(dates)):
        dates[i] = datetime.datetime.fromtimestamp(dates[i]).strftime('%Y-%m-%d')
    if dates:
        return dates


def plotly_messages_freq(dates: list) -> None:
    a = Counter(dates)
    x = list(a.keys())
    y = list(a.values())
    data = [go.Scatter(x=x,y=y)]
    py.iplot(data)

num = get_friends(user_id)['response']['count']
def get_network(user_id, as_edgelist=True):
    edges = []
    ids = []
    for i in range(num):
        print(get_friends(user_id)['response']['items'][i]['id'])
    for i in range(len(ids)):
        time.sleep(0.3333333334)
        temp2 = get_friends(user_id)['response']['items']
        ids2 = [get_friends(ids[i])['response']['items'][l]['id'] for l in range(num)]
        for j in range(len(ids2)):
            if ids[i] == ids2[j]:
                edges.append((i, j))
        return edges


def plot_graph(user_id):
    surnames = []
    for i in range(num):
        surnames.append(get_friends(user_id, 'last_name')['response']['items'])
        time.sleep(0.4)
    edges = get_network(user_id)
    g = Graph(vertex_attrs={"shape": "circle",
                            "label": vertices,
                            "size": 10},
              edges=edges, directed=False)

    n = len(vertices)
    visual_style = {
        "vertex_size": 20,
        "edge_color": "gray",
        "layout": g.layout_fruchterman_reingold(
            maxiter=100000,
            area=n ** 2,
            repulserad=n ** 2)
    }

    clusters = g.community_multilevel()
    pal = igraph.drawing.colors.ClusterColoringPalette(len(clusters))
    g.vs['color'] = pal.get_many(clusters.membership)
    plot(g, **visual_style)


if __name__ == '__main__':
    print('Примерный возраст:', age_predict(user_id))
    plot_graph(141948816)
