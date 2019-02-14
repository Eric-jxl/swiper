from libs.http import render_json
from social.logic import rcmd


def rcmd_users(request):
    '''获取推荐用户列表'''
    users = rcmd(request.user)
    data = [user.to_dict() for user in users]
    return render_json(data)


def like(request):
    sid = request.POST.get('sid')
    return render_json()


def superlike(request):
    sid = request.POST.get('sid')
    return render_json()


def dislike(request):
    sid = request.POST.get('sid')
    return render_json()


def rewind(request):
    return render_json()


def show_liked_me(request):
    return render_json()
