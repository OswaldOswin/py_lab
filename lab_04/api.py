import requests
import datetime
import plotly
from pprint import pprint as pp
from config import config

user_id = int(input('Enter id: '))

plotly.tools.set_credentials_file(username=config['plotly_username'], api_key=['plotly_api_key'])


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
    'v': config.get['v'],
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
print(age_predict(user_id))


def messages_get_history(user_id: int, offset=0, count=20):

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


def count_dates_from_messages(messages):
    """ Получить список дат и их частот

    :param messages: список сообщений
    """
    messages = messages_get_history(user_id)
    items = messages['response']['items']
    freq_list = []
    for item in items:
        freq_list.append(item['date'])
    for i in range(len(freq_list)):
        freq_list[i] = datetime.datetime.fromtimestamp(freq_list[i]).strftime('%d.%m.%Y')
    return freq_list
print(count_dates_from_messages(messages_get_history(user_id)))


def plotly_messages_freq(freq_list):
    """ Построение графика с помощью Plot.ly

    :param freq_list: список дат и их частот
    """
    data = [go.Scatter(x=freq_list[0], y=freq_list[1])]
    plotly.plotly.plot(data)


def get_network(users_ids, as_edgelist=True):
    pass

def plot_graph(graph):
    # PUT YOUR CODE HERE
    pass
