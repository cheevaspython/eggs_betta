from collections import OrderedDict

from rest_framework import serializers


class ValidationMassEggs():
    """
    Валидирует суммарный вес продукции яиц к одной фуре.
    """
    STANDART_CATEGORIES = ('c0', 'c1', 'c2', 'c3', 'dirt')
    EGGS_CATEGORY_MASS_MEANING = {'cB':85, 'c0': 75, 'c1': 65, 'c2': 55, 'c3': 45, 'dirt': 65}
    MAXIMUM_WEIGHT_ONE_TRUCK = 19656000                                                                          
    ONE_BOX_STANDART = 36
    ONE_BOX_cB = 30

    def __init__(self, validated_data: OrderedDict | dict):
        self.validated_data = validated_data
        self._mass_hash_map = dict()
        self._quantity_hash_map = dict()

    def start_validate_mass(self):
        self.search_eggs_and_fill_hash_maps()
        self.check_for_maximum_mass_in_one_truck()
        self.check_for_capacity_in_boxes()

    def search_eggs_and_fill_hash_maps(self):
        """
        Парсит входящие данные.
        """
        for egg in self.validated_data:
            if egg in self.EGGS_CATEGORY_MASS_MEANING.keys():
                if self.validated_data[egg]:
                    mass = self.validated_data[egg]*self.EGGS_CATEGORY_MASS_MEANING[egg]
                    self._mass_hash_map[egg] = mass
                    self._quantity_hash_map[egg] = self.validated_data[egg]
 
    def check_for_maximum_mass_in_one_truck(self):
        """
        Сравнивает общую массу с допустимой.
        """
        if sum(self._mass_hash_map.values()) > self.MAXIMUM_WEIGHT_ONE_TRUCK:
            current_mass = sum(self._mass_hash_map.values())
            raise serializers.ValidationError(
                f'Суммарный вес продукции: {current_mass}, ' + 
                f'превышает допустимый для перевозки: {self.MAXIMUM_WEIGHT_ONE_TRUCK}'
            )

    def check_for_capacity_in_boxes(self):
        """
        Проверяет количество кратности коробкам исходя из категории. 
        """
        for cat, quantity in self._quantity_hash_map.items():
            if cat in self.STANDART_CATEGORIES:
                if quantity % self.ONE_BOX_STANDART:
                    raise serializers.ValidationError(
                        f'Указанное количество: {quantity}дес. - не кратно коробке: {self.ONE_BOX_STANDART}дес.'
                    )
            else:
                if quantity % self.ONE_BOX_cB:
                    raise serializers.ValidationError( 
                        f'Указанное количество: {quantity}дес. - не кратно коробке для высшей кат.: {self.ONE_BOX_cB}дес.'
                    )


