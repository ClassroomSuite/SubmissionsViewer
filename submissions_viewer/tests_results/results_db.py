import requests


class ResultsDB:
    def __init__(self):
        self.db = dict()

    def pull_db(self, url):
        try:
            res = requests.get(url)
            if res.ok:
                self.db.clear()
                self.db.update(res.json())
            else:
                self.db.clear()
                raise Exception(f'Bad request: {res.text}')
        except:
            self.db.clear()
            raise Exception(f'Bad url')

    def filter_db(self, filter_value):
        filtered_db = dict()
        filtered_keys = list(filter(lambda name: str(name).find(filter_value) != -1, self.db.keys()))
        for key in filtered_keys:
            if key != 'null' and key != 'scripts':
                filtered_db[key] = self.db[key]
        return filtered_db

    def __getitem__(self, item):
        return self.db[item]
