from fastapi import FastAPI
from app.data_directory import router  # Import your app modules

app = FastAPI()

# Include the routers from app modules
app.include_router(router.router, tags=["data_directory"])


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app="main:app", host="0.0.0.0", port=8000)
