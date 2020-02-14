from agentmanager.common.models import Account
from agentmanager.common.models import ChargingItem as ChargingItem
from agentmanager.common.models import Invcode
from agentmanager.common.models import Payment
from agentmanager.util import format


def get_account(account):
    for key in Account(None, None, None, None, None).__dict__:
        if key not in account:
            account[key] = None
    return Account(pid=account['id'],
                   name=account['name'],
                   balance=account['balance'],
                   ref_resource=account['ref_resource'],
                   total_pay=account['total_pay'])


def get_payment(payment):
    pid = None
    pay_at = None
    amount = None
    ptype = None
    account_id = None
    if 'id' in payment:
        pid = payment['id']
    if 'pay_at' in payment and payment['pay_at']:
        pay_at = format.str2date(payment['pay_at'])
    if 'amount' in payment:
        amount = payment['amount']
    if 'ptype' in payment:
        ptype = payment['ptype']
    if 'account_id' in payment:
        account_id = payment['account_id']
    pt = Payment(pid=pid,
                 pay_at=pay_at,
                 ptype=ptype,
                 amount=amount,
                 account_id=account_id)
    if 'trade_num' in payment:
        pt.set_tn(payment['trade_num'])
    if 'trade_success' in payment and\
            payment['trade_success'] == 1:
        pt.set_success()
    return pt


def get_charging_item(charging_item):
    for key in ChargingItem(None, None, None, None, None, None, None, None).\
            __dict__:
        if key not in charging_item:
            charging_item[key] = None
    charge_from = None
    if charging_item['charge_from'] is not None:
        charge_from = format.str2date(charging_item['charge_from'])
    charge_to = None
    if charging_item['charge_to'] is not None:
        charge_to = format.str2date(charging_item['charge_to'])
    return ChargingItem(pid=charging_item['id'],
                        charge_from=charge_from,
                        charge_to=charge_to,
                        charge_fee=charging_item['charge_fee'],
                        product_id=charging_item['product_id'],
                        transaction_num=charging_item['transaction_num'],
                        region_name=charging_item['region_name'],
                        account_id=charging_item['account_id'])


def get_invcode(inv):
    id = None
    if 'id' in inv:
        id = inv['id']
    invcode = None
    if 'invcode' in inv:
        invcode = inv['invcode']
    expired = None
    if 'expired' in inv and inv['expired']:
        expired = format.str2date(inv['expired'])
    worth = None
    if 'worth' in inv:
        worth = inv['worth']
    codetype = None
    if 'codetype' in inv:
        codetype = inv['codetype']
    status = None
    if 'status' in inv:
        status = inv['status']
    use_at = None
    if 'use_at' in inv and inv['use_at']:
        use_at = format.str2date(inv['use_at'])
    create_at = None
    if 'create_at' in inv and inv['create_at']:
        create_at = format.str2date(inv['create_at'])
    use_by = None
    if 'use_by' in inv:
        use_by = inv['use_by']
    return Invcode(pid=id,
                   invcode=invcode,
                   expired=expired,
                   worth=worth,
                   codetype=codetype,
                   status=status,
                   use_at=use_at,
                   use_by=use_by,
                   create_at=create_at)
