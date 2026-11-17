import re
import urllib.request
from pathlib import Path

SOURCE_URL = (
    "https://adguardteam.github.io/"
    "HostlistsRegistry/assets/filter_1.txt"
)

OUTPUT_FILE = Path("domains.txt")


def main():
    print("Downloading AdGuard DNS Filter...")

    request = urllib.request.Request(
        SOURCE_URL,
        headers={"User-Agent": "PKN-AdGuard-Converter/1.0"}
    )

    with urllib.request.urlopen(request, timeout=120) as response:
        content = response.read().decode("utf-8", errors="replace")

    domains = set()

    for line in content.splitlines():
        line = line.strip()

        if not line or line.startswith(("!", "#", "@@")):
            continue

        match = re.fullmatch(
            r"\|\|([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})\^",
            line
        )

        if match:
            domain = match.group(1).lower().rstrip(".")
            labels = domain.split(".")

            if all(
                label
                and len(label) <= 63
                and re.fullmatch(
                    r"[a-z0-9](?:[a-z0-9-]*[a-z0-9])?",
                    label
                )
                for label in labels
            ):
                domains.add(domain)

    result = sorted(domains)

    OUTPUT_FILE.write_text(
        "\n".join(result) + "\n",
        encoding="utf-8"
    )

    print("================================")
    print("PKN ADGUARD CONVERTER")
    print("================================")
    print(f"Total unique domains: {len(result):,}")
    print(f"Output: {OUTPUT_FILE}")
    print("Conversion completed.")


if __name__ == "__main__":
    main()
