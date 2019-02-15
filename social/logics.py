import datetime

from user.models import User
from social.models import Swiped
from social.models import Friend


def rcmd(user):
    '''推荐算法'''
    today = datetime.date.today()
    max_year = today.year - user.profile.min_dating_age
    min_year = today.year - user.profile.max_dating_age

    # 筛选出被用户划过的 sid 列表
    user_swiped = Swiped.objects.filter(uid=user.id).only('sid')
    swiped_sid_list = [swiped.sid for swiped in user_swiped]

    # 取出满足条件的用户
    users = User.objects.filter(
        sex=user.profile.dating_sex,
        location=user.profile.location,
        birth_year__lte=max_year,
        birth_year__gte=min_year,
    ).exclude(id__in=swiped_sid_list)[:10]

    return users


def like_someone(user, sid):
    '''喜欢'''
    # 添加滑动记录
    Swiped.objects.create(uid=user.id, sid=sid, flag='like')

    # 检查对方是否喜欢过我
    if Swiped.is_liked(sid, user.id):
        # 如果喜欢过，建立好友关系
        Friend.make_friends(user.id, sid)
        # TODO: 给 对方 推送一条消息，通知新增好友
        return True
    return False


def superlike_someone(user, sid):
    '''超级喜欢'''
    # 添加滑动记录
    Swiped.objects.create(uid=user.id, sid=sid, flag='superlike')

    # 检查对方是否喜欢过我
    if Swiped.is_liked(sid, user.id):
        # 如果喜欢过，建立好友关系
        Friend.make_friends(user.id, sid)
        # TODO: 给 对方 推送一条消息，通知新增好友
        return True
    return False


def dislike_someone(user, sid):
    pass
