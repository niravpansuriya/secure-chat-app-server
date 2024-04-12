import jwt
from chat_app.settings import SECRET_KEY


def generate_token(payload):
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token


def decode_token(token):
    try:
        decoded_payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return decoded_payload
    except jwt.InvalidTokenError:
        return False
