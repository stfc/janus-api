"""Tests for data conversion helper functions."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import numpy as np

mock_data_dir = MagicMock()
with patch.dict("sys.modules", {"api.constants": MagicMock(DATA_DIR=mock_data_dir)}):
    from api.utils.singlepoint_helper import handle_data_types


def test_convert_ndarray_to_list_with_array():
    """Test convert_ndarray_to_list function with a np array."""
    array = np.array([1, 2, 3])
    result = handle_data_types(array)
    assert result == [1, 2, 3]


def test_convert_ndarray_to_list_with_nested_dict():
    """Test convert_ndarray_to_list function with a nested dict."""
    nested_dict = {"a": np.array([1, 2, 3]), "b": {"c": np.array([4, 5, 6])}}
    result = handle_data_types(nested_dict)
    expected = {"a": [1, 2, 3], "b": {"c": [4, 5, 6]}}
    assert result == expected


def test_convert_ndarray_to_list_with_list():
    """Test convert_ndarray_to_list function with list of np arrays."""
    list_of_arrays = [np.array([1, 2]), np.array([3, 4])]
    result = handle_data_types(list_of_arrays)
    assert result == [[1, 2], [3, 4]]


def test_convert_ndarray_to_list_with_non_numpy():
    """Test convert_ndarray_to_list function with a float value."""
    obj = -843.033131230741
    result = handle_data_types(obj)
    assert result == -843.033131230741
