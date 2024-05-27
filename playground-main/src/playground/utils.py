import contextlib
import os
import sys
import traceback


def tb_info():
    return "".join(traceback.format_exception(*sys.exc_info())).strip()


def is_windows():
    return "nt" in os.name


@contextlib.contextmanager
def temp_chdir(new_dir):
    old_dir = os.getcwd()
    os.chdir(new_dir)
    try:
        yield
    finally:
        os.chdir(old_dir)