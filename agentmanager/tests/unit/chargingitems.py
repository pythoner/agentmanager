# import datetime
#
# from agentmanager.common.models import ChargingItem
# from agentmanager.util import format
#
# now = datetime.datetime.utcnow()
# charge_from = now - datetime.timedelta(seconds=20)
# charge_from_str = format.date2str(charge_from)
# charge_from_display = '"charge_from": "' + charge_from_str + '"'
# charge_to = now + datetime.timedelta(seconds=20)
# charge_to_str = format.date2str(charge_to)
# charge_to_display = '"charge_to": "' + charge_to_str + '"'
#
#
# def _get_default_chargingitem():
#
#     return ChargingItem(pid=1,
#                         charge_from=charge_from,
#                         charge_to=charge_to,
#                         charge_fee=10,
#                         product_id=1,
#                         transaction_num=("dewxgdfewcfwcewvffffffffykufcewgfyug"
#                                          "idfhwwwrgki8gutyucgfddddddds"),
#                         region_name="RegionOne",
#                         account_id=1)
#
#
# def generate_chargingitem(**kwargs):
#     chargingitem = _get_default_chargingitem()
#     for k, v in kwargs.iteritems():
#         if hasattr(chargingitem, k):
#             setattr(chargingitem, k, v)
#     return chargingitem