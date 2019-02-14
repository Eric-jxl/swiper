import re
import os
from random import randrange

import requests
from django.core.cache import cache
from django.conf import settings

from swiper import config
from common import keys


def is_phonenum(phonenum):
    '''检查参数是否是手机号'''
    pattern = r'(13\d|15[012356789]|166|17[78]|18[0126789]|199)\d{8}$'
    return True if re.match(pattern, phonenum) else False


def gen_random_code(length=4):
    '''产生随机码'''
    code = randrange(10 ** length)
    template = '%%0%dd' % length
    return template % code


def send_vcode(phonenum):
    '''向第三方平台发送验证码'''
    vcode = gen_random_code()
    # 将验证码存入缓存，并设置过期时间
    cache.set(keys.VCODE % phonenum, vcode, 180)

    params = config.YZX_SMS_PARAMS.copy()
    params['mobile'] = phonenum
    params['param'] = vcode
    response = requests.post(config.YZX_SMS_API, json=params)

    if response.status_code == 200:
        result = response.json()
        print(result)
        if result.get('msg') == 'OK':
            return True
    return False


def save_upload_file(filename, upload_file):
    '''保存上传文件到本地'''
    filepath = os.path.join(settings.BASE_DIR, settings.MEDIA_ROOT, filename)
    with open(filepath, 'wb') as newfile:
        for chunk in upload_file.chunks():
            newfile.write(chunk)
    return filename, filepath
