from django.contrib import admin

from product_eggs.models.base_client import BuyerCardEggs, SellerCardEggs, \
    LogicCardEggs
from product_eggs.models.applications import ApplicationFromBuyerBaseEggs, \
    ApplicationFromSellerBaseEggs
from product_eggs.models.additional_expense import AdditionalExpenseEggs
from product_eggs.models.base_deal import BaseDealEggsModel
from product_eggs.models.messages import MessageToUserEggs
from product_eggs.models.requisites import RequisitesEggs
from product_eggs.models.documents import DocumentsDealEggsModel, \
    DocumentsContractEggsModel
from product_eggs.models.origins import OriginsDealEggs
from product_eggs.models.tails import TailsContragentModelEggs


@admin.register(ApplicationFromBuyerBaseEggs)
class ApplicationFromBuyerBaseEggsAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'current_buyer', 'owner',
        'delivery_window_from', 'delivery_window_until' 
    )


@admin.register(ApplicationFromSellerBaseEggs)
class ApplicationFromSellerBaseEggsAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'current_seller', 'owner',
        'delivery_window_from', 'delivery_window_until' 
    )


@admin.register(MessageToUserEggs)
class MessageToUserEggsAdmin(admin.ModelAdmin):
    list_display = ('message_to', 'message', 'created_date')
    list_filter = ('created_date', )


class BuyerCardEggsAdminIsline(admin.TabularInline):
    model = BuyerCardEggs


@admin.register(RequisitesEggs)
class RequisitesEggsAdmin(admin.ModelAdmin):
    list_display = ('general_manager', 'inn')
    inlines = [BuyerCardEggsAdminIsline]


@admin.register(BuyerCardEggs)
class BuyerCardEggsAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'inn', 'general_manager', 'phone',
        'email', 
    )
    list_filter = ('name', 'inn')
    fieldsets = (
        ('Основная информация', {
            'fields': (('name', 'inn', 'general_manager'),
                       ('contact_person', 'phone', 'email'),
                       'manager', 'comment', 'region', )
        }),
        ('Платежная информация', {
            'fields': (( 'balance',), ('pay_limit', 'balance_form_one'),
                       ('pay_limit_cash', 'balance_form_two'), ('tails'),
                       'requisites', 'documents_contract')
        }),
        ('Адреса складов', {
            'fields' : ('warehouse_address_1', 
            'warehouse_address_2', 'warehouse_address_3')
        }),
    )


@admin.register(SellerCardEggs)
class SellerCardEggsAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'inn', 'general_manager', 'phone',
        'email', 
                    )
    list_filter = ('name', 'inn')
    fieldsets = (
        ('Основная информация', {
            'fields': (('name', 'inn', 'general_manager'),
                       ('contact_person', 'phone', 'email'),
                       'manager', 'comment','region', )
        }),
        ('Платежная информация', {
            'fields': (( 'balance', 'balance_form_one', 'balance_form_two'), ('tails'),
                       'requisites', 'documents_contract',)
        }),
        ('Адреса производств', {
            'fields' : ('prod_address_1', 
            'prod_address_2', 'prod_address_3')
        }),
    )


@admin.register(LogicCardEggs)
class LogicCardEggsAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'inn', 'general_manager', 'phone',
        'email', 
                    )
    list_filter = ('name', 'inn')
    fieldsets = (
        ('Основная информация', {
            'fields': (('name', 'inn', 'general_manager'),
                       ('contact_person', 'phone', 'email'),
                       'comment',)
        }),
        ('Платежная информация', {
            'fields': (( 'balance', 'balance_form_one', 'balance_form_two'),
                       'requisites', 'documents_contract')
        }),
    )


admin.site.register(
        [
            BaseDealEggsModel,
            AdditionalExpenseEggs, DocumentsDealEggsModel, 
            OriginsDealEggs, DocumentsContractEggsModel,
            TailsContragentModelEggs,
        ]
)
