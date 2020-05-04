# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring
import datetime as dti
import pytest  # type: ignore
import nineties.parser as p


VALID_FUTURE_ISO = "3210-09-08T07:06:05.432"
VALID_FUTURE_ISO_CEST = VALID_FUTURE_ISO + "+0200"
VALID_FUTURE_ISO_CEST_COLON = VALID_FUTURE_ISO + "+02:00"
VALID_FUTURE_DT_UTC_FROM_CEST = dti.datetime.strptime(
    "3210-09-08T05:06:05.432", p.ISO_FMT
)
VALID_FUTURE_DT_UTC_FROM_UTC = dti.datetime.strptime(VALID_FUTURE_ISO, p.ISO_FMT)


def test_parse_timestamp_ok():
    assert p.parse_timestamp(None) is None


def test_parse_timestamp_ok_null():
    assert p.parse_timestamp(p.JR_NULL) is None


def test_parse_timestamp_ok_future_iso_cest():
    then = VALID_FUTURE_DT_UTC_FROM_CEST
    assert p.parse_timestamp(VALID_FUTURE_ISO_CEST) == then
    assert p.parse_timestamp(VALID_FUTURE_ISO_CEST_COLON) == then


def test_parse_timestamp_ok_future_iso_implicit_utc():
    then = VALID_FUTURE_DT_UTC_FROM_UTC
    assert p.parse_timestamp(VALID_FUTURE_ISO) == then
    assert p.parse_timestamp(VALID_FUTURE_ISO + "+00:00") == then


def test_parse_timestamp_ok_future_iso_utc():
    then = VALID_FUTURE_DT_UTC_FROM_UTC
    assert p.parse_timestamp(VALID_FUTURE_ISO + "+0000") == then
    assert p.parse_timestamp(VALID_FUTURE_ISO + "+00:00") == then
    assert p.parse_timestamp(VALID_FUTURE_ISO + "-0000") == then
    assert p.parse_timestamp(VALID_FUTURE_ISO + "-00:00") == then


def test_parse_timestamp_nok_outer_length():
    with pytest.raises(ValueError):
        p.parse_timestamp("" * 23)


def test_parse_timestamp_nok_offset_length():
    with pytest.raises(AssertionError):
        p.parse_timestamp(VALID_FUTURE_ISO + "+12:34X")
    with pytest.raises(AssertionError):
        p.parse_timestamp(VALID_FUTURE_ISO + "+1234X")


def test_parse_timestamp_nok_offset_sign():
    with pytest.raises(AssertionError):
        p.parse_timestamp(VALID_FUTURE_ISO + "*1234")


def test_parse_timestamp_nok_offset_hours_value():
    with pytest.raises(ValueError):
        p.parse_timestamp(VALID_FUTURE_ISO + "+XX34")


def test_parse_timestamp_nok_offset_minutes_value():
    with pytest.raises(ValueError):
        p.parse_timestamp(VALID_FUTURE_ISO + "+12XX")


def test_parse_dsl_entry_nok_no_content():
    assert p.parse_dsl_entry(None) == {}
    assert p.parse_dsl_entry("") == {}


def test_parse_dsl_entry_nok_start_data_wrong():
    text_entry = '"tag@42(a=b,e=' + "do_not_care" + ']"'
    with pytest.raises(ValueError):
        p.parse_dsl_entry(text_entry, final_key="e")


def test_parse_dsl_entry_nok_only_kv_seps():
    text_entry = (
        '"tag@42[=,=,=,=,==,===,=,' + p.FINAL_DSL_KEY + "=" + "do_not_care" + ']"'
    )
    assert p.parse_dsl_entry(text_entry) == {"final": "do_not_care"}


def test_parse_dsl_entry_nok_start_data_multiple():
    text_entry = '"tag@42[[a=b,' + p.FINAL_DSL_KEY + "=" + "do_not_care" + ']"'
    assert p.parse_dsl_entry(text_entry) == {"[a": "b", "final": "do_not_care"}


def test_parse_dsl_entry_nok_missing_kv_sep_and_value():
    text_entry = '"tag@42(a=b,c,e=' + "do_not_care" + ']"'
    with pytest.raises(ValueError):
        p.parse_dsl_entry(text_entry, final_key="e")


def test_parse_dsl_entry_nok_rococo_wrong():
    text_entry = "'tag@42[a=b,e=" + "no_strip" + "]'"
    assert p.parse_dsl_entry(text_entry, final_key="e") == {"a": "b", "e": "no_strip]'"}


def test_parse_dsl_entry_ok_final_value_contains_key():
    text_entry = '"tag@42[a=b,e=e=e,e=e,date=2]"'
    assert p.parse_dsl_entry(text_entry, final_key="e") == {
        "a": "b",
        "e": "e=e,e=e,date=2",
    }


def test_parse_dsl_entry_nok_final_key_wrong_implicit():
    text_entry = '"tag@42[a=b,wrong=' + "do_not_care" + ']"'
    with pytest.raises(ValueError):
        p.parse_dsl_entry(text_entry)


def test_parse_dsl_entry_nok_final_key_wrong_explicit():
    text_entry = '"tag@42[a=b,right=' + "do_not_care" + ']"'
    with pytest.raises(ValueError):
        p.parse_dsl_entry(text_entry, final_key="wrong")


def test_parse_dsl_entry_ok():
    text_entry = '"tag@42[a=b,' + p.FINAL_DSL_KEY + "=" + p.JR_NULL + ']"'
    assert p.parse_dsl_entry(text_entry) == {"a": "b", p.FINAL_DSL_KEY: p.NA}


def test_parse_dsl_entry_ok_final_data():
    text_entry = '"tag@42[a=b,' + p.FINAL_DSL_KEY + "=" + ",,,,,===" + ']"'
    assert p.parse_dsl_entry(text_entry) == {"a": "b", p.FINAL_DSL_KEY: ",,,,,==="}


def test_parse_dsl_entry_ok_date():
    text_entry = (
        '"tag@42[daTE='
        + VALID_FUTURE_ISO_CEST_COLON
        + ","
        + p.FINAL_DSL_KEY
        + "="
        + p.JR_NULL
        + ']"'
    )
    assert p.parse_dsl_entry(text_entry) == {
        "daTE": VALID_FUTURE_DT_UTC_FROM_CEST,
        p.FINAL_DSL_KEY: p.NA,
    }


def test_parse_dsl_entry_nok_date_value_invalid():
    text_entry = (
        '"tag@42[daTE=9999'
        + VALID_FUTURE_ISO_CEST_COLON
        + ","
        + p.FINAL_DSL_KEY
        + "="
        + p.JR_NULL
        + ']"'
    )
    with pytest.raises(ValueError, match=r"time data '9999.*"):
        assert p.parse_dsl_entry(text_entry)


def test_parse_dsl_entry_ok_id_sequence():
    text_entry = (
        '"tag@42[iD=42,myID=-1,someSequence=0,'
        + p.FINAL_DSL_KEY
        + "="
        + p.JR_NULL
        + ']"'
    )
    assert p.parse_dsl_entry(text_entry) == {
        "iD": 42,
        "myID": -1,
        "someSequence": 0,
        p.FINAL_DSL_KEY: p.NA,
    }


def test_parse_dsl_entry_nok_id_value_no_int():
    text_entry = '"tag@42[iD=no_int,' + p.FINAL_DSL_KEY + "=" + p.JR_NULL + ']"'
    message = r"invalid literal for int\(\) with base 10: 'no_int'"
    with pytest.raises(ValueError, match=message):
        assert p.parse_dsl_entry(text_entry)


def test_parser_split_kv_ok():
    assert p.split_kv("pragma", "ag") == ("pr", "ma")
    assert p.split_kv("start", "s") == (None,) * 2
    assert p.split_kv("+==", "=") == ("+", "=")
    assert p.split_kv("==", "=") == (None,) * 2
    assert p.split_kv("=", "=") == (None,) * 2
    assert p.split_kv("=", "+") == (None, "=")
    assert p.split_kv("", "+") == (None, "")
    assert p.split_kv("", "ä") == (None, "")


def test_parser_split_kv_nok():
    assert p.split_kv("", 42) == (None, "")


def test_parser_split_issue_key_ok():
    text_key = "BAZ-42"
    assert p.split_issue_key(text_key) == ("BAZ", 42)


def test_parser_split_issue_key_ok_negative():
    text_key = "BAZ--42"
    assert p.split_issue_key(text_key) == ("BAZ", -42)


def test_parser_split_issue_key_nok_wrong_sep():
    text_key = "BAZ_42"
    message = text_key + r" is not a valid issue key composed of project and serial"
    with pytest.raises(ValueError, match=message):
        assert p.split_issue_key(text_key)


def test_parser_split_issue_key_nok_no_serial():
    no_serial = "Bar"
    text_key = "Foo-" + no_serial
    message = r"invalid literal for int\(\) with base 10: '" + no_serial + "'"
    with pytest.raises(ValueError, match=message):
        assert p.split_issue_key(text_key)


def test_parser_sorted_issue_keys_ok():
    text_keys = ("BAZ-42", "BAR-999", "BAZ-41", "A-1")
    sorted_keys = ("A-1", "BAR-999", "BAZ-41", "BAZ-42")
    assert tuple(p.sorted_issue_keys_gen(text_keys)) == sorted_keys


def test_parser_sorted_issue_keys_ok_corner_min():
    text_keys = ("BAZ-42",)
    sorted_keys = text_keys
    assert tuple(p.sorted_issue_keys_gen(text_keys)) == sorted_keys


def test_parser_sorted_issue_keys_ok_empty():
    text_keys = tuple()
    sorted_keys = text_keys
    assert tuple(p.sorted_issue_keys_gen(text_keys)) == sorted_keys


def test_parser_sorted_issue_keys_ok_empty_string():
    text_keys = ""
    sorted_keys = tuple()
    assert tuple(p.sorted_issue_keys_gen(text_keys)) == sorted_keys


def test_parser_sorted_issue_keys_nok_non_iterable():
    data = 42
    message = r"'int' object is not iterable"
    with pytest.raises(TypeError, match=message):
        tuple(p.sorted_issue_keys_gen(data))


def test_parser_most_common_issue_projects_ok():
    text_keys = ("BAZ-42", "BAR-999", "BAZ-41", "A-1")
    most_common = [("BAZ", 2), ("BAR", 1), ("A", 1)]
    assert p.most_common_issue_projects(text_keys) == most_common


def test_parser_most_common_issue_projects_ok_duplicates():
    text_keys = ("BAZ-42", "BAR-999", "BAZ-42", "A-1")
    most_common = [("BAZ", 2), ("BAR", 1), ("A", 1)]
    assert p.most_common_issue_projects(text_keys) == most_common


def test_parser_stable_make_unique_ok():
    data = ("BAZ-41", "BAR-999", "BAZ-41", "A-1")
    stable_unique = ("BAZ-41", "BAR-999", "A-1")
    assert tuple(p.stable_make_unique(data)) == stable_unique


def test_parser_stable_make_unique_ok_empty():
    data = tuple()
    stable_unique = tuple()
    assert tuple(p.stable_make_unique(data)) == stable_unique


def test_parser_stable_make_unique_nok_non_iterable():
    data = 42
    message = r"'int' object is not iterable"
    with pytest.raises(TypeError, match=message):
        tuple(p.stable_make_unique(data))


def test_parser_stable_make_unique_nok_non_hashable():
    data = ({}, [], set())
    message = r"unhashable type: 'dict'"
    with pytest.raises(TypeError, match=message):
        tuple(p.stable_make_unique(data))
