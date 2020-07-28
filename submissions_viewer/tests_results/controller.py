import threading

from submissions_viewer.tests_results.results_db import ResultsDB
from submissions_viewer.tests_results.results_widgets import ResultsWidgets
from submissions_viewer.tests_results.runner import Runner


class Controller:
    def __init__(self, ui_out, plots_out):
        self.ui_out = ui_out
        self.plots_out = plots_out
        self.wg = ResultsWidgets()
        self.db = ResultsDB()
        self.interrupt_refresh_plots = threading.Event()
        self.wg['search_filter']
        self.wg['update_url'].on_click(
            lambda _: self.apply_url(),
        )
        self.wg['search_filter'].observe(
            handler=lambda _: self.apply_filter(),
            names=['value']
        )
        self.wg['interrupt_button'].on_click(lambda _: self.apply_interrupt())
        self.wg['resume_button'].on_click(lambda _: self.apply_resume())
        self.wg._display(self.ui_out)

    def apply_interrupt(self):
        self.interrupt_refresh_plots.set()
        self.set_widgets_interaction(disabled=False)

    def apply_filter(self):
        filter_value = self.wg['search_filter'].value
        filtered_db = self.db.filter_db(filter_value)
        choices = list(filtered_db.keys())
        self.wg.update_dropdown(choices)

    def apply_url(self):
        try:
            self.db.pull_db(self.wg['url'].value)
            self.wg['request_status'].value = True
            self.wg['request_status'].description = f'Success'
        except Exception as e:
            self.wg['request_status'].value = False
            self.wg['request_status'].description = f'{e}'
        finally:
            self.apply_filter()

    def pull_and_filter_db(self):
        self.db.pull_db(self.wg['url'].value)
        if self.wg['dropdown'].value == 'All':
            return self.db.filter_db(self.wg['search_filter'].value)
        else:
            return self.db.filter_db(self.wg['dropdown'].value)

    def set_widgets_interaction(self, disabled: bool):
        self.wg['url'].disabled = disabled
        self.wg['update_url'].disabled = disabled
        self.wg['search_filter'].disabled = disabled
        self.wg['dropdown'].disabled = disabled
        self.wg['update_interval'].disabled = disabled
        self.wg['resume_button'].disabled = disabled
        self.wg['interrupt_button'].disabled = not disabled

    def apply_resume(self):
        for thread in threading.enumerate():
            if thread.getName() == 'refresh_plots':
                thread.join(timeout=0)
        self.set_widgets_interaction(disabled=True)
        filter_value = self.wg['search_filter'].value \
            if self.wg['dropdown'].value == 'All' \
            else self.wg['dropdown'].value
        runner = Runner(
            url=self.wg['url'].value,
            filter_value=filter_value,
            update_interval=self.wg['update_interval'].value,
            interrupt_refresh_plots=self.interrupt_refresh_plots,
            outs=self.plots_out
        )
        threading.Thread(name='refresh_plots', target=runner, daemon=True).start()
