import requests
import time
from config import config


def get(url: str, params={}, timeout=5, max_retries=5, backoff_factor=0.3) -> dict:
    for i in range(max_retries):
        try:
            res = requests.get(url, params=params, timeout=timeout)
            return res
        except requests.exceptions.RequestException:
            if i == max_retries - 1:
                raise
            backoff_value = backoff_factor * (2 ** i)
            time.sleep(backoff_value)


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



print(messages_get_history(456246064))
