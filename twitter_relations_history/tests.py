# -*- coding: utf-8 -*-
from django.test import TestCase
from models import RelationsHistory, NoDeltaForFirstHistory
from twitter_api.factories import UserFactory
import mock

GROUP_ID = 30221121

class TwitterRelationsHistoryMigrationTest(TestCase):

    @mock.patch('twitter_api.models.User')
    def test_relations_history(self, User, *args, **kwargs):
        user = UserFactory()
        User.remote.fetch_followers_ids_for_user.return_value = [1,2,3]
        RelationsHistory.objects.update_for_user(user)

        self.assertEqual(RelationsHistory.objects.count(), 1)
        instance1 = RelationsHistory.objects.all()[0]
        self.assertListEqual(instance1.followers_ids, [1,2,3])
        self.assertEqual(instance1.followers_count, 3)
        self.assertRaises(NoDeltaForFirstHistory, lambda: instance1.followers_entered_ids)
        self.assertRaises(NoDeltaForFirstHistory, lambda: instance1.followers_left_ids)

        User.remote.fetch_followers_ids_for_user.return_value = [1,2,3,4,5,6]
        RelationsHistory.objects.update_for_user(user)

        self.assertEqual(RelationsHistory.objects.count(), 2)
        instance2 = RelationsHistory.objects.order_by('-time')[0]
        self.assertListEqual(instance2.followers_ids, [1,2,3,4,5,6])
        self.assertListEqual(instance2.followers_entered_ids, [4,5,6])
        self.assertListEqual(instance2.followers_left_ids, [])
        self.assertEqual(instance2.followers_count, 6)
        self.assertEqual(instance2.followers_entered_count, 3)
        self.assertEqual(instance2.followers_left_count, 0)

        User.remote.fetch_followers_ids_for_user.return_value = [1,2,7]
        RelationsHistory.objects.update_for_user(user)

        self.assertEqual(RelationsHistory.objects.count(), 3)
        instance3 = RelationsHistory.objects.order_by('-time')[0]
        self.assertListEqual(instance3.followers_ids, [1,2,7])
        self.assertListEqual(instance3.followers_entered_ids, [7])
        self.assertListEqual(instance3.followers_left_ids, [3,4,5,6])
        self.assertEqual(instance3.followers_count, 3)
        self.assertEqual(instance3.followers_entered_count, 1)
        self.assertEqual(instance3.followers_left_count, 4)

        self.assertListEqual(instance3.followers_entered_ids(instance1), [7]) # TODO: implement it later
        self.assertListEqual(instance3.followers_left_ids(instance1), [3])
        self.assertEqual(instance3.followers_entered_count(instance1), 1)
        self.assertEqual(instance3.followers_left_count(instance1), 1)

#     def test_deleting_hiding_histories(self):
#
#         for i in range(1,7):
#             UserFactory.create(remote_id=i)
#
#         group = GroupFactory.create(remote_id=GROUP_ID)
#         stat1 = GroupMigration.objects.create(group=group, members_ids=[1,2,3,4,5])
#         stat1.save_final()
#         stat2 = GroupMigration.objects.create(group=group, members_ids=[1,2,3,4,6])
#         stat2.save_final()
#         stat3 = GroupMigration.objects.create(group=group, members_ids=[1,2,3,5,7])
#         stat3.save_final()
#
#         # difference between stat2 and stat1
#         self.assertEqual(stat2.members_entered_ids, [6])
#         self.assertEqual(stat2.members_left_ids, [5])
#         # difference between stat3 and stat2
#         self.assertEqual(stat3.members_entered_ids, [5,7])
#         self.assertEqual(stat3.members_left_ids, [4,6])
#
#         stat2.delete()
#         stat3 = GroupMigration.objects.get(id=stat3.id)
#
#         # difference between stat3 and stat1
#         self.assertEqual(stat3.members_entered_ids, [7])
#         self.assertEqual(stat3.members_left_ids, [4])
#
#         stat4 = GroupMigration.objects.create(group=group, members_ids=[1,2,3,4,6])
#         stat4.save_final()
#
#         # difference between stat4 and stat3
#         self.assertEqual(stat4.members_entered_ids, [4,6])
#         self.assertEqual(stat4.members_left_ids, [5,7])
#
#         stat3.hide()
#         stat4 = GroupMigration.objects.get(id=stat4.id)
#
#         # difference between stat4 and stat1
#         self.assertEqual(stat4.members_entered_ids, [6])
#         self.assertEqual(stat4.members_left_ids, [5])
#
#         stat5 = GroupMigration.objects.create(group=group, members_ids=[1,2,3,5,7])
#         stat5.save_final()
#
#         # difference between stat5 and stat4
#         self.assertEqual(stat5.members_entered_ids, [5,7])
#         self.assertEqual(stat5.members_left_ids, [4,6])
#
#         stat4.hidden = True
#         stat4.save()
#         stat5 = GroupMigration.objects.get(id=stat5.id)
#
#         # difference between stat5 and stat1
#         self.assertEqual(stat5.members_entered_ids, [7])
#         self.assertEqual(stat5.members_left_ids, [4])