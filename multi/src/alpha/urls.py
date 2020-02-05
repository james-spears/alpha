"""alpha URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from rest_framework import routers

from registrar.views import (
    GoogleOauth2Redirect,
    GoogleOauth2Callback,
    GoogleOauth2TestPass,
    GoogleOauth2TestFail,
    JWTRefreshViewSet,
    UsernameViewSet,
    CompanyViewSet,
    ModuleViewSet,
    ApiKeyViewSet,
    Oauth2EndpointViewSet,
    )

ROUTER = routers.DefaultRouter()
BASE_URL = 'api/v1/'

# oath2 endpoints
ROUTER.register(
    'oauth2', GoogleOauth2Redirect,
    basename='googleoauth2redirect')
ROUTER.register(
    'oauth2/callback', GoogleOauth2Callback,
    basename='googleoauth2callback')
ROUTER.register(
    'oauth2/google/passed', GoogleOauth2TestPass,
    basename='googleoauth2testpass')
ROUTER.register(
    'oauth2/google/failed', GoogleOauth2TestFail,
    basename='googleoauth2testfail')
ROUTER.register(
    'token/refresh', JWTRefreshViewSet,
    basename='tokenrefresh')

# model endpoints
ROUTER.register(
    'model/user', UsernameViewSet,
    basename='modeluser')
ROUTER.register(
    'model/company', CompanyViewSet,
    basename='modelcompany')
ROUTER.register(
    'model/module', ModuleViewSet,
    basename='modelmodule')
ROUTER.register(
    'model/oauth2endpoint', Oauth2EndpointViewSet,
    basename='modeloauth2endpoint')
ROUTER.register(
    'model/apikey', ApiKeyViewSet,
    basename='modelapikey')


admin.site.site_header = "Alpha Admin"
admin.site.site_title = "Alpha Portal"
admin.site.index_title = "Welcome to the Alpha Portal"

urlpatterns = [
    path('admin/', admin.site.urls),
    path(BASE_URL, include((ROUTER.urls, 'alpha'), namespace='api')),
]
