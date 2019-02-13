import json

from django.http import HttpResponse
from django.conf import settings


def render_json(data=None, code=0):
    result = {
        'data': data,
        'code': code
    }

    if settings.DEBUG:
        json_str = json.dumps(result, ensure_ascii=False, indent=4, sort_keys=True)
    else:
        json_str = json.dumps(result, ensure_ascii=False, separators=(',', ':'))
    return HttpResponse(json_str)
