from notifications.models import Notification
import xadmin
from common.basemodel import Baseadminmodel

class Notifyadmin(Baseadminmodel):
    list_display = ['nfrom','recipient','status','verb','msg','actor','target','unread','timestamp','readedstamp']
    list_filter = Notification.get_fields()
    admin_show_field=['nfrom','target']
    list_editable = ['unread']
    def queryset(self):
        qs=super(Notifyadmin, self).queryset()
        if not self.user.is_superuser:
            qs=qs.filter(nfrom=self.user)
            for field in self.admin_show_field:
                if field in self.list_display:self.list_display.remove(field)
        return qs
    def get_list_queryset(self):
        qs=super(). get_list_queryset()
        return qs.myprefetch_related('actor','target')
xadmin.site.register(Notification, Notifyadmin)