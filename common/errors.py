'''系统错误码'''

class LogicError(Exception):
    '''逻辑错误基类'''
    code = None


def gen_logic_error(name, code):
    '''创建一个逻辑错误'''
    return type(name, (LogicError,), {'code': code})


OK = gen_logic_error('OK', 0)
PlatformErr = gen_logic_error('PlatformErr', 1000)  # 第三方平台错误
PhoneErr = gen_logic_error('PhoneErr', 1001)  # 手机号错误
VcodeErr = gen_logic_error('VcodeErr', 1002)  # 无效的验证码
LoginRequire = gen_logic_error('LoginRequire', 1003)  # 用户未登录
ProfileErr = gen_logic_error('ProfileErr', 1004)  # 个人资料错误
FlagErr = gen_logic_error('FlagErr', 1005)  # 滑动类型错误
RewindLimit = gen_logic_error('RewindLimit', 1006)  # 反悔次数达到上限
NotHasPerm = gen_logic_error('NotHasPerm', 1007)  # 用户不具备某权限
