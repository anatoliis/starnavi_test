from django.urls import path

from social_network.users.views.create_user import CreateUserView
from social_network.users.views.obtain_token import ObtainTokenView
from social_network.users.views.token_refresh import DecoratedTokenRefreshView
from social_network.users.views.user_activity import UserActivityView

app_name = "social_network"

urlpatterns = [
    path("signup/", CreateUserView.as_view(), name="signup"),
    path("token/", ObtainTokenView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", DecoratedTokenRefreshView.as_view(), name="token_refresh"),
    path("activity/", UserActivityView.as_view(), name="activity"),
]
