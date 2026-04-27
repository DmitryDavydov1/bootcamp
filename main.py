from fastapi import FastAPI
import uvicorn
from app.api import recommendations, data_upload
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Recommendation System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(data_upload.router)
app.include_router(recommendations.router)
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
