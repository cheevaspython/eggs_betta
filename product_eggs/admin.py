from django.contrib import admin

from product_eggs.models.balance import BalanceBaseClientEggs
from product_eggs.models.base_client import (
    BuyerCardEggs, SellerCardEggs, LogicCardEggs
)
from product_eggs.models.applications import (
    ApplicationFromBuyerBaseEggs, ApplicationFromSellerBaseEggs
)
from product_eggs.models.additional_expense import AdditionalExpenseEggs
from product_eggs.models.base_deal import BaseDealEggsModel
from product_eggs.models.comment import CommentEggs
from product_eggs.models.entity import EntityEggs
from product_eggs.models.messages import MessageToUserEggs
from product_eggs.models.requisites import RequisitesEggs
from product_eggs.models.documents import (
    DocumentsDealEggsModel, DocumentsContractEggsModel
)
from product_eggs.models.origins import OriginsDealEggs
from product_eggs.models.tails import TailsContragentModelEggs
from product_eggs.models.contact_person import ContactPersonEggs


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
    list_display = ('inn', 'name')
    inlines = [BuyerCardEggsAdminIsline]


@admin.register(BuyerCardEggs)
class BuyerCardEggsAdmin(admin.ModelAdmin):
    list_display = (
        'inn', 'manager',
    )
    list_filter = ('inn', 'requisites__name', 'manager', )
    fieldsets = (
        ('Основная информация', {
            'fields': (('inn',),
           ('contact_person', ),
           'manager', 'guest', 'comment', 'region', )
        }),
        ('Платежная информация', {
            'fields': ('requisites', 'documents_contract')
        }),
        ('Адреса складов', {
            'fields' : ('warehouse_address_1',
            'warehouse_address_2', 'warehouse_address_3')
        }),
    )


@admin.register(SellerCardEggs)
class SellerCardEggsAdmin(admin.ModelAdmin):
    list_display = (
        'inn', 'manager',
    )
    list_filter = ('inn', 'requisites__name', 'manager', )
    fieldsets = (
        ('Основная информация', {
            'fields': (('inn',),
                       ('contact_person', ),
                       'manager', 'guest', 'comment', 'region', )
        }),
        ('Платежная информация', {
            'fields': ('requisites', 'documents_contract')
        }),
        ('Адреса производств', {
            'fields' : ('prod_address_1',
            'prod_address_2', 'prod_address_3')
        }),
    )


@admin.register(LogicCardEggs)
class LogicCardEggsAdmin(admin.ModelAdmin):
    list_display = (
        'inn', 'manager',
    )
    list_filter = ('inn', 'requisites__name', 'manager', )
    fieldsets = (
        ('Основная информация', {
            'fields': (('inn',),
                       ('contact_person', ),
                       'manager', 'guest', 'comment', 'region', )
        }),
        ('Платежная информация', {
            'fields': ('requisites', 'documents_contract')
        }),
    )


admin.site.register(
        [
            BaseDealEggsModel,
            AdditionalExpenseEggs, DocumentsDealEggsModel,
            OriginsDealEggs, DocumentsContractEggsModel,
            TailsContragentModelEggs, CommentEggs,
            ContactPersonEggs, BalanceBaseClientEggs,
            EntityEggs
        ]
)
