from django.contrib import admin
from visual_api import views
from django.urls import include, path
from rest_framework import routers

router = routers.DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path(r'visual/', views.MyViews.as_view(), name='visual_api'),
    path(r'detail/', views.MyDetail.as_view(), name='visual_det'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
]