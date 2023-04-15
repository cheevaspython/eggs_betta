from django.urls import path, include

from product_eggs.routers import application_from_buyer_router, \
    application_from_seller_router, buyer_card_eggs_router, \
    seller_card_eggs_router, logic_card_eggs_router, messages_to_users_router, \
    documents_router, base_deal_router, additional_expense_router, \
    balance_router, download_router, requisites_router, tails_router
from product_eggs.views.messages_view import RequestUserMessage
from product_eggs.views.left_sidebar_view import LeftBarEggsViewSet
from product_eggs.views.is_active_offer_view import FieldIsActiveOffApiview


urlpatterns = [
    path('seller_card/', include(seller_card_eggs_router.urls)),
    path('buyer_card/', include(buyer_card_eggs_router.urls)),
    path('logic_card/', include(logic_card_eggs_router.urls)),
    path('requisites/', include(requisites_router.urls)),

    path('balance/', include(balance_router.urls)),
    
    path('application_from_seller/', include(application_from_seller_router.urls)),
    path('application_from_buyer/', include(application_from_buyer_router.urls)),
    path('base_deal/', include(base_deal_router.urls)),
    
    path('additional_expense/', include(additional_expense_router.urls)),
    path('tails/', include(tails_router.urls)),

    path('downloads/', include(download_router.urls)),
    path('documents/', include(documents_router.urls)),
    
    path('message_to_user/', include(messages_to_users_router.urls)),
    path('request_user_message/', RequestUserMessage.as_view(), name='message_request_user'),
    path('left_side_bar/', LeftBarEggsViewSet.as_view(), name='left_side_bar'),
    path('field_is_active_off/', FieldIsActiveOffApiview.as_view(), name='field_is_active_off'),
]
