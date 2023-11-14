from django.db.models.query import QuerySet
from django.test import TestCase

from product_eggs.models.base_deal import BaseDealEggsModel
from product_eggs.models.messages import MessageToUserEggs
from product_eggs.services.create_model import CreatorNewModel
from product_eggs.tests.create_models import TestModelCreator
from users.models import CustomUser


class TestMessages(TestCase):

    def get_message(self, deal: BaseDealEggsModel, user: CustomUser) -> QuerySet:
        return MessageToUserEggs.objects.filter(current_base_deal=deal, message_to=user)

    def test_message_create(self):
        test_obj = TestModelCreator()
        message = 'test message'
        user = test_obj.create_user('fin')
        deal = test_obj.create_base_deal(3)

        all_before = MessageToUserEggs.objects.all()
        b = self.get_message(deal, user)
        self.assertFalse(b)
        self.assertFalse(all_before)

        new_model = CreatorNewModel(
            ('MessageToUserEggs',),
            message = message,
            message_to = user,
            current_base_deal = deal,
            # current_seller = self._seller, #TODO
            # current_buyer = self._buyer,
            # current_logic = self._logic,
            # current_app_seller = self._app_seller,
            # current_app_buyer = self._app_buyer,
            # info = self._info,
            # done = self._done,
        )
        new_model.create()

        all_after = MessageToUserEggs.objects.all()
        a = self.get_message(deal, user)
        self.assertTrue(a)
        self.assertNotEqual(a, b)
        self.assertNotEqual(all_before, all_after)


