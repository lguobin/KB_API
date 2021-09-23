import time
import redis

class SimpleRedis(object):
    def __init__(self, **REDIS_HOSTS):
        self._redis_pool = redis.ConnectionPool(**REDIS_HOSTS)

    def Cache(self):
        return redis.Redis(connection_pool=self._redis_pool)

class _Cache:
    def __init__(self, **_REDIS_HOSTS):
        self.GlobalCache = SimpleRedis(**_REDIS_HOSTS).Cache()

    def save_GlobalParams(self, TCase_object, _params):
        seconds = 86400 * 7               # 保存临时变量
        now = int(time.time())
        expires_time = now + seconds
        saveData = dict()
        saveData["source"] = TCase_object
        saveData["updateTime"] = now
        saveData["expiresTime"] = expires_time
        saveData["params"] = _params
        # GlobalCache.hmset('globalParams', _params)
        self.GlobalCache.hset("globalParams", TCase_object, saveData)
        return True

    def get_GlobalParams(self):
        global_vars = self.GlobalCache.hgetall("globalParams")
        if global_vars == {} or global_vars == None:
            return {}
        else:
            result = {}
            __global_vars = { key.decode(): val.decode() for key, val in global_vars.items() }
            aa = [ eval(val).get("params") for _, val in __global_vars.items() ]
            for index in range(len(aa)):
                result.update(aa[index])
            return result


# 废弃
# def save_GlobalParams(TCase_object, _params):
#     # 保存临时变量
#     seconds = 86400 * 7
#     now = int(time.time())
#     expires_time = now + seconds
#     saveData = dict()
#     saveData["source"] = TCase_object
#     saveData["updateTime"] = now
#     saveData["expiresTime"] = expires_time
#     saveData["params"] = _params
#     # GlobalCache.hmset('globalParams', _params)
#     GlobalCache.hset("globalParams", TCase_object, saveData)
#     return True


# def get_GlobalParams():
#     global_vars = GlobalCache.hgetall("globalParams")
#     if global_vars == {} or global_vars == None:
#         return {}
#     else:
#         result = {}
#         __global_vars = { key.decode(): val.decode() for key, val in global_vars.items() }
#         aa = [ eval(val).get("params") for _, val in __global_vars.items() ]
#         for index in range(len(aa)):
#             result.update(aa[index])
#         return result