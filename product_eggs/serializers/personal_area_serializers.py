from rest_framework import serializers

# from product_eggs.models.base_deal import BaseDealEggsModel
#
#
# class PersonalAreaDealSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = BaseDealEggsModel
#         fields = ['comment_body_json', 'tmp_json']



class DataForPersonAreaSerializer(serializers.Serializer):
    start_date = serializers.DateField(
        input_formats=["%Y-%m-%d", 'iso-8601'],
        required=False
    )
    end_date = serializers.DateField(
        input_formats=["%Y-%m-%d", 'iso-8601'],
        required=False
    )
