from libs.http import render_json
from social import logics
from social.models import Swiped
from social.models import Friend
from user.models import User
from vip.logics import need_perm


def rcmd_users(request):
    '''获取推荐用户列表'''
    users = logics.rcmd(request.user)
    user_info = [user.to_dict() for user in users]
    return render_json(user_info)


@logics.add_swipe_score
def like(request):
    '''喜欢'''
    sid = int(request.POST.get('sid'))
    matched = logics.like_someone(request.user, sid)
    return render_json({'is_matched': matched})


@need_perm('superlike')
@logics.add_swipe_score
def superlike(request):
    '''超级喜欢'''
    sid = int(request.POST.get('sid'))
    matched = logics.superlike_someone(request.user, sid)
    return render_json({'is_matched': matched})


@logics.add_swipe_score
def dislike(request):
    '''不喜欢'''
    sid = int(request.POST.get('sid'))
    Swiped.swipe(request.user.id, sid, 'dislike')
    return render_json()


@need_perm('rewind')
def rewind(request):
    '''反悔'''
    # 可以不依赖客户端参数，什么都不需要传
    logics.rewind(request.user)
    return render_json()


@need_perm('show_liked_me')
def show_liked_me(request):
    uid_list = Swiped.who_liked_me(request.user.id)
    users = User.objects.filter(id__in=uid_list)
    user_info = [user.to_dict() for user in users]
    return render_json(user_info)


def friends(request):
    '''查看好友列表'''
    friend_id_list = Friend.friend_list(request.user.id)
    my_friends = User.objects.filter(id__in=friend_id_list)
    friend_info = [friend.to_dict() for friend in my_friends]
    return render_json(friend_info)


def top10(request):
    rank_data = logics.get_top_n(10)
    result = [[user.to_dict(), score] for user, score in rank_data]
    return render_json(result)
