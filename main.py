from fastapi import FastAPI
from app.data_directory import router  # Import your app modules
from database import SessionLocal  # Import the database engine

app = FastAPI()

# Include the routers from app modules
app.include_router(router.router, tags=["data_directory"])


@app.on_event("startup")
async def startup_db_client():
    # Set up database session here
    app.db = SessionLocal()


@app.on_event("shutdown")
async def shutdown_db_client():
    # Close the database session here
    app.db.close()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app="main:app", host="0.0.0.0", port=8000, reload=True)
