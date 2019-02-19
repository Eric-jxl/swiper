from redis import Redis
from django.conf import settings


rds = Redis(**settings.REDIS)
