redis-db
========

ORM for managing cache of django models using redis. Models data can be cached just once and as 
per requirements it can be fetched using filters. 

No-Sql in retrieval of model objects.

  Dependencies:
    
    django >=1.3    [Django](https://www.djangoproject.com/)
    
    redis-py        [Redis-Py](https://github.com/andymccurdy/redis-py)
    
    redis-server    [Redis](http://redis.io/)
    

  User Manual :
    
    from redis_db.manager import CacheManager
    
    class Person(models.Model):
      """
      Person model, contains basic details.
      """
      name = models.CharField(max_length = 255)
      email = models.EmailField(max_length = 100)
      gender = models.ChoiceField(choices = (('M', 'Male'), ('F', 'Female')))
      
      #custom managers
      objects = models.Manager()
      cache_objects = CacheManager(key = 'person-cache')
      
  Creating Cache Data (one time process) 
    
    qs = Person.objects.all()
    Person.cache_objects.store(qs)    # qs can be anything, filtered queryset or model object itself
    
  Retrieving Objects from cache (No-SQL)
  
  1- All objects
      
      objs = Person.cache_objects.all()  # returns list of Person Objects. Note - Gives back list not queryset,
                                         # because querysets itself is lazy query
      
  2 - Filters usage
    
      objs = Person.cache_objects.filter(gender = 'M')   # all male Person's Objects
      
  3 - Get a specific object based on id
    
      obj = Person.cache_objects.get(id= 10) 
    
  
  Note : 

  For non reference objects there is no query at all but in case of ForiegnKey retreival it makes 
  a query to get that object.
  
  
      
