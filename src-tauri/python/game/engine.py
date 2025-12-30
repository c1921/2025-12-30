from game.state import default_state, load_state, save_state


MAX_DAY_LOGS = 30


def tick_day(state_path: str, multiplier: int) -> int:
    state = load_state(state_path)
    day = _get_int(state.get("day"), 1)
    if day < 1:
        day = 1
    multiplier = max(0, multiplier)
    for _ in range(multiplier):
        day += 1
        state["day"] = day
        _apply_daily_rules(state, day)
    save_state(state_path, state)
    return day


def get_state(state_path: str) -> dict:
    state = load_state(state_path)
    day = _get_int(state.get("day"), 1)
    if day < 1:
        day = 1
    food_stock = _get_int(state.get("food_stock"), 0)
    if food_stock < 0:
        food_stock = 0
    return {
        "day": day,
        "food_stock": food_stock,
        "npcs": state.get("npcs", []),
    }


def get_logs(state_path: str, limit: int) -> list:
    state = load_state(state_path)
    logs = state.get("day_logs")
    if not isinstance(logs, list):
        logs = []
    if isinstance(limit, bool) or not isinstance(limit, int) or limit < 1:
        return []
    if len(logs) <= limit:
        return logs
    return logs[-limit:]


def reset_state(state_path: str) -> dict:
    state = default_state()
    save_state(state_path, state)
    return state


def _apply_daily_rules(state: dict, day: int) -> None:
    food_stock = _get_int(state.get("food_stock"), 0)
    if food_stock < 0:
        food_stock = 0
    npcs = state.get("npcs")
    if not isinstance(npcs, list):
        npcs = []
    day_logs = state.get("day_logs")
    if not isinstance(day_logs, list):
        day_logs = []

    day_log = {
        "day": day,
        "food_stock_before": food_stock,
        "food_stock_after": food_stock,
        "npc_changes": [],
    }

    for npc in npcs:
        if not isinstance(npc, dict):
            continue
        alive = _get_bool(npc.get("alive"), True)
        npc["alive"] = alive
        if not alive:
            continue
        hunger_before = _get_int(npc.get("hunger"), 0)
        health_before = _get_int(npc.get("health"), 100)
        mood_before = _get_int(npc.get("mood"), 0)
        hunger = hunger_before
        health = health_before
        mood = mood_before

        hunger += 10
        if food_stock > 0:
            food_stock -= 1
            hunger -= 20
        hunger = _clamp(hunger, 0, 100)

        if hunger > 70:
            health -= 5
        if hunger < 30:
            health += 1
        health = _clamp(health, 0, 100)

        if hunger > 70:
            mood -= 3
        if health < 50:
            mood -= 2
        else:
            mood += 1
        mood = _clamp(mood, -50, 50)

        died = False
        if health <= 0:
            alive = False
            npc["alive"] = False
            died = True

        npc["hunger"] = hunger
        npc["health"] = health
        npc["mood"] = mood

        change = {
            "npc_id": _coerce_str(npc.get("id")),
            "hunger_before": hunger_before,
            "hunger_after": hunger,
            "health_before": health_before,
            "health_after": health,
            "mood_before": mood_before,
            "mood_after": mood,
        }
        if died:
            change["died"] = True
        day_log["npc_changes"].append(change)

    state["food_stock"] = food_stock
    state["npcs"] = npcs
    day_log["food_stock_after"] = food_stock
    day_logs.append(day_log)
    state["day_logs"] = _trim_logs(day_logs, MAX_DAY_LOGS)


def _trim_logs(day_logs: list, max_entries: int) -> list:
    if max_entries < 1:
        return []
    if len(day_logs) <= max_entries:
        return day_logs
    return day_logs[-max_entries:]


def _clamp(value: int, min_value: int, max_value: int) -> int:
    if value < min_value:
        return min_value
    if value > max_value:
        return max_value
    return value


def _get_int(value: object, default: int) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        return default
    return value


def _get_bool(value: object, default: bool) -> bool:
    if not isinstance(value, bool):
        return default
    return value


def _coerce_str(value: object) -> str | None:
    if value is None:
        return None
    return str(value)
