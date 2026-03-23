from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routers.users_routers import router as user_router
from db.session import init_db

app = FastAPI(on_startup=[
    init_db
], on_shutdown=[])

app.include_router(user_router)

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