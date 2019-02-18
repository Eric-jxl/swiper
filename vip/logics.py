from common import errors


def need_perm(perm_name):
    '''权限检查装饰器'''
    def deco(view_func):
        def wrap(request):
            # 取出用户
            user = request.user
            # 检查用户是否具有 `perm_name` 权限
            if user.vip.has_perm(perm_name):
                return view_func(request)
            else:
                raise errors.NotHasPerm
        return wrap
    return deco
