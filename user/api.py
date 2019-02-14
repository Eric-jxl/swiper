from urllib.parse import urljoin

from django.core.cache import cache
from django.conf import settings

from swiper import config
from common import errors
from common import keys
from libs.http import render_json
from libs.qncloud import upload_qncloud
from user.logics import is_phonenum
from user.logics import send_vcode
from user.logics import save_upload_file
from user.models import User
from user.forms import ProfileForm


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


def get_profile(request):
    '''获取个人资料'''
    user = request.user
    profile_data = user.profile.to_dict('vibration', 'only_matche', 'auto_play')
    return render_json(profile_data)


def set_profile(request):
    '''修改个人资料'''
    form = ProfileForm(request.POST)
    if form.is_valid():
        profile = form.save(commit=False)
        profile.id = request.user.id
        profile.save()
        return render_json()
    else:
        return render_json(form.errors, code=errors.PROFILE_ERR)


def upload_avatar(request):
    '''上传个人头像'''
    user = request.user

    avatar = request.FILES.get('avatar')

    # 将文件保存到本地
    filename = 'Avatar-%s' % user.id
    filename, filepath = save_upload_file(filename, avatar)

    # 将本地文件上传到七牛云
    upload_qncloud(filename, filepath)

    # 记录头像 URL
    user.avatar = urljoin(config.QN_HOST, filename)
    user.save()

    return render_json()
