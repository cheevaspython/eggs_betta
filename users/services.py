from typing import OrderedDict

from users.models import CustomUser


def master_pass_validate(data: OrderedDict, user: CustomUser) -> bool | None:
    if user.master_password:
        if user.master_password == data['entered_password']:
            return True
    else:
        return False
