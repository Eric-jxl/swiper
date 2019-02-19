from django.db import models
from django.core.cache import cache

from common import keys


def to_dict(self, *exclude):
    '''
    将 model 对象转换成一个属性字典

    exclude: 需要排出的字段名
    '''
    attr_dict = {}
    for field in self._meta.fields:
        field_name = field.attname
        if field_name not in exclude:
            attr_dict[field_name] = getattr(self, field_name)
    return attr_dict


def get(cls, *args, **kwargs):
    """先从缓存获取数据，缓存中没有，总数据库获取"""
    pk = kwargs.get('id') or kwargs.get('pk')  # 获取主键的值
    if pk is not None:
        key = keys.MODEL % (cls.__name__, pk)  # 定义缓存 key
        # 从缓存中获取数据
        model_obj = cache.get(key)
        if isinstance(model_obj, cls):
            return model_obj

    # 缓存里没有，从数据库获取
    model_obj = cls.objects.get(*args, **kwargs)

    # 将取出的数据写入缓存
    key = keys.MODEL % (cls.__name__, model_obj.pk)
    cache.set(key, model_obj)

    return model_obj


def get_or_create(cls, defaults=None, **kwargs):
    """为 objects.get_or_create 添加缓存处理"""
    pk = kwargs.get('id') or kwargs.get('pk')  # 获取主键的值
    if pk is not None:
        key = keys.MODEL % (cls.__name__, pk)  # 定义缓存 key
        # 从缓存中获取数据
        model_obj = cache.get(key)
        if isinstance(model_obj, cls):
            return model_obj, False

    # 缓存里没有，执行原来的 get_or_create
    model_obj, created = cls.objects.get_or_create(defaults, **kwargs)

    # 将取出的数据写入缓存
    key = keys.MODEL % (cls.__name__, model_obj.pk)
    cache.set(key, model_obj)

    return model_obj, created


def save(self, force_insert=False, force_update=False, using=None,
         update_fields=None):
    '''添加了缓存处理的 save 方法'''
    # 先将数据通过原 save 方法保存到数据库
    self._save(force_insert=False, force_update=False, using=None, update_fields=None)

    # 将 model 对象存入缓存
    key = keys.MODEL % (self.__class__.__name__, self.pk)
    cache.set(key, self)


def patch_model():
    '''通过 MonkeyPatch 的方式为 Model 对象打补丁'''
    # 动态为 Model 增加方法
    models.Model.to_dict = to_dict
    models.Model.get = classmethod(get)
    models.Model.get_or_create = classmethod(get_or_create)

    # 修改原 save 方法
    models.Model._save = models.Model.save
    models.Model.save = save
