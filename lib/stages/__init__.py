import sys

from . import appium
from . import autoconf
from . import obfuscator
from . import python
from . import report
from . import visualizer

def get_stages():
    def _gen():
        module = sys.modules[__name__]
        for name in dir(module):
            maybe_module = getattr(module, name)
            if not hasattr(maybe_module, 'Stage'):
                continue

            yield name, maybe_module.Stage

    return dict(_gen())
