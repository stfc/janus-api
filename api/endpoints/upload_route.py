"""Contains routes for uploading files and accessing uploaded files."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from fastapi.responses import JSONResponse

from api.utils.upload_helper import (
    calculate_md5_checksum,
    get_all_filenames,
    read_file,
    save_file,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/upload", tags=["upload"])


@router.post("/single")
async def upload_single(
    file: Annotated[UploadFile, File()],
    file_hash: Annotated[str, Form()],
) -> None:
    """
    Upload a single file.

    Parameters
    ----------
    file : UploadFile
        The file to be uploaded.
    file_hash : str
        The MD5 hash of the file.

    Raises
    ------
    HTTPException
        If there is an error during the upload process.
    """
    try:
        file_content = await file.read()
        logger.info("Hash matches: %s", calculate_md5_checksum(file_content, file_hash))
        save_file(file_content, file.filename)
    except Exception as e:
        logger.error(f"Error during file upload: {e}")
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.get("/files")
async def get_files() -> list[str]:
    """
    Get a list of all uploaded files.

    Returns
    -------
    list[str]
        A list of filenames of all uploaded files.
    """
    return get_all_filenames()


@router.get("/file/{target_file}")
async def return_file_contents(target_file: str) -> str:
    """
    Get the contents of the specified file.

    Parameters
    ----------
    target_file : str
        The file to be read.

    Returns
    -------
    JSONResponse
        A JSON response containing the file contents, filename, and file format.

    Raises
    ------
    HTTPException
        If the file is not found or cannot be read.
    """
    try:
        file_content = read_file(target_file)
        file_format = Path(target_file).suffix.lstrip(".")
        return JSONResponse(
            content={
                "fileName": target_file,
                "fileFormat": file_format,
                "content": file_content,
            }
        )
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail="File not found") from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
