# -*- coding: utf-8 -*-
from django.db import models
from django.db.models.query import QuerySet
from django.core.exceptions import MultipleObjectsReturned
from twitter_api import fields
from twitter_api.utils import api
from twitter_api.models import User
from datetime import datetime
import logging

log = logging.getLogger('twitter_relations_history')

class NoDeltaForFirstHistory(ValueError):
    pass

def ModelQuerySetManager(ManagerBase=models.Manager):
    '''
    Function that return Manager for using QuerySet class inside the model definition
    @param ManagerBase - parent class Manager
    '''
    if not issubclass(ManagerBase, models.Manager):
        raise ValueError("Parent class for ModelQuerySetManager must be models.Manager or it's child")

    class Manager(ManagerBase):
        '''
        Manager based on QuerySet class inside the model definition
        '''
        def get_query_set(self):
            return self.model.QuerySet(self.model)

    return Manager()

class RelationsHistoryQueryset(object):

    @property
    def visible(self):
        return self.exclude(hidden=True).exclude(time__isnull=True)

    @property
    def light(self):
        return self.defer(
            'followers_ids',
        )

class RelationsHistoryManager(models.Manager, RelationsHistoryQueryset):

    def update_for_user(self, user, offset=0):
        '''
        Fetch all users for this user, save them as IDs and after make m2m relations
        '''
        try:
            stat, created = self.get_or_create(user=user, time=None)
        except MultipleObjectsReturned:
            self.filter(user=user, time=None).delete()
            stat = self.create(user=user, time=None, offset=0)
            created = True

        if created:
            stat.set_defaults()

        stat.time = datetime.now()
        stat.followers_ids = user.fetch_followers_ids(all=True)
        stat.update()
        stat.save()

#        signals.group_migration_updated.send(sender=RelationsHistory, instance=stat)

#     def update_group_users_m2m(self, stat, offset=0):
#         '''
#         Fetch all users of group, make new m2m relations, remove old m2m relations
#         '''
#         group = stat.group
#
#         ids = stat.followers_ids
#         ids_left = set(group.users.values_list('remote_id', flat=True)).difference(set(ids))
#
#         offset = offset or stat.offset
#         errors = 0
#
#         while True:
#             ids_sliced = ids[offset:offset+1000]
#             if len(ids_sliced) == 0:
#                 break
#
#             log.debug('Fetching users for group "%s", offset %d' % (group, offset))
#             try:
#                 users = User.remote.fetch(ids=ids_sliced, only_expired=True)
#             except Exception, e:
#                 log.error('Error %s while getting users for group "%s": "%s", offset %d' % (e.__class__, group, e, offset))
#                 errors += 1
#                 if errors == 10:
#                     log.error('Fail - number of unhandled errors while updating users for group "%s" more than 10, offset %d' % (group, offset))
#                     break
#                 continue
#
#             if len(users) == 0:
#                 stat.offset = 0
#                 stat.save()
#                 break
#             else:
#                 for user in users:
#                     if user.id:
#                         group.users.add(user)
#                 stat.offset = offset
#                 stat.save()
#                 offset += 1000
#
#         # process left users of group
#         log.info('Removing %s left users for group "%s"' % (len(ids_left), group))
#         for remote_id in ids_left:
#             group.users.remove(User.objects.get(remote_id=remote_id))
#
#         signals.group_users_updated.send(sender=Group, instance=group)
#         log.info('Updating m2m relations of users for group "%s" successfuly finished' % (group,))
#         return True

class RelationsHistory(models.Model):
    class Meta:
        verbose_name = u'Relations history of twitter users'
        verbose_name_plural = u'Relations histories of twitter users'
        unique_together = ('user','time')
        ordering = ('user','time','-id')

    class QuerySet(QuerySet, RelationsHistoryQueryset):
        pass

#     class MethodDelta(object):
#         def __init__(self, client, method_name):
#             self.client = client
#             self.method_name = method_name
#
#         def __getattr__(self, key):
#             return RelationsHistory.MethodDelta(self.client, '.'.join((self.method_name, key)))
#
#         def __call__(self, prev=None):
#             if not prev:
#                 prev = self.prev
#             if prev:
#                 delta = RelationsHistoryDelta.objects.get_or_create(history_from=prev, history_to=self)[0]
#                 return getattr(delta, self.method_name)
#             else:
#                 raise NoDeltaForFirstHistory("This history doesn't have previous history")

    user = models.ForeignKey(User, verbose_name=u'User', related_name='relations_history')
    time = models.DateTimeField(u'Datetime', null=True)

    hidden = models.BooleanField(u'Скрыть')

    offset = models.PositiveIntegerField(default=0)

    followers_ids = fields.PickledObjectField(default=[])
    followers_count = models.PositiveIntegerField(default=0)

    objects = ModelQuerySetManager(RelationsHistoryManager)

    def set_defaults(self):
        '''
        It's neccesary to call after creating of every instance,
        because `default` attribute of fields.PickledObjectField doesn't work properly
        '''
        self.followers_ids = []

    _next = None
    _prev = None

    @property
    def next(self):
        try:
            assert self._next
        except AssertionError:
            try:
                self._next = self.user.relations_history.visible.filter(time__gt=self.time).order_by('time')[0]
            except IndexError:
                return None
        return self._next

    @property
    def prev(self):
        try:
            assert self._prev
        except AssertionError:
            try:
                self._prev = self.user.relations_history.visible.filter(time__lt=self.time).order_by('-time')[0]
            except IndexError:
                return None
        return self._prev

    def get_delta(self, name, prev=None):
        if name in [field.name for field in RelationsHistoryDelta._meta.fields if 'followers' in field.name]:
            if not prev:
                prev = self.prev
            if prev:
                delta = RelationsHistoryDelta.objects.get_or_create(history_from=prev, history_to=self)[0]
                return getattr(delta, name)
            else:
                raise NoDeltaForFirstHistory("This history doesn't have previous history")
        else:
            raise AttributeError("type object '%s' has no attribute '%s'" % (self.__class__, name))

    def __getattr__(self, name):
        return self.get_delta(name)
#        return RelationsHistory.MethodDelta(self, name)

    def delete(self, *args, **kwargs):
        '''
        Recalculate next stat members instance
        '''
        self.hide()
        super(RelationsHistory, self).delete(*args, **kwargs)

    def hide(self):
        '''
        Hide curent migration, and recalculate fields of next migrations
        '''
        self.hidden = True
        self.save()

    def update_next(self):
        next_stat = self.next
        if next_stat:
            next_stat.update()
            next_stat.save()

    def save(self, *args, **kwargs):
        update_next = False
        if self.id and self.hidden != self.__class__.objects.light.get(id=self.id).hidden:
            update_next = True

        super(RelationsHistory, self).save(*args, **kwargs)

        if update_next:
            self.update_next()

    def update(self):
        self.update_migration()
        self.update_counters()

    def update_migration(self):
        return
        prev_stat = self.prev
        if prev_stat and self.user:
            self.members_left_ids = list(set(prev_stat.followers_ids).difference(set(self.followers_ids)))
            self.members_entered_ids = list(set(self.followers_ids).difference(set(prev_stat.followers_ids)))

    def update_counters(self):
        for field_name in ['followers']:
            setattr(self, field_name + '_count', len(getattr(self, field_name + '_ids')))

class RelationsHistoryDelta(models.Model):
    class Meta:
        unique_together = ('history_from','history_to')

    history_from = models.ForeignKey(RelationsHistory, related_name='deltas_from')
    history_to = models.ForeignKey(RelationsHistory, related_name='deltas_to')

    followers_left_ids = fields.PickledObjectField(default=[])
    followers_entered_ids = fields.PickledObjectField(default=[])

    followers_left_count = models.PositiveIntegerField(default=0)
    followers_entered_count = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):

        self.followers_left_ids = list(set(self.history_from.followers_ids).difference(set(self.history_to.followers_ids)))
        self.followers_entered_ids = list(set(self.history_to.followers_ids).difference(set(self.history_from.followers_ids)))

        self.followers_left_count = len(self.followers_left_ids)
        self.followers_entered_count = len(self.followers_entered_ids)

        super(RelationsHistoryDelta, self).save(*args, **kwargs)

import signals