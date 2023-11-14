from rest_framework import serializers

from product_eggs.models.comment import CommentEggs


class CommentEggSerializer(serializers.ModelSerializer):

    class Meta:
        model = CommentEggs
        fields = ['comment_body_json', 'tmp_json']


class CommentEggWsSerializer(serializers.ModelSerializer):

    class Meta:
        model = CommentEggs
        fields = ['comment_body_json']
