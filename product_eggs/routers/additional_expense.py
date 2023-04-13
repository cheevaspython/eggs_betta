from rest_framework import routers

from product_eggs.views.additional_expense_view import AdditionalExpenseEggsModelViewSet 


additional_expense_router = routers.SimpleRouter()
additional_expense_router.register(r'', AdditionalExpenseEggsModelViewSet)

