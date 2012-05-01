from django.shortcuts import render
from apps.redisutils import get_redis_connection


def stats_index(request):
    data = {}
    redis = get_redis_connection()
    urls = {}
    total_hits = total_misses = 0
    for uri, count in redis.zrange('plog:hits', 0, -1, withscores=True):
        count = int(count)
        total_hits += count
        if uri not in urls:
            urls[uri] = {'hits': 0, 'misses': 0}
        urls[uri]['hits'] += count
    for uri, count in redis.zrange('plog:misses', 0, -1, withscores=True):
        count = int(count)
        total_misses += count
        if uri not in urls:
            urls[uri] = {'hits': 0, 'misses': 0}
        urls[uri]['misses'] += count

    data['total_hits'] = total_hits
    data['total_misses'] = total_misses
    for v in urls.values():
        v['ratio'] = round(100.0 * v['misses'] / v['hits'], 1)
    data['urls'] = urls

    return render(request, 'stats/index.html', data)