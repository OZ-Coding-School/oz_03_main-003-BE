import os
from dataclasses import dataclass, field
from typing import cast, Dict, Any

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


def get_google_tokens_and_user_data(google_data_json):
    access_token = google_data_json["access_token"]
    id_token = google_data_json["id_token"]

    # payload에 들어있는 사용자 정보를 가져오려면 jwt를 decode 해야한다
    decoded_id_token = decode_jwt(id_token)
    user_data = {
        "email": decoded_id_token.get("email"),
        "name": decoded_id_token.get("name"),
        "profile_image": decoded_id_token.get("picture"),
    }
    return access_token, user_data


def get_google_public_keys():
    """
    Google의 공개키를 가져와주는 함수
    """
    response = requests.get("https://www.googleapis.com/oauth2/v3/certs")
    if response.status_code != 200:
        raise ImproperlyConfigured("Failed to fetch Google public keys")
    return response.json()


def decode_jwt(jwt_token) -> Any:
    try:
        decoded_token = jwt.decode(jwt_token, options={"verify_signature": False})
        return decoded_token
    except jwt.ExpiredSignatureError:
        return {"error": "ID token has expired"}
    except jwt.InvalidTokenError:
        return {"error": "Invalid ID token"}


def get_jwt_tokens_for_user(user) -> Dict:
    refresh: RefreshToken = cast(RefreshToken, RefreshToken.for_user(user))
    return {
        "access": str(refresh.access_token),
        "refresh": str(refresh),
    }
