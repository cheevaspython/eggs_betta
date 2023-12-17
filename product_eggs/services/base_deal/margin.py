

def calculate_margin(instance) -> float:
    """
    Высчитывает маржу стоимостей закупки и продажи плюс стоимость доставки.
    Также учитывает НДС.
    """
    from product_eggs.models.base_deal import BaseDealEggsModel
    from product_eggs.services.base_deal.deal_services import calc_expense_total_for_margin

    if isinstance(instance, BaseDealEggsModel):
        if instance.additional_expense:
            expense_total = calc_expense_total_for_margin(instance.additional_expense)
        else:
            expense_total = 0

        purchase_price_with_tax = (
            instance.cB_white*instance.seller_cB_white_cost +
            instance.cB_cream*instance.seller_cB_cream_cost +
            instance.cB_brown*instance.seller_cB_brown_cost +
            instance.c0_white*instance.seller_c0_white_cost +
            instance.c0_cream*instance.seller_c0_cream_cost +
            instance.c0_brown*instance.seller_c0_brown_cost +
            instance.c1_white*instance.seller_c1_white_cost +
            instance.c1_cream*instance.seller_c1_cream_cost +
            instance.c1_brown*instance.seller_c1_brown_cost +
            instance.c2_white*instance.seller_c2_white_cost +
            instance.c2_cream*instance.seller_c2_cream_cost +
            instance.c2_brown*instance.seller_c2_brown_cost +
            instance.c3_white*instance.seller_c3_white_cost +
            instance.c3_cream*instance.seller_c3_cream_cost +
            instance.c3_brown*instance.seller_c3_brown_cost +
            instance.dirt*instance.seller_dirt_cost
        )

        tax_seller = round((purchase_price_with_tax/110)*10, 2)
        purchase_price_tax_free = purchase_price_with_tax - tax_seller

        delivery_with_tax = instance.delivery_cost
        if instance.delivery_form_payment == 1:
            tax_delivery = (delivery_with_tax/120)*20
        else:
            tax_delivery = 0
        delivery_tax_free = delivery_with_tax - tax_delivery

        production_cost_tax_free = purchase_price_tax_free + delivery_tax_free + expense_total
        tax_paid = tax_seller + tax_delivery

        sales_price_whith_tax = (
            instance.cB_white*instance.buyer_cB_white_cost +
            instance.cB_cream*instance.buyer_cB_cream_cost +
            instance.cB_brown*instance.buyer_cB_brown_cost +
            instance.c0_white*instance.buyer_c0_white_cost +
            instance.c0_cream*instance.buyer_c0_cream_cost +
            instance.c0_brown*instance.buyer_c0_brown_cost +
            instance.c1_white*instance.buyer_c1_white_cost +
            instance.c1_cream*instance.buyer_c1_cream_cost +
            instance.c1_brown*instance.buyer_c1_brown_cost +
            instance.c2_white*instance.buyer_c2_white_cost +
            instance.c2_cream*instance.buyer_c2_cream_cost +
            instance.c2_brown*instance.buyer_c2_brown_cost +
            instance.c3_white*instance.buyer_c3_white_cost +
            instance.c3_cream*instance.buyer_c3_cream_cost +
            instance.c3_brown*instance.buyer_c3_brown_cost +
            instance.dirt*instance.buyer_dirt_cost
        )

        tax_buyer = (sales_price_whith_tax/110)*10
        sales_price_tax_free = sales_price_whith_tax - tax_buyer

        margin_tax_free = sales_price_tax_free - production_cost_tax_free
        tax_difference = tax_paid - tax_buyer

        margin = margin_tax_free + tax_difference

        try:
            if cur_pay := instance.additional_expense.logic_pay:
                margin = margin - cur_pay
        except AttributeError:
            pass

        return round(margin, 2)

    return 0


def calculate_margin_import(instance) -> float:
    """
    Высчитывает маржу стоимостей закупки и продажи плюс стоимость доставки.
    Также учитывает НДС.
    Формула импорта.
    """
    from product_eggs.models.base_deal import BaseDealEggsModel

    if isinstance(instance, BaseDealEggsModel):

        purchase_price = (
            instance.cB_white*instance.seller_cB_white_cost +
            instance.cB_cream*instance.seller_cB_cream_cost +
            instance.cB_brown*instance.seller_cB_brown_cost +
            instance.c0_white*instance.seller_c0_white_cost +
            instance.c0_cream*instance.seller_c0_cream_cost +
            instance.c0_brown*instance.seller_c0_brown_cost +
            instance.c1_white*instance.seller_c1_white_cost +
            instance.c1_cream*instance.seller_c1_cream_cost +
            instance.c1_brown*instance.seller_c1_brown_cost +
            instance.c2_white*instance.seller_c2_white_cost +
            instance.c2_cream*instance.seller_c2_cream_cost +
            instance.c2_brown*instance.seller_c2_brown_cost +
            instance.c3_white*instance.seller_c3_white_cost +
            instance.c3_cream*instance.seller_c3_cream_cost +
            instance.c3_brown*instance.seller_c3_brown_cost +
            instance.dirt*instance.seller_dirt_cost
        )

        delivery_price = instance.delivery_cost

        if instance.additional_expense: #TODO additional_expense f1 or f2
            production_cost = purchase_price + delivery_price + instance.additional_expense.expense_total
        else:
            production_cost = purchase_price + delivery_price

        sales_price_whith_tax = (
            instance.cB_white*instance.buyer_cB_white_cost +
            instance.cB_cream*instance.buyer_cB_cream_cost +
            instance.cB_brown*instance.buyer_cB_brown_cost +
            instance.c0_white*instance.buyer_c0_white_cost +
            instance.c0_cream*instance.buyer_c0_cream_cost +
            instance.c0_brown*instance.buyer_c0_brown_cost +
            instance.c1_white*instance.buyer_c1_white_cost +
            instance.c1_cream*instance.buyer_c1_cream_cost +
            instance.c1_brown*instance.buyer_c1_brown_cost +
            instance.c2_white*instance.buyer_c2_white_cost +
            instance.c2_cream*instance.buyer_c2_cream_cost +
            instance.c2_brown*instance.buyer_c2_brown_cost +
            instance.c3_white*instance.buyer_c3_white_cost +
            instance.c3_cream*instance.buyer_c3_cream_cost +
            instance.c3_brown*instance.buyer_c3_brown_cost +
            instance.dirt*instance.buyer_dirt_cost
        )

        tax_buyer = (sales_price_whith_tax/110)*10
        sales_price_tax_free = sales_price_whith_tax - tax_buyer

        margin = sales_price_tax_free - production_cost
        return round(margin, 2)

    return 0
