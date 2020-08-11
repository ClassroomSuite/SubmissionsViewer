import webbrowser

import requests
from IPython import display
from ipywidgets import widgets


def get_file(url):
    try:
        res = requests.get(url)
        if res.ok:
            return res.content.decode('utf-8')
        else:
            raise Exception(f'Bad request: {res.text}')
    except:
        raise Exception(f'Bad url')


def get_line_counts(files):
    line_counts = dict()
    for f in files:
        lines = f.split('\n')
        unique_lines = set(lines)
        for line in unique_lines:
            line_counts.setdefault(line, 0)
            line_counts[line] += 1
    return line_counts


def score_lines(file, line_counts):
    lines = file.split('\n')
    scores = list(map(lambda line: line_counts[line], lines))
    return scores


def _get_scores(files):
    line_counts = get_line_counts(files)
    files_scores = list(map(lambda file: score_lines(file, line_counts), files))
    return files_scores


def get_formatted_scores(files):
    files_scores = _get_scores(files)
    formatted_scores = []
    for scores in files_scores:
        formatted_scores.append(
            list(map(
                lambda score: f'{100 * score / len(files_scores):.2f}% ({score}/{len(files_scores)})\n',
                scores
            ))
        )
    return formatted_scores


class FilesWidgets:
    def __init__(self, out: widgets.Output, get_filtered_db):
        self.wg = dict()
        self.files = dict()
        self.scores = dict()
        self._get_filtered_db = get_filtered_db
        self._create()
        self._add_functionality()
        self._display(out)
        self.update_selection_options()

    def _create(self):
        default_layout = widgets.Layout(width='auto', height='auto')
        self.wg['organization'] = widgets.Text(
            value='',
            description='Organization',
            layout=default_layout
        )
        self.wg['filter'] = widgets.Text(
            description='Filter',
            placeholder='Repository names must contain',
            layout=default_layout
        )
        self.wg['filename'] = widgets.Text(
            value='exercice.py',
            description='Filename',
            layout=default_layout
        )
        self.wg['request_url'] = widgets.Text(
            description='Request URL',
            value=f'https://raw.githubusercontent.com/{self.wg["organization"].value}/%RepositoryName%/master/{self.wg["filename"].value}',
            layout=default_layout,
            disabled=True
        )
        self.wg['get_files'] = widgets.Button(description='Fetch submissions')
        self.wg['get_files_status'] = widgets.Valid(value=True, description='Ready', layout=default_layout)
        self.wg['previous_button'] = widgets.Button(description='Previous')
        self.wg['next_button'] = widgets.Button(description='Next')
        self.wg['open_in_browser'] = widgets.Button(description='Open in GitHub', layout=default_layout)
        self.wg['open_file'] = widgets.Checkbox(description='File only', layout=default_layout)
        self.wg['repository_select'] = widgets.Dropdown(
            description='Select',
            layout=widgets.Layout(width='600px'))
        self.wg['max_preview_lines'] = widgets.IntText(
            value=100,
            disabled=False,
            layout=widgets.Layout(width='50px')
        )
        self.wg['preview_lines_range'] = widgets.IntRangeSlider(
            value=[0, 20],
            min=0,
            max=self.wg['max_preview_lines'].value,
            step=1,
            description='Lines range:',
            continuous_update=True,
            orientation='horizontal',
            readout=True,
            readout_format='d',
            layout=widgets.Layout(width='500px')
        )
        self.wg['repository_grading'] = widgets.HTML(
            layout=widgets.Layout(
                width='auto',
                height='auto',
                border='solid 1px',
                padding='2px 10px 2px 10px'
            )
        )
        html_layout = widgets.Layout(width='auto', height='auto', padding='20px 100px 0px 20px')
        self.wg['file_preview_stats'] = widgets.HTML(layout=html_layout)
        self.wg['file_preview'] = widgets.HTML(layout=html_layout)
        self.wg['file_view_stats'] = widgets.HTML(layout=html_layout)
        self.wg['file_view'] = widgets.HTML(layout=html_layout)
        file_preview_box = widgets.HBox((self.wg['file_preview'], self.wg['file_preview_stats']))
        file_view_box = widgets.HBox((self.wg['file_view'], self.wg['file_view_stats']))
        lines_range_box = widgets.HBox((self.wg['preview_lines_range'], self.wg['max_preview_lines']))
        self.wg['accordion'] = widgets.Accordion(
            children=[
                widgets.VBox((lines_range_box, file_preview_box)),
                file_view_box
            ]
        )
        self.wg['accordion'].set_title(0, 'Preview')
        self.wg['accordion'].set_title(1, 'File')

    def _add_functionality(self):
        self.wg['organization'].observe(lambda _: self._update_request_url())
        self.wg['filename'].observe(lambda _: self._update_request_url())
        self.wg['filter'].observe(lambda _: self._apply_filter())
        self.wg['max_preview_lines'].observe(lambda _: self._update_max_preview_lines())
        self.wg['get_files'].on_click(lambda _: self.update_files_and_scores())
        self.wg['previous_button'].on_click(lambda _: self._select_previous())
        self.wg['next_button'].on_click(lambda _: self._select_next())
        self.wg['open_in_browser'].on_click(lambda _: self._open_browser())
        self.wg['repository_select'].observe(lambda _: self._apply_select())
        self.wg['preview_lines_range'].observe(lambda _: self._update_file_preview())

    def _display(self, out: widgets.Output):
        @out.capture()
        def _display():
            display.display(widgets.HTML('<h1>View submissions files</h1>'))
            display.display(self.wg['organization'])
            display.display(self.wg['filter'])
            display.display(self.wg['filename'])
            display.display(self.wg['request_url'])
            display.display(widgets.HBox((self.wg['get_files'], self.wg['get_files_status'])))
            display.display(
                widgets.HBox((self.wg['repository_select'], self.wg['open_in_browser'], self.wg['open_file'])))
            display.display(widgets.HBox((self.wg['previous_button'], self.wg['next_button'])))
            display.display(self.wg['repository_grading'])
            display.display(self.wg['accordion'])

        _display()

    def _apply_filter(self):
        self._update_request_url()
        self.update_selection_options()
        self._apply_select()

    def _update_max_preview_lines(self):
        self.wg['preview_lines_range'].max = self.wg['max_preview_lines'].value

    def _open_browser(self):
        org = self.wg['organization'].value
        repo = self.wg['repository_select'].value
        filename = self.wg['filename'].value
        if self.wg['open_file'].value == True:
            webbrowser.open(f'https://github.com//{org}/{repo}/blob/master/{filename}')
        else:
            webbrowser.open(f'https://github.com//{org}/{repo}')

    def _update_request_url(self):
        org = self.wg['organization'].value
        filename = self.wg['filename'].value
        repository_filter = self.wg['filter'].value
        self.wg[
            'request_url'].value = f'https://raw.githubusercontent.com/{org}/%Repository name containing: {repository_filter}%/master/{filename}'

    def _update_file_view(self, file=None, line_scores=None):
        selection = self.wg['repository_select'].value
        try:
            file = self.files[selection]
            line_scores = self.scores[selection]
        except KeyError:
            self.wg['file_view_stats'].value = '<p>Couldn\'t get stats</p>'
            self.wg['file_view'].value = '<p>Couldn\'t get file</p>'
        else:
            self.wg['file_view_stats'].value = '<pre><code>' + ''.join(line_scores) + '</code></pre>'
            self.wg['file_view'].value = '<pre><code>' + file + '</code></pre>'

    def _update_file_preview(self):
        selection = self.wg['repository_select'].value
        try:
            file = self.files[selection]
            line_scores = self.scores[selection]
        except KeyError:
            self.wg['file_preview_stats'].value = '<p>Couldn\'t get stats</p>'
            self.wg['file_preview'].value = '<p>Couldn\'t get file</p>'
        else:
            lines_range = self.wg['preview_lines_range']
            file_lines = [line + '\n' for line in file.split('\n')]
            selected_lines = file_lines[lines_range.lower: min(lines_range.upper, len(file_lines))]
            selected_scores = line_scores[lines_range.lower: min(lines_range.upper, len(line_scores))]
            self.wg['file_preview_stats'].value = '<pre><code>' + ''.join(selected_scores) + '</code></pre>'
            self.wg['file_preview'].value = '<pre><code>' + ''.join(selected_lines) + '</code></pre>'

    def _get_request_urls(self, repository_names):
        org = self.wg['organization'].value
        filename = self.wg['filename'].value
        urls = list(map(
            lambda
                repo: f'https://raw.githubusercontent.com/{org}/{repo}/master/{filename}',
            repository_names
        ))
        return urls

    def _get_files(self, urls):
        files = []
        self.wg['get_files_status'].value = True
        self.wg['get_files_status'].description = f'Success'
        num_failed = 0
        for url in urls:
            try:
                file = get_file(url)
                files.append(file)
            except:
                num_failed += 1
                files.append('Couldn\'t get file')
                self.wg['get_files_status'].value = False
                self.wg['get_files_status'].description = f'{num_failed} failed'
        return files

    def update_selection_options(self):
        repository_names = self._get_filtered_repository_names()
        if len(repository_names) > 0:
            self.wg['repository_select'].options = repository_names
            self.wg['repository_select'].value = repository_names[0]
        else:
            self.wg['repository_select'].options = ['Not found']
            self.wg['repository_select'].value = 'Not found'

    def update_files_and_scores(self):
        self.update_selection_options()
        repository_names = self._get_filtered_repository_names()
        urls = self._get_request_urls(repository_names)
        files = self._get_files(urls)
        formatted_scores = get_formatted_scores(files)
        self.files = dict(zip(repository_names, files))
        self.scores = dict(zip(repository_names, formatted_scores))
        self._apply_select()

    def _select_previous(self):
        options = list(self.wg['repository_select'].options)
        index = options.index(self.wg['repository_select'].value)
        new_index = max(0, index - 1)
        self.wg['repository_select'].value = options[new_index]
        self._apply_select()

    def _select_next(self):
        options = list(self.wg['repository_select'].options)
        index = options.index(self.wg['repository_select'].value)
        new_index = min(len(options) - 1, index + 1)
        self.wg['repository_select'].value = options[new_index]
        self._apply_select()

    def _apply_select(self):
        self._update_repository_grading()
        self._update_file_preview()
        self._update_file_view()

    def _update_repository_grading(self):
        filter_value = self.wg['filter'].value
        filtered_db = self._get_filtered_db(filter_value)
        try:
            test_dict = filtered_db[self.wg['repository_select'].value]
            grading_html = 'Test results:<br>'
            for test_name, test_result in test_dict.items():
                result = "ok" if test_result["passing"] else "fail"
                grading_html += f'- {test_name}: {result}<br>'
            self.wg['repository_grading'].value = grading_html
        except:
            self.wg['repository_grading'].value = '<p>Couldn\'t apply grading</p>'

    def _get_filtered_repository_names(self):
        filter_value = self.wg['filter'].value
        filtered_db = self._get_filtered_db(filter_value)
        return list(filtered_db.keys())
