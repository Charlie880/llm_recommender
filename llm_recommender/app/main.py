from fastapi import FastAPI, Depends
from app.api.v1.routes.auth import router as auth_router  # Import your auth routes
from app.api.v1.routes.logout import router as logout_router  # Import profile routes
from app.db.session import engine, Base
from app.core.config import settings  # Import the settings to use in the app
from app.api.v1.routes.product import router as product_router  # Import product routes
from app.api.v1.routes.recommendation import router as recommendation_router  # Import recommendation routes
from app.api.v1.routes.profile import router as profile_router  # Import profile routes
from app.core.dependencies import get_current_user  # Import get_current_user dependency
from app.api.v1.routes import feedback as feedback_router

# Initialize FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.api_version,
    debug=settings.app_debug,
)

app = FastAPI()

app.include_router(auth_router, prefix="/auth", tags=["Sign Up/Login"])
app.include_router(profile_router, prefix="/profile", tags=["Profile"])
app.include_router(logout_router, prefix="/auth", tags=["Log Out"])
app.include_router(product_router, prefix="/products", tags=["Products"])
app.include_router(recommendation_router, prefix="/recommendations", tags=["Recommendations"], dependencies=[Depends(get_current_user)])
app.include_router(feedback_router.router, prefix="/feedback", tags=["Feedback"],  dependencies=[Depends(get_current_user)])