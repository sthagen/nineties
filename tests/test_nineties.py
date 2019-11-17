# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring,no-name-in-module
import os
from unittest import mock
import pytest  # type: ignore
import nineties.nineties as n

FOLDER_PATH = os.path.join("tests", "data")
ELEMENTS_IN_FOLDER_PATH = [
    "23450123T123456_empty.xz",
    "23450123T133456_foo.xz",
    "23450123T143456_baz.xz",
]
SHA256_OF_ELEMENTS_IN_FOLDER_PATH = [
    "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    "7d2ef141eadd8f200cdf13762ec3260e20509ef2cda11bce29f5701ff966bb4e",
    "7d2ef141eadd8f200cdf13762ec3260e20509ef2cda11bce29f5701ff966bb4e",
]
PAIRS_FROM_LIST = [
    (name, os.path.join(FOLDER_PATH, name)) for name in ELEMENTS_IN_FOLDER_PATH
]

HASH_MAP_FOLDER_PATH = {
    SHA256_OF_ELEMENTS_IN_FOLDER_PATH[0]: [(ELEMENTS_IN_FOLDER_PATH[0], 0)],
    SHA256_OF_ELEMENTS_IN_FOLDER_PATH[1]: [
        (ELEMENTS_IN_FOLDER_PATH[1], 104),
        (ELEMENTS_IN_FOLDER_PATH[2], 104),
    ],
}


def test_nineties_triage_ok():
    hash_map = {
        "a": [
            ("23450123T12345_foo", 1),
            ("23450123T13345_bar", 1),
            ("23450123T14345_baz", 1),
        ]
    }
    keep, remove = ["23450123T12345_foo", "23450123T14345_baz"], ["23450123T13345_bar"]
    assert n.triage_hashes(hash_map) == (keep, remove)


def test_nineties_triage_ok_size_zero():
    hash_map = {
        "a": [
            ("23450123T12345_foo", 0),
            ("23450123T13345_bar", 0),
            ("23450123T14345_baz", 0),
        ]
    }
    keep, remove = [], [name for name, _ in hash_map["a"]]
    assert n.triage_hashes(hash_map) == (keep, remove)


def test_nineties_triage_ok_pair():
    hash_map = {"a": [("23450123T12345_foo", 1), ("23450123T13345_bar", 1)]}
    keep, remove = [name for name, _ in hash_map["a"]], []
    assert n.triage_hashes(hash_map) == (keep, remove)


def test_nineties_triage_ok_single():
    hash_map = {"a": [("23450123T12345_foo", 1)]}
    keep, remove = [name for name, _ in hash_map["a"]], []
    assert n.triage_hashes(hash_map) == (keep, remove)


def test_nineties_triage_ok_empty():
    hash_map = {}
    keep, remove = [], []
    assert n.triage_hashes(hash_map) == (keep, remove)


def test_nineties_triage_nok_values_empty():
    hash_map = {"a": []}
    message = r"list index out of range"
    with pytest.raises(IndexError, match=message):
        n.triage_hashes(hash_map)


def test_nineties_triage_ok_four():
    hash_map = {
        "a": [
            ("23450123T12345_foo", 1),
            ("23450123T13345_bar", 1),
            ("23450123T14345_baz", 1),
            ("23450123T15345_ok", 1),
        ]
    }
    keep, remove = (
        ["23450123T12345_foo", "23450123T15345_ok"],
        ["23450123T13345_bar", "23450123T14345_baz"],
    )
    assert n.triage_hashes(hash_map) == (keep, remove)


@mock.patch("os.listdir")
def test_nineties_list_dir_ok_mock(ld_mock):
    a_folder_path = "faked-folder.really"
    names_mock = ["a", "b", "c"]
    ld_mock.return_value = names_mock
    names = n.list_dir(a_folder_path)
    ld_mock.assert_called_with(a_folder_path)
    assert ld_mock.return_value == names
    assert names == names_mock


@mock.patch("os.listdir")
def test_nineties_elements_of_gen_ok_mock(ld_mock):
    a_folder_path = "faked-folder.really"
    names_mock = ["b", "c", "a"]
    pairs = [(name, os.path.join(a_folder_path, name)) for name in sorted(names_mock)]
    ld_mock.return_value = names_mock
    names = [name for name in n.elements_of_gen(a_folder_path)]
    ld_mock.assert_called_with(a_folder_path)
    assert ld_mock.return_value == names_mock
    assert names == pairs


def test_nineties_list_dir_ok_real():
    assert n.list_dir(FOLDER_PATH) == ELEMENTS_IN_FOLDER_PATH


def test_nineties_elements_of_gen_ok_real():
    names = [name for name in n.elements_of_gen(FOLDER_PATH)]
    assert names == PAIRS_FROM_LIST


def test_nineties_read_folder_ok_real():
    assert n.read_folder(FOLDER_PATH) == HASH_MAP_FOLDER_PATH
