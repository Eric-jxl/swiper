from django.core.cache import cache

from common import errors
from common import keys
from libs.http import render_json
from user.logics import is_phonenum
from user.logics import send_vcode
from user.models import User


def submit_phone(request):
    '''提交手机号，发送验证码'''
    phonenum = request.POST.get('phonenum')
    if is_phonenum(phonenum):
        # 向短信平台发送验证码
        if send_vcode(phonenum):
            return render_json()
        else:
            return render_json(code=errors.PLATFORM_ERR)
    else:
        return render_json(code=errors.PHONE_ERR)


def submit_vcode(request):
    '''提交验证码，进行登录注册'''
    phone = request.POST.get('phonenum')
    vcode = request.POST.get('vcode')

    # 从缓存取出验证码，并进行验证
    cached_vcode = cache.get(keys.VCODE % phone)
    if vcode == cached_vcode:
        # 执行登录、注册
        user, _ = User.objects.get_or_create(phonenum=phone, nickname=phone)
        request.session['uid'] = user.id
        return render_json(data=user.to_dict())
    else:
        return render_json(code=errors.VCODE_ERR)
