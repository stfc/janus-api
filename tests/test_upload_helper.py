"""Tests for upload helper functions."""

from __future__ import annotations

import hashlib
from pathlib import Path
from unittest.mock import MagicMock, patch

mock_data_dir = MagicMock()

with patch.dict(
    "sys.modules", {"janus_api.constants": MagicMock(DATA_DIR=mock_data_dir)}
):
    from janus_api.utils.upload_helper import (
        calculate_md5_checksum,
        get_all_filenames,
        save_file,
    )


def test_get_all_filenames(tmp_path):
    """Test if getter returns all of the filenames correctly."""
    filenames = ["file1.txt", "file2.txt"]
    for filename in filenames:
        (tmp_path / filename).write_text("Test content")

    result = get_all_filenames(tmp_path)

    assert sorted(result) == sorted(filenames)


def test_save_file(tmp_path):
    """Test if save file function saves a given file in the correct directory."""
    file_content = b"Test file content"
    filename = "testfile.txt"

    file_path = save_file(file_content, filename, tmp_path)

    assert Path(file_path).exists()
    assert Path(file_path).read_bytes() == file_content


def test_calculate_md5_checksum(tmp_path):
    """Test for checksum check when the hash should match."""
    file_chunk = b"Test data for checksum"
    received_hash = hashlib.md5(file_chunk).hexdigest()
    result = calculate_md5_checksum(file_chunk, received_hash)

    assert result


def test_calculate_md5_checksum_mismatch(tmp_path):
    """Test for checksum check when the hash is incorrect."""
    file_chunk = b"Test data for checksum"
    received_hash = "incorrecthash"
    result = calculate_md5_checksum(file_chunk, received_hash)

    assert not result
