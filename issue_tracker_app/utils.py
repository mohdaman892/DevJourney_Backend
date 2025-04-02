import jwt
import datetime
import os
from typing_extensions import Any

# Secret key for signing the token (keep it secure)
SECRET_KEY: str = os.environ["SECRET_KEY"]


def create_new_jwt_token(payload: dict[str, Any]) -> str:
    exp_time: datetime = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    payload["expiration_time"] = exp_time.timestamp()  # Expiration time

    # Encode JSON into JWT token
    token: str = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

    return token


def decode_jwt_token(token: str) -> dict | str:
    try:
        # Decode the JWT
        decoded_payload: dict = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return decoded_payload
    except jwt.ExpiredSignatureError:
        raise Exception("Token has expired!")
    except jwt.InvalidTokenError:
        raise Exception("Invalid token!")


def refresh_jwt_token(get_response):

    def middleware(request):
        if "HTTP_X_JWT" in request.META:
            decoded_token = decode_jwt_token(request.META["HTTP_X_JWT"])
            request.META["HTTP_X_JWT"] = create_new_jwt_token(decoded_token)
            request.META["USER_ROLE"] = decoded_token.get("role", "")
        response = get_response(request)

        return response

    return middleware

