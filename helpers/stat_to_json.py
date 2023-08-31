# https://stackoverflow.com/a/58684090

import os


def stat_to_json(fp: str) -> dict:
    s_obj = os.stat(fp)
    return {k: getattr(s_obj, k) for k in dir(s_obj) if k.startswith('st_')}
