import argparse
import json
import sys

from game.engine import get_logs, get_state, reset_state, tick_day


def run_server(state_path: str) -> int:
    while True:
        line = sys.stdin.readline()
        if not line:
            return 0
        line = line.strip()
        if not line:
            continue
        if line.startswith("{"):
            try:
                request = json.loads(line)
            except json.JSONDecodeError as err:
                print(json.dumps({"ok": False, "error": f"invalid json: {err}"}))
                sys.stdout.flush()
                continue
            try:
                response = handle_request(state_path, request)
            except Exception as err:
                response = {"ok": False, "error": str(err)}
            print(json.dumps(response))
            sys.stdout.flush()
            continue
        try:
            multiplier = int(line)
        except ValueError:
            print("0")
            sys.stdout.flush()
            continue
        day = tick_day(state_path, multiplier)
        print(day)
        sys.stdout.flush()


def handle_request(state_path: str, request: dict) -> dict:
    cmd = request.get("cmd")
    if cmd == "state":
        state = get_state(state_path)
        return {"ok": True, "state": state}
    if cmd == "tick":
        multiplier = request.get("multiplier", 1)
        if isinstance(multiplier, bool) or not isinstance(multiplier, int):
            multiplier = 1
        day = tick_day(state_path, multiplier)
        state = get_state(state_path)
        return {"ok": True, "day": day, "food_stock": state.get("food_stock", 0), "state": state}
    if cmd == "logs":
        limit = request.get("limit", 20)
        if isinstance(limit, bool) or not isinstance(limit, int):
            limit = 20
        logs = get_logs(state_path, limit)
        return {"ok": True, "logs": logs}
    if cmd == "reset":
        state = reset_state(state_path)
        return {"ok": True, "state": state}
    return {"ok": False, "error": f"unknown command: {cmd}"}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--state", required=True)
    parser.add_argument("--multiplier", type=int)
    parser.add_argument("--server", action="store_true")
    args = parser.parse_args()

    if args.server:
        return run_server(args.state)

    if args.multiplier is None:
        print("missing --multiplier", file=sys.stderr)
        return 2

    day = tick_day(args.state, args.multiplier)
    print(day)
    return 0


if __name__ == "__main__":
    sys.exit(main())
