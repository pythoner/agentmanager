"""Tests for agentmanager/api/handler/account.py"""

import mock
from oslotest import base

import agentmanager.api.handler.account as account_han
from agentmanager.common import models

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import UnmappedInstanceError


class MockRequest(object):

    def __init__(self, path):
        self.path = path
        self.arguments = {}


class MockQuery():
    number = 1
    count = -1


class TestAccount(base.BaseTestCase):

    accounts = list()
    account = models.Account(pid='1',
                             balance=10,
                             total_pay=10,
                             ref_resource='gjudsvfk',
                             name='a10')
    accounts.append(account)

    @mock.patch('tornado.web.RequestHandler.__init__', return_value=None)
    @mock.patch('tornado.web.RequestHandler.write')
    @mock.patch('tornado.web.RequestHandler.set_status')
    @mock.patch('agentmanager.common.log.ContextAdapter.error')
    @mock.patch('agentmanager.db.api_sqlalchemy.SQLAlchemyConnection.'
                'get_account_id', return_value=account)
    @mock.patch('agentmanager.api.rbac.enforce')
    def test_get_exitent_account(self, mock_enforce,
                                 mock_get_account_id,
                                 mock_log_error,
                                 mock_tornado_set_status,
                                 mock_tornado_write, mock_tornado_init):
        account_handler = account_han.AccountHandler()
        setattr(account_handler, 'request', MockRequest('/account/1'))
        account_handler.get()
        args = str(mock_tornado_write.call_args)
        self.assertTrue('"total_pay": 10.0' in args)
        self.assertTrue('"balance": 10.0' in args)
        self.assertTrue('"name": "a10"' in args)
        self.assertTrue('"id": "1"' in args)
        self.assertTrue('"ref_resource": "gjudsvfk"' in args)

    """test get a account which id is negative"""
    @mock.patch('tornado.web.RequestHandler.__init__', return_value=None)
    @mock.patch('tornado.web.RequestHandler.write')
    @mock.patch('tornado.web.RequestHandler.set_status')
    @mock.patch('agentmanager.common.log.ContextAdapter.error')
    @mock.patch('agentmanager.db.api_sqlalchemy.SQLAlchemyConnection.'
                'get_account_id', return_value=None)
    @mock.patch('agentmanager.api.rbac.enforce')
    def test_get_negativeid_account(self, mock_enforce,
                                    mock_get_account_id,
                                    mock_log_error,
                                    mock_tornado_set_status,
                                    mock_tornado_write, mock_tornado_init):
        account_handler = account_han.AccountHandler()
        setattr(account_handler, 'request', MockRequest('/account/-1'))
        account_handler.get()
        msg = 'Account -1 Not Found'
        mock_tornado_write.assert_called_once_with(msg)
        mock_log_error.assert_called_once_with(msg)
        mock_tornado_set_status.assert_called_once_with(404)

    @mock.patch('tornado.web.RequestHandler.__init__', return_value=None)
    @mock.patch('tornado.web.RequestHandler.write')
    @mock.patch('tornado.web.RequestHandler.set_status')
    @mock.patch('agentmanager.common.log.ContextAdapter.error')
    @mock.patch('agentmanager.db.api_sqlalchemy.SQLAlchemyConnection.'
                'get_account_id', return_value=None)
    @mock.patch('agentmanager.api.rbac.enforce')
    def test_get_inexitent_account(self, mock_enforce,
                                   mock_get_account_id,
                                   mock_log_error,
                                   mock_tornado_set_status,
                                   mock_tornado_write, mock_tornado_init):
        account_handler = account_han.AccountHandler()
        setattr(account_handler, 'request', MockRequest('/account/1'))
        account_handler.get()
        msg = 'Account 1 Not Found'
        mock_tornado_write.assert_called_once_with(msg)
        mock_log_error.assert_called_once_with(msg)
        mock_tornado_set_status.assert_called_once_with(404)

    @mock.patch('tornado.web.RequestHandler.__init__', return_value=None)
    @mock.patch('tornado.web.RequestHandler.write')
    @mock.patch('tornado.web.RequestHandler.set_status')
    @mock.patch('agentmanager.common.log.ContextAdapter.error')
    @mock.patch('agentmanager.db.api_sqlalchemy.SQLAlchemyConnection.'
                'get_accounts',
                return_value=models.Result(accounts, 1, MockQuery()))
    @mock.patch('agentmanager.api.rbac.enforce')
    def test_list_account(self, mock_enforce,
                          mock_get_accounts,
                          mock_log_error,
                          mock_tornado_set_status,
                          mock_tornado_write, mock_tornado_init):
        account_handler = account_han.AccountHandler()
        setattr(account_handler, 'request', MockRequest('/account'))
        account_handler.get()
        args = str(mock_tornado_write.call_args)
        self.assertTrue('"pagation.total": 1' in args)
        self.assertTrue('"pagation.count": -1' in args)
        self.assertTrue('"pagation.number": 1' in args)
        self.assertTrue('"accounts":' in args)
        self.assertTrue('"ref_resource": "gjudsvfk"' in args)
        self.assertTrue('"name": "a10"' in args)
        self.assertTrue('"total_pay": 10.0' in args)
        self.assertTrue('"id": "1"' in args)
        self.assertTrue('"balance": 10.0' in args)

    @mock.patch('tornado.web.RequestHandler.__init__', return_value=None)
    @mock.patch('tornado.web.RequestHandler.write')
    @mock.patch('tornado.web.RequestHandler.set_status')
    @mock.patch('agentmanager.common.log.ContextAdapter.error')
    @mock.patch('agentmanager.db.api_sqlalchemy.SQLAlchemyConnection.'
                'get_accounts',
                return_value=models.Result(list(), 0, MockQuery()))
    @mock.patch('agentmanager.api.rbac.enforce')
    def test_list_empty_account(self, mock_enforce,
                                mock_get_accounts,
                                mock_log_error,
                                mock_tornado_set_status,
                                mock_tornado_write, mock_tornado_init):
        account_handler = account_han.AccountHandler()
        setattr(account_handler, 'request', MockRequest('/account'))
        account_handler.get()
        args = str(mock_tornado_write.call_args)
        self.assertTrue('"pagation.total": 0' in args)
        self.assertTrue('"accounts": []' in args)

    @mock.patch('tornado.web.RequestHandler.__init__', return_value=None)
    @mock.patch('tornado.web.RequestHandler.write')
    @mock.patch('tornado.web.RequestHandler.set_status')
    @mock.patch('agentmanager.common.log.ContextAdapter.error')
    @mock.patch('agentmanager.db.api_sqlalchemy.SQLAlchemyConnection.'
                'save_account',
                return_value=account)
    @mock.patch('agentmanager.db.api_sqlalchemy.SQLAlchemyConnection.'
                'get_account_id',
                return_value=models.Account(pid='1',
                                            balance=10,
                                            total_pay=10,
                                            ref_resource='gjudscdsvfk',
                                            name='a10'))
    @mock.patch('agentmanager.api.rbac.enforce')
    def test_create_account_success(self, mock_enforce,
                                    mock_get_account_id,
                                    mock_save_account,
                                    mock_log_error,
                                    mock_tornado_set_status,
                                    mock_tornado_write, mock_tornado_init):
        account_json = {u"balance": 10,
                        u"total_pay": 10,
                        u"ref_resource": u"gjudsvfk",
                        u"name": u"a10"}
        account_handler = account_han.AccountHandler()
        account_handler.json_body = account_json
        setattr(account_handler, 'request', MockRequest('/account'))
        account_handler.post()
        args = str(mock_tornado_write.call_args)
        self.assertTrue('"total_pay": 10.0' in args)
        self.assertTrue('"balance": 10.0' in args)
        self.assertTrue('"name": "a10"' in args)
        self.assertTrue('"id": "1"' in args)
        self.assertTrue('"ref_resource": "gjudscdsvfk"' in args)
        mock_tornado_set_status.assert_called_once_with(201)

    @mock.patch('tornado.web.RequestHandler.__init__', return_value=None)
    @mock.patch('tornado.web.RequestHandler.write')
    @mock.patch('tornado.web.RequestHandler.set_status')
    @mock.patch('agentmanager.common.log.ContextAdapter.error')
    @mock.patch('agentmanager.db.api_sqlalchemy.SQLAlchemyConnection.'
                'save_account',
                side_effect=IntegrityError(None, None, "Duplicate entry"))
    @mock.patch('agentmanager.api.rbac.enforce')
    def test_create_duplicated_account(self, mock_enforce,
                                       mock_save_acccount,
                                       mock_log_error,
                                       mock_tornado_set_status,
                                       mock_tornado_write, mock_tornado_init):
        account_json = {u"balance": 1.122222,
                        u"total_pay": 10.11,
                        u"id": 131,
                        u"ref_resource": u"gugjhb",
                        u"name": u"p2"}
        account_handler = account_han.AccountHandler()
        account_handler.json_body = account_json
        setattr(account_handler, 'request', MockRequest('/account'))
        account_handler.post()
        msg = 'A account with ref_resource gugjhb already exists.'
        mock_tornado_write.assert_called_once_with(msg)
        mock_log_error.assert_called_once_with(msg)
        mock_tornado_set_status.assert_called_once_with(409)

    @mock.patch('tornado.web.RequestHandler.__init__', return_value=None)
    @mock.patch('tornado.web.RequestHandler.write')
    @mock.patch('tornado.web.RequestHandler.set_status')
    @mock.patch('agentmanager.common.log.ContextAdapter.error')
    @mock.patch('agentmanager.api.rbac.enforce')
    def test_create_balanceerror_account(self, mock_enforce,
                                         mock_log_error,
                                         mock_tornado_set_status,
                                         mock_tornado_write,
                                         mock_tornado_init):
        account_json = {u"balance": 1.122215346822,
                        u"total_pay": 10.11,
                        u"id": 131,
                        u"ref_resource": u"gugjhb",
                        u"name": u"p2"}
        account_handler = account_han.AccountHandler()
        account_handler.json_body = account_json
        setattr(account_handler, 'request', MockRequest('/account'))
        account_handler.post()
        msg = "The number of decimal places for"\
              " account balance must be less than or equal to 6"
        mock_tornado_write.assert_called_once_with(msg)
        mock_log_error.assert_called_once_with(msg)
        mock_tornado_set_status.assert_called_once_with(400)

    @mock.patch('tornado.web.RequestHandler.__init__', return_value=None)
    @mock.patch('tornado.web.RequestHandler.write')
    @mock.patch('tornado.web.RequestHandler.set_status')
    @mock.patch('agentmanager.common.log.ContextAdapter.error')
    @mock.patch('agentmanager.api.rbac.enforce')
    def test_create_negativetotalpay_account(self, mock_enforce,
                                             mock_log_error,
                                             mock_tornado_set_status,
                                             mock_tornado_write,
                                             mock_tornado_init):
        account_json = {u"balance": 1.12,
                        u"total_pay": -10.11,
                        u"id": 131,
                        u"ref_resource": u"xdswfdfe",
                        u"name": u"p2"}
        account_handler = account_han.AccountHandler()
        account_handler.json_body = account_json
        setattr(account_handler, 'request', MockRequest('/account'))
        account_handler.post()
        msg = 'The total_pay must be greater than or equal to 0'
        mock_tornado_write.assert_called_once_with(msg)
        mock_log_error.assert_called_once_with(msg)
        mock_tornado_set_status.assert_called_once_with(400)

    @mock.patch('tornado.web.RequestHandler.__init__', return_value=None)
    @mock.patch('tornado.web.RequestHandler.write')
    @mock.patch('tornado.web.RequestHandler.set_status')
    @mock.patch('agentmanager.common.log.ContextAdapter.error')
    @mock.patch('agentmanager.api.rbac.enforce')
    def test_create_refnone_account(self, mock_enforce,
                                    mock_log_error,
                                    mock_tornado_set_status,
                                    mock_tornado_write, mock_tornado_init):
        account_json = {u"balance": 1.122,
                        u"total_pay": 10.11,
                        u"id": 131,
                        u"name": u"p2"}
        account_handler = account_han.AccountHandler()
        account_handler.json_body = account_json
        setattr(account_handler, 'request', MockRequest('/account'))
        account_handler.post()
        msg = 'The ref_resource is not allowed to be None'
        mock_tornado_write.assert_called_once_with(msg)
        mock_log_error.assert_called_once_with(msg)
        mock_tornado_set_status.assert_called_once_with(400)

    @mock.patch('tornado.web.RequestHandler.__init__', return_value=None)
    @mock.patch('tornado.web.RequestHandler.write')
    @mock.patch('tornado.web.RequestHandler.set_status')
    @mock.patch('agentmanager.common.log.ContextAdapter.error')
    @mock.patch('agentmanager.api.rbac.enforce')
    def test_create_refnull_account(self, mock_enforce,
                                    mock_log_error,
                                    mock_tornado_set_status,
                                    mock_tornado_write, mock_tornado_init):
        account_json = {u"balance": 1.12222,
                        u"total_pay": 10.11,
                        u"id": 131,
                        u"ref_resource": u"",
                        u"name": u"p2"}
        account_handler = account_han.AccountHandler()
        account_handler.json_body = account_json
        setattr(account_handler, 'request', MockRequest('/account'))
        account_handler.post()
        msg = 'The ref_resource is not allowed to be a null character'
        mock_tornado_write.assert_called_once_with(msg)
        mock_log_error.assert_called_once_with(msg)
        mock_tornado_set_status.assert_called_once_with(400)

    @mock.patch('tornado.web.RequestHandler.__init__', return_value=None)
    @mock.patch('tornado.web.RequestHandler.write')
    @mock.patch('tornado.web.RequestHandler.set_status')
    @mock.patch('agentmanager.common.log.ContextAdapter.error')
    @mock.patch('agentmanager.db.api_sqlalchemy.SQLAlchemyConnection.'
                'get_account_id',
                return_value=account)
    @mock.patch('agentmanager.db.api_sqlalchemy.SQLAlchemyConnection.'
                'update_account',
                return_value=account)
    @mock.patch('agentmanager.api.rbac.enforce')
    def test_update_account_testidtype(self, mock_enforce,
                                       mock_update_account,
                                       mock_get_account_id,
                                       mock_log_error,
                                       mock_tornado_set_status,
                                       mock_tornado_write,
                                       mock_init):
        account_json = {u"balance": 10,
                        u"total_pay": 10,
                        u"ref_resource": u"gjudsvfk",
                        u"name": u"a10",
                        u"id": 121}
        account_handler = account_han.AccountHandler()
        setattr(account_handler, 'request', MockRequest('/account/121'))
        account_handler.json_body = account_json
        account_handler.put()
        args = mock_update_account.call_args[0][0]
        self.assertEqual(args.id, 121)
        self.assertTrue(isinstance(args.id, int))

    @mock.patch('tornado.web.RequestHandler.__init__', return_value=None)
    @mock.patch('tornado.web.RequestHandler.write')
    @mock.patch('tornado.web.RequestHandler.set_status')
    @mock.patch('agentmanager.common.log.ContextAdapter.error')
    @mock.patch('agentmanager.db.api_sqlalchemy.SQLAlchemyConnection.'
                'get_account_id',
                return_value=account)
    @mock.patch('agentmanager.db.api_sqlalchemy.SQLAlchemyConnection.'
                'update_account',
                return_value=account)
    @mock.patch('agentmanager.api.rbac.enforce')
    def test_update_account_success(self, mock_enforce,
                                    mock_update_account,
                                    mock_get_account_id,
                                    mock_log_error,
                                    mock_tornado_set_status,
                                    mock_tornado_write,
                                    mock_tornado_init):
        account_json = {u"balance": 10,
                        u"total_pay": 10,
                        u"ref_resource": u"gjudsvfk",
                        u"name": u"a10",
                        u"id": 1}
        account_handler = account_han.AccountHandler()
        setattr(account_handler, 'request', MockRequest('/account/1'))
        account_handler.json_body = account_json
        account_handler.put()
        args = str(mock_tornado_write.call_args)
        self.assertTrue('"total_pay": 10.0' in args)
        self.assertTrue('"balance": 10.0' in args)
        self.assertTrue('"name": "a10"' in args)
        self.assertTrue('"id": 1' in args)
        self.assertTrue('"ref_resource": "gjudsvfk"' in args)

    @mock.patch('tornado.web.RequestHandler.__init__', return_value=None)
    @mock.patch('tornado.web.RequestHandler.write')
    @mock.patch('tornado.web.RequestHandler.set_status')
    @mock.patch('agentmanager.common.log.ContextAdapter.error')
    @mock.patch('agentmanager.api.rbac.enforce')
    def test_update_account_balanceerror(self, mock_enforce,
                                         mock_log_error,
                                         mock_tornado_set_status,
                                         mock_tornado_write,
                                         mock_tornado_init):
        account_json = {u"balance": 1.1222552,
                        u"total_pay": 10.11,
                        u"id": 131,
                        u"ref_resource": u"hhhy",
                        u"name": u"p2"}
        account_handler = account_han.AccountHandler()
        setattr(account_handler, 'request', MockRequest('/account/1'))
        account_handler.json_body = account_json
        account_handler.put()
        msg = "The number of decimal places for"\
            " account balance must be less than or equal to 6"
        mock_tornado_write.assert_called_once_with(msg)
        mock_log_error.assert_called_once_with(msg)
        mock_tornado_set_status.assert_called_once_with(400)

    @mock.patch('tornado.web.RequestHandler.__init__', return_value=None)
    @mock.patch('tornado.web.RequestHandler.write')
    @mock.patch('tornado.web.RequestHandler.set_status')
    @mock.patch('agentmanager.common.log.ContextAdapter.error')
    @mock.patch('agentmanager.api.rbac.enforce')
    def test_update_account_refnull(self, mock_enforce,
                                    mock_log_error,
                                    mock_tornado_set_status,
                                    mock_tornado_write,
                                    mock_tornado_init):
        account_json = {u"balance": 1.1222552,
                        u"total_pay": 10.11,
                        u"id": 131,
                        u"ref_resource": u"",
                        u"name": u"p2"}
        account_handler = account_han.AccountHandler()
        setattr(account_handler, 'request', MockRequest('/account/1'))
        account_handler.json_body = account_json
        account_handler.put()
        msg = "The ref_resource is not allowed to be a null character"
        mock_tornado_write.assert_called_once_with(msg)
        mock_log_error.assert_called_once_with(msg)
        mock_tornado_set_status.assert_called_once_with(400)

    @mock.patch('tornado.web.RequestHandler.__init__', return_value=None)
    @mock.patch('tornado.web.RequestHandler.write')
    @mock.patch('tornado.web.RequestHandler.set_status')
    @mock.patch('agentmanager.common.log.ContextAdapter.error')
    @mock.patch('agentmanager.api.rbac.enforce')
    def test_update_account_refnone(self, mock_enforce,
                                    mock_log_error,
                                    mock_tornado_set_status,
                                    mock_tornado_write,
                                    mock_tornado_init):
        account_json = {u"balance": 1.1222552,
                        u"total_pay": 10.11,
                        u"id": 131,
                        u"ref_resource": None,
                        u"name": u"p2"}
        account_handler = account_han.AccountHandler()
        setattr(account_handler, 'request', MockRequest('/account/1'))
        account_handler.json_body = account_json
        account_handler.put()
        msg = "The ref_resource is not allowed to be None"
        mock_tornado_write.assert_called_once_with(msg)
        mock_log_error.assert_called_once_with(msg)
        mock_tornado_set_status.assert_called_once_with(400)

    @mock.patch('tornado.web.RequestHandler.__init__', return_value=None)
    @mock.patch('tornado.web.RequestHandler.write')
    @mock.patch('tornado.web.RequestHandler.set_status')
    @mock.patch('agentmanager.common.log.ContextAdapter.error')
    @mock.patch('agentmanager.db.api_sqlalchemy.SQLAlchemyConnection.'
                'get_account_id',
                return_value=account)
    @mock.patch('agentmanager.db.api_sqlalchemy.SQLAlchemyConnection.'
                'update_account',
                side_effect=IntegrityError(None, None, 'Duplicate entry'))
    @mock.patch('agentmanager.api.rbac.enforce')
    def test_update_account_duplicate(self, mock_enforce,
                                      mock_update_account,
                                      mock_get_account_id,
                                      mock_log_error,
                                      mock_tornado_set_status,
                                      mock_tornado_write,
                                      mock_tornado_init):
        account_json = {u"balance": 10,
                        u"total_pay": 10,
                        u"ref_resource": u"gjudsvfk",
                        u"name": u"a10",
                        u"id": 11}
        account_handler = account_han.AccountHandler()
        setattr(account_handler, 'request', MockRequest('/account/1'))
        account_handler.json_body = account_json
        account_handler.put()
        msg = "A account with ref_resource gjudsvfk already exists."
        mock_tornado_write.assert_called_once_with(msg)
        mock_log_error.assert_called_once_with(msg)
        mock_tornado_set_status.assert_called_once_with(409)

    @mock.patch('tornado.web.RequestHandler.__init__', return_value=None)
    @mock.patch('tornado.web.RequestHandler.write')
    @mock.patch('tornado.web.RequestHandler.set_status')
    @mock.patch('agentmanager.common.log.ContextAdapter.error')
    @mock.patch('agentmanager.db.api_sqlalchemy.SQLAlchemyConnection.'
                'get_account_id',
                return_value=None)
    @mock.patch('agentmanager.api.rbac.enforce')
    def test_update_inexitent_account(self, mock_enforce,
                                      mock_get_account_id,
                                      mock_log_error,
                                      mock_tornado_set_status,
                                      mock_tornado_write,
                                      mock_tornado_init):
        account_json = {u"balance": 10,
                        u"total_pay": 10,
                        u"ref_resource": u"gjudsvfk",
                        u"name": u"a10",
                        u"id": 12}
        account_handler = account_han.AccountHandler()
        setattr(account_handler, 'request', MockRequest('/account/1'))
        account_handler.json_body = account_json
        account_handler.put()
        msg = "No account with id 12 exists"
        mock_tornado_write.assert_called_once_with(msg)
        mock_log_error.assert_called_once_with(msg)
        mock_tornado_set_status.assert_called_once_with(404)

    @mock.patch('tornado.web.RequestHandler.__init__', return_value=None)
    @mock.patch('tornado.web.RequestHandler.write')
    @mock.patch('tornado.web.RequestHandler.set_status')
    @mock.patch('agentmanager.common.log.ContextAdapter.error')
    @mock.patch('agentmanager.db.api_sqlalchemy.SQLAlchemyConnection.'
                'delete_account',
                side_effect=UnmappedInstanceError(None, None))
    @mock.patch('agentmanager.api.rbac.enforce')
    def test_delete_inexitent_account(self, mock_enforce,
                                      mock_delete_account,
                                      mock_log_error,
                                      mock_tornado_set_status,
                                      mock_tornado_write,
                                      mock_tornado_init):
        account_handler = account_han.AccountHandler()
        setattr(account_handler, 'request', MockRequest('/account/1'))
        account_handler.delete()
        msg = 'No account with id 1 exists'
        mock_tornado_write.assert_called_once_with(msg)
        mock_log_error.assert_called_once_with(msg)
        mock_tornado_set_status.assert_called_once_with(404)

    @mock.patch('tornado.web.RequestHandler.__init__', return_value=None)
    @mock.patch('tornado.web.RequestHandler.write')
    @mock.patch('tornado.web.RequestHandler.set_status')
    @mock.patch('agentmanager.common.log.ContextAdapter.error')
    @mock.patch('agentmanager.db.api_sqlalchemy.SQLAlchemyConnection.'
                'delete_account',
                return_value=True)
    @mock.patch('agentmanager.api.rbac.enforce')
    def test_delete_exitent_account(self, mock_enforce,
                                    mock_delete_account,
                                    mock_log_error,
                                    mock_tornado_set_status,
                                    mock_tornado_write,
                                    mock_tornado_init):
        account_handler = account_han.AccountHandler()
        setattr(account_handler, 'request', MockRequest('/account/15'))
        account_handler.delete()
        mock_tornado_write.assert_not_called()
        mock_log_error.assert_not_called()
        mock_tornado_set_status.assert_called_once_with(204)
        mock_delete_account.assert_called_once_with('15')
