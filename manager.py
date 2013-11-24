import json

from .redisdb import RedisCacheDB
from django.core import serializers


class CacheManager(RedisCacheDB):
    """CacheManager, Models directly intracts with this 
     class.
    """
   
    ################### Setter Functions #####################
    
    def store(self, obj):
        """
        loads multiple data or modify existing one
        """
        if hasattr(obj, '__iter__'):
            data = self.serialize(obj)
        else:
            data = self.serialize([obj])
        map_dict = self.get_map(data)
        return self.engine.hmset(self.key, map_dict)

    def delete(self, *ids):
        """
        can be deleted multiple objects from set using id
        """
        self.engine.hdel(self.key, *ids)

    ####################### Retrieval Functions ##############
    def get(self, id):
        """
        get element by using id
        """
        obj = self.engine.hget(self.key, id)
        if obj:
            obj_dict = eval(obj)
            obj = self.deserialize([obj_dict])[0]
            return obj
        else:
            raise ObjDoesNotExist(
                'Redis does not contain object for %s' % id)

    def all(self):
        """
        get all items for key
        """
        data_list = self.engine.hgetall(self.key).values()
        data_list = [eval(each) for each in data_list]
        return self.deserialize(data_list)

    def count(self):
        """
        number of total objects in model
        """
        return self.engine.hlen(self.key)

    def filter(self, **kwargs):
        """
        filter with specific kwargs
        like name = 'redis' or id=5
        """
        lmdas = self.get_lambda_func(**kwargs)
        resp = self.filter_query(filters=lmdas)
        return self.deserialize(resp)

