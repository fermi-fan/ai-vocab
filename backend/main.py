from fastapi import FastAPI, HTTPException, status

from ai_service import generate_entry_with_ai
from schemas import (
    EntryCreate,
    EntryDeleteResponse,
    EntryListResponse,
    EntryResponse,
    EntryUpdate,
)
from entry_store import (
    create_entry_record,
    delete_entry_record,
    get_entry_record,
    list_entry_records,
    update_entry_record,
)

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "AI Vocabulary Assistant API is running"}


@app.post("/entries", response_model=EntryResponse, status_code=status.HTTP_201_CREATED)
def create_entry(entry_in: EntryCreate):
    content = entry_in.content
    ai_result = generate_entry_with_ai(content, entry_in.context)
    new_entry = create_entry_record(content, ai_result)

    return new_entry


@app.get("/entries", response_model=EntryListResponse)
def get_entries():
    return list_entry_records()


@app.get("/entries/{entry_id}", response_model=EntryResponse)
def get_entry(entry_id: int):
    entry = get_entry_record(entry_id)

    if entry is None:
        raise HTTPException(status_code=404, detail="Entry not found")

    return entry

@app.patch(
    "/entries/{entry_id}",
    response_model=EntryResponse,
)
def update_entry(
    entry_id: int,
    entry_in: EntryUpdate,
):
    update_data = entry_in.model_dump(
        exclude_unset=True,
        exclude_none=True,
    )

    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No update fields provided",
        )

    updated_entry = update_entry_record(
        entry_id,
        update_data,
    )

    if updated_entry is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Entry not found",
        )

    return updated_entry




@app.delete("/entries/{entry_id}", response_model=EntryDeleteResponse)
def delete_entry(entry_id: int):
    deleted_entry = delete_entry_record(entry_id)

    if deleted_entry is None:
        raise HTTPException(status_code=404, detail="Entry not found")

    return {
        "message": "Entry deleted successfully",
        "deleted": deleted_entry,
    }