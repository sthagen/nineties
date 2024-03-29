# -*- coding: utf-8 -*-
"""Command line arg for nineties."""
import json
import os
import sys
from typing import no_type_check

try:
    from faker import Faker
except ImportError as err:
    raise ImportError('dependency faker not found - please pip install faker. Details %s' % (err,))


import nineties.parser as p90
import nineties.privacy as priv

# Below to profit from insert ordering of dicts in 3.6+
if tuple(sys.version_info) < (3, 6):
    raise RuntimeError('python version 3.6 or higher required (better dicts)')


FAKE = Faker()
Faker.seed(42)


@no_type_check
def parse(json_text, process_with):
    """Dive deep ..."""
    data = json.loads(json_text)
    record = {}
    for key, value in data.items():
        if key in process_with:
            record[key] = process_with[key](value)

    return record


@no_type_check
def main(argv=None):
    """Drive the understanding ..."""
    argv = sys.argv if argv is None else argv
    parser_map = {
        'dsl': p90.parse_dsl_entry,
        'timestamp': p90.parse_timestamp,
        'name': priv.safe_name,
    }
    for text_or_file in argv[1:]:
        if os.path.isfile(text_or_file):
            with open(text_or_file, 'rt') as json_file:
                all_text = json_file.read()
            data = parse(all_text, parser_map)
        else:
            if p90.START_DATA in text_or_file:
                data = parse(text_or_file, parser_map)
            else:
                data = {'error': text_or_file}

        print(data)
