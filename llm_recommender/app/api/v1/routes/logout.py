from fastapi import APIRouter, Response

router = APIRouter()

@router.post("/logout")
async def logout_user(response: Response):
    # Clear the authentication cookie
    response.delete_cookie(
        key="access_token",
        samesite="Lax"
    )
    return {"message": "Successfully logged out"}