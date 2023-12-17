from collections import namedtuple
from datetime import datetime
from django.db.models import Q, F, When, Case, DateTimeField
from django.db.models.query import QuerySet

from product_eggs.models.base_deal import BaseDealEggsModel
from product_eggs.services.validationerror import custom_error
from product_eggs.models.personal_area import PersonalSalaryBalanceEggs
from users.models import CustomUser

HashJsonBook = namedtuple('hash_balance', ['hash_amount', 'hash_date'])


class PersonalSalaryBalanceService():
    """
    Принимает 2 даты и менеджера
    Возвращает баланс, сделки и таблицу забранных денег за период
    """
    manager_roles: tuple = ("1", "2", "3", "5")
    month_balance_hash: float = 0

    def __init__(self,
            start_date: datetime,
            end_date: datetime,
            manager: CustomUser,
            entitys_list: list[str]
        ):
        self.start_date = start_date
        self.end_date = end_date
        self.manager = manager
        self.entitys_list = entitys_list
        self.manager_balances: QuerySet
        self.cur_bal: float = 0
        self.comp_bal: float = 0
        self.inwork_bal: float = 0
        self.result_data: dict = {}

    def _check_manager_role(self) -> None:
        if self.manager.role not in self.manager_roles:
            raise custom_error('wrong user role for calc salary', 433)

    def get_all_manager_balances(self):
        self.manager_balances: QuerySet = self.manager.manager_pa.all()
        if not self.manager_balances:
            raise custom_error('manager has no any balance!', 433)

    def _get_cur_salary_balance(self, entity_inn: str) -> PersonalSalaryBalanceEggs | None:
        if self.manager_balances:
            return self.manager_balances.filter(entity=entity_inn).first()

    def get_cur_balance_for_date(self):
        if month_balance_hash := self._try_to_get_month_hash(self.manager, self.start_date):
            self.cur_bal += month_balance_hash.hash_amount
            manager_deals_after_hash_date = BaseDealEggsModel.objects.filter(Q(status=4)).filter(
                Q(seller__manager=self.manager.pk) |
                Q(buyer__manager=self.manager.pk) |
                Q(deal_manager=self.manager.pk)
            ).annotate(
                seller_percent=Case(
                    When(seller__manager=self.manager.pk, then=F('margin')*0.05),
                # output_field=IntegerField(),
                ),
                buyer_percent=Case(
                    When(buyer__manager=self.manager.pk, then=F('margin')*0.05),
                # output_field=IntegerField(),
                ),
                manager_percent=Case(
                    When(deal_manager=self.manager.pk, then=F('margin')*0.045),
                # output_field=IntegerField(),
                )
            ).values(
                'id', 'documents_id', 'deal_our_pay_amount', 'deal_our_debt_UPD',
                'deal_buyer_pay_amount', 'logic_our_pay_amount', 'deal_status',
                'seller', 'buyer', 'entity', 'seller__manager', 'buyer__manager', 'deal_manager',
                'is_active', 'status', 'margin', 'close_deal_date', 'deal_buyer_debt_UPD',
                'seller_percent', 'buyer_percent', 'manager_percent', 'payback_day_for_buyer',
                'id_from_1c', 'postponement_pay_for_buyer', 'delivery_date_to_buyer',
            ).filter(
                Q(close_deal_date__gte=month_balance_hash.hash_date) &
                Q(close_deal_date__lte=self.end_date)
            )
            manager_deals_complete_between_hashdate_and_startdate = manager_deals_after_hash_date.filter(
                Q(close_deal_date__lt=self.start_date)
            )
            #часть между hash и стартовой датой
            salary_between_hash_and_cur_date = self._calc_query_salary_amount(manager_deals_complete_between_hashdate_and_startdate)
            self.cur_bal += salary_between_hash_and_cur_date
            #get between hash and startdate
            if update_wage_book := self._get_updated_entitys_wage_book(self.start_date, month_balance_hash.hash_date):
                self.cur_bal -= sum(list(map(lambda y: sum(map(lambda x: x[0], y.values())), update_wage_book.values())))
        else:
            manager_complete_deals_before_startdate = BaseDealEggsModel.objects.filter(Q(status=4)).filter(
                Q(seller__manager=self.manager.pk) |
                Q(buyer__manager=self.manager.pk) |
                Q(deal_manager=self.manager.pk)
            ).annotate(
                seller_percent=Case(
                    When(seller__manager=self.manager.pk, then=F('margin')*0.05),
                ),
                buyer_percent=Case(
                    When(buyer__manager=self.manager.pk, then=F('margin')*0.05),
                ),
                manager_percent=Case(
                    When(deal_manager=self.manager.pk, then=F('margin')*0.045),
                )
            ).values(
                'id', 'documents_id', 'deal_our_pay_amount', 'deal_our_debt_UPD',
                'deal_buyer_pay_amount', 'logic_our_pay_amount', 'deal_status',
                'seller', 'buyer', 'entity', 'seller__manager', 'buyer__manager', 'deal_manager',
                'is_active', 'status', 'margin', 'close_deal_date', 'deal_buyer_debt_UPD',
                'seller_percent', 'buyer_percent', 'manager_percent', 'payback_day_for_buyer',
                'id_from_1c', 'postponement_pay_for_buyer', 'delivery_date_to_buyer',
            ).filter(
                Q(close_deal_date__lt=self.start_date)
            )
            #часть до стартовой даты
            salary_before_start_date = self._calc_query_salary_amount(manager_complete_deals_before_startdate)
            self.cur_bal += salary_before_start_date
            #sub salary if get_wade
            if update_wage_book := self._get_updated_entitys_wage_book(self.start_date):
                self.cur_bal -= sum(list(map(lambda y: sum(map(lambda x: x[0], y.values())), update_wage_book.values())))

    def _get_updated_entitys_wage_book(self, end_date: datetime, start_date: datetime | None = None) -> dict[str, dict] | None:
            updated_entity_book = {}
            for cur_entity in self.entitys_list:
                if tmp_data := self._get_cur_salary_balance(cur_entity):
                    updated_geted_wage = {
                        cur_date: cur_wage for cur_date, cur_wage in tmp_data.get_wage_dict.items()
                            if self._get_wade_datas_find((cur_date, cur_wage), end_date, start_date)
                    }
                    updated_entity_book[cur_entity] = updated_geted_wage
            return updated_entity_book if len(updated_entity_book.items()) else None

    def get_manager_deals(self) -> None:
        #завершенные сделки в периоде
        self.manager_complete_deals_in_period = BaseDealEggsModel.objects.filter(Q(status=4)).filter(
                Q(seller__manager=self.manager.pk) |
                Q(buyer__manager=self.manager.pk) |
                Q(deal_manager=self.manager.pk)
            ).annotate(
                seller_percent=Case(
                    When(seller__manager=self.manager.pk, then=F('margin')*0.05),
                ),
                buyer_percent=Case(
                    When(buyer__manager=self.manager.pk, then=F('margin')*0.05),
                ),
                manager_percent=Case(
                    When(deal_manager=self.manager.pk, then=F('margin')*0.045),
                )
            ).values(
                'id', 'documents_id', 'deal_our_pay_amount', 'deal_our_debt_UPD',
                'deal_buyer_pay_amount', 'logic_our_pay_amount', 'deal_status',
                'seller', 'buyer', 'entity', 'seller__manager', 'buyer__manager', 'deal_manager',
                'is_active', 'status', 'margin', 'close_deal_date', 'deal_buyer_debt_UPD',
                'seller_percent', 'buyer_percent', 'manager_percent', 'payback_day_for_buyer',
                'id_from_1c', 'postponement_pay_for_buyer', 'delivery_date_to_buyer',
        ).filter(
            Q(close_deal_date__gte=self.start_date) &
            Q(close_deal_date__lte=self.end_date)
        )
        #текущие сделки
        self.manager_deals_in_work = BaseDealEggsModel.objects.filter(Q(status=3)).filter(
                Q(seller__manager=self.manager.pk) |
                Q(buyer__manager=self.manager.pk) |
                Q(deal_manager=self.manager.pk)
            ).annotate(
                seller_percent=Case(
                    When(seller__manager=self.manager.pk, then=F('margin')*0.05),
                ),
                buyer_percent=Case(
                    When(buyer__manager=self.manager.pk, then=F('margin')*0.05),
                ),
                manager_percent=Case(
                    When(deal_manager=self.manager.pk, then=F('margin')*0.045),
                )
            ).values(
                'id', 'documents_id', 'deal_our_pay_amount', 'deal_our_debt_UPD',
                'deal_buyer_pay_amount', 'logic_our_pay_amount', 'deal_status',
                'seller', 'buyer', 'entity', 'seller__manager', 'buyer__manager', 'deal_manager',
                'is_active', 'status', 'margin', 'close_deal_date', 'deal_buyer_debt_UPD',
                'seller_percent', 'buyer_percent', 'manager_percent', 'payback_day_for_buyer',
                'id_from_1c', 'postponement_pay_for_buyer', 'delivery_date_to_buyer',
            )
        #часть между стартовой датой и конечной (вкл) в завершенных сделках
        salary_complete_in_period = self._calc_query_salary_amount(self.manager_complete_deals_in_period)
        self.comp_bal = salary_complete_in_period
        #часть стартовой датой и конечной (вкл) в незавершенных сделках
        salary_in_work_after_startdate = self._calc_query_salary_amount(self.manager_deals_in_work)
        self.inwork_bal = salary_in_work_after_startdate

    def _calc_query_salary_amount(self, query: QuerySet) -> float:
        result: float = 0
        for cur_deal in query:
            if cur_deal['seller__manager'] == self.manager.pk:
                result += round((cur_deal['margin']/100*5), 2)
            if cur_deal['buyer__manager'] == self.manager.pk:
                result += round((cur_deal['margin']/100*5), 2)
            if cur_deal['deal_manager'] == self.manager.pk:
                result += round((cur_deal['margin']/100*4.5), 2)
        return result

    @staticmethod
    def _try_to_get_month_hash(
            cur_manager: CustomUser,
            cur_date: datetime,
        ) -> HashJsonBook | None:
        """
        Ищет в хэше промежуточное значение баланса
        """
        try:
            year_month: str = str(cur_date.year) + '-' + str(cur_date.month)
            tmp_balance = cur_manager.manager_pa.month_hash_dict[year_month]
            tmp_date = datetime.strptime(year_month + '-01',"%Y-%m-%d")
            return HashJsonBook(tmp_balance, tmp_date)
        except (KeyError, AttributeError):
            pass

    @staticmethod
    def _get_wade_datas_find(date_and_wage: tuple[str, float], date_end: datetime, date_start: datetime | None = None) -> float| None:
        convert_date = datetime.strptime(date_and_wage[0], "%Y-%m-%d")
        if date_start:
            if convert_date >= date_start and convert_date <= date_end:
                return date_and_wage[1]
            else:
                return None
        else:
            if convert_date <= date_end:
                return date_and_wage[1]
            else:
                return None

    def _construct_result_data(self):
        self.result_data['period_comp_deals'] = self.manager_complete_deals_in_period
        self.result_data['period_deals_in_work'] = self.manager_deals_in_work
        self.result_data['cur_balance'] = self.cur_bal
        self.result_data['period_comp_deals_balance'] = self.comp_bal
        self.result_data['period_in_work_deals_balance'] = self.inwork_bal
        if update_wage_book := self._get_updated_entitys_wage_book(self.end_date, self.start_date):
            self.result_data['geted_wade_book'] = update_wage_book

    def main(self) -> dict:
        self._check_manager_role()
        self.get_all_manager_balances()
        self.get_cur_balance_for_date()
        self.get_manager_deals()
        self._construct_result_data()
        return self.result_data




