import logging
import json


def short_detail(data):
    data = json.loads(data)
    return data['uptime']


def full_detail(data):
    data = json.loads(data)
    return '\n'.join(['%s: %s' % (k, v) for k, v in data.iteritems()])


def get_from_system(params):
    pass
