"""social_network URL Configuration

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
from django.urls import include
from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

app_name = "social_network"

schema_view = get_schema_view(
    openapi.Info(
        title="Social Network API",
        default_version="v1",
        description="Take-home task",
        contact=openapi.Contact(email="anatolii.sukovach@gmail.com"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path("api/", include("social_network.api.urls", namespace="api")),
    path("api/users/", include("social_network.users.urls", namespace="users")),
    path(
        "api/redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"
    ),
]
