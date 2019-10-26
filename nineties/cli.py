# -*- coding: utf-8 -*-
"""Command line arg for nineties."""

import nineties.parser as p90


def main(argv):
    """Drive the understanding ..."""
    for sprint_entry in argv[1:]:
        print(p90.parse_dsl_entry(sprint_entry))
