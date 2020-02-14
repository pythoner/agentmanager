# """Tests for RBAC scenarios"""
#
# import os
#
# from agentmanager.api import rbac
# from agentmanager.common import exception
#
#
# from oslo_config import fixture as fixture_config
# from oslo_policy import opts
# from oslo_utils import fileutils
# from oslotest import base
#
#
# class MockRequest(object):
#
#     def __init__(self, path, headers={}):
#         self.path = path
#         self.headers = headers
#         self.arguments = {}
#
#
# class TestRBAC(base.BaseTestCase):
#
#     @classmethod
#     def setUpClass(cls):
#         super(TestRBAC, cls).setUpClass()
#         cls.policy_json = ('{"admin_required": "role:admin",'
#                            '"cloud_admin": '
#                            '"rule:admin_required and domain_id:default",'
#                            '"cloud_admin_and_agentmanager_user": '
#                            '"rule:cloud_admin and user_name:agentmanager",'
#                            '"default": "rule:admin_required",'
#                            '"account:create_account": "rule:cloud_admin",'
#                            '"account:delete_account": "rule:cloud_admin",'
#                            '"account:update_account": "rule:cloud_admin",'
#                            '"account:get_account": "",'
#                            '"account:list_accounts": "",'
#                            '"account:create_chargingitem": '
#                            '"rule:cloud_admin_and_agentmanager_user",'
#                            '"account:delete_chargingitem": "!",'
#                            '"account:get_chargingitem": "",'
#                            '"account:list_chargingitems": "",'
#                            '"account:create_invcode": "rule:cloud_admin",'
#                            '"account:delete_invcode": "rule:cloud_admin",'
#                            '"account:update_invcode": "",'
#                            '"account:check_invcode": "",'
#                            '"account:get_invcode": "rule:cloud_admin",'
#                            '"account:list_invcodes": "rule:cloud_admin",'
#                            '"account:create_payment": '
#                            '"rule:cloud_admin_and_agentmanager_user",'
#                            '"account:delete_payment": "!",'
#                            '"account:update_payment": '
#                            '"rule:cloud_admin_and_agentmanager_user",'
#                            '"account:get_payment": "",'
#                            '"account:list_payments": ""}')
#         cls.tempfile = fileutils.write_to_tempfile(content=cls.policy_json,
#                                                    prefix='policy',
#                                                    suffix='.json')
#
#     @classmethod
#     def tearDownClass(cls):
#         super(TestRBAC, cls).tearDownClass()
#         os.remove(cls.tempfile)
#
#     def setUp(self):
#         super(TestRBAC, self).setUp()
#         self.CONF = self.useFixture(fixture_config.Config()).conf
#         self.CONF([], project='agentmanager', validate_default_values=True)
#         opts.set_defaults(self.CONF)
#         self.CONF.set_override("policy_file", TestRBAC.tempfile,
#                                group='oslo_policy')
#
#     def test_default_rule_with_non_admin(self):
#         headers = {'X-User-Domain-Id': 'default',
#                    'X-Domain-Name': None,
#                    'X-User-Name': u'agentmanager',
#                    'X-Roles': u'member',
#                    'X-User': u'agentmanager',
#                    'X-Project-Domain-Name': 'Default',
#                    'X-Project-Domain-Id': 'default',
#                    'X-User-Id': u'f4333089dad843d2ba55ae28b0e4ed0c',
#                    'X-Tenant': u'services',
#                    'X-Project-Name': u'services',
#                    'X-Role': u'admin',
#                    'X-Domain-Id': None}
#         self.assertRaises(exception.ForbiddenError,
#                           rbac.enforce, "dummy_action",
#                           MockRequest('/dummypath', headers))
#
#     def test_create_account_failed_with_non_admin(self):
#         headers = {'X-User-Domain-Id': 'default',
#                    'X-Domain-Name': None,
#                    'X-User-Name': u'agentmanager',
#                    'X-Roles': u'member',
#                    'X-User': u'agentmanager',
#                    'X-Project-Domain-Name': 'Default',
#                    'X-Project-Domain-Id': 'default',
#                    'X-User-Id': u'f4333089dad843d2ba55ae28b0e4ed0c',
#                    'X-Tenant': u'services',
#                    'X-Project-Name': u'services',
#                    'X-Role': u'admin',
#                    'X-Domain-Id': None}
#         self.assertRaises(exception.ForbiddenError,
#                           rbac.enforce, "create_account",
#                           MockRequest('/account', headers))
#
#     def test_create_account_failed_with_non_default_domain(self):
#         headers = {'X-User-Domain-Id': 'demo',
#                    'X-Domain-Name': None,
#                    'X-User-Name': u'agentmanager',
#                    'X-Roles': u'admin',
#                    'X-User': u'agentmanager',
#                    'X-Project-Domain-Name': 'demo',
#                    'X-Project-Domain-Id': 'demo',
#                    'X-User-Id': u'f4333089dad843d2ba55ae28b0e4ed0c',
#                    'X-Tenant': u'services',
#                    'X-Project-Name': u'services',
#                    'X-Role': u'admin',
#                    'X-Domain-Id': None}
#         self.assertRaises(exception.ForbiddenError,
#                           rbac.enforce, "create_account",
#                           MockRequest('/account', headers))
#
#     def test_create_account_success_with_cloudadmin(self):
#         headers = {'X-User-Domain-Id': 'default',
#                    'X-Domain-Name': None,
#                    'X-User-Name': u'agentmanager',
#                    'X-Roles': u'admin',
#                    'X-User': u'agentmanager',
#                    'X-Project-Domain-Name': 'Default',
#                    'X-Project-Domain-Id': 'default',
#                    'X-User-Id': u'f4333089dad843d2ba55ae28b0e4ed0c',
#                    'X-Tenant': u'services',
#                    'X-Project-Name': u'services',
#                    'X-Role': u'admin',
#                    'X-Domain-Id': None}
#         rbac.enforce("create_account",
#                      MockRequest('/account', headers))
#
#     def test_create_chargingitem_failed_without_billing_and_cloudadmin(self):
#         headers = {'X-User-Domain-Id': 'demo',
#                    'X-Domain-Name': None,
#                    'X-User-Name': u'user01',
#                    'X-Roles': u'admin',
#                    'X-User': u'user01',
#                    'X-Project-Domain-Name': 'demo',
#                    'X-Project-Domain-Id': 'demo',
#                    'X-User-Id': u'f4333089dad843d2ba55ae28b0e4ed0c',
#                    'X-Tenant': u'services',
#                    'X-Project-Name': u'services',
#                    'X-Project-Id': u'8f5f0e1adeb149328a7a2e5ecb8489a3',
#                    'X-Role': u'admin',
#                    'X-Domain-Id': None}
#         self.assertRaises(exception.ForbiddenError,
#                           rbac.enforce, "create_chargingitem",
#                           MockRequest('/chargingitem', headers))
#
#     def test_create_chargingitem_failed_without_billing(self):
#         headers = {'X-User-Domain-Id': 'default',
#                    'X-Domain-Name': None,
#                    'X-User-Name': u'user01',
#                    'X-Roles': u'admin',
#                    'X-User': u'user01',
#                    'X-Project-Domain-Name': 'Default',
#                    'X-Project-Domain-Id': 'default',
#                    'X-User-Id': u'f4333089dad843d2ba55ae28b0e4ed0c',
#                    'X-Tenant': u'services',
#                    'X-Project-Name': u'services',
#                    'X-Project-Id': u'8f5f0e1adeb149328a7a2e5ecb8489a3',
#                    'X-Role': u'admin',
#                    'X-Domain-Id': None}
#         self.assertRaises(exception.ForbiddenError,
#                           rbac.enforce, "create_chargingitem",
#                           MockRequest('/chargingitem', headers))
#
#     def test_create_chargingitem_failed_without_cloudadmin(self):
#         headers = {'X-User-Domain-Id': 'demo',
#                    'X-Domain-Name': None,
#                    'X-User-Name': u'agentmanager',
#                    'X-Roles': u'admin',
#                    'X-User': u'agentmanager',
#                    'X-Project-Domain-Name': 'demo',
#                    'X-Project-Domain-Id': 'demo',
#                    'X-User-Id': u'f4333089dad843d2ba55ae28b0e4ed0c',
#                    'X-Tenant': u'services',
#                    'X-Project-Name': u'services',
#                    'X-Project-Id': u'8f5f0e1adeb149328a7a2e5ecb8489a3',
#                    'X-Role': u'admin',
#                    'X-Domain-Id': None}
#         self.assertRaises(exception.ForbiddenError,
#                           rbac.enforce, "create_chargingitem",
#                           MockRequest('/chargingitem', headers))
#
#     def test_create_chargingitem_success_with_billing_and_cloudadmin(self):
#         headers = {'X-User-Domain-Id': 'default',
#                    'X-Domain-Name': None,
#                    'X-User-Name': u'agentmanager',
#                    'X-Roles': u'admin',
#                    'X-User': u'agentmanager',
#                    'X-Project-Domain-Name': 'Default',
#                    'X-Project-Domain-Id': 'default',
#                    'X-User-Id': u'f4333089dad843d2ba55ae28b0e4ed0c',
#                    'X-Tenant': u'services',
#                    'X-Project-Name': u'services',
#                    'X-Project-Id': u'8f5f0e1adeb149328a7a2e5ecb8489a3',
#                    'X-Role': u'admin',
#                    'X-Domain-Id': None}
#         rbac.enforce("create_chargingitem",
#                      MockRequest('/chargingitem', headers))
#
#     def test_delete_chargingitem_failed_with_any_user(self):
#         headers = {'X-User-Domain-Id': 'default',
#                    'X-Domain-Name': None,
#                    'X-User-Name': u'agentmanager',
#                    'X-Roles': u'admin',
#                    'X-User': u'agentmanager',
#                    'X-Project-Domain-Name': 'Default',
#                    'X-Project-Domain-Id': 'default',
#                    'X-User-Id': u'f4333089dad843d2ba55ae28b0e4ed0c',
#                    'X-Tenant': u'services',
#                    'X-Project-Name': u'services',
#                    'X-Project-Id': u'8f5f0e1adeb149328a7a2e5ecb8489a3',
#                    'X-Role': u'admin',
#                    'X-Domain-Id': None}
#         self.assertRaises(exception.ForbiddenError,
#                           rbac.enforce, "delete_chargingitem",
#                           MockRequest('/chargingitem', headers))
