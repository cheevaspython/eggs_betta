from product_eggs.models.documents import DocumentsContractEggsModel


def calc_tails_in_json_field(
        documents_model: DocumentsContractEggsModel,
        form: str) -> float:
    """
    parse json tail fields in DocumentsContractEggsModel,
    calc tails,
    return amount
    """
    total_tail_amount: float = 0
    print('start_parser', form)

    for a in documents_model.tail_dict_json:
        tmp_json_dict = documents_model.tail_dict_json[a]
        if isinstance(tmp_json_dict, dict):
            try:
                if tmp_json_dict[form] > 0:
                    total_tail_amount += tmp_json_dict[form] 
            except:
                pass


    print(total_tail_amount)
    return total_tail_amount
