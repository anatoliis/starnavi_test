from unittest.mock import patch, MagicMock

from social_network.models import User
from social_network.users.authentication import Authentication


@patch("social_network.users.authentication.update_user_last_request_timestamp")
@patch("social_network.users.authentication.JWTAuthentication.get_user")
def test_authentication__update_last_request_timestamp(
    mocked_get_user: MagicMock,
    mocked_update_user_last_request_timestamp: MagicMock,
    user: User,
):
    mocked_get_user.return_value = user

    auth_plugin = Authentication()
    user = auth_plugin.get_user(validated_token="token")

    mocked_update_user_last_request_timestamp.assert_called_once_with(user)
