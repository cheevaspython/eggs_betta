from collections import OrderedDict

from product_eggs.services.validationerror import custom_error


class ValidationMassEggs():
    """
    Валидирует суммарный вес продукции яиц к одной фуре.
    """
    STANDART_CATEGORIES = (
        'c1_white', 'c1_cream', 'c1_brown',
        'c2_white', 'c2_cream', 'c2_brown',
        'c3_white', 'c3_cream', 'c3_brown',
        'dirt'
    )
    EGGS_CATEGORY_MASS_MEANING = {
        'cB_white':85, 'cB_cream':85, 'cB_brown':85,
        'c0_white': 75, 'c0_cream': 75, 'c0_brown': 75,
        'c1_white': 65, 'c1_cream': 65, 'c1_brown': 65,
        'c2_white': 55, 'c2_cream': 55, 'c2_brown': 55,
        'c3_white': 45, 'c3_cream': 45, 'c3_brown': 45,
        'dirt': 65
    }
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
                    mass = self.validated_data[egg]*self.EGGS_CATEGORY_MASS_MEANING[egg]*10
                    self._mass_hash_map[egg] = mass
                    self._quantity_hash_map[egg] = self.validated_data[egg]

    def check_for_maximum_mass_in_one_truck(self):
        """
        Сравнивает общую массу с допустимой.
        """
        if sum(self._mass_hash_map.values()) > self.MAXIMUM_WEIGHT_ONE_TRUCK:
            raise custom_error(
                f'Суммарный вес продукции: {sum(self._mass_hash_map.values())}, ' +
                f'превышает допустимый для перевозки: {self.MAXIMUM_WEIGHT_ONE_TRUCK}',
                402
            )

    def check_for_capacity_in_boxes(self):
        """
        Проверяет количество кратности коробкам исходя из категории.
        """
        for cat, quantity in self._quantity_hash_map.items():
            if cat in self.STANDART_CATEGORIES:
                if quantity % self.ONE_BOX_STANDART:
                    raise custom_error(
                        f'Указанное количество: {quantity}дес. - не кратно коробке: {self.ONE_BOX_STANDART}дес.',
                        402
                    )
            else:
                if quantity % self.ONE_BOX_cB:
                    raise custom_error(
                        f'Указанное количество: {quantity}дес. - не кратно коробке для высшей кат.: {self.ONE_BOX_cB}дес.',
                        402
                    )


