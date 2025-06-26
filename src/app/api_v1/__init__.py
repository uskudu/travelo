from app.api_v1.user.routers import router as user_router
from app.api_v1.admin.routers import router as admin_router

routers = [user_router, admin_router]
