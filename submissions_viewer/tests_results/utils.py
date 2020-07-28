import time

import ipywidgets as widgets
from IPython import display


def _display(out: widgets.Output, content, clear_output=True):
    @out.capture(clear_output=clear_output, wait=True)
    def _display_out():
        display.display(content)
        time.sleep(1)

    _display_out()
