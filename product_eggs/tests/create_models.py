import random
from datetime import date
from product_eggs.models.additional_expense import AdditionalExpenseEggs
from product_eggs.models.balance import BalanceBaseClientEggs
from product_eggs.models.base_deal import BaseDealEggsModel
from product_eggs.models.applications import ApplicationFromSellerBaseEggs, ApplicationFromBuyerBaseEggs
from product_eggs.models.base_client import SellerCardEggs, BuyerCardEggs, LogicCardEggs
from product_eggs.models.comment import CommentEggs
from product_eggs.models.entity import EntityEggs
from product_eggs.models.requisites import RequisitesEggs
from product_eggs.models.documents import DocumentsContractEggsModel, DocumentsDealEggsModel, OriginsDealEggs
from product_eggs.models.contact_person import ContactPersonEggs
from product_eggs.models.tails import TailsContragentModelEggs
from users.models import CustomUser


class TestModelCreator():

    def __init__(self):
        ...

    def create_requisites(self) -> RequisitesEggs:
        requisites = RequisitesEggs.objects.get_or_create(
            name = self.create_random_username(),
            inn = self.create_random_inn(),
            kpp = self.create_random_inn()[:-1],
        )
        return requisites[0]

    def create_entity(self,
            name: str | None = None,
            inn: str | None = None) -> EntityEggs:
        if name is None:
            name = self.create_random_username()
        if inn is None:
            inn = self.create_random_inn()
        entity = EntityEggs.objects.get_or_create(
            name=name,
            inn=inn,
        )
        return entity[0]

    def create_docs_origin(self) -> OriginsDealEggs:
        docs_origin = OriginsDealEggs.objects.create()
        return docs_origin

    def create_deal_docs(self) -> DocumentsDealEggsModel:
        docs = DocumentsDealEggsModel.objects.create(
           origins = self.create_docs_origin(),
        )
        return docs

    def create_docs_contract(self) -> DocumentsContractEggsModel:
        docs = DocumentsContractEggsModel.objects.create()
        return docs

    def create_tail(self) -> TailsContragentModelEggs:
        tail = TailsContragentModelEggs.objects.create()
        return tail

    def create_comment_json(self) -> CommentEggs:
        comment = CommentEggs.objects.create()
        return comment

    def create_contact_person(self) -> ContactPersonEggs:
        person = ContactPersonEggs.objects.create()
        return person

    def create_user(self, user_type: str) -> CustomUser:
        USER_TYPES = {
            'manager': '2',
            'logic': '4',
            'napr': '5',
            'fin': '6',
            'buh': '7',
        }
        if user_type in USER_TYPES:
            user = CustomUser.objects.create(
                username = self.create_random_username(),
                password = 'test1234567pass',
                role = USER_TYPES[user_type],
            )
            user.save()
            return user
        else:
            raise ValueError('create user type -> wrong')

    def create_random_username(self) -> str:
        username = ''
        for _ in range(10):
            username += self.create_randletter()
        return username

    def create_random_inn(self) -> str:
        inn = ''
        for _ in range(10):
            inn += str(self.create_randnumber())
        return inn

    def create_randletter(self) -> str:
        return chr(random.randint(ord('a'), ord('z')))

    def create_randnumber(self) -> int:
        return random.randint(0, 9)

    def create_balance(self,
            client: SellerCardEggs | BuyerCardEggs | LogicCardEggs,
            ) -> BalanceBaseClientEggs:
        client_buyer, client_logic, client_seller = None, None, None
        if isinstance(client, SellerCardEggs):
            client_seller = client
        elif isinstance(client, BuyerCardEggs):
            client_buyer = client
        elif isinstance(client, LogicCardEggs):
            client_logic = client
        balance_model = BalanceBaseClientEggs.objects.create(
            entity=self.create_entity(name='Пилигрим', inn='5612163931'),
            tails=self.create_tail(),
            client_seller=client_seller,
            client_buyer=client_buyer,
            client_logic=client_logic,
        )
        return balance_model

    def create_seller(self) -> SellerCardEggs:
        seller = SellerCardEggs.objects.create(
            inn = self.create_random_inn(),
            prod_address_1 = 'test prod addr',
            region = 'test region',
            requisites = self.create_requisites(),
            documents_contract = self.create_docs_contract(),
            # contact_person = self.create_contact_person(),
            manager = self.create_user('manager'),
        )
        return seller

    def create_buyer(self) -> BuyerCardEggs:
        buyer = BuyerCardEggs.objects.create(
            inn = self.create_random_inn(),
            warehouse_address_1 = 'test prod addr',
            region = 'test region',
            requisites = self.create_requisites(),
            documents_contract = self.create_docs_contract(),
            # contact_person = self.create_contact_person(),
            manager = self.create_user('manager'),
        )
        return buyer

    def create_additional_exp(self) -> AdditionalExpenseEggs:
        exp = AdditionalExpenseEggs.objects.create()
        return exp

    def create_logic(self) -> LogicCardEggs:
        logic = LogicCardEggs.objects.create(
            inn = self.create_random_inn(),
            region = 'test region',
            requisites = self.create_requisites(),
            documents_contract = self.create_docs_contract(),
            manager = self.create_user('manager'),
        )
        return logic

    def create_app_seller(self) -> ApplicationFromSellerBaseEggs:
        app_seller = ApplicationFromSellerBaseEggs.objects.create(
            delivery_window_from = date.today(),
            delivery_window_until = date.today(),
            owner = self.create_user('manager'),
            region = 'test_region',
            cB_white = 3600,
            cB_white_fermer = True,
            cB_cream = 3600,
            cB_cream_fermer = False,
            cB_brown = 3600,
            cB_brown_fermer = True,
            c0_white = 3600,
            c0_white_fermer = False,
            c0_cream = 3600,
            c0_cream_fermer = True,
            c0_brown = 3600,
            c0_brown_fermer = False,
            c1_white = 3000,
            c1_white_fermer = True,
            c1_cream = 3000,
            c1_cream_fermer = False,
            c1_brown = 3000,
            c1_brown_fermer = True,
            c2_white = 3000,
            c2_cream = 3000,
            c2_brown = 3000,
            c3_white = 3000,
            c3_cream = 3000,
            c3_brown = 3000,
            dirt = 3000,
            current_seller = self.create_seller(),
            comment_json = self.create_comment_json(),
            cB_white_cost = 60,
            cB_cream_cost = 59,
            cB_brown_cost = 58,
            c0_white_cost = 57,
            c0_cream_cost = 56,
            c0_brown_cost = 55,
            c1_white_cost = 54,
            c1_cream_cost = 53,
            c1_brown_cost = 52,
            c2_white_cost = 51,
            c2_cream_cost = 50,
            c2_brown_cost = 49,
            c3_white_cost = 48,
            c3_cream_cost = 47,
            c3_brown_cost = 46,
            dirt_cost = 45,
            loading_address = 'test_load_addr',
            import_application = False,
            postponement_pay = 1,
        )
        return app_seller

    def create_app_buyer(self) -> ApplicationFromBuyerBaseEggs:
        app_buyer = ApplicationFromBuyerBaseEggs.objects.create(
            delivery_window_from = date.today(),
            delivery_window_until = date.today(),
            owner = self.create_user('manager'),
            region = 'test_region',
            cB_white = 3600,
            cB_white_fermer = True,
            cB_cream = 3600,
            cB_cream_fermer = False,
            cB_brown = 3600,
            cB_brown_fermer = True,
            c0_white = 3600,
            c0_white_fermer = False,
            c0_cream = 3600,
            c0_cream_fermer = True,
            c0_brown = 3600,
            c0_brown_fermer = False,
            c1_white = 3000,
            c1_white_fermer = True,
            c1_cream = 3000,
            c1_cream_fermer = False,
            c1_brown = 3000,
            c1_brown_fermer = True,
            c2_white = 3000,
            c2_cream = 3000,
            c2_brown = 3000,
            c3_white = 3000,
            c3_cream = 3000,
            c3_brown = 3000,
            dirt = 3000,
            current_buyer = self.create_buyer(),
            comment_json = self.create_comment_json(),
            cB_white_cost = 70,
            cB_cream_cost = 69,
            cB_brown_cost = 68,
            c0_white_cost = 67,
            c0_cream_cost = 66,
            c0_brown_cost = 65,
            c1_white_cost = 64,
            c1_cream_cost = 63,
            c1_brown_cost = 62,
            c2_white_cost = 61,
            c2_cream_cost = 60,
            c2_brown_cost = 59,
            c3_white_cost = 58,
            c3_cream_cost = 57,
            c3_brown_cost = 56,
            dirt_cost = 55,
            unloading_address = 'test_load_addr',
            postponement_pay = 1,
        )
        return app_buyer

    def create_base_deal(self,
            status: int = 1,
            entity: EntityEggs | None = None) -> BaseDealEggsModel:
        if entity is None:
            entity = EntityEggs.objects.get_or_create(
                    name='Пилигрим',
                    inn='5612163931',
            )[0]
        app_seller = self.create_app_seller()
        app_buyer = self.create_app_buyer()
        base_deal_model = BaseDealEggsModel.objects.create(
            # log_status_calc_query = {}
            # log_status_conf_calc_query = {}
            # log_status_deal_query = {}
            # log_status_edit_query = {}
            application_from_buyer = app_buyer,
            application_from_seller = app_seller,
            buyer = app_buyer.current_buyer,
            seller = app_seller.current_seller,
            owner = self.create_user('napr'),
            current_logic = self.create_logic(),
            additional_expense = self.create_additional_exp(),
            documents = self.create_deal_docs(),
            comment_json = self.create_comment_json(),
            status = status,
            deal_status = 0,
            delivery_form_payment = 1,
            delivery_type_of_payment = 1,
            comment = 'test comment',
            note_calc = 'test_note',
            note_conf_calc = '',
            entity=entity,
            # is_active = True,
            # cash = True,
            import_application = False,
            calc_to_confirm = False,
            calc_ready = False,
            logic_confirmed = False,
            deal_status_ready_to_change = False,
            delivery_by_seller = False,
            delivery_cost = 100000.10,
            delivery_date_from_seller = date.today(),
            delivery_date_to_buyer = date.today(),
            loading_address = 'test load addr',
            unloading_address = 'test unload addrr',
            # actual_loading_date = '',
            # actual_unloading_date = '',
            # logic_our_debt_for_app_contract = 0,
            # logic_our_debt_UPD = 0,
            # logic_our_pay_amount = 0,
            # payback_day_for_us = date.today(),
            # payback_day_for_buyer = date.today(),
            # postponement_pay_for_us = 1,
            # postponement_pay_for_buyer = 2,
            # deal_our_pay_amount = 0,
            # deal_buyer_pay_amount = 0,
            # deal_our_debt_UPD = 0,
            # deal_buyer_debt_UPD = 0,
            # margin = 0,
            cB_white = 3600,
            cB_white_fermer = True,
            cB_cream = 3600,
            cB_cream_fermer = False,
            cB_brown = 3600,
            cB_brown_fermer = True,
            c0_white = 3600,
            c0_white_fermer = False,
            c0_cream = 3600,
            c0_cream_fermer = True,
            c0_brown = 3600,
            c0_brown_fermer = False,
            c1_white = 3000,
            c1_white_fermer = True,
            c1_cream = 3000,
            c1_cream_fermer = False,
            c1_brown = 3000,
            c1_brown_fermer = True,
            c2_white = 3000,
            c2_cream = 3000,
            c2_brown = 3000,
            c3_white = 3000,
            c3_cream = 3000,
            c3_brown = 3000,
            dirt = 3000,
            seller_cB_white_cost = 60,
            seller_cB_cream_cost = 59,
            seller_cB_brown_cost = 58,
            seller_c0_white_cost = 57,
            seller_c0_cream_cost = 56,
            seller_c0_brown_cost = 55,
            seller_c1_white_cost = 54,
            seller_c1_cream_cost = 53,
            seller_c1_brown_cost = 52,
            seller_c2_white_cost = 51,
            seller_c2_cream_cost = 50,
            seller_c2_brown_cost = 49,
            seller_c3_white_cost = 48,
            seller_c3_cream_cost = 47,
            seller_c3_brown_cost = 46,
            seller_dirt_cost = 45,
            buyer_cB_white_cost = 70,
            buyer_cB_cream_cost = 69,
            buyer_cB_brown_cost = 68,
            buyer_c0_white_cost = 67,
            buyer_c0_cream_cost = 66,
            buyer_c0_brown_cost = 65,
            buyer_c1_white_cost = 64,
            buyer_c1_cream_cost = 63,
            buyer_c1_brown_cost = 62,
            buyer_c2_white_cost = 61,
            buyer_c2_cream_cost = 60,
            buyer_c2_brown_cost = 59,
            buyer_c3_white_cost = 58,
            buyer_c3_cream_cost = 57,
            buyer_c3_brown_cost = 56,
            buyer_dirt_cost = 55,
        )
        return base_deal_model


