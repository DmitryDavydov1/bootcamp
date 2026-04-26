from fastapi import FastAPI
import uvicorn
from app.api import recommendations, data_upload

app = FastAPI(title="Recommendation System")

app.include_router(data_upload.router)
app.include_router(recommendations.router)
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
