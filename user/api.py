import logging

from django.core.cache import cache
from django.conf import settings

from common import errors
from common import keys
from libs.http import render_json
from user.logics import is_phonenum
from user.logics import send_vcode
from user.logics import save_avatar
from user.models import User
from user.forms import ProfileForm

inf_log = logging.getLogger('inf')


def submit_phone(request):
    '''提交手机号，发送验证码'''
    phonenum = request.POST.get('phonenum')

    if is_phonenum(phonenum):
        # 向短信平台发送验证码
        if send_vcode(phonenum):
            return render_json()
        else:
            return render_json(code=errors.PlatformErr.code)
    else:
        return render_json(code=errors.PhoneErr.code)


def submit_vcode(request):
    '''提交验证码，进行登录注册'''
    phone = request.POST.get('phonenum')
    vcode = request.POST.get('vcode')

    # 从缓存取出验证码，并进行验证
    cached_vcode = cache.get(keys.VCODE % phone)
    if vcode == cached_vcode:
        # 执行登录、注册
        user, _ = User.get_or_create(phonenum=phone, nickname=phone)
        inf_log.info(f'uid = {user.id}')
        request.session['uid'] = user.id
        return render_json(data=user.to_dict())
    else:
        return render_json(code=errors.VcodeErr.code)


def get_profile(request):
    '''获取个人资料'''
    user = request.user

    # 定义 key，并从缓存中获取
    key = keys.PROFILE % user.id
    profile_data = cache.get(key)
    print('get from cache: %s' % profile_data)

    # 如果缓存中没有数据，从数据库获取，将取到的数据写入缓存
    if profile_data is None:
        profile_data = user.profile.to_dict('vibration', 'only_matche', 'auto_play')
        print('get from DB: %s' % profile_data)
        cache.set(key, profile_data)
        print('set to cache')

    return render_json(profile_data)


def set_profile(request):
    '''修改个人资料'''
    form = ProfileForm(request.POST)
    if form.is_valid():
        profile = form.save(commit=False)
        profile.id = request.user.id
        profile.save()

        # 数据发生变化后，更新缓存
        key = keys.PROFILE % profile.id
        profile_data = profile.to_dict('vibration', 'only_matche', 'auto_play')
        cache.set(key, profile_data)

        return render_json()
    else:
        return render_json(form.errors, code=errors.ProfileErr.code)


def upload_avatar(request):
    '''上传个人头像'''
    avatar = request.FILES.get('avatar')
    save_avatar.delay(request.user, avatar)
    return render_json()
