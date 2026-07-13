#!/usr/bin/env python3
def main():
    from pathlib import Path
    from tzlocal import get_localzone_name

    env_file = Path(".env")
    tz = get_localzone_name()  # e.g. America/Denver

    lines = env_file.read_text().splitlines() if env_file.exists() else []
    lines = [line for line in lines if not line.startswith("TZ=")]
    lines.append(f"TZ={tz}")

    env_file.write_text("\n".join(lines) + "\n")
    print(f"TZ={tz}")

if __name__ == "__main__":
    main()
