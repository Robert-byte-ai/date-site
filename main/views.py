from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import mixins, viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import F, ExpressionWrapper, FloatField

from .models import User, Match
from .serializers import (
    UserListSerializer,
    UserRegisterSerializer,
    MatchSerializer
)
from .utils import distance_1


class UserViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = (AllowAny,)
    serializer_class = UserListSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('gender', 'first_name', 'last_name')

    def get_queryset(self,):
        user = self.request.user
        queryset = User.objects.exclude(username=user.username)
        distance = self.request.query_params.get('distance')
        if distance:
            queryset = queryset.annotate(
                dis=ExpressionWrapper(
                    distance_1(
                        user.latitude,
                        F('latitude'),
                        user.longitude,
                        F('longitude')
                    ),
                    output_field=FloatField()
                )
            ).filter(dis__lt=float(distance))
        return queryset


class RegisterViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = UserRegisterSerializer
    permission_classes = (AllowAny,)


class MatchViewSet(APIView):
    permission_classes = (IsAuthenticated,)

    @action(detail=True, methods=['POST'])
    def post(self, request, pk=None):
        user = request.user
        liked_user = get_object_or_404(User, pk=self.kwargs['pk'])
        serializer = MatchSerializer(data=request.data, context={"request": request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            if Match.objects.filter(user=liked_user, liked_user=user).exists():
                self.send_notification(liked_user, user)
                self.send_notification(user, liked_user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors)

    def send_notification(self, user1, user2):
        send_mail(
            'Уведомление',
            f'Вы понравились: {user2.username}, его/ее почта: {user2.email}',
            'company@gmail.com',
            [user1.email],
        )
