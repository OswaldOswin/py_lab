import requests
from datetime import datetime
import plotly
from datetime import datetime, timedelta


config = {
    'VK_ACCESS_TOKEN': 'Tокен доступа для ВК',
    'PLOTLY_USERNAME': 'Имя пользователя Plot.ly',
    'PLOTLY_API_KEY': 'Ключ доступа Plot.ly'
}


'''def get(url, params={}, timeout=5, max_retries=5, backoff_factor=0.3):
    """ Выполнить GET-запрос

    :param url: адрес, на который необходимо выполнить запрос
    :param params: параметры запроса
    :param timeout: максимальное время ожидания ответа от сервера
    :param max_retries: максимальное число повторных запросов
    :param backoff_factor: коэффициент экспоненциального нарастания задержки
    """
    '''


def get_friends(user_id: int, fields: str):
    """ Вернуть данных о друзьях пользователя

    :param user_id: идентификатор пользователя, список друзей которого нужно получить
    :param fields: список полей, которые нужно получить для каждого пользователя
    """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert isinstance(fields, str), "fields must be string"
    assert user_id > 0, "user_id must be positive integer"

    domain = "https://api.vk.com/method"
    access_token = 'ebff99b08bbfe1123bc27d71e7eb39e692586f3465641f777ef3636b3fa4517747fc98828cd9e49db37e0'

    query_params = {
    'domain': domain,
    'access_token': access_token,
    'user_id': user_id,
    'fields': fields
    }

    query = "{domain}/friends.get?access_token={access_token}&user_id={user_id}&fields={fields}&v=5.53".format(**query_params)
    response = requests.get(query)
    return response


def age_predict(user_id):
    """ Наивный прогноз возраста по возрасту друзей

    Возраст считается как медиана среди возраста всех друзей пользователя

    :param user_id: идентификатор пользователя
    """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert user_id > 0, "user_id must be positive integer"

    num = get_friends(141948816, 'bdate').json()['response']['count']
    a = []
    for i in range(num):
        a.append(get_friends(141948816, 'bdate').json()['response']['items'][i]['bdate'])
    return a
num = get_friends(141948816, 'bdate').json()['response']['count']
a = []
for i in range(num):
    a.append(get_friends(141948816, 'bdate').json()['response']['items'][i]['bdate'])
print(a)



def messages_get_history(user_id, offset=0, count=20):
    """ Получить историю переписки с указанным пользователем

    :param user_id: идентификатор пользователя, с которым нужно получить историю переписки
    :param offset: смещение в истории переписки
    :param count: число сообщений, которое нужно получить
    """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert user_id > 0, "user_id must be positive integer"
    assert isinstance(offset, int), "offset must be positive integer"
    assert offset >= 0, "user_id must be positive integer"
    assert count >= 0, "user_id must be positive integer"
    # PUT YOUR CODE HERE
    pass

def count_dates_from_messages(messages):
    """ Получить список дат и их частот

    :param messages: список сообщений
    """
    pass
    # PUT YOUR CODE HERE


def plotly_messages_freq(freq_list):
    """ Построение графика с помощью Plot.ly

    :param freq_list: список дат и их частот
    """
    pass
    # PUT YOUR CODE HERE


def get_network(users_ids, as_edgelist=True):
    # PUT YOUR CODE HERE
    pass

def plot_graph(graph):
    # PUT YOUR CODE HERE
    pass
