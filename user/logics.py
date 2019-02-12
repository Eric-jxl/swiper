import re
from random import randrange

import requests

from swiper import config


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
    params = config.YZX_SMS_PARAMS.copy()
    params['mobile'] = phonenum
    params['param'] = gen_random_code()
    response = requests.post(config.YZX_SMS_API, json=params)

    if response.status_code == 200:
        result = response.json()
        print(result)
        if result.get('msg') == 'OK':
            return True
    return False
