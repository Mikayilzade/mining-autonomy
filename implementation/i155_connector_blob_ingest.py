"""I155 fail-closed GitHub connector blob ingest bridge.

Accepts connector-delivered UTF-8 content only when it matches an expected Git blob SHA.
This module performs no network access and does not execute I113. Its purpose is to
prevent manual transcription/reformatting from silently weakening I154 source binding.
"""
from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from hashlib import sha1
from pathlib import Path

SCHEMA = "mining-autonomy/i155-connector-blob-ingest/v1"


@dataclass(frozen=True)
class IngestReceipt:
    schema: str
    path: str
    expected_git_blob_sha: str
    actual_git_blob_sha: str
    accepted: bool
    bytes_written: int
    network_enabled: bool = False
    i113_executed: bool = False
    spend_or_value_movement: bool = False


def git_blob_sha(data: bytes) -> str:
    return sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


def valid_sha(value: str) -> bool:
    if len(value) != 40:
        return False
    try:
        int(value, 16)
    except ValueError:
        return False
    return True


def ingest(*, relative_path: str, expected_sha: str, content: str, root: Path) -> IngestReceipt:
    expected = expected_sha.lower()
    data = content.encode("utf-8")
    actual = git_blob_sha(data)
    accepted = bool(relative_path and valid_sha(expected) and actual == expected)
    written = 0
    if accepted:
        target = root / relative_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        written = len(data)
    return IngestReceipt(
        schema=SCHEMA,
        path=relative_path,
        expected_git_blob_sha=expected,
        actual_git_blob_sha=actual,
        accepted=accepted,
        bytes_written=written,
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", required=True)
    parser.add_argument("--expected-sha", required=True)
    parser.add_argument("--root", required=True)
    parser.add_argument("--content-file", required=True)
    args = parser.parse_args()
    content = Path(args.content_file).read_text(encoding="utf-8")
    receipt = ingest(relative_path=args.path, expected_sha=args.expected_sha, content=content, root=Path(args.root))
    print(json.dumps(asdict(receipt), indent=2, sort_keys=True))
    return 0 if receipt.accepted else 2


if __name__ == "__main__":
    raise SystemExit(main())
