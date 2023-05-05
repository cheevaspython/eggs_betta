from django.db.models.query import RawQuerySet

from product_eggs.models.base_deal import BaseDealEggsModel
        

def status_calc_list_query_is_active(pk: int | None = None) -> RawQuerySet:
    add_data = f'c.id = {pk} AND' if pk else ''
    status_calculate_is_active = BaseDealEggsModel.objects.raw(
        f"""SELECT  c.id, c."cB", c.c0, c.c1, c.c2, c.c3, c.dirt, c."seller_cB_cost",
                c.seller_c0_cost, c.seller_c1_cost, c.seller_c2_cost,
                c.seller_c3_cost, c.seller_dirt_cost, c."buyer_cB_cost",
                c.buyer_c0_cost, c.buyer_c1_cost, c.buyer_c2_cost,
                c.buyer_c3_cost, c.buyer_dirt_cost, c.application_from_buyer_id,
                c.application_from_seller_id, c.buyer_id, c.seller_id, c.owner_id,
                c.status, c.comment, c.note_calc, c.cash, c.import_application,
                c.delivery_cost, c.is_active, c.delivery_form_payment, 
                c.delivery_type_of_payment, c.delivery_by_seller, 
                c.delivery_date_from_seller, c.delivery_date_to_buyer, 
                c.deal_buyer_pay_amount, c.deal_our_pay_amount, 
                c.loading_address, c.unloading_address, c.margin, 
                c.postponement_pay_for_us, c.postponement_pay_for_buyer,
                c.logic_our_pay_amount,
                b.inn, b.name as buyer_name, s.inn, s.name as seller_name,
                u.id, u.username as owner_name
            FROM "BaseDealModelEggs" AS c
            INNER JOIN "BuyerCardEggs" AS b ON b.inn = c.buyer_id
            INNER JOIN "SellerCardEggs" AS s ON s.inn = c.seller_id
            LEFT JOIN "users_customuser" AS u ON u.id = c.owner_id
            WHERE {add_data} c.is_active = true AND c.status = 1 
            ORDER BY c.id;"""
    )
    return status_calculate_is_active


def status_conf_calc_list_query_is_active(pk: int | None = None) -> RawQuerySet:
    add_data = f'c.id = {pk} AND' if pk else ''
    status_conf_calculate_is_active = BaseDealEggsModel.objects.raw(
        f"""SELECT  c.id, c."cB", c.c0, c.c1, c.c2, c.c3, c.dirt, c."seller_cB_cost",
                c.seller_c0_cost, c.seller_c1_cost, c.seller_c2_cost,
                c.seller_c3_cost, c.seller_dirt_cost, c."buyer_cB_cost",
                c.buyer_c0_cost, c.buyer_c1_cost, c.buyer_c2_cost,
                c.buyer_c3_cost, c.buyer_dirt_cost, c.current_logic_id,
                c.additional_expense_id, c.application_from_buyer_id,
                c.application_from_seller_id, c.buyer_id, c.seller_id,
                c.owner_id, c.status, c.comment, c.note_calc, c.note_conf_calc,
                c.cash, c.import_application, c.delivery_form_payment,
                c.delivery_cost, c.is_active, c.calc_ready, c.logic_confirmed,
                c.delivery_type_of_payment, c.delivery_by_seller, 
                c.delivery_date_from_seller, c.delivery_date_to_buyer, 
                c.deal_buyer_pay_amount, c.deal_our_pay_amount, 
                c.logic_our_debt_for_app_contract, c.logic_our_pay_amount,
                c.loading_address, c.unloading_address, c.margin, c.documents_id,
                c.postponement_pay_for_us, c.postponement_pay_for_buyer,
                b.inn, b.name as buyer_name, s.inn, s.name as seller_name,
                u.id, u.username as owner_name,
                l.name as logic_name, l.inn as logic_inn,
                a.id, a.expense_total, a.expense_detail_json 
            FROM "BaseDealModelEggs" AS c
            INNER JOIN "BuyerCardEggs" AS b ON b.inn = c.buyer_id
            INNER JOIN "SellerCardEggs" AS s ON s.inn = c.seller_id
            LEFT JOIN "users_customuser" AS u ON u.id = c.owner_id
            LEFT JOIN additional_expense AS a ON a.id = c.additional_expense_id
            LEFT JOIN "LogicCardEggs" AS l ON l.inn = c.current_logic_id
            WHERE {add_data} c.is_active = true AND c.status = 2 
            ORDER BY c.id;"""
    )
    return status_conf_calculate_is_active


def status_deal_list_query_is_active(pk: int | None = None) -> RawQuerySet:
    add_data = f'c.id = {pk} AND' if pk else ''
    status_deal_is_active = BaseDealEggsModel.objects.raw(
        f"""SELECT  c.id, c."cB", c.c0, c.c1, c.c2, c.c3, c.dirt, c."seller_cB_cost",
                c.seller_c0_cost, c.seller_c1_cost, c.seller_c2_cost,
                c.seller_c3_cost, c.seller_dirt_cost, c."buyer_cB_cost",
                c.buyer_c0_cost, c.buyer_c1_cost, c.buyer_c2_cost,
                c.buyer_c3_cost, c.buyer_dirt_cost, c.current_logic_id,
                c.additional_expense_id, c.application_from_buyer_id,
                c.application_from_seller_id, c.buyer_id, c.seller_id,
                c.owner_id, c.status, c.comment, c.note_calc, c.note_conf_calc,
                c.cash, c.import_application, c.delivery_form_payment,
                c.delivery_cost, c.is_active, c.calc_ready, c.logic_confirmed,
                c.delivery_type_of_payment, c.delivery_by_seller, 
                c.delivery_date_from_seller, c.delivery_date_to_buyer, 
                c.logic_our_debt_for_app_contract, c.logic_our_pay_amount,
                c.loading_address, c.unloading_address, c.margin, c.documents_id,
                c.postponement_pay_for_us, c.postponement_pay_for_buyer,
                c.documents_id, c.deal_status, c.actual_loading_date,
                c.actual_unloading_date, c.payback_day_for_us, c.payback_day_for_buyer,
                c.deal_buyer_pay_amount, c.deal_our_pay_amount, 
                c."deal_our_debt_UPD", c."deal_buyer_debt_UPD",
                c."logic_our_debt_UPD",
                b.inn, b.name as buyer_name, s.inn, s.name as seller_name,
                u.id, u.username as owner_name, 
                l.name as logic_name, l.inn as logic_inn,
                a.id, a.expense_total, a.expense_detail_json
            FROM "BaseDealModelEggs" AS c
            INNER JOIN "BuyerCardEggs" AS b ON b.inn = c.buyer_id
            INNER JOIN "SellerCardEggs" AS s ON s.inn = c.seller_id
            LEFT JOIN "users_customuser" AS u ON u.id = c.owner_id
            LEFT JOIN additional_expense AS a ON a.id = c.additional_expense_id
            LEFT JOIN "LogicCardEggs" AS l ON l.inn = c.current_logic_id
            WHERE {add_data} c.is_active = true AND c.status = 3 
            ORDER BY c.id;"""
    )
    return status_deal_is_active


def status_comp_deal_list_query_is_active(pk: int | None = None) -> RawQuerySet:
    add_data = f'c.id = {pk} AND' if pk else ''
    status_deal_is_active = BaseDealEggsModel.objects.raw(
        f"""SELECT  c.id, c."cB", c.c0, c.c1, c.c2, c.c3, c.dirt, c."seller_cB_cost",
                c.seller_c0_cost, c.seller_c1_cost, c.seller_c2_cost,
                c.seller_c3_cost, c.seller_dirt_cost, c."buyer_cB_cost",
                c.buyer_c0_cost, c.buyer_c1_cost, c.buyer_c2_cost,
                c.buyer_c3_cost, c.buyer_dirt_cost, c.current_logic_id,
                c.additional_expense_id, c.application_from_buyer_id,
                c.application_from_seller_id, c.buyer_id, c.seller_id,
                c.owner_id, c.status, c.comment, c.note_calc, c.note_conf_calc,
                c.cash, c.import_application, 
                c.delivery_cost, c.is_active, c.calc_ready, c.logic_confirmed,
                c.delivery_type_of_payment, c.delivery_by_seller, 
                c.delivery_date_from_seller, c.delivery_date_to_buyer, 
                c.logic_our_debt_for_app_contract, c.logic_our_pay_amount,
                c.loading_address, c.unloading_address, c.margin, c.documents_id,
                c.postponement_pay_for_us, c.postponement_pay_for_buyer,
                c.documents_id, c.deal_status, c.actual_loading_date,
                c.actual_unloading_date, c.payback_day_for_us, c.payback_day_for_buyer,
                c.deal_our_pay_amount, c.deal_buyer_pay_amount, 
                c."deal_our_debt_UPD", c."deal_buyer_debt_UPD",
                c."logic_our_debt_UPD",
                c.log_status_calc_query, c.log_status_conf_calc_query,
                c.log_status_deal_query,
                b.inn, b.name as buyer_name, s.inn, s.name as seller_name,
                u.id, u.username as owner_name, 
                l.name as logic_name, l.inn as logic_inn,
                a.id, a.expense_total, a.expense_detail_json
            FROM "BaseDealModelEggs" AS c
            INNER JOIN "BuyerCardEggs" AS b ON b.inn = c.buyer_id
            INNER JOIN "SellerCardEggs" AS s ON s.inn = c.seller_id
            LEFT JOIN "users_customuser" AS u ON u.id = c.owner_id
            LEFT JOIN additional_expense AS a ON a.id = c.additional_expense_id
            LEFT JOIN "LogicCardEggs" AS l ON l.inn = c.current_logic_id
            WHERE {add_data} c.is_active = true AND c.status = 3 
            ORDER BY c.id;"""
    )
    return status_deal_is_active


# def status_deal_list_query_is_active_with_docs(pk: int | None = None) -> RawQuerySet:
#
#     add_data = f'c.id = {pk} AND' if pk else ''
#
#     status_deal_is_active = BaseDealEggsModel.objects.raw(
#         f"""SELECT  c.id, c."cB", c.c0, c.c1, c.c2, c.c3, c.dirt, c."seller_cB_cost",
#                 c.seller_c0_cost, c.seller_c1_cost, c.seller_c2_cost,
#                 c.seller_c3_cost, c.seller_dirt_cost, c."buyer_cB_cost",
#                 c.buyer_c0_cost, c.buyer_c1_cost, c.buyer_c2_cost,
#                 c.buyer_c3_cost, c.buyer_dirt_cost, c.current_logic_id,
#                 c.additional_expense_id, c.application_from_buyer_id,
#                 c.application_from_seller_id, c.buyer_id, c.seller_id,
#                 c.owner_id, c.status, c.comment, c.note_calc, c.note_conf_calc,
#                 c.cash, c.import_application, 
#                 c.delivery_cost, c.is_active, c.calc_ready, c.logic_confirmed,
#                 c.delivery_type_of_payment, c.delivery_by_seller, 
#                 c.delivery_date_from_seller, c.delivery_date_to_buyer, 
#                 c.loading_address, c.unloading_address, c.margin, 
#                 c.postponement_pay_for_us, c.postponement_pay_for_buyer,
#                 c.documents_id, c.deal_status, c.actual_loading_date,
#                 c.actual_unloading_date, c.payback_day_for_us, c.payback_day_for_buyer,
#                 c.current_deal_our_debt, c.current_deal_buyer_debt, 
#                 c."deal_our_debt_UPD", c."deal_buyer_debt_UPD",
#                 b.inn, b.name as buyer_name, s.inn, s.name as seller_name,
#                 u.id, u.username as owner_name, 
#                 l.id, l.name as logic_name, l.inn as logic_inn,
#                 a.id, a.expense_total, a.expense_detail_json
#             FROM "BaseDealModelEggs" AS c
#             INNER JOIN "BuyerCardEggs" AS b ON b.inn = c.buyer_id
#             INNER JOIN "SellerCardEggs" AS s ON s.inn = c.seller_id
#             LEFT JOIN "users_customuser" AS u ON u.id = c.owner_id
#             LEFT JOIN additional_expense AS a ON a.id = c.additional_expense_id
#             LEFT JOIN "LogicEggs" AS l ON l.id = c.current_logic_id
#             INNER JOIN 
#               (SELECT id, payment_for_contract, payment_order_incoming, payment_order_outcoming,
#                   specification_seller, account_to_seller, account_to_seller, account_to_buyer, 
#                   application_contract_logic, account_to_logic, "UPD_incoming", account_invoicing_from_seller,
#                   product_invoice_from_seller, "UPD_outgoing", account_invoicing_from_buyer, 
#                   product_invoice_from_buyer, veterinary_certificate_buyer, veterinary_certificate_seller,
#                   "international_deal_CMR", "international_deal_TTN", "UPD_logic", account_invoicing_logic, 
#                   product_invoice_logic
#             FROM "DocumentsDealEggs") doc_detail ON doc_detail.id = c.documents_id
#             WHERE {add_data} c.is_active = true AND c.status = 3 
#             ORDER BY c.id;"""
#     )
#     return status_deal_is_active
