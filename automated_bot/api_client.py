from dataclasses import dataclass
from typing import Dict, Optional
from urllib.parse import urljoin

import requests


@dataclass
class User:
    __slots__ = ["username", "password", "access_token", "user_id"]

    username: str
    password: str
    access_token: Optional[str]
    user_id: Optional[str]


class APIClient:
    api_url: str

    sign_up_endpoint = "users/signup/"
    auth_endpoint = "users/token/"
    posts_endpoint = "posts/"
    like_post_endpoint = "posts/{post_id}/like/"

    def __init__(self, api_url: str):
        self.api_url = api_url

    def sign_up(self, user: User) -> Dict:
        response = self._send_request(
            method="post",
            uri=self.sign_up_endpoint,
            payload={"username": user.username, "password": user.password},
        )
        user.user_id = response["id"]
        return response

    def authenticate(self, user: User) -> Dict:
        response = self._send_request(
            method="post",
            uri=self.auth_endpoint,
            payload={"username": user.username, "password": user.password},
        )
        user.access_token = response["access"]
        return response

    def create_post(self, user: User, content: str) -> Dict:
        return self._send_request(
            method="post",
            uri=self.posts_endpoint,
            payload={"content": content},
            access_token=user.access_token,
        )

    def like_post(self, user: User, post_id: int) -> Dict:
        return self._send_request(
            method="post",
            uri=self.like_post_endpoint.format(post_id=post_id),
            access_token=user.access_token,
        )

    def _send_request(
        self,
        method: str,
        uri: str,
        payload: Optional[Dict] = None,
        access_token: Optional[str] = None,
    ) -> Dict:
        url = urljoin(self.api_url, uri)
        headers = {"Authorization": f"Bearer {access_token}"} if access_token else {}

        method_to_call = getattr(requests, method)
        response = method_to_call(url=url, data=payload, headers=headers)
        response.raise_for_status()

        return response.json()
