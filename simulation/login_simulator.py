import argparse
import random
import time

import requests


DEFAULT_USERS = [
    "admin",
    "administrator",
    "root",
    "support",
    "backup",
    "service",
    "john",
    "alice",
]

DEFAULT_PASSWORDS = [
    "password123",
    "Welcome123",
    "admin123",
    "qwerty123",
    "letmein",
    "Summer2026",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate controlled login attempts against your own HoneyWatch instance."
    )
    parser.add_argument(
        "--target",
        default="http://127.0.0.1:8000/login",
        help="HoneyWatch login URL. Use only systems you own or are authorized to test.",
    )
    parser.add_argument("--count", type=int, default=12, help="Number of login attempts.")
    parser.add_argument("--delay", type=float, default=0.35, help="Delay between attempts in seconds.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if args.count < 1 or args.count > 500:
        raise SystemExit("--count must be between 1 and 500")
    if args.delay < 0:
        raise SystemExit("--delay cannot be negative")

    print(f"Target: {args.target}")
    print(f"Attempts: {args.count}")

    for index in range(1, args.count + 1):
        username = random.choice(DEFAULT_USERS)
        password = random.choice(DEFAULT_PASSWORDS)
        try:
            response = requests.post(
                args.target,
                data={"username": username, "password": password},
                timeout=5,
                allow_redirects=False,
                headers={"User-Agent": "HoneyWatch-Controlled-Simulator/1.0"},
            )
            print(
                f"{index:03d} username={username!r} status={response.status_code}"
            )
        except requests.RequestException as exc:
            print(f"{index:03d} request failed: {exc}")

        time.sleep(args.delay)


if __name__ == "__main__":
    main()
