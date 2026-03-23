import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routers.users_routers import router as user_router
from api.routers.producers_routers import router as producers_router
from api.routers.watches_routers import router as watches_router
from api.routers.verification_codes_routers import router as verification_codes_router
from api.routers.discounts_routers import router as discounts_router
from api.routers.orders_routers import router as orders_router
from api.routers.orders_watches_routers import router as orders_watches_router
from api.routers.admin_users_routers import router as admin_users_router
from api.routers.admin_producers_routers import router as admin_producers_router
from api.routers.admin_watches_routers import router as admin_watches_router
from api.routers.admin_orders_routers import router as admin_orders_router
from api.routers.admin_discounts_routers import router as admin_discounts_router
from api.routers.admin_logs_routers import router as admin_logs_router
from api.routers.admin_stats_routers import router as admin_stats_router
from db.session import init_db

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

app = FastAPI(on_startup=[
    init_db
], on_shutdown=[])

# Публичные роутеры
app.include_router(user_router)
app.include_router(producers_router)
app.include_router(watches_router)
app.include_router(verification_codes_router)
app.include_router(discounts_router)
app.include_router(orders_router)
app.include_router(orders_watches_router)

# Админ роутеры (требуют is_admin=True)
app.include_router(admin_users_router)
app.include_router(admin_producers_router)
app.include_router(admin_watches_router)
app.include_router(admin_orders_router)
app.include_router(admin_discounts_router)
app.include_router(admin_logs_router)
app.include_router(admin_stats_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
            "http://localhost:3000",
            "http://localhost:5173",
            "http://127.0.0.1:3000",
            "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app)