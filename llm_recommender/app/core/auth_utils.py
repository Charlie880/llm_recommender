# app/core/auth_utils.py
from fastapi import Request, HTTPException, status

def get_token_from_request(request: Request) -> str:
    auth_header = request.headers.get("Authorization")
    cookie_token = request.cookies.get("access_token")

    if auth_header and auth_header.startswith("Bearer "):
        return auth_header[7:]
    elif cookie_token and cookie_token.startswith("Bearer "):
        return cookie_token[7:]
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or malformed token"
        )
