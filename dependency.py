import subprocess
import importlib
import importlib.util
from contextlib import contextmanager


@contextmanager
def setup(module_name, pip_package_name=None, pip="pip3", retry=3):
    if not importlib.util.find_spec(module_name):
        for i in range(retry):
            subprocess.check_call(
                [pip, 'install', pip_package_name if pip_package_name else module_name])
            if importlib.util.find_spec(module_name):
                break
    yield
