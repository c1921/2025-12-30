from dataclasses import dataclass, field
from typing import Optional

from .character import Character


class NPC(Character):
    pass


@dataclass
class DayLog:
    day: int
    food_stock_before: int
    food_stock_after: int
    npc_changes: list[dict]
    summary: Optional[str] = None

    def __post_init__(self) -> None:
        _require_int("day", self.day)
        if self.day < 1:
            raise ValueError("day must be >= 1")
        _require_int("food_stock_before", self.food_stock_before)
        _require_int("food_stock_after", self.food_stock_after)
        if not isinstance(self.npc_changes, list):
            raise TypeError("npc_changes must be list")
        if self.summary is not None and not isinstance(self.summary, str):
            raise TypeError("summary must be str or None")


@dataclass
class WorldState:
    day: int = 1
    food_stock: int = 0
    npcs: list[NPC] = field(default_factory=list)
    day_logs: list[DayLog] = field(default_factory=list)

    def __post_init__(self) -> None:
        _require_int("day", self.day)
        if self.day < 1:
            raise ValueError("day must be >= 1")
        _require_int("food_stock", self.food_stock)
        if self.food_stock < 0:
            raise ValueError("food_stock must be >= 0")
        if not isinstance(self.npcs, list):
            raise TypeError("npcs must be list")
        if not isinstance(self.day_logs, list):
            raise TypeError("day_logs must be list")

    def advance_day(self, days: int = 1) -> int:
        _require_int("days", days)
        if days < 0:
            raise ValueError("days must be >= 0")
        self.day += days
        return self.day

    def record_day_log(self, log: DayLog, max_entries: int) -> None:
        if not isinstance(log, DayLog):
            raise TypeError("log must be DayLog")
        _require_int("max_entries", max_entries)
        if max_entries < 1:
            raise ValueError("max_entries must be >= 1")
        self.day_logs.append(log)
        if len(self.day_logs) > max_entries:
            self.day_logs = self.day_logs[-max_entries:]


def _require_int(name: str, value: int) -> None:
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{name} must be int")
