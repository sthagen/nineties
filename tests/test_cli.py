# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring
import pytest  # type: ignore
import nineties.cli as cli


def test_cli_main_ok():
    argv = ["ignored", '"a[c=d,date=2019-12-12T12:12:12.123+0200,final=f]"']
    assert cli.main(argv) is None


def test_cli_main_nok():
    argv = ["ignored", '"a[c=d,not_final=do_not_care]"']
    message = r"not enough values to unpack \(expected 2, got 1\)"
    with pytest.raises(ValueError, match=message):
        cli.main(argv)
