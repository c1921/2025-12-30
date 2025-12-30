import argparse
import sys

from game.engine import tick_day


def run_server(state_path: str) -> int:
    while True:
        line = sys.stdin.readline()
        if not line:
            return 0
        line = line.strip()
        if not line:
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
