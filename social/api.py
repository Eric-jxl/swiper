from libs.http import render_json
from social import logics
from social.models import Swiped


def rcmd_users(request):
    '''获取推荐用户列表'''
    users = logics.rcmd(request.user)
    data = [user.to_dict() for user in users]
    return render_json(data)


def like(request):
    '''喜欢'''
    sid = int(request.POST.get('sid'))
    matched = logics.like_someone(request.user, sid)
    return render_json({'is_matched': matched})


def superlike(request):
    '''超级喜欢'''
    sid = int(request.POST.get('sid'))
    matched = logics.superlike_someone(request.user, sid)
    return render_json({'is_matched': matched})


def dislike(request):
    '''不喜欢'''
    sid = int(request.POST.get('sid'))
    Swiped.swipe(request.user.id, sid, 'dislike')
    return render_json()


def rewind(request):
    '''反悔'''
    # 能不依赖客户端参数的，什么都不需要传
    return render_json()


def show_liked_me(request):
    return render_json()


def friends(request):
    return render_json()
