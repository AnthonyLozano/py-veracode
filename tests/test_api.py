# from unittest import TestCase
# from unittest.mock import MagicMock
# from vcapi import Api, Credential
# import logging
#
# TEST_APP_ID = 284174
# TEST_BUILD_ID = 1139745
#
# class TestApi(TestCase):
#     def setUp(self):
#         #self.api = Api()
#         self.api = Api(credential_file='test-credential')
#
#     def tearDown(self):
#         pass
#
#     def test_get_app_list(self):
#         print(self.api.get_app_list())
#
#     def test_get_build_info(self):
#         self.api.submit = MagicMock(return_value=open('data/build-info-response.xml'))
#         print(self.api.get_build_info(123))
#         self.api.submit.assert_called()
#
#     def test_get_file_list(self):
#         print(self.api.get_file_list(TEST_APP_ID))
#
#     def test_upload_file(self):
#         z = self.api.upload_file(TEST_APP_ID, 'data/testbin/HelloWorld.class')
#         print(z)
#
#     def test_begin_prescan(self):
#         z = self.api.begin_prescan(TEST_APP_ID, auto_scan=True)
#         print(z)
#
#     def test_get_build_list(self):
#         print(self.api.get_build_list(TEST_APP_ID))
#
#     def test_get_policy_list(self):
#         print(self.api.get_policy_list())
#
#     def test_get_prescan_results(self):
#         res = self.api.get_prescan_results(TEST_APP_ID, TEST_BUILD_ID)
#         print(res)
#
#     def test_get_app_info(self):
#         res = self.api.get_app_info(TEST_APP_ID)
#         print(res)
