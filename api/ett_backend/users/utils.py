import os
from dataclasses import dataclass, field
from typing import Any, Dict, cast

import jwt
import requests
from django.core.exceptions import ImproperlyConfigured
from rest_framework_simplejwt.tokens import RefreshToken


@dataclass
class GoogleEnvironments:
    """
    init=False : __post_init__ 함수를 호출할 수 있다.
    repr=False : 객체를 print로 찍을 때 해당 필드 데이터는 보이지 않게 됨
    """

    _google_client_id: str = field(init=False, repr=False)
    _google_client_secret: str = field(init=False, repr=False)
    _main_domain: str = field(init=False, repr=False)
    _google_state: str = field(init=False, repr=False)

    def __post_init__(self):
        # 기능은 init과 동일
        # dataclass에서 자동으로 생성한 init이 __post_init__을 호출해준다.
        self._google_client_id = self.get_env_variable("GOOGLE_CLIENT_ID")
        self._google_client_secret = self.get_env_variable("GOOGLE_CLIENT_SECRET")
        self._main_domain = self.get_env_variable("MAIN_DOMAIN")
        self._google_state = self.get_env_variable("GOOGLE_CSRF_STATE")

    @staticmethod
    def get_env_variable(name):
        value = os.getenv(name)
        if not value:
            raise ImproperlyConfigured(f"{name} is not set")
        return value

    @property
    def google_client_id(self):
        return self._google_client_id

    @property
    def google_client_secret(self):
        return self._google_client_secret

    @property
    def main_domain(self):
        return self._main_domain

    @property
    def google_state(self):
        return self._google_state


def get_jwt_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        "access": str(refresh.access_token),
        "refresh": str(refresh),
    }

def generate_new_access_token_for_user(refresh_token):
    token = RefreshToken(refresh_token)
    return str(token.access_token)

def set_jwt_cookie(response, jwt_tokens):
    response.set_cookie(
        key="access",
        value=jwt_tokens["access"],
        httponly=True,
        samesite="Lax",
        secure=True,
    )
    response.set_cookie(
        key="refresh",
        value=jwt_tokens["refresh"],
        httponly=True,
        samesite="Lax",
        secure=True,
    )
    return response

def set_access_cookie(response, access_token):
    response.set_cookie(
        key="access",
        value=access_token,
        httponly=True,
        samesite="Lax",
        secure=True,
    )
    return response

def set_refresh_cookie(response, refresh_token):
    response.set_cookie(
        key="refresh",
        value=refresh_token,
        httponly=True,
        samesite="Lax",
        secure=True,
    )
    return response