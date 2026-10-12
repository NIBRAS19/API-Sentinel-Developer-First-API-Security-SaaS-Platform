from datetime import datetime, timedelta, timezone
import uuid, jwt
from django.conf import settings

ALGORITHM='HS256'

def create_token(user_id, token_type, lifetime):
    now=datetime.now(timezone.utc)
    payload={'sub':str(user_id),'type':token_type,'iat':int(now.timestamp()),'exp':int((now+lifetime).timestamp()),'jti':str(uuid.uuid4())}
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=ALGORITHM)

def access_token(user_id):
    return create_token(user_id,'access',timedelta(minutes=settings.JWT_ACCESS_MINUTES))

def refresh_token(user_id):
    return create_token(user_id,'refresh',timedelta(days=settings.JWT_REFRESH_DAYS))

def decode_token(token, expected_type=None):
    payload=jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
    if expected_type and payload.get('type') != expected_type:
        raise jwt.InvalidTokenError('Unexpected token type')
    return payload
