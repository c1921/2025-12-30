from dataclasses import dataclass
import uuid


@dataclass
class Character:
    id: uuid.UUID
    name: str
    job: str
    hunger: int
    health: int
    mood: int
    alive: bool

    def __post_init__(self) -> None:
        if not isinstance(self.id, uuid.UUID):
            raise TypeError("id must be uuid.UUID")
        if not isinstance(self.name, str):
            raise TypeError("name must be str")
        if not isinstance(self.job, str):
            raise TypeError("job must be str")
        _require_int("hunger", self.hunger)
        _require_int("health", self.health)
        _require_int("mood", self.mood)
        if not isinstance(self.alive, bool):
            raise TypeError("alive must be bool")
        _require_range("hunger", self.hunger, 0, 100)
        _require_range("health", self.health, 0, 100)
        _require_range("mood", self.mood, -50, 50)


def _require_int(name: str, value: int) -> None:
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{name} must be int")


def _require_range(name: str, value: int, min_value: int, max_value: int) -> None:
    if value < min_value or value > max_value:
        raise ValueError(f"{name} must be between {min_value} and {max_value}")
