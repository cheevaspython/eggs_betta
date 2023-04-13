
def calculate_margin_python(instance) -> float: 
    """
    Высчитывает маржу стоимостей закупки и продажи плюс стоимость доставки.
    Также учитывает НДС.
    """
    from product_eggs.models.base_deal import BaseDealEggsModel

    if isinstance(instance, BaseDealEggsModel):
        if instance.additional_expense:
            expense_total = instance.additional_expense.expense_total
        else: 
            expense_total = 0

        purchase_price_with_tax = (instance.cB*instance.seller_cB_cost + 
        instance.c0*instance.seller_c0_cost + instance.c1*instance.seller_c1_cost + 
        instance.c2*instance.seller_c2_cost + instance.c3*instance.seller_c3_cost + 
        instance.dirt*instance.seller_dirt_cost)

        tax_seller = round((purchase_price_with_tax/110)*10, 2)
        purchase_price_tax_free = purchase_price_with_tax - tax_seller 

        delivery_with_tax = instance.delivery_cost
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
    return 0




# def calculate_margin_python_import(
#             instance: CalculateEggs | DealEggs, delivery_cost: float,
#             expense_total: float=0) -> float: 
#     """
#     Высчитывает маржу стоимостей закупки и продажи плюс стоимость доставки.
#     Также учитывает НДС.
#     Формула импорта.
#     """
#     purchase_price = (instance.cB*instance.seller_cB_cost + 
#         instance.c0*instance.seller_c0_cost + instance.c1*instance.seller_c1_cost + 
#         instance.c2*instance.seller_c2_cost + instance.c3*instance.seller_c3_cost + 
#         instance.dirt*instance.seller_dirt_cost)
#
#     delivery_price = delivery_cost
#
#     production_cost = purchase_price + delivery_price + expense_total
#
#     sales_price_whith_tax = (instance.cB*instance.buyer_cB_cost + 
#         instance.c0*instance.buyer_c0_cost + instance.c1*instance.buyer_c1_cost + 
#         instance.c2*instance.buyer_c2_cost + instance.c3*instance.buyer_c3_cost + 
#         instance.dirt*instance.buyer_dirt_cost)
#     tax_buyer = (sales_price_whith_tax/110)*10
#     sales_price_tax_free = sales_price_whith_tax - tax_buyer
#
#     margin = sales_price_tax_free - production_cost
#
#     return round(margin, 2)
