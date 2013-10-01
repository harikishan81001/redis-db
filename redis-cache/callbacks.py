"""
callback function, used as invalidating cache existing data,
can be used as signals callbacks
"""
import json
from django.core import serializers
from django.db.models.signals import (
                                    post_save,
                                    post_delete,
                                    pre_delete,
                                    pre_save)
from .redisdb import RedisCacheDB


class InvalidObj(Exception):
    pass

def cache_invalidator(*args, **kwargs):
    try:
        signal = kwargs['signal']
        model = kwargs['sender']
        instance = kwargs['instance']
        # serializiing model instance in json format
        if isinstance(model, instance):
            obj_dict = serialize_obj(instance)
        else:
            raise InvalidObj(
                'object is not instance of %s' % model.__class__)
        manager = getattr(model, 'cache_objects'):
        if signal == post_save or signal == pre_save:
            if kwargs['created']:
                manager.add_single(obj_dict['id'], obj_dict)
           else:
               manager.modify_obj(obj_dict['id'], obj_dict)     
        elif signal == pre_delete or signal== post_delete:
            manager.delete(obj_dict['id'])
        else:
            raise InvalidObj(
                'type %s signal is not supported ' % signal)
    except KeyError as e:
        raise e('callback does not have sender,'\
            'signal is not configured properly')
    except AttributeError as e:
        raise e('model is not configured properly'\
        'cache_objects attribute missing')
    
def serialize_obj(instance):
    j_list = serializers.serialize('json', [instance])
    j = json.loads(j_list)
    resp = j[0]['fields']
    resp.update({'id': j[0]['pk']}
    return resp

