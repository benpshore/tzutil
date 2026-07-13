#!/usr/bin/env python3
import re
import subprocess
from pathlib import Path


def get_system_timezone() -> str:
	"""Detect the host's configured IANA timezone.

	Tries sources in order:
	1. /etc/timezone (simple text file)
	2. /etc/localtime symlink target
	3. timedatectl show -p Timezone
	4. tzlocal.get_localzone_name() (fallback)

	Returns:
		Valid IANA timezone name (e.g., "America/Denver")

	Raises:
		OSError: If no timezone can be detected from any source
	"""
	tz = None

	# Try /etc/timezone
	try:
		tz_file = Path("/etc/timezone")
		if tz_file.exists():
			tz = tz_file.read_text().strip()
			if tz and _is_valid_iana_tz(tz):
				return tz
	except Exception:
		pass

	# Try /etc/localtime symlink
	try:
		localtime = Path("/etc/localtime")
		if localtime.is_symlink():
			target = localtime.resolve()
			# Extract timezone from path like /usr/share/zoneinfo/America/Denver
			match = re.search(r"/zoneinfo/(.+)$", str(target))
			if match:
				tz = match.group(1)
				if _is_valid_iana_tz(tz):
					return tz
		elif localtime.exists():
			# /etc/localtime is a file, try to infer from it (less reliable)
			pass
	except Exception:
		pass

	# Try timedatectl
	try:
		result = subprocess.run(
			["timedatectl", "show", "-p", "Timezone", "--value"],
			capture_output=True,
			text=True,
			timeout=5,
		)
		if result.returncode == 0:
			tz = result.stdout.strip()
			if tz and _is_valid_iana_tz(tz):
				return tz
	except (FileNotFoundError, subprocess.TimeoutExpired, Exception):
		pass

	# Try tzlocal as fallback
	try:
		from tzlocal import get_localzone_name

		tz = get_localzone_name()
		if tz and _is_valid_iana_tz(tz):
			return tz
	except Exception:
		pass

	raise OSError("Could not determine system timezone from any source")


def _is_valid_iana_tz(tz: str) -> bool:
	"""Validate that a string matches IANA timezone format.

	IANA timezones are typically Continent/City or have multiple parts.
	Examples: America/Denver, Europe/London, UTC, Etc/UTC, Etc/GMT+5
	"""
	if not tz:
		return False
	# Allow single component (UTC, GMT) or slash-separated (Continent/City or deeper)
	if "/" in tz:
		parts = tz.split("/")
		return all(part and part.replace("_", "").replace("-", "").replace("+", "").isalnum() for part in parts)
	# Single component timezone (UTC, GMT, etc.)
	return tz.replace("_", "").replace("-", "").replace("+", "").isalnum()


def main() -> None:
	"""Print the detected system timezone to stdout."""
	try:
		tz = get_system_timezone()
		print(tz)
	except OSError as e:
		raise SystemExit(f"ERROR: {e}") from e


if __name__ == "__main__":
	main()
