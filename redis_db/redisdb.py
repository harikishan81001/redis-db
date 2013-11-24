import json

from redis import Redis

from .exceptions import ObjDoesNotExist
from django.core import serializers


class RedisCacheDB(object):
    def __init__(self, key, cache_timeout=300, **conn_kargs):
        self.conn_kwargs = conn_kargs
        self.key = self.get_key(key)
        self.engine = self.get_engine()

    def get_engine(self):
        return Redis(**self.conn_kwargs)

    def get_key(self, key):
        return '%s-%s' % ('[CACHE(V-1)]', key)

    def filter_query(self, filters=None, limit = None):
        data = self.engine.hgetall(self.key)
        data = [eval(each) for each in data.values()]
        resp_list = []
        for each in iter(data):
            if filters:
                passes = True
                for f in filters:
                    if not f(each):
                        passes = False
                        break
                if not passes:
                    continue

            resp_list.append(each)
        return resp_list
    
    @staticmethod
    def gen_lamda(key, val):
        if isinstance(val, int):
            lmd = eval(
                "lambda i: i['fields']['%s'] == %s" % (
                key,val))
        else:
            lmd = eval(
                "lambda i: i['fields']['%s'] == '%s'" % (
                key,val))
        return lmd

    def get_lambda_func(self, **kwargs):
        lmf = []
        for key, val in kwargs.items():
            lmf.append(self.gen_lamda(key, val))
        return lmf

    def deserialize(self, obj_list):
        data = json.dumps(obj_list)
        gen = serializers.deserialize("json", data)
        return [each.object for each in gen]
    
    def serialize(self, obj_list):
        return json.loads(
            serializers.serialize('json', obj_list))
    
    def get_map(self, objs):
        map_dict = {}
        for each in iter(objs):
            map_dict[each['pk']] = each
        return map_dict

