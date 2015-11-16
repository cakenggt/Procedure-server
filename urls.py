from django.conf.urls import url
from rest_framework.authtoken import views as authViews

from . import views

urlpatterns = [
    url(r'^api-token-auth/', authViews.obtain_auth_token),
]
