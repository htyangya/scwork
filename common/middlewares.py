from django.core.cache import cache
from django.utils.deprecation import MiddlewareMixin
from threading import local

from users.models import UserProfile,Company

_thread_locals = local()
def get_current_user(num=True):
    return getattr(_thread_locals, 'user', 1 if num else UserProfile.objects.get(pk=1))
def get_current_request():
    return getattr(_thread_locals, 'request', None)

def get_current_company(num=True):
    user=getattr(_thread_locals, 'user',1)
    if isinstance(user,UserProfile):
        return user.company
    return 1 if num else Company.objects.get(pk=1)

class ZxMiddleware(MiddlewareMixin):

    def process_request(self, request):
        user=request.user
        if not user.id:return None
        #设置当前线程的user对象
        _thread_locals.user = user
        _thread_locals.request=request
        #获取最新索引信息
        online_users_name=self.get_online_users_name()
        cache.set(user.username,user.__str__(),60*15)#不用if判定，每次访问都默认往后延15分钟
        if user.username not in  online_users_name:
            #如果遇到新用户登陆，更新一下索引
            online_users_name.append(user.username)
            cache.set("online_users_name", online_users_name)

    def get_online_users_name(self):
        online_users = cache.get_many(cache.get("online_users_name", [])).keys()
        return list(online_users)

def get_onlie_users():
    return list(cache.get_many(cache.get("online_users_name", [])).values())