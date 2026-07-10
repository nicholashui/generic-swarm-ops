def enqueue(name: str, payload: dict) -> dict:
    return {"task": name, "payload": payload}
