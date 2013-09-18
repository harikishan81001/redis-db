from redis import Redis

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
        data = self.all()
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

    def get_lambda_func(self, **kwargs):
        lmf = []
        for key, val in kwargs.items():
            if isinstance(val, int):
                lmf.append(eval("lambda i: i['%s'] == %s" % (key,val)))
            else:
                lmf.append(eval("lambda i: i['%s'] == '%s'" % (key,val)))
        return lmf

    def initial_set(self, data_list):
        """
        loads multiple data dicts in single hit
        """
        map_dict = {}
        try:
            for each in iter(data_list):
                if isinstance(each, dict):
                    map_dict.update({each['id']:each})
        except KeyError:
            raise
        return self.engine.hmset(self.key, map_dict)


    ################### Setter Functions #####################

    def add_multiple(self, obj_list):
        """
        loads multiple data or modify existing one
        """
        return self.initial_set(data_list=obj_list)

    def add_single(self, id, data):
        """
        add single object dict in pool of objects
        """
        return self.engine.hset(self.key, id, data)

    def modify_obj(self, id, obj_dict):
        """
        modify existing object
        """
        self.engine.hset(self.key, id, obj_dict)

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
            obj = eval(obj)
        return obj

    def all(self):
        """
        get all items for key
        """
        data_dict = self.engine.hgetall(self.key)
        json_list = []
        keys = data_dict.keys()

        for each in iter(keys):
            json_list.append(eval(data_dict[each]))
        return json_list

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
        return self.filter_query(filters=lmdas)
