''' Django notifications models file '''
# -*- coding: utf-8 -*-
# pylint: disable=too-many-lines
from datetime import datetime
from distutils.version import StrictVersion  # pylint: disable=no-name-in-module,import-error
from common.messagesender import TYPECHOICE
from common import messagesender
from django import get_version
from django.conf import settings
from django.contrib.auth.models import Group
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ImproperlyConfigured
from django.db import models
from django.db.models.query import QuerySet
from django.utils import timezone
from django.utils.six import text_type
from jsonfield.fields import JSONField
from model_utils import Choices

from common.basemodel import Basemodel
from notifications import settings as notifications_settings
from notifications.signals import notify
from notifications.utils import id2slug

if StrictVersion(get_version()) >= StrictVersion('1.8.0'):
    from django.contrib.contenttypes.fields import GenericForeignKey  # noqa
else:
    from django.contrib.contenttypes.generic import GenericForeignKey  # noqa


EXTRA_DATA = notifications_settings.get_config()['USE_JSONFIELD']


def is_soft_delete():
    return notifications_settings.get_config()['SOFT_DELETE']


def assert_soft_delete():
    if not is_soft_delete():
        msg = """To use 'deleted' field, please set 'SOFT_DELETE'=True in settings.
        Otherwise NotificationQuerySet.unread and NotificationQuerySet.read do NOT filter by 'deleted' field.
        """
        raise ImproperlyConfigured(msg)


class NotificationQuerySet(models.query.QuerySet):
    ''' Notification QuerySet '''
    def myprefetch_related(self,*ps):
        if not ps:return self
        generics = {}
        for item in self:
            for p in ps:
                ctid=getattr(item, p + '_content_type_id')
                objid=getattr(item,p+'_object_id')
                generics.setdefault(ctid, set()).add(objid)

        content_types = ContentType.objects.in_bulk(generics.keys())

        relations = {}
        for ct, fk_list in generics.items():
            ct_model = content_types[ct].model_class()
            relations[ct] = ct_model.objects.in_bulk(list(fk_list))

        for item in self:
            for p in ps:
                ctid = getattr(item, p + '_content_type_id')
                objid = getattr(item, p + '_object_id')
                setattr(item, p + '_content_type',content_types[ctid])
                setattr(item, p, relations[ctid][int(objid)])

        return self

    def unsent(self):
        return self.filter(emailed=False)

    def sent(self):
        return self.filter(emailed=True)

    def unread(self, include_deleted=False):
        """Return only unread items in the current queryset"""
        if is_soft_delete() and not include_deleted:
            return self.filter(unread=True, deleted=False)

        # When SOFT_DELETE=False, developers are supposed NOT to touch 'deleted' field.
        # In this case, to improve query performance, don't filter by 'deleted' field
        return self.filter(unread=True)

    def read(self, include_deleted=False):
        """Return only read items in the current queryset"""
        if is_soft_delete() and not include_deleted:
            return self.filter(unread=False, deleted=False)

        # When SOFT_DELETE=False, developers are supposed NOT to touch 'deleted' field.
        # In this case, to improve query performance, don't filter by 'deleted' field
        return self.filter(unread=False)

    def mark_all_as_read(self, recipient=None):
        """Mark as read any unread messages in the current queryset.

        Optionally, filter these by recipient first.
        """
        # We want to filter out read ones, as later we will store
        # the time they were marked as read.
        qset = self.unread(True)
        if recipient:
            qset = qset.filter(recipient=recipient)

        return qset.update(unread=False,readedstamp=datetime.now(),status="已读")

    def mark_all_as_unread(self, recipient=None):
        """Mark as unread any read messages in the current queryset.

        Optionally, filter these by recipient first.
        """
        qset = self.read(True)

        if recipient:
            qset = qset.filter(recipient=recipient)

        return qset.update(unread=True)

    def deleted(self):
        """Return only deleted items in the current queryset"""
        assert_soft_delete()
        return self.filter(deleted=True)

    def active(self):
        """Return only active(un-deleted) items in the current queryset"""
        assert_soft_delete()
        return self.filter(deleted=False)

    def mark_all_as_deleted(self, recipient=None):
        """Mark current queryset as deleted.
        Optionally, filter by recipient first.
        """
        assert_soft_delete()
        qset = self.active()
        if recipient:
            qset = qset.filter(recipient=recipient)

        return qset.update(deleted=True)

    def mark_all_as_active(self, recipient=None):
        """Mark current queryset as active(un-deleted).
        Optionally, filter by recipient first.
        """
        assert_soft_delete()
        qset = self.deleted()
        if recipient:
            qset = qset.filter(recipient=recipient)

        return qset.update(deleted=False)

    def mark_as_unsent(self, recipient=None):
        qset = self.sent()
        if recipient:
            qset = qset.filter(recipient=recipient)
        return qset.update(emailed=False)

    def mark_as_sent(self, recipient=None):
        qset = self.unsent()
        if recipient:
            qset = qset.filter(recipient=recipient)
        return qset.update(emailed=True)


class Notification(Basemodel):
    """
    Action model describing the actor acting out a verb (on an optional
    target).
    Nomenclature based on http://activitystrea.ms/specs/atom/1.0/

    Generalized Format::

        <actor> <verb> <time>
        <actor> <verb> <target> <time>
        <actor> <verb> <action_object> <target> <time>

    Examples::

        <justquick> <reached level 60> <1 minute ago>
        <brosner> <commented on> <pinax/pinax> <2 hours ago>
        <washingtontimes> <started follow> <justquick> <8 minutes ago>
        <mitsuhiko> <closed> <issue 70> on <mitsuhiko/flask> <about 2 hours ago>

    Unicode Representation::

        justquick reached level 60 1 minute ago
        mitsuhiko closed issue 70 on mitsuhiko/flask 3 hours ago

    HTML Representation::

        <a href="http://oebfare.com/">brosner</a> commented on <a href="http://github.com/pinax/pinax">pinax/pinax</a> 2 hours ago # noqa

    """
    LEVELS = Choices('success', 'info', 'warning', 'error')
    level = models.CharField(choices=LEVELS, default=LEVELS.info, max_length=20)
    type=models.CharField( max_length=50,null=True,verbose_name="类型",choices=TYPECHOICE)
    href=models.CharField( max_length=200,null=True,verbose_name="链接")
    msg=models.CharField( max_length=200,null=True,verbose_name="附语")
    status = models.CharField(verbose_name="状态",max_length=20,choices=(("待发送","待发送"),("已发送","已发送"),("已读","已读"),),default="已发送")
    nfrom=models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name='send_notifications',
        on_delete=models.CASCADE,
        verbose_name="发件人"
    )
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=False,
        related_name='notifications',
        on_delete=models.CASCADE,
        verbose_name="接收人"
    )
    unread = models.BooleanField(default=True, blank=False, db_index=True,verbose_name='是否未读')

    actor_content_type = models.ForeignKey(ContentType, related_name='notify_actor', on_delete=models.CASCADE)
    actor_object_id = models.CharField(max_length=255)
    actor = GenericForeignKey('actor_content_type', 'actor_object_id')

    verb = models.CharField(max_length=255,verbose_name='通知内容')
    description = models.TextField(blank=True, null=True)

    target_content_type = models.ForeignKey(
        ContentType,
        related_name='notify_target',
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )
    target_object_id = models.CharField(max_length=255, blank=True, null=True)
    target = GenericForeignKey('target_content_type', 'target_object_id')

    action_object_content_type = models.ForeignKey(ContentType, blank=True, null=True,
                                                   related_name='notify_action_object', on_delete=models.CASCADE)
    action_object_object_id = models.CharField(max_length=255, blank=True, null=True)
    action_object = GenericForeignKey('action_object_content_type', 'action_object_object_id')

    timestamp = models.DateTimeField(default=timezone.now, db_index=True,verbose_name="通知时间")
    readedstamp = models.DateTimeField(null=True,blank=True,db_index=True,verbose_name='已读时间')

    public = models.BooleanField(default=True, db_index=True)
    deleted = models.BooleanField(default=False, db_index=True,verbose_name='是否删除')
    emailed = models.BooleanField(default=False, db_index=True)

    data = JSONField(blank=True, null=True)
    objects = NotificationQuerySet.as_manager()

    class Meta:
        ordering = ('-timestamp',)
        app_label = 'notifications'
        verbose_name="我发出的通知"
        verbose_name_plural=verbose_name

    def get_target_text(self):
        text=messagesender.DESC[int(self.type)]
        if self.type == '6':
            return text.format(str(self.target),self.target.id)
        else:
            return text.format(str(self.target))

    def get_target_url(self):
        return self.target.get_model_url('list')

    def __unicode__(self):
        return "ntf-"+str(self.id)

    def __str__(self):  # Adds support for Python 3
        return "ntf-"+str(self.id)

    def timesince(self, now=None):
        """
        Shortcut for the ``django.utils.timesince.timesince`` function of the
        current timestamp.
        """
        from django.utils.timesince import timesince as timesince_
        return timesince_(self.timestamp, now)

    @property
    def slug(self):
        return id2slug(self.id)

    def mark_as_read(self):
        if self.unread:
            self.unread = False
            self.readedstamp=datetime.now()
            self.status="已读"
            self.save()

    def mark_as_unread(self):
        if not self.unread:
            self.unread = True
            self.save()


def notify_handler(verb, **kwargs):
    """
    Handler function to create Notification instance upon action signal call.
    """
    # Pull the options out of kwargs
    kwargs.pop('signal', None)
    recipient = kwargs.pop('recipient')
    actor = kwargs.pop('sender')
    optional_objs = [
        (kwargs.pop(opt, None), opt)
        for opt in ('target', 'action_object')
    ]
    public = bool(kwargs.pop('public', True))
    description = kwargs.pop('description', None)
    timestamp = kwargs.pop('timestamp', timezone.now())
    level = kwargs.pop('level', Notification.LEVELS.info)

    # Check if User or Group
    if isinstance(recipient, Group):
        recipients = recipient.user_set.all()
    elif isinstance(recipient, (QuerySet, list)):
        recipients = recipient
    else:
        recipients = [recipient]

    new_notifications = []

    myfields={field:kwargs.pop(field, None) for field in ['nfrom', 'type', 'status', 'href', 'msg']}


    for recipient in recipients:
        newnotify = Notification(
            recipient=recipient,
            actor_content_type=ContentType.objects.get_for_model(actor),
            actor_object_id=actor.pk,
            verb=text_type(verb),
            public=public,
            description=description,
            timestamp=timestamp,
            level=level,
        )
        for field,value in myfields.items():
            setattr(newnotify,field,value)
        # Set optional objects
        for obj, opt in optional_objs:
            if obj is not None:
                setattr(newnotify, '%s_object_id' % opt, obj.pk)
                setattr(newnotify, '%s_content_type' % opt,
                        ContentType.objects.get_for_model(obj))

        if kwargs and EXTRA_DATA:
            newnotify.data = kwargs

        newnotify.save()
        new_notifications.append(newnotify)

    return


# connect the signal
notify.connect(notify_handler, dispatch_uid='notifications.models.notification')
