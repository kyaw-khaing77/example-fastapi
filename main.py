from fastapi import FastAPI
from app.routes.posts import router as posts_router
from app.routes.users import router as users_router
from app.routes.auth import router as auth_router
from app.routes.votes import router as votes_router

app = FastAPI()


# Include routes
app.include_router(posts_router)
app.include_router(users_router)
app.include_router(auth_router)
app.include_router(votes_router)


@app.get("/")
def read_root():
    return {"message": "Hello, World!"}


# create tables at startup
@app.on_event("startup")
def on_startup():
    # import models so they are registered
    from app import models  # noqa: F401, E402
    from app.database import engine, Base

    Base.metadata.create_all(bind=engine)