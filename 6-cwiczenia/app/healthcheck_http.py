import sys
import urllib.request


def main() -> int:
    try:
        with urllib.request.urlopen("http://127.0.0.1:5000/health", timeout=2) as response:
            if response.status == 200:
                return 0
    except Exception:
        return 1
    return 1


if __name__ == "__main__":
    sys.exit(main())
