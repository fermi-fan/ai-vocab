from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


app = FastAPI()

entries = []



class EntryCreate(BaseModel):
    content: str
    context: str | None = None



@app.get("/")
def read_root():
    return {"message": "AI Vocabulary API is running!"}

@app.post("/entries/")
def create_entry(entry_in: EntryCreate):
    content = entry_in.content.strip()

    if not content:
        raise HTTPException(status_code=400, detail="Content cannot be empty.")

    new_entry = {
        "id": len(entries) + 1,
        "content": content,
        "entry_type": "word",
        "chinese_meaning": "这里是模拟AI生成的中文意思",
        "explanation": "当前还没有接入真实 AI，先用 mock 结果跑通接口。",
        "part_of_speech": "unknown",
        "familiarity_level": 0,
    }

    entries.append(new_entry)

    return new_entry

@app.get("/entries/")
def get_entries():
    return {
        "total": len(entries),
        "items": entries,
    }

@app.get("/entries/{entry_id}")
def get_entry(entry_id: int):
    for entry in entries:
        if entry["id"] == entry_id:
            return entry

    raise HTTPException(status_code=404, detail="Entry not found.")    

@app.delete("/entries/{entry_id}")
def delete_entry(entry_id :int):
    for index, entry in enumerate(entries):
        if entry.get("id") == entry_id:
            deleted_entry = entries.pop(index)

            return {
                "message": "Entry deleted successfully.",
                "deleted": deleted_entry,
                }