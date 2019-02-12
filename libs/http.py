import json

from django.http import HttpResponse


def render_json(data, code=0):
    result = {
        'data': data,
        'code': code
    }

    json_str = json.dumps(result, separators=(',', ':'))
    return HttpResponse(json_str)
