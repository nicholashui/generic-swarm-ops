from hashlib import sha256
import json


def request_fingerprint(payload: dict) -> str:
    return sha256(json.dumps(payload, sort_keys=True).encode("utf-8")).hexdigest()
