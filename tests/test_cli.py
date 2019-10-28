# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring,unused-import,reimported
import datetime as dti
import sys
from unittest import mock
import pytest  # type: ignore
import nineties.cli as cli
import nineties.parser as p90
import nineties.privacy as priv

JSON_TEXT = """{
    "dsl": "a[c=d,id=2019,final=f]",
    "remove": "entry",
    "name": "j.",
    "timestamp": "3210-09-08T05:06:05.432+02:00"
}"""

PARSED_TEXT = {
    "dsl": {"c": "d", "id": 2019, "final": "f"},
    "name": "Allison Hill",
    "timestamp": dti.datetime(3210, 9, 8, 3, 6, 5, 432000),
}

PARSED_TEXT_NO_NAME = {
    "dsl": {"c": "d", "id": 2019, "final": "f"},
    "timestamp": dti.datetime(3210, 9, 8, 3, 6, 5, 432000),
}


def test_python_version_guard():
    with mock.patch.object(sys, "version_info") as v_info:
        v_info.major = 3
        v_info.minor = 5
        del sys.modules["nineties.cli"]
        with pytest.raises(RuntimeError, match=r".*higher.*"):
            import nineties.cli


def test_import_guards():
    with mock.patch.dict(sys.modules, {"faker": None}):
        with pytest.raises(ImportError, match=r".*faker.*"):
            import nineties.cli


def test_cli_main_ok():
    argv = ["ignored", '{"dsl": "a[c=d,date=2019-12-12T12:12:12.123+0200,final=f]"}']
    assert cli.main(argv) is None


def test_cli_main_ok_id():
    argv = ["ignored", '{"dsl": "a[c=d,id=2019,final=f]"}']
    assert cli.main(argv) is None


def test_cli_main_ok_timestamp():
    argv = ["ignored", '{"timestamp": "2019-12-12T12:12:12.121+0200"}']
    assert cli.main(argv) is None


def test_cli_main_nok():
    argv = ["ignored", '"a[c=d,not_final=do_not_care]"']
    message = r"'str' object has no attribute 'items'"
    with pytest.raises(AttributeError, match=message):
        cli.main(argv)


def test_cli_parse_ok():
    parser_map = {"dsl": p90.parse_dsl_entry, "timestamp": p90.parse_timestamp}
    assert cli.parse(JSON_TEXT, parser_map) == PARSED_TEXT_NO_NAME


def test_cli_parse_ok_safe():
    parser_map = {
        "dsl": p90.parse_dsl_entry,
        "name": priv.safe_name,
        "timestamp": p90.parse_timestamp,
    }
    assert cli.parse(JSON_TEXT, parser_map) == PARSED_TEXT


@mock.patch("os.path.isfile")
def test_repo_init_virtual(if_mock):
    a_file = "faked-file.really"
    if_mock.return_value = True
    mock_open = mock.mock_open(read_data=JSON_TEXT)

    argv = ["ignored", a_file]
    with mock.patch("builtins.open", mock_open):
        outcome = None
        try:
            cli.main(argv)
        except IOError as err:  # pragma: no cover
            outcome = err

    if_mock.assert_called_with(a_file)
    assert if_mock.return_value is True
    assert outcome is None
