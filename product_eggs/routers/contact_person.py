from rest_framework import routers

from product_eggs.views.contact_person_view import ContactPersonView

contact_person_router = routers.SimpleRouter()
contact_person_router.register(r'', ContactPersonView)
