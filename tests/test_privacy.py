# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring,unused-import,reimported
from unittest import mock
import importlib
import json
import os
import pytest  # type: ignore
import nineties.privacy as priv

ALIASES_ENV_VALUE = None
ALIASES_ENV = priv.ALIASES_ENV
NAME_ALIAS = "j."
NAME_ENTITY = "jane"
JSON_TEXT = '{"' + priv.NAME + '": {"' + NAME_ALIAS + '": "' + NAME_ENTITY + '"}}'
EFFECTIVE_VALUE = {priv.NAME: {NAME_ALIAS: NAME_ENTITY}, priv.EMAIL: {}, priv.TEXT: {}}

S_NAMES = ("Allison Hill", "Noah Rhodes")
NAME_SAFE_FIRST = S_NAMES[0]
EMAIL_ALIAS = "a.b@c.de"
S_EMAIL = "jeffrey94@hotmail.com"
S_TEXT = "Beautiful instead ahead despite measure ago current."


def setup():
    global ALIASES_ENV_VALUE  # pylint: disable=global-statement
    ALIASES_ENV_VALUE = os.getenv(ALIASES_ENV)


def teardown():
    if ALIASES_ENV_VALUE is None:
        os.environ[ALIASES_ENV] = ""
    else:
        os.environ[ALIASES_ENV] = ALIASES_ENV_VALUE


def test_privacy_expose_aliases_ok_set_empty():
    os.environ[ALIASES_ENV] = ''
    message = r"Expecting value: line 1 column 1 \(char 0\)"
    with pytest.raises(json.decoder.JSONDecodeError, match=message):
        importlib.reload(priv)


def test_privacy_expose_aliases_ok_set_json_object_text():
    os.environ[priv.ALIASES_ENV] = json.dumps(priv.EMPTY_ALIASES)
    importlib.reload(priv)
    assert priv.expose_aliases() == priv.EMPTY_ALIASES


def test_privacy_expose_aliases_ok_set_json_object_text_non_default():
    os.environ[priv.ALIASES_ENV] = JSON_TEXT
    importlib.reload(priv)
    assert priv.expose_aliases() == EFFECTIVE_VALUE


def test_privacy_expose_aliases_nok_set_json_non_object_text():
    os.environ[priv.ALIASES_ENV] = '[1, 2, 3, "foo"]'
    message = r"list indices must be integers or slices, not str"
    with pytest.raises(TypeError, match=message):
        importlib.reload(priv)


@mock.patch("os.path.isfile")
def test_privacy_expose_aliases_ok_set_json_file(if_mock):
    a_file = "faked-file.really"
    if_mock.return_value = True
    mock_open = mock.mock_open(read_data=JSON_TEXT)

    os.environ[priv.ALIASES_ENV] = a_file
    with mock.patch("builtins.open", mock_open):
        importlib.reload(priv)

    if_mock.assert_called_with(a_file)
    assert if_mock.return_value is True
    assert priv.expose_aliases() == EFFECTIVE_VALUE


def test_privacy_expose_aliases_asp_ok_set_json_object_text_non_default():
    os.environ[priv.ALIASES_ENV] = JSON_TEXT
    importlib.reload(priv)
    assert priv.expose_aliases(priv.NAME) == {NAME_ALIAS: NAME_ENTITY}


def test_privacy_expose_surrogates_asp_ok_set_json_object_text_non_default():
    os.environ[priv.ALIASES_ENV] = JSON_TEXT
    importlib.reload(priv)
    assert priv.expose_surrogates(priv.NAME) == {NAME_ENTITY: NAME_SAFE_FIRST}


def test_privacy_ensure_privacy_asp_ok_name():
    os.environ[priv.ALIASES_ENV] = JSON_TEXT
    importlib.reload(priv)
    assert priv.ensure_privacy(priv.NAME, NAME_ALIAS) == NAME_SAFE_FIRST


def test_privacy_ensure_privacy_asp_ok_name_new():
    os.environ[priv.ALIASES_ENV] = JSON_TEXT
    importlib.reload(priv)
    assert priv.ensure_privacy(priv.NAME, "n.n.") == S_NAMES[1]


def test_privacy_sentence_ok():
    assert priv.sentence() == S_TEXT


def test_privacy_safe_email_ok():
    assert priv.safe_email(EMAIL_ALIAS) == S_EMAIL
