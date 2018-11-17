import requests
import datetime
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


def get(url, params={}, timeout=5, max_retries=5, backoff_factor=0.3):

    for retry in range(max_retries):
        try:
            response = requests.get(url, params=params, timeout=timeout)
            return response
        except requests.exceptions.RequestException:
            if retry == max_retries - 1:
                raise
            backoff_value = backoff_factor * (2 ** retry)
            time.sleep(backoff_value)


def get_friends(user_id: int, fields: str) -> dict:

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
    response = requests.get(query)
    return response.json()


def age_predict(user_id: str) -> int:

    assert isinstance(user_id, int), "user_id must be positive integer"
    assert user_id > 0, "user_id must be positive integer"

    #получаем список дат рождения
    dates = []
    ages = []
    data = get_friends(user_id, 'bdate')
    friends = data['response']['items']
    num = data['response']['count']
    for i in range(num):
        if friends[i].get('bdate'):
            dates.append(friends[i]['bdate'])
    #учитываем только даты с годом
    new = []
    for elem in dates:
        if len(elem) in range(8, 11):
            new.append(elem)
        dates = new
    #считаем возраст друзей
    for elem in dates:
        b = []
        a = elem
        b = a.split('.')
        for i in range(3):
            b[i] = int(b[i])
        data = datetime.date(b[2], b[1], b[0])
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
print(age_predict(116913967))


def messages_get_history(user_id: int, offset=0, count=20) -> dict:

    assert isinstance(user_id, int), "user_id must be positive integer"
    assert user_id > 0, "user_id must be positive integer"
    assert isinstance(offset, int), "offset must be positive integer"
    assert offset >= 0, "user_id must be positive integer"
    assert count >= 0, "user_id must be positive integer"

    query_params = {
    'domain': config.get('domain'),
    'access_token': config.get('access_token'),
    'v': config.get('v'),
    'user_id': user_id,
    'offset': offset,
    'count': count
    }

    query = "{domain}/messages.getHistory?access_token={access_token}&user_id={user_id}&offset={offset}&v={v}".format(**query_params)
    response = requests.get(query)
    messages = response.json()
    return messages


def count_dates_from_messages(messages: dict) -> list:
    messages = messages_get_history(user_id)
    items = messages['response']['items']
    dates = []
    for item in items:
        dates.append(item['date'])
    for i in range(len(dates)):
        dates[i] = datetime.datetime.fromtimestamp(dates[i]).strftime('%Y-%m-%d')
    if dates:
        return dates
    else:
        return [0]

def plotly_messages_freq(dates):
    a = Counter(dates)
    x = list(a.keys())
    y = list(a.values())
    data = [go.Scatter(x=x,y=y)]
    py.iplot(data)
#plotly_messages_freq(count_dates_from_messages(messages_get_history(user_id)))

def get_network(user_id=config.get('my_id'), as_edgelist=True):
    id_list = get_friends(user_id)['response']['items']
    edges = [(0,2),(0,1),(0,3),
    (1,0),(1,2),(1,3),
    (2,0),(2,1),(2,3),(2,4),
    (3,0),(3,1),(3,2),
    (4,5),(4,6),
    (5,4),(5,6),
    (6,4),(6,5)]

    g = Graph(vertex_attrs={"label":vertices},
    edges=edges, directed=False)

    N = len(vertices)
    visual_style = {}
    visual_style["layout"] = g.layout_fruchterman_reingold(
    maxiter=1000,
    area=N**3,
    repulserad=N**3)

    plot(g, **visual_style)

    g.simplify(multiple=True, loops=True)

    pal = igraph.drawing.colors.ClusterColoringPalette(len(clusters))
    g.vs['color'] = pal.get_many(clusters.membership)


def plot_graph(graph):
    # PUT YOUR CODE HERE
    pass
