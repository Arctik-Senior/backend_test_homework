import sys
from pathlib import Path
from io import StringIO

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent
sys.path.append(str(BASE_DIR))


class Capturing(list):
    """
    Class for capturing function stdout.
    Usage:
     with Capturing() as func_output:
         func()

    check func() output in func_output variable
    """

    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._string = StringIO()
        return self

    def __exit__(self, *args):
        self.extend(self._string.getvalue().splitlines())
        del self._string
        sys.stdout = self._stdout


def pytest_make_parametrize_id(config, val):
    return repr(val)
