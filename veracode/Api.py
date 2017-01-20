import requests
from bs4 import BeautifulSoup

from .App import App
from .Build import Build
from .Credential import Credential


class Api:
    VERACODE_API_URL = 'https://analysiscenter.veracode.com/api/5.0/'

    def __init__(self, credential_file=None, credential=None):
        if credential:
            self.credential = credential
        elif credential_file:
            self.credential = Credential.read_credential_from_file(credential_file)
        else:
            self.credential = Credential.read_credential_from_file()

    def begin_prescan(self, app_id: int, auto_scan: bool = None, sandbox_id: int = None,
                      scan_all_nonfatal_top_level_modules: bool = None):
        payload = {'app_id': app_id}
        if auto_scan:
            payload['auto_scan'] = auto_scan
        if sandbox_id:
            payload['sandbox_id'] = sandbox_id
        if scan_all_nonfatal_top_level_modules:
            payload['scan_all_nonfatal_top_level_modules'] = scan_all_nonfatal_top_level_modules
        soup = self.submit_and_soupify("beginprescan.do", payload=payload)
        return self.parse_build_info(soup)

    def begin_scan(self, app_id: int, scan_all_top_level_modules: bool = None, scan_selected_modules: bool = None,
                   scan_previously_selected_modules: bool = None, sandbox_id: int = None):
        payload = {'app_id': app_id}
        if scan_all_top_level_modules:
            payload['scan_all_top_level_modules'] = scan_all_top_level_modules
        if scan_selected_modules:
            payload['scan_selected_modules'] = scan_selected_modules
        if scan_previously_selected_modules:
            payload['scan_previously_selected_modules'] = scan_previously_selected_modules
        if sandbox_id:
            payload['sandbox_id'] = sandbox_id
        self.submit_and_soupify('beginscan.do', payload=payload)

    def delete_app(self, app_id: int):
        payload = {'app_id': app_id}
        self.submit_and_soupify('deleteapp.do', payload=payload)

    def delete_build(self, app_id: int, sandbox_id: int = None):
        payload = {'app_id': app_id}
        if sandbox_id:
            payload['sandbox_id'] = None
        soup = self.submit_and_soupify("getbuildinfo.do", payload=payload)
        return self.parse_build_list(soup)

    def get_app_info(self, app_id: int) -> dict:
        soup = self.submit_and_soupify("getappinfo.do", payload={'app_id': app_id})
        return soup.application.attrs

    def get_app_list(self):
        soup = self.submit_and_soupify("getapplist.do")
        apps = [App(api=self, **app_tag.attrs) for app_tag in soup.applist.find_all('app')]
        return apps

    def get_build_info(self, app_id: int, build_id: int = None, sandbox_id: int = None):
        payload = {'app_id': app_id}
        if build_id:
            payload['build_id'] = build_id
        if sandbox_id:
            payload['sandbox_id'] = sandbox_id
        soup = self.submit_and_soupify("getbuildinfo.do", payload=payload)
        return self.parse_build_info(soup)

    def get_build_list(self, app_id: int):
        payload = {'app_id': app_id}
        soup = self.submit_and_soupify("getbuildlist.do", payload=payload)
        return self.parse_build_list(soup)

    @staticmethod
    def parse_build_info(soup):
        build_info = soup.build.attrs
        build_info['app_id'] = soup.buildinfo.attrs['app_id']
        return build_info

    def parse_build_list(self, soup):
        app_id = soup.buildlist['app_id']
        return [Build(api=self, app_id=app_id, **build_tag.attrs) for build_tag in soup.buildlist.find_all('build')]

    def get_file_list(self, app_id: int, build_id: int = None, sandbox_id: int = None):
        payload = {'app_id': app_id}
        if build_id:
            payload['build_id'] = build_id
        if sandbox_id:
            payload['sandbox_id'] = sandbox_id
        soup = self.submit_and_soupify('getfilelist.do', payload=payload)
        return self.parse_file_list(soup)

    def get_policy_list(self):
        soup = self.submit_and_soupify('getpolicylist.do')
        return soup.policies.attrs['names'].split(',')

    def get_prescan_results(self, app_id: int, build_id: int, sandbox_id: int = None):
        payload = {'app_id': app_id,
                   'build_id': build_id}
        if sandbox_id:
            payload['sandbox_id'] = sandbox_id
        soup = self.submit_and_soupify('getprescanresults.do', payload=payload)
        return soup  # TODO parse this xml

    def upload_file(self, app_id: int, filepath: str, sandbox_id: int = None, save_as: str = None):
        payload = {'app_id': app_id}
        if sandbox_id:
            payload['sandbox_id'] = sandbox_id
        if save_as:
            payload['save_as'] = save_as
        module_file = {'file': open(filepath, 'rb')}
        soup = self.submit_and_soupify('uploadfile.do', payload=payload, files=module_file)
        return self.parse_file_list(soup)

    def remove_file(self, app_id: int, file_id: int, sandbox_id: int = None):
        payload = {'app_id': app_id,
                   'file_id': file_id}
        if sandbox_id:
            payload['sandbox_id'] = sandbox_id
        soup = self.submit_and_soupify('removefile.do', payload=payload)
        return self.parse_file_list(soup)

    @staticmethod
    def parse_file_list(file_list: BeautifulSoup):
        return [file.attrs for file in file_list.filelist.find_all('file')]

    def submit(self, api_endpoint, payload=None, files=None):
        return requests.post(self.VERACODE_API_URL + api_endpoint, params=payload, files=files,
                             auth=(self.credential.username, self.credential.password)).text

    def submit_and_soupify(self, api_endpoint, payload=None, files=None):
        response = self.submit(api_endpoint, payload, files)
        return BeautifulSoup(response, 'html.parser')
