# main.py

from fastapi import FastAPI
from routes.restaurant import router as restaurant_router
from routes.cafe import router as cafe_router

app = FastAPI()

app.include_router(restaurant_router, prefix="/api", tags=["restaurants"])
app.include_router(cafe_router, prefix="/api", tags=["cafes"])

@app.get("/")
def root():
    return {"Hello": "World!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
