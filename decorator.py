import jwt
from flask import request, current_app
from models import User
from functools import wraps


def token_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if "Authorization" in request.headers:
            token = request.headers.get("Authorization")
            if token:
                try:
                    data = jwt.decode(token, current_app.secret_key, algorithms=["HS256"])
                    user = User.query.filter(
                        User.email == data["email"]).first()
                    if not user:
                        return {"message": "user not found"}, 401
                except Exception as e:
                    return {"message": "Invalid token", "error": str(e)}, 401
            else:
                return {"message": "Authentication token required"}, 401
        else:
            return {"message": "Authorization required"}, 401

        return func(*args, **kwargs)

    return wrapper
