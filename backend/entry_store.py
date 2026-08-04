entries = []
next_entry_id = 1


def create_entry_record(content: str, ai_result: dict) -> dict:
    global next_entry_id

    new_entry = {
        "id": next_entry_id,
        "content": content,
        "entry_type": ai_result["entry_type"],
        "chinese_meaning": ai_result["chinese_meaning"],
        "explanation": ai_result["explanation"],
        "part_of_speech": ai_result["part_of_speech"],
        "familiarity_level": 0,
    }

    entries.append(new_entry)
    next_entry_id += 1

    return new_entry


def list_entry_records() -> dict:
    return {
        "total": len(entries),
        "items": entries,
    }


def get_entry_record(entry_id: int) -> dict | None:
    for entry in entries:
        if entry.get("id") == entry_id:
            return entry

    return None


def delete_entry_record(entry_id: int) -> dict | None:
    for index, entry in enumerate(entries):
        if entry.get("id") == entry_id:
            return entries.pop(index)

    return None

def update_entry_record(
    entry_id: int,
    update_data: dict,
) -> dict | None:
    entry = get_entry_record(entry_id)

    if entry is None:
        return None

    entry.update(update_data)

    return entry


def reset_entry_store() -> None:
    global next_entry_id

    entries.clear()
    next_entry_id = 1