from agentmanager.common import exception
from agentmanager.common import log
import agentmanager.db.factory as connection
from agentmanager.util import format

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import exc

# LOG = log.logger(__name__)
db = connection.get_connection()
#
#
# class AccountService():
#
#     @staticmethod
#     def get_accounts(query):
#         LOG.info('Get accounts...')
#         accounts = db.get_accounts(query)
#         LOG.info('Get accounts end...')
#         return accounts
#
#     @staticmethod
#     def get_account_id(pid):
#         LOG.info('Get account...')
#         account = db.get_account_id(pid)
#         LOG.info('Get account end...')
#         return account
#
#     @staticmethod
#     def get_account_ref_resource(ref_resource):
#         LOG.info('Get account by ref resource...')
#         account = db.get_account_ref_resource(ref_resource)
#         LOG.info('Get account by ref resource end...')
#         return account
#
#     @staticmethod
#     def save_account(account):
#         LOG.info('Save account...')
#         if (account.balance is not None) and \
#                 (not format.meet_decimal_digits(account.balance)):
#             msg = "The number of decimal places for"\
#                   " account balance must be less than or equal to 6"
#             raise exception.InvalidInputError(msg)
#         if(account.total_pay is not None) and (account.total_pay < 0):
#             msg = 'The total_pay must be greater than or equal to 0'
#             raise exception.InvalidInputError(msg)
#         if(account.ref_resource is None):
#             msg = 'The ref_resource is not allowed to be None'
#             raise exception.InvalidInputError(msg)
#         if account.ref_resource == '':
#             msg = 'The ref_resource is not allowed to be a null character'
#             raise exception.InvalidInputError(msg)
#         try:
#             account = db.save_account(account)
#         except IntegrityError as e:
#             if 'Duplicate entry' in e.message:
#                 msg = 'A account with ref_resource %s already exists.' % account.ref_resource
#                 raise exception.ConflictError(msg)
#             else:
#                 raise
#         db_account = db.get_account_id(account.id)
#         LOG.info('Save account end...')
#         return db_account
#
#     @staticmethod
#     def update_account(account):
#         LOG.info('Update account...')
#         if account.ref_resource is None:
#             msg = 'The ref_resource is not allowed to be None'
#             raise exception.InvalidInputError(msg)
#         if account.ref_resource == '':
#             msg = 'The ref_resource is not allowed to be a null character'
#             raise exception.InvalidInputError(msg)
#         if (account.balance is not None) and \
#                 (not format.meet_decimal_digits(account.balance)):
#             msg = "The number of decimal places for"\
#                   " account balance must be less than or equal to 6"
#             raise exception.InvalidInputError(msg)
#         persist_account = db.get_account_id(account.id)
#         if persist_account is None:
#             msg = "No account with id %s exists" % account.id
#             raise exception.NotFoundError(msg)
#         try:
#             db.update_account(account)
#         except IntegrityError as e:
#             if 'Duplicate entry' in e.message:
#                 msg = 'A account with ref_resource %s already exists.' % \
#                     (account.ref_resource)
#                 raise exception.ConflictError(msg)
#         LOG.info('Update account end...')
#         return account
#
#     @staticmethod
#     def delete_account(pid):
#         LOG.info('delete account...')
#         try:
#             db.delete_account(pid)
#         except exc.UnmappedInstanceError:
#             raise exception.NotFoundError(
#                 "No account with id %s exists" % pid)
#         LOG.info('delete account done...')
