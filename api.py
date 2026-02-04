import json
import os
import uuid
from typing import List

from fastapi import (
    APIRouter,
    Depends,
    FastAPI,
    HTTPException,
    WebSocket,
    WebSocketDisconnect,
)
from pydantic import BaseModel

app = FastAPI(
    title="AA-MR",
    description="AA-MR Tool",
    version="2.0.0",
)

from fastapi.middleware.cors import CORSMiddleware

from src.agents import main_agent

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust origins as needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load data from JSON file
DATA_FILE = "db.json"


def load_db():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)


def save_db(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)


# Initialize db from file
db = load_db()

knowledge_router = APIRouter()


class Knowledge(BaseModel):
    id: str | None = None
    title: str
    content: str
    category: str


def get_db():
    return db


@knowledge_router.get("/knowledge/", response_model=List[Knowledge])
async def read_knowledge(db=Depends(get_db)):
    """Retrieve all knowledge entries."""
    db = load_db()
    return db


@knowledge_router.post("/knowledge/", response_model=Knowledge)
async def create_knowledge(knowledge: Knowledge, db=Depends(load_db)):
    """Create a new knowledge entry."""
    knowledge.id = str(uuid.uuid4())
    if any(i["id"] == knowledge.id for i in db):
        raise HTTPException(status_code=400, detail="Knowledge ID already exists")
    db.append(knowledge.model_dump())
    save_db(db)
    return knowledge


@knowledge_router.get("/knowledge/{knowledge_id}", response_model=Knowledge)
async def read_knowledge_item(knowledge_id: str, db=Depends(get_db)):
    """Retrieve a knowledge entry by its ID."""
    item = next((i for i in db if i["id"] == knowledge_id), None)
    if not item:
        raise HTTPException(status_code=404, detail="Knowledge not found")
    return Knowledge(**item)


@knowledge_router.put("/knowledge/{knowledge_id}", response_model=Knowledge)
async def update_knowledge(knowledge_id: str, knowledge: Knowledge, db=Depends(get_db)):
    """Update an existing knowledge entry."""
    for i in db:
        if i["id"] == knowledge_id:
            i["title"] = knowledge.title
            i["content"] = knowledge.content
            i["category"] = knowledge.category
            save_db(db)
            return knowledge
    raise HTTPException(status_code=404, detail="Knowledge not found")


@knowledge_router.delete("/knowledge/{knowledge_id}")
async def delete_knowledge(knowledge_id: str, db=Depends(get_db)):
    """Delete an existing knowledge entry."""
    new_db = [i for i in db if i["id"] != knowledge_id]
    save_db(new_db)

    return {"message": "Knowledge deleted"}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            response = await main_agent.arun(data, stream=False, debug_mode=False)

            await websocket.send_text(response.content)
    except WebSocketDisconnect:
        print("Client disconnected")


app.include_router(knowledge_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8081)
