from product_eggs.routers.applications import (
    application_from_buyer_router, application_from_seller_router
)
from product_eggs.routers.base_card import (
    buyer_card_eggs_router, seller_card_eggs_router,
    logic_card_eggs_router, guest_card_eggs_router
)
from product_eggs.routers.base_deal import base_deal_router
from product_eggs.routers.message_to_user import messages_to_users_router
from product_eggs.routers.documents import documents_router
from product_eggs.routers.additional_expense import additional_expense_router
from product_eggs.routers.balance import (
    balance_router, balance_model_router
)
from product_eggs.routers.download_files import download_router
from product_eggs.routers.requisites import requisites_router
from product_eggs.routers.tails import tails_router
from product_eggs.routers.comments import comments_router
from product_eggs.routers.contact_person import contact_person_router

__all__ = (
    'application_from_buyer_router',
    'application_from_seller_router',
    'buyer_card_eggs_router',
    'seller_card_eggs_router',
    'logic_card_eggs_router',
    'base_deal_router',
    'messages_to_users_router',
    'documents_router',
    'additional_expense_router',
    'balance_router',
    'balance_model_router',
    'download_router',
    'requisites_router',
    'tails_router',
    'guest_card_eggs_router',
    'comments_router',
    'contact_person_router',
)
