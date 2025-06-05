class Singleton(object):
    _objs = {}

    def __new__(cls, *args, **kwargs):
        cls_dict = cls._objs.get(cls)
        if cls_dict is not None:
            return cls_dict['obj']

        obj = object.__new__(cls)
        cls._objs[cls] = {'obj': obj, 'init': False}
        setattr(cls, '__init__', cls.decorate_init(cls.__init__))
        return obj

    @classmethod
    def decorate_init(cls, func):
        def init_wrap(*args, **kwargs):
            if not cls._objs[cls]['init']:
                func(*args, **kwargs)
                cls._objs[cls]['init'] = True
            return

        return init_wrap
