from django.db.models import QuerySet 

from product_eggs.models.calcs_deal_eggs import CalculateEggs, ConfirmedCalculateEggs, DealEggs

        
def calc_list_select_related_is_active() -> QuerySet:
    calculate_is_active = CalculateEggs.objects.select_related(
        'application_from_buyer', 'application_from_seller', 'owner', 
    ).filter(is_active=True)
    return calculate_is_active


def conf_calc_list_select_related_is_active() -> QuerySet:
    confirmed_calculate_is_active = ConfirmedCalculateEggs.objects.select_related(
        'current_calculate', 'current_logic', 'owner', 'additional_expense', 
    ).filter(is_active=True)
    return confirmed_calculate_is_active


def deal_list_select_related_is_active() -> QuerySet:
    deal_is_active = DealEggs.objects.select_related(
        'confirmed_calculate', 'owner', 'documents', 
    ).select_related(
        'confirmed_calculate__current_calculate', 'confirmed_calculate__current_logic', 
        'confirmed_calculate__owner', 'confirmed_calculate__additional_expense',
        'documents__origins',
    ).select_related(
        'confirmed_calculate__current_logic__requisites',
        'confirmed_calculate__current_calculate__owner',
    ).filter(is_active=True)
    return deal_is_active 
