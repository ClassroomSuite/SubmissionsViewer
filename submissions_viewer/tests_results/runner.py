import os
import threading
import time

import ipywidgets as widgets
import matplotlib.pyplot as plt
from IPython import display

from submissions_viewer.tests_results.figures import Figures
from submissions_viewer.tests_results.results_db import ResultsDB
from submissions_viewer.tests_results.utils import _display


class Runner:
    def __init__(self,
                 url,
                 filter_value,
                 update_interval,
                 interrupt_refresh_plots,
                 outs: widgets.Output
                 ):
        self.url = url
        self.filter_value = filter_value
        self.update_interval = update_interval
        self.interrupt_refresh_plots = interrupt_refresh_plots
        self.outs = outs
        self.db = ResultsDB()

    def __call__(self):
        self.interrupt_refresh_plots.clear()
        threading.Timer(3600, lambda _: self.interrupt_refresh_plots.set).start()
        interval_timeout = threading.Event()

        figures = Figures()
        while not self.interrupt_refresh_plots.is_set():
            interval_timeout.clear()
            threading.Timer(self.update_interval, interval_timeout.set).start()
            self.show_figures(figures)
            while True:
                if interval_timeout.wait(timeout=1):
                    break
                if self.interrupt_refresh_plots.wait(timeout=1):
                    break

    def _pull_and_filter_db(self):
        self.db.pull_db(self.url)
        if self.filter_value == 'All':
            return self.db.filter_db('')
        else:
            return self.db.filter_db(self.filter_value)

    def show_figures(self, figures):
        filtered_db = self._pull_and_filter_db()
        if not os.path.exists('./figs'):
            os.mkdir('./figs')
        self._show_figure(
            fig=figures.num_passing_per_test(filtered_db),
            filename='fig0.png',
            out=self.outs[0]
        )
        self._show_figure(
            fig=figures.num_passing_per_test(filtered_db),
            filename='fig1.png',
            out=self.outs[1]
        )
        self._show_figure(
            fig=figures.num_passing_per_test(filtered_db),
            filename='fig2.png',
            out=self.outs[2]
        )
        self._show_figure(
            fig=figures.num_passing_per_test(filtered_db),
            filename='fig3.png',
            out=self.outs[3]
        )

    def _show_figure(self, fig, filename, out):
        fullpath = f'./figs/{filename}'
        try:
            os.remove(fullpath)
        except FileNotFoundError as e:
            pass
        try:
            fig.savefig(fullpath, bbox_inches='tight')
            plt.close(fig)
            time.sleep(0.1)
            img = display.Image(filename=fullpath)
            _display(
                out,
                img,
                clear_output=False
            )
        except FileNotFoundError as e:
            pass
