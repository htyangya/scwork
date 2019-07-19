from django.shortcuts import redirect

from notifications.models import Notification

import xadmin
from xadmin import views
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

class Noticeview(views.CommAdminView):
    def set_page_obj(self,objects):
        try:
            page = self.request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(objects, 10,request=self.request)
        notices=p.page(page)
        context = super().get_context()
        context["notices_pageobj"]=notices
        context["count"] = len(objects)
        self.context=context
    def set_obj_breadcrumbs(self,dict):
        context = super().get_context()
        context["breadcrumbs"].append(dict)
        context["title"] = dict.get('title')
        self.context = context
    def get_context(self):
        return super().get_context()


class UnreadView(Noticeview):
    def update_to_do(self):
        request=self.request
        to_do=request.GET.get('todo',None)
        if not to_do: return
        if to_do=='all':
            self.user.notifications.unread().mark_all_as_read()
        elif to_do=='top':
            ids=[notify.id for notify in self.user.notifications.unread()[:10]]
            Notification.objects.filter(id__in=ids).mark_all_as_read()
        else:
            try:
                id = int(to_do)
                n=Notification.objects.get(id=id)
                n.mark_as_read()
                return n.get_target_url()
            except:
                pass

    def get(self, request, *args, **kwargs):
        re=self.update_to_do()
        if re:return redirect(re)
        self.set_obj_breadcrumbs({'url': '/notice/unread/', 'title': "未读消息"})
        objects=self.user.notifications.unread().exclude(status="待发送").prefetch_related('nfrom').myprefetch_related('actor','target')
        self.set_page_obj(objects)
        context=self.context
        context["type"]='未读通知'
        return self.template_response('xadmin/views/messages.html', context)
xadmin.site.register_view(r'notice/unread/$', UnreadView,name='unread')


class ReadView(Noticeview):
    def update_to_do(self):
        request=self.request
        to_do=request.GET.get('todo',None)
        if not to_do:return
        if to_do=='all':
            self.user.notifications.read().mark_all_as_deleted()
        elif to_do=='top':
            ids = [notify.id for notify in self.user.notifications.read()[:10]]
            Notification.objects.filter(id__in=ids).mark_all_as_deleted()
        else:
            try:
                id=int(to_do)
                Notification.objects.filter(id=id).mark_all_as_deleted()
            except:
                pass

    def get(self, request, *args, **kwargs):
        self.update_to_do()
        self.set_obj_breadcrumbs({'url': 'notice/read/', 'title': "已读消息"})
        objects = self.user.notifications.read().exclude(status="待发送").prefetch_related('nfrom').myprefetch_related('actor','target')
        self.set_page_obj(objects)
        context = self.context
        context["type"]='已读通知'
        return self.template_response('xadmin/views/messages_read.html', context)

xadmin.site.register_view(r'notice/read/$', ReadView,name='read')