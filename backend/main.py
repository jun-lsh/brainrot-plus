from fastapi import FastAPI
import uvicorn

from services.llm_service import generate_script
from config import client, model_instance
app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/generate")
def generate(query: str):
    result = generate_script(query, model_instance, client)
    return result




if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)