from django.db.models import QuerySet
                                                         
from product_eggs.models.calcs_deal_eggs import CalculateEggs, ConfirmedCalculateEggs, \
    DealEggs
                                                                                                                                               

def calculate_margin_python(
        instance: CalculateEggs | DealEggs, delivery_cost: float,
        expense_total: float=0) -> float: 
    """
    Высчитывает маржу стоимостей закупки и продажи плюс стоимость доставки.
    Также учитывает НДС.
    """
    purchase_price_with_tax = (instance.cB*instance.seller_cB_cost + 
        instance.c0*instance.seller_c0_cost + instance.c1*instance.seller_c1_cost + 
        instance.c2*instance.seller_c2_cost + instance.c3*instance.seller_c3_cost + 
        instance.dirt*instance.seller_dirt_cost)
    tax_seller = round((purchase_price_with_tax/110)*10, 2)
    purchase_price_tax_free = purchase_price_with_tax - tax_seller 

    delivery_with_tax = delivery_cost
    if instance.delivery_type_of_payment:
        tax_delivery = (delivery_with_tax/120)*20
    else: 
        tax_delivery = 0
    delivery_tax_free = delivery_with_tax - tax_delivery

    production_cost_tax_free = purchase_price_tax_free + delivery_tax_free + expense_total
    tax_paid = tax_seller + tax_delivery

    sales_price_whith_tax = (instance.cB*instance.buyer_cB_cost + 
        instance.c0*instance.buyer_c0_cost + instance.c1*instance.buyer_c1_cost + 
        instance.c2*instance.buyer_c2_cost + instance.c3*instance.buyer_c3_cost + 
        instance.dirt*instance.buyer_dirt_cost)
    tax_buyer = (sales_price_whith_tax/110)*10
    sales_price_tax_free = sales_price_whith_tax - tax_buyer

    margin_tax_free = sales_price_tax_free - production_cost_tax_free  
    tax_difference = tax_paid - tax_buyer

    margin = margin_tax_free + tax_difference

    return round(margin, 2)


def calculate_margin_python_import(
            instance: CalculateEggs | DealEggs, delivery_cost: float,
            expense_total: float=0) -> float: 
    """
    Высчитывает маржу стоимостей закупки и продажи плюс стоимость доставки.
    Также учитывает НДС.
    Формула импорта.
    """
    purchase_price = (instance.cB*instance.seller_cB_cost + 
        instance.c0*instance.seller_c0_cost + instance.c1*instance.seller_c1_cost + 
        instance.c2*instance.seller_c2_cost + instance.c3*instance.seller_c3_cost + 
        instance.dirt*instance.seller_dirt_cost)

    delivery_price = delivery_cost

    production_cost = purchase_price + delivery_price + expense_total

    sales_price_whith_tax = (instance.cB*instance.buyer_cB_cost + 
        instance.c0*instance.buyer_c0_cost + instance.c1*instance.buyer_c1_cost + 
        instance.c2*instance.buyer_c2_cost + instance.c3*instance.buyer_c3_cost + 
        instance.dirt*instance.buyer_dirt_cost)
    tax_buyer = (sales_price_whith_tax/110)*10
    sales_price_tax_free = sales_price_whith_tax - tax_buyer

    margin = sales_price_tax_free - production_cost

    return round(margin, 2)


def add_margin_field_calculate(instance_queryset: QuerySet[CalculateEggs]) -> None:
    """
    Добавляет поле margin в коллекцию модели CalculateEggs.
    """
    for calc in instance_queryset:
        if calc.import_application:
            setattr(calc, 'margin', calculate_margin_python_import(calc, calc.delivery_cost))
        else:
            setattr(calc, 'margin', calculate_margin_python(calc, calc.delivery_cost))


def add_margin_field_to_conf_calc(instance_queryset: QuerySet[ConfirmedCalculateEggs]) -> None:
    """
    Добавляет поле margin в коллекцию модели ConfirmedCalculateEggs.
    """
    for conf_calc in instance_queryset:
        if conf_calc.current_calculate.import_application:
            setattr(
                conf_calc, 'margin',
                calculate_margin_python_import(
                    conf_calc.current_calculate, 
                    conf_calc.delivery_cost,
                    conf_calc.additional_expense.expense_total,
                )
            )
        else:
            setattr(
                conf_calc, 'margin',
                calculate_margin_python(
                    conf_calc.current_calculate, 
                    conf_calc.delivery_cost,
                    conf_calc.additional_expense.expense_total,
                )
            )


def add_margin_field_to_deal(instance_queryset: QuerySet[DealEggs]) -> None:
    """
    Добавляет поле margin в коллекцию модели DealEggs.
    """
    for deal in instance_queryset:
        if deal.import_application:
            setattr(
                deal, 'margin',
                calculate_margin_python_import(
                    deal, 
                    deal.delivery_cost,
                    deal.confirmed_calculate.additional_expense.expense_total,
                )
            )
        else:
            setattr(
                deal, 'margin',
                calculate_margin_python(
                    deal, 
                    deal.delivery_cost,
                    deal.confirmed_calculate.additional_expense.expense_total,
                )
            )


