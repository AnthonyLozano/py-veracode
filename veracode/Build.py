from .App import App


class Build:
    def __init__(self, api=None, app_id: int = None, build_id: int = None, version: str = None):
        self.api = api
        self.app_id = app_id
        self.build_id = build_id
        self.version = version
        self.app = App(app_id=app_id, api=api)

    def begin_prescan(self):
        raise NotImplementedError

    def begin_scan(self):
        raise NotImplementedError

    def __str__(self):
        return f'Build #{self.build_id} for app_id: {self.app_id}'

    def __repr__(self):
        return f'Build(api={self.api}, app_id={self.app_id}, build_id={self.build_id}, version="{self.version}"'
