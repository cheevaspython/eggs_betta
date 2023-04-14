from typing import Iterable

from product_eggs.models.base_client import BuyerCardEggs, LogicCardEggs, \
    SellerCardEggs
from product_eggs.models.base_deal import BaseDealEggsModel
from product_eggs.services.create_model import CreatorNewModel
from product_eggs.services.data_class import BaseMessageForm


class MessagesCreator():
    """
    Create messages.
    """
    def __init__(self, message_form: BaseMessageForm):
        self.data = message_form
        self._seller = None
        self._buyer = None
        self._logic = None
        self._base_deal = None
        self.user = None
        self.idetify_model()
        self.identify_user()
        
    def idetify_model(self):
        """
        Add value idetify model.
        """
        if isinstance(self.data.model, BuyerCardEggs):
            self._buyer = self.data.model
        elif isinstance(self.data.model, SellerCardEggs):
            self._seller = self.data.model
        elif isinstance(self.data.model, LogicCardEggs):
            self._logic = self.data.model
        elif isinstance(self.data.model, BaseDealEggsModel):
            self._base_deal = self.data.model

    def identify_user(self):
        """
        If user is not iterable, make him tuple.
        """
        if isinstance(self.data.user, Iterable):
            self.user = self.data.user
        else:
            self.user = (self.data.user,)

    def create_message(self):
        """
        Create new model MessageToUserEggs.  
        """
        print(self.user)
        if isinstance(self.user, Iterable):
            for user in self.user:
                self.new_model = CreatorNewModel(
                    ('MessageToUserEggs',),
                    message = self.data.message,
                    message_to = user,
                    current_base_deal = self._base_deal,
                    current_seller = self._seller,
                    current_buyer = self._buyer,
                    current_logic = self._logic,
                )
                self.new_model.create()
