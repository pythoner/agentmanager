# import base
# import re
# from agentmanager.api import rbac
# from agentmanager.common import exception
# from agentmanager.common import json2object
# from agentmanager.common import models
# from agentmanager.common import object2json
# import agentmanager.service.account as account_ser
#
#
# class AccountHandler(base.BaseHandler):
#     def abstract_get(self):
#         response = None
#         arguments = self.request.arguments
#         if re.match(r'^/account$', self.request.path):
#             if arguments:
#                 response = self.get_accounts(self.query)
#             else:
#                 response = self.get_accounts(self.__get_default_query())
#         elif re.match(r'^/account/(-?[0-9]+)$', self.request.path):
#             ids = self.request.path.split('/')
#             response = self.get_account_id(ids[2])
#
#         self.write(response)
#
#     def abstract_post(self):
#         response = self.save_account(self.json_body)
#         self.write(response)
#
#     def abstract_put(self):
#         response = self.update_account(self.json_body)
#         self.write(response)
#
#     def abstract_delete(self):
#         ids = self.request.path.split('/')
#         self.delete_account(ids[2])
#
#     def delete_account(self, pid):
#         rbac.enforce("delete_account", self.request)
#         account_service = account_ser.AccountService()
#         account_service.delete_account(pid)
#
#     def get_accounts(self, query):
#         rbac.enforce("list_accounts", self.request)
#         account_service = account_ser.AccountService()
#         result = account_service.get_accounts(query)
#         return object2json.get_accounts_json(result)
#
#     def get_account_id(self, pid):
#         rbac.enforce("get_account", self.request)
#         account_service = account_ser.AccountService()
#         account = account_service.get_account_id(pid)
#         if account:
#             return object2json.get_account_json(account)
#         else:
#             raise exception.NotFoundError('Account %s Not Found' % pid)
#
#     def get_account_ref_resource(self, ref_resource):
#         account_service = account_ser.AccountService()
#         account = account_service.get_account_ref_resource(ref_resource)
#         return object2json.get_account_json(account)
#
#     def save_account(self, account_json):
#         rbac.enforce("create_account", self.request)
#         account = json2object.get_account(account_json)
#         account_service = account_ser.AccountService()
#         account = account_service.save_account(account)
#         return object2json.get_account_json(account)
#
#     def update_account(self, account_json):
#         rbac.enforce("update_account", self.request)
#         account = json2object.get_account(account_json)
#         account_service = account_ser.AccountService()
#         account = account_service.update_account(account)
#         return object2json.get_account_json(account)
#
#     def __get_default_query(self):
#         query = models.Query()
#         query.set_query('', 1, -1, 'account.id', 'asc')
#         return query
