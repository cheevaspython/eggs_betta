import logging

from datetime import datetime

from collections import OrderedDict

from django.test import TestCase

from rest_framework.exceptions import ValidationError

from product_eggs.services.comments import get_instance_for_comment, get_log_to_comment, parse_comment_tmp_json
from product_eggs.services.data_class.data_class import CommentData
from product_eggs.tests.create_models import TestModelCreator

logger = logging.getLogger(__name__)


class TestCommentsService(TestCase):

    def test_get_instance_for_comment(self):
        test_obj = TestModelCreator()
        app_seller = test_obj.create_app_seller()
        app_buyer = test_obj.create_app_buyer()
        deal = test_obj.create_base_deal()
        res = get_instance_for_comment(app_seller.pk, 'app_seller')
        self.assertEqual(res, app_seller)
        res1 = get_instance_for_comment(app_buyer.pk, 'app_buyer')
        self.assertEqual(res1, app_buyer)
        res2 = get_instance_for_comment(deal.pk, 'base_deal')
        self.assertEqual(res2, deal)
        self.assertRaises(ValidationError, get_instance_for_comment, 18, 'app_seller')

    def test_get_log_to_comment(self):
        test_obj = TestModelCreator()
        comment = test_obj.create_comment_json()
        user = test_obj.create_user('manager')
        app_seller = test_obj.create_app_seller()
        comment_data = CommentData(
            owner_id=user.pk,
            owner_name=user.username,
            comment='test_comment',
            model_id=app_seller.pk,
            model_type='app_seller',
            date_time=str(datetime.today()),
        )
        res = get_log_to_comment(comment_data)
        self.assertTrue(res)
        self.assertIs(type(res), dict)

    def test_parse_comment_tmp_json(self):
        test_obj = TestModelCreator()
        app_seller = test_obj.create_app_seller()
        user = test_obj.create_user('manager')
        tmp_json = {
            'comment': 'some_comment',
            'model_id': app_seller.pk,
            'model_type': 'app_seller',
        }
        val_data = OrderedDict([
            ('one', 'two'),
            ('foo', 'test_note'),
            ('tmp_json', tmp_json)
        ])
        res = parse_comment_tmp_json(val_data, user)
        self.assertTrue(res)
        self.assertIs(type(res), CommentData)



