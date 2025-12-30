import json
import os
import uuid


def load_state(path: str) -> dict:
    if not os.path.exists(path):
        return _default_state()
    try:
        with open(path, "r", encoding="utf-8") as handle:
            data = json.load(handle)
            if isinstance(data, dict):
                return _normalize_state(data)
    except Exception:
        pass
    return _default_state()


def save_state(path: str, state: dict) -> None:
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(state, handle)


def default_state() -> dict:
    return _default_state()


def _default_state() -> dict:
    return {
        "day": 1,
        "food_stock": 50,
        "npcs": _default_npcs(),
        "day_logs": [],
    }


def _normalize_state(state: dict) -> dict:
    day = _coerce_int(state.get("day"), 1)
    if day < 1:
        day = 1
    food_stock = _coerce_int(state.get("food_stock"), 50)
    if food_stock < 0:
        food_stock = 0
    npcs = state.get("npcs")
    if not isinstance(npcs, list):
        npcs = _default_npcs()
    if len(npcs) == 0:
        npcs = _default_npcs()
    day_logs = state.get("day_logs")
    if not isinstance(day_logs, list):
        day_logs = []
    state["day"] = day
    state["food_stock"] = food_stock
    state["npcs"] = npcs
    state["day_logs"] = day_logs
    return state


def _coerce_int(value: object, default: int) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        return default
    return value


def _default_npcs() -> list:
    npcs = []
    for index in range(1, 25):
        npcs.append(
            {
                "id": str(uuid.uuid4()),
                "name": f"Name{index:02d}",
                "job": "Unknown",
                "hunger": 30,
                "health": 90,
                "mood": 0,
                "alive": True,
            }
        )
    return npcs
