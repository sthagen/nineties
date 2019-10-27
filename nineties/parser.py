# -*- coding: utf-8 -*-
"""Parsers for issues from the Nineties."""
import datetime as dti
import operator
from typing import Tuple

ISO_FMT = "%Y-%m-%dT%H:%M:%S.%f"
ISO_LENGTH = len("YYYY-mm-ddTHH:MM:SS.fff")
TZ_OP = {"+": operator.sub, "-": operator.add}  # + indicates ahead of UTC

JR_NULL = "<null>"
NA = "n/a"

START_DATA, END_DATA = "[", "]"
REC_SEP, KV_SEP = ",", "="
FINAL_DSL_KEY = "final"


def split_at(text_fragment: str, pos: int) -> Tuple:
    """Split text fragment by position and return pair as tuple."""
    return text_fragment[:pos], text_fragment[pos:]


def parse_timestamp(text_stamp):
    """
    Parse the timestamp formats found in REST responses from the Nineties.

    Return as datetime timestamp in UTC (implicit).
    """
    if text_stamp is None or text_stamp == JR_NULL:
        return None

    iso_value, off = split_at(text_stamp, ISO_LENGTH)
    local_time = dti.datetime.strptime(iso_value, ISO_FMT)
    if not off:
        return local_time

    sign_pos = 0
    assert off and off[sign_pos] in TZ_OP

    m_start = 3 if ":" not in off else 4
    assert len(off) == m_start + 2

    oper, hours, minutes = off[sign_pos], int(off[1:3]), int(off[m_start:])

    return TZ_OP[oper](local_time, dti.timedelta(hours=hours, minutes=minutes))


def split_kv(text_pair, sep):
    """Helper."""
    try:
        key, value = text_pair.split(sep, 1)
    except ValueError:
        return None, text_pair
    if not key:
        return None, None
    return key, value


def parse_dsl_entry(text_entry, final_key=None):
    """
    Parse some nifty dict() like argument list where the final rhs is untrusted.

    Return a dict of the pairs upon success or empty otherwise.
    """
    if not text_entry:
        return {}
    rococo = '"' + END_DATA
    text_entry = text_entry.strip(rococo)
    _, payload = text_entry.split(START_DATA, 1)  # final rhs may by anything

    final_key = FINAL_DSL_KEY if final_key is None else final_key
    final_key_indicator = REC_SEP + final_key + KV_SEP
    empty_goal_indicator = final_key_indicator + JR_NULL
    if (  # pylint: disable=bad-continuation
        payload.endswith(empty_goal_indicator)
        and payload.count(final_key_indicator) == 1
    ):
        text_pairs = payload.split(REC_SEP)
    else:
        others, final = payload.split(final_key_indicator, 1)
        text_pairs = others.split(REC_SEP) + [final_key + KV_SEP + final]

    pairs = [split_kv(text_pair, KV_SEP) for text_pair in text_pairs]
    record = {k: v for k, v in pairs if k}

    for key, value in record.items():
        key_lower = key.lower()
        if "date" in key_lower:
            record[key] = parse_timestamp(value)
        elif "id" in key_lower or "sequence" in key_lower:
            record[key] = int(value)
        elif key == final_key and value == JR_NULL:
            record[key] = NA

    return record
