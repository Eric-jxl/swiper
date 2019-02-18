from libs.http import render_json
from vip.models import Vip


def show_vip(request):
    '''显示所有的 Vip 与 权限'''
    all_vip_info = []
    for vip in Vip.objects.all():
        vip_info = vip.to_dict()
        vip_info['perm'] = []
        for perm in vip.perms():
            perm_info = perm.to_dict()
            vip_info['perm'].append(perm_info)
        all_vip_info.append(vip_info)
    return render_json(all_vip_info)
