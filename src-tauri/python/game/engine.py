from game.state import load_state, save_state


def tick_day(state_path: str, multiplier: int) -> int:
    state = load_state(state_path)
    day = max(0, state.get("day", 0))
    day += max(0, multiplier)
    state["day"] = day
    save_state(state_path, state)
    return day
