from datetime import datetime

from dateutil.parser import parse as datetime_parser

from veracode import Api


class App:
    def __init__(self, app_id: int = None,
                 api: Api = None,
                 app_name: str = None,
                 description: str = None,
                 business_criticality: str = None,
                 teams: str = None,
                 origin: str = None,
                 industry_vertical: str = None,
                 app_type: str = None,
                 deployment_method: str = None,
                 is_web_application: str = None,
                 modified_date: datetime = None,
                 cots: str = None,
                 vast: str = None,
                 business_unit: str = None,
                 tags: str = None,
                 policy_updated_date: datetime = None):
        """

        :type api: Api
        :param app_id: Id of app
        :param app_name:  Optional name of app
        :param api: instance to use for methods in this instance
        """
        self.id = app_id
        self.name = app_name
        self.api = api
        self.description = description
        self.business_criticality = business_criticality
        self.teams = teams
        self.origin = origin
        self.industry_vertical = industry_vertical
        self.app_type = app_type
        self.deployment_method = deployment_method
        self.is_web_application = is_web_application
        self.modified_date = modified_date
        self.cots = cots
        self.vast = vast
        self.business_unit = business_unit
        self.tags = tags
        self.policy_updated_date = policy_updated_date

    def retrieve_info(self):
        attrs = self.api.get_app_info(self.id)
        if 'modified_date' in attrs:
            attrs['modified_date'] = datetime_parser(attrs['modified_date'])
        if 'policy_updated_date' in attrs:
            attrs['policy_updated_date'] = datetime_parser(attrs['policy_updated_date'])
        for key, value in attrs.items():
            setattr(self, key, value)

    def get_build_info(self, build_id: int = None, sandbox_id: int = None):
        return self.api.get_build_info(self.id, build_id, sandbox_id)

    def begin_prescan(self,
                      autoscan: bool = False,
                      sandbox_id: int = None,
                      scan_all_nonfatal_top_level_modules: bool = False):
        pass

    def __repr__(self):
        return f'App(app_id={self.id})'
