import time
import jwt
from uuid import uuid4
from app import service


class JWTException(Exception):

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return "%s" % (self.message)


def decode(request):
    """
    Returns the de-codification od the JWT in the request, with the following claims:
      - iss: The issuer of the token.
      - jti: The unique identifier of the token.
      - sub: The subject of the token (optional).
      - iat: Epoch of the issue date.
      - exp: Expiration epoch date of the token.
      - user_id: TrueVault user ID of the token.
      - access_token: TrueVault access token.
    """
    token = service.config.get('JWT_TOKEN')
    return jwt.decode(token, service.config.get('JWT_SECRET'), algorithm='HS256')


def generate_jwt_oauth2(user, access_token):
    """
    Return a new JSON Web Token, with the following claims:
      - iss: The issuer of the token.
      - jti: The unique identifier of the token.
      - sub: The subject of the token (optional).
      - iat: Epoch of the issue date.
      - exp: Expiration epoch date of the token.
      - user_id: TrueVault user ID of the token.
      - access_token: TrueVault access token.
    """
    jti = str(uuid4())
    now = int(time.time())
    payload = {
        'iss': 'auth.ubiome.com',
        'iat': int(time.time()),
        'jti': jti,
        'exp': now + 86399,
        'access_token': access_token,
        'user_id': user.get('user_id', None),
        'document_id': user.get('document_id', None),
        'group_id': user.get('group_id', None),
    }
    return jwt.encode(payload, service.config.get('JWT_SECRET'), algorithm='HS256')


def parse_jwt_oauth2(token):
    return jwt.decode(token, service.config.get('JWT_SECRET'), algorithm='HS256')
