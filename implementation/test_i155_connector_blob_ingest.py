from pathlib import Path
from i155_connector_blob_ingest import git_blob_sha, ingest


def test_exact_connector_bytes_are_written(tmp_path: Path):
    content = "hello\n"
    sha = git_blob_sha(content.encode())
    receipt = ingest(relative_path="implementation/x.py", expected_sha=sha, content=content, root=tmp_path)
    assert receipt.accepted is True
    assert (tmp_path / "implementation/x.py").read_text() == content
    assert receipt.network_enabled is False
    assert receipt.i113_executed is False


def test_reformatted_content_fails_closed_and_writes_nothing(tmp_path: Path):
    original = "a = 1\n\nprint(a)\n"
    sha = git_blob_sha(original.encode())
    changed = "a=1\nprint(a)\n"
    receipt = ingest(relative_path="implementation/x.py", expected_sha=sha, content=changed, root=tmp_path)
    assert receipt.accepted is False
    assert not (tmp_path / "implementation/x.py").exists()
    assert receipt.bytes_written == 0


def test_invalid_expected_sha_fails_closed(tmp_path: Path):
    receipt = ingest(relative_path="implementation/x.py", expected_sha="bad", content="x", root=tmp_path)
    assert receipt.accepted is False
