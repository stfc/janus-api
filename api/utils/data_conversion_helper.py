"""Helper functions for performing data conversion."""

from __future__ import annotations

from typing import Any

from ase.spacegroup import Spacegroup
import numpy as np


def handle_data_types(
    data: dict[str, Any] | list | np.ndarray | float | Spacegroup,
) -> dict[str, Any] | list | float:
    """
    Recursive function to convert data types into a usable format for fastAPI.

    Parameters
    ----------
    data : dict[str, Any] | list | np.ndarray | float | Spacegroup
        The object to be checked and potentially converted.

    Returns
    -------
    dict[str, Any] | list | float
        Converted data.
    """
    if isinstance(data, np.ndarray):
        return data.tolist()
    if isinstance(data, Spacegroup):
        return {
            "international": data.symbol,
            "number": data.no,
            "hall": data.hall_symbol,
            "setting": data.setting,
            "symmetry_operations": [str(op) for op in data],
        }
    if isinstance(data, dict):
        return {k: handle_data_types(v) for k, v in data.items()}
    if isinstance(data, list):
        return [handle_data_types(i) for i in data]
    return data
