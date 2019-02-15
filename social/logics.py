import datetime

from django.core.cache import cache

from swiper import config
from common import keys
from common import errors
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
    Swiped.swipe(user.id, sid, 'like')

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
    Swiped.swipe(user.id, sid, 'superlike')

    # 检查对方是否喜欢过我
    if Swiped.is_liked(sid, user.id):
        # 如果喜欢过，建立好友关系
        Friend.make_friends(user.id, sid)
        # TODO: 给 对方 推送一条消息，通知新增好友
        return True
    return False


def rewind(user):
    '''反悔操作, 撤销上一次滑动操作'''
    # 检查今天是否已经达到 3 次
    key = keys.REWIND_TIMES % user.id
    rewind_times = cache.get(key, 0)
    if rewind_times >= config.REWIND_TIMES:
        raise errors.RewindLimit
    else:
        # 获取当天剩余秒数
        now = datetime.datetime.now()
        timeout = 86400 - now.hour * 3600 - now.minute * 60 - now.second

        # 通过时间戳计算今天的剩余秒数
        # timeout = 86400 - (time.time() + 3600 * 8) % 86400

        cache.set(key, rewind_times + 1, timeout)  # 计数加一，并设置有效期到今晚 0 点

    # 取出上一次操作
    try:
        swiped = Swiped.objects.filter(uid=user.id).latest('time')
    except Swiped.DoesNotExist:
        return

    # 检查上一次是否完成过匹配，如果完成匹配需撤销好友关系
    if swiped.flag in ['like', 'superlike']:
        Friend.break_off(user.id, swiped.sid)

    swiped.delete()
