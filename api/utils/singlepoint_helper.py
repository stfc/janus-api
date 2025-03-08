"""Helper functions for performing singeploint calculations."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from janus_core.calculations.single_point import SinglePoint
from janus_core.helpers.janus_types import Architectures, Properties
import numpy as np

from api.schemas.singlepoint_schemas import SinglePointResults

DATA_DIR = Path("/home/cameron/janus-web/data")


def convert_ndarray_to_list(
    data: dict[str, Any] | list | np.ndarray | float,
) -> dict[str, Any]:
    """
    Recursive function to convert numpy arrays into a useable format for fastAPI.

    Parameters
    ----------
    data : dict[str, Any] | list | np.ndarray | float
        The object to be checked and potentially converted.

    Returns
    -------
    dict[str, Any]
        Dictionary of properties calculated.
    """
    if isinstance(data, np.ndarray):
        return data.tolist()
    if isinstance(data, dict):
        return {k: convert_ndarray_to_list(v) for k, v in data.items()}
    if isinstance(data, list):
        return [convert_ndarray_to_list(i) for i in data]
    return data


def singlepoint(
    struct: Path,
    arch: Architectures = "mace_mp",
    properties: list[Properties] = ("energy", "forces", "stress"),
    range_selector: str = ":",
    write_results: bool = True,
    results_path: Path = DATA_DIR / "results/",
    format: str = "extxyz",
) -> SinglePointResults:
    """
    Perform single point calculations and return results.

    Parameters
    ----------
    struct : Path
        Path of structure to simulate.
    arch : Architectures
        MLIP architecture to use for single point calculations. Default is "mace_mp".
    properties : List[Properties]
        Physical properties to calculate. Default is ("energy", "forces", "stress").
    range_selector : str
        Range of indices to include from the structure. Default is all.
    write_results : bool
        Tells function if to save the results of the calculation or not,
        default is True.
    results_path : Path
        Location to save the results, default is Path = DATA_DIR / "results/".
    format : str
        File format to output results as, default is "extxyz".

    Returns
    -------
    dict[str, Any]
        Results of the single point calculations.
    """
    read_kwargs = {"index": range_selector}
    results_path = results_path / f"{struct.stem}-results.{format}"
    write_kwargs = {"filename": results_path, "format": format}

    singlepoint_kwargs = {
        "struct_path": struct,
        "properties": properties,
        "arch": arch,
        "device": "cpu",
        "read_kwargs": read_kwargs,
        "write_results": write_results,
        "write_kwargs": write_kwargs,
    }

    s_point = SinglePoint(**singlepoint_kwargs)

    s_point.run()
    results = convert_ndarray_to_list(s_point.results)
    results["results_path"] = results_path

    for result in results:
        print(type(results[result]), result, results[result])

    return results
