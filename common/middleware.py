import logging

from django.utils.deprecation import MiddlewareMixin

from common import errors
from libs.http import render_json
from user.models import User

err_log = logging.getLogger('err')


class AuthMiddleware(MiddlewareMixin):
    WHITE_LIST = [
        '/api/user/submit_phone',
        '/api/user/submit_vcode',
        '/api/vip/show_vip'
    ]

    def process_request(self, request):
        # 如果当前 URL 在白名单中，直接返回
        if request.path in self.WHITE_LIST:
            return

        uid = request.session.get('uid')
        if not uid:
            # 如果未登录，返回错误码
            return render_json(code=errors.LoginRequire.code)
        else:
            # 如果已登录，取出 user 对象，并绑定到 request
            request.user = User.get(id=uid)


class LogicErrorMiddleware(MiddlewareMixin):
    def process_exception(self, request, exception):
        if isinstance(exception, errors.LogicError):
            err_log.error(exception)
            return render_json(code=exception.code)
