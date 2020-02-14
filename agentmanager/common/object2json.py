from agentmanager.util import format

import json


def get_account(account):
    object_dict = {}
    if account:
        object_dict['id'] = account.id
        object_dict['name'] = account.name
        if account.balance is not None:
            object_dict['balance'] = float(account.balance)
        else:
            object_dict['balance'] = account.balance
        object_dict['ref_resource'] = account.ref_resource
        if account.total_pay is not None:
            object_dict['total_pay'] = float(account.total_pay)
        else:
            object_dict['total_pay'] = account.total_pay
    return object_dict


def get_account_json(account):
    return json.dumps(get_account(account))


def get_accounts_json(result):
    objects_list = []
    for account in result.results:
        objects_list.append(get_account(account))
    object_dict = {'accounts': objects_list}
    return json.dumps(dict(object_dict, **__get_pagation(result)))


def __get_pagation(result):
    pagation_dic = {}
    pagation_dic['pagation.total'] = result.total
    pagation_dic['pagation.number'] = result.query.number
    pagation_dic['pagation.count'] = result.query.count
    return pagation_dic


def get_price(price):
    object_dict = {}
    if price:
        object_dict['id'] = price.id
        object_dict['name'] = price.name
        object_dict['ptype'] = price.ptype
        object_dict['account_id'] = price.account_id
    return object_dict


def get_payment(payment):
    object_dict = {}
    if payment:
        if payment.pay_at is not None:
            object_dict['pay_at'] = format.date2str(payment.pay_at)
        else:
            object_dict['pay_at'] = payment.pay_at
        object_dict['id'] = payment.id
        object_dict['ptype'] = payment.ptype
        object_dict['trade_num'] = payment.trade_num
        object_dict['trade_success'] = payment.trade_success
        if payment.amount is not None:
            object_dict['amount'] = float(payment.amount)
        else:
            object_dict['amount'] = payment.amount
        object_dict['account_id'] = payment.account_id
    return object_dict


def get_payment_json(payment):
    return json.dumps(get_payment(payment))


def get_payments_json(result):
    objects_list = []
    for payment in result.results:
        objects_list.append(get_payment(payment))
    object_dict = {'payments': objects_list}
    return json.dumps(dict(object_dict, **__get_pagation(result)))


def get_charging_item(charging_item):
    object_dict = {}
    if charging_item:
        object_dict['id'] = charging_item.id
        if charging_item.charge_from is not None:
            object_dict['charge_from'] = format.\
                date2str(charging_item.charge_from)
        else:
            object_dict['charge_from'] = charging_item.charge_from
        if charging_item.charge_to is not None:
            object_dict['charge_to'] = format.date2str(charging_item.charge_to)
        else:
            object_dict['charge_to'] = charging_item.charge_to
        if charging_item.charge_fee is not None:
            object_dict['charge_fee'] = float(charging_item.charge_fee)
        else:
            object_dict['charge_fee'] = charging_item.charge_fee
        object_dict['product_id'] = charging_item.product_id
        object_dict['transaction_num'] = charging_item.transaction_num
        object_dict['region_name'] = charging_item.region_name
        object_dict['account_id'] = charging_item.account_id
    return object_dict


def get_chargingitem_json(charging_item):
    return json.dumps(get_charging_item(charging_item))


def get_chargingitems_json(result):
    objects_list = []
    for charge in result.results:
        objects_list.append(get_charging_item(charge))
    object_dict = {'chargingitems': objects_list}
    return json.dumps(dict(object_dict, **__get_pagation(result)))


def get_invcode(result):
    object_dict = {}
    if result:
        object_dict['id'] = result.id
        object_dict['invcode'] = result.invcode
        if result.worth is not None:
            object_dict['worth'] = float(result.worth)
        else:
            object_dict['worth'] = result.worth
        object_dict['codetype'] = result.codetype
        object_dict['status'] = result.status
        if result.expired is not None:
            object_dict['expired'] = format.date2str(result.expired)
        else:
            object_dict['expired'] = result.expired
        if result.use_at is not None:
            object_dict['use_at'] = format.date2str(result.use_at)
        else:
            object_dict['use_at'] = result.use_at
        object_dict['use_by'] = result.use_by
        if result.create_at is not None:
            object_dict['create_at'] = format.date2str(result.create_at)
        else:
            object_dict['create_at'] = result.create_at
    return object_dict


def get_verifyfailed_json():
    object_dict = {}
    object_dict['check_result'] = "verifyfailed"
    return json.dumps(dict(object_dict))


def get_invcode_json(invcode):
    return json.dumps(get_invcode(invcode))


def get_invcodes_save_json(invcodes):
    objects_list = []
    for invcode in invcodes:
        objects_list.append(get_invcode(invcode))
    object_dict = {'invcodes': objects_list}
    return json.dumps(dict(object_dict))


def get_invcodes_json(result):
    objects_list = []
    for invcode in result.results:
        objects_list.append(get_invcode(invcode))
    object_dict = {'invcodes': objects_list}
    return json.dumps(dict(object_dict, **__get_pagation(result)))
