import json
import os


def load_state(path: str) -> dict:
    if not os.path.exists(path):
        return {"day": 0}
    try:
        with open(path, "r", encoding="utf-8") as handle:
            data = json.load(handle)
            if isinstance(data, dict) and isinstance(data.get("day"), int):
                return data
    except Exception:
        pass
    return {"day": 0}


def save_state(path: str, state: dict) -> None:
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(state, handle)
