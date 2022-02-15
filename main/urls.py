from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView

from .views import UserViewSet, RegisterViewSet, MatchViewSet

router_1 = DefaultRouter()

router_1.register(
    r'list',
    UserViewSet,
    basename='list'
)

router_1.register(
    r'clients/create',
    RegisterViewSet,
    basename='create'
)

urlpatterns = [
    path('clients/<int:pk>/match/', MatchViewSet.as_view()),
    path('', include(router_1.urls)),
    path(
        'create/',
        TokenObtainPairView.as_view(),
        name='token_obtain_pair'
    ),
]
