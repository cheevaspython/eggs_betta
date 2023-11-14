from datetime import datetime
from django.test import TestCase
from product_eggs.services.data_class.data_class_documents import PrePayOrderDataForSave

from product_eggs.tests.create_models import TestModelCreator


class TestCreateDataClasses(TestCase):

    def test_prepayorderdataforsave(self):
        res = {
            'date': datetime.now().date().strftime('%d/%m/%Y'),
            'number':'1239128313',
            'pay_quantity':'100000',
            'inn':'1000000000',
            'entity': '5612163931',
            'doc_type':'tail_payment',
            'client_type':'buyer',
            'cash': False,
        }
        result = PrePayOrderDataForSave(**res)
        self.assertIs(type(result), PrePayOrderDataForSave)

