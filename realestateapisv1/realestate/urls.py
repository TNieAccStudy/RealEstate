from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from realestate import views

router = DefaultRouter()

router.register('acquisitions', views.AcquisitionViewSet, basename='acquisitions')
router.register('users', views.UserViewSet, basename='user')
router.register('lookings', views.LookingViewSet, basename='looking')
router.register('additionals', views.AdditionalInfoViewSet, basename='additional')
router.register('articles', views.HouseArticleViewSet, basename='article')

urlpatterns = [
    path('api/', include(router.urls)),
]
