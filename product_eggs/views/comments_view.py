from dataclasses import asdict
from datetime import datetime
from typing import OrderedDict

from rest_framework import status, viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from product_eggs.services.comments import get_log_to_comment, parse_comment_tmp_json
from product_eggs.models.comment import CommentEggs
from product_eggs.serializers.comments_serializers import CommentEggSerializer


class CommentsEggsModelViewSet(viewsets.ViewSet):
    queryset = CommentEggs.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        serializer = CommentEggSerializer(self.queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['patch'])
    def update_comment(self, request, pk=None) -> Response:
        instance = self.queryset.get(pk=pk)
        serializer = CommentEggSerializer(
            instance, data=request.data, partial=True
        )
        serializer.is_valid()

        if isinstance(serializer.validated_data, OrderedDict):
            if data_for_save := parse_comment_tmp_json(
                    serializer.validated_data, request.user):
                instance.comment_body_json.update(
                    {str(datetime.today()): asdict(data_for_save)}
                )
                if log := get_log_to_comment(data_for_save):
                    instance.logs.update(
                        {str(datetime.today()): log}
                    )
                instance.tmp_json = {}
                instance.save()
                return Response(status=status.HTTP_200_OK)

        return Response('Wrong tmp_json')





