PRODUCT_STATUS = {'deleted': -1, 'disable': 0, 'active': 1,
                  'suspend': 2, 'stop': 3}

INVCODE_STATUS = {'verify_failed': -1, 'available': 0, 'used': 1,
                  'overtime': 2, 'wrong_status': 3}

PI_TYPE = {'fix': 'fix', 'multi': 'multi', 'range': 'range'}


class Query():
    def set_query(self, query, pageno, pagesize, order_by, sort):
        self.query = query
        self.pageno = pageno
        self.pagesize = pagesize
        self.order_by = order_by
        self.sort = sort

    def get_start(self):
        return (self.pageno - 1) * self.pagesize

    def get_end(self):
        # If number is 1 and count is -1, return the whole query group.
        if self.pageno == 1 and self.pagesize == -1:
            return None
        return self.pageno * self.pagesize


class Result():
    def __init__(self, results, total, query):
        self.results = results
        self.query = query
        self.total = total


class Base():
    def __init__(self, pid):
        self.id = pid


class Account(Base):
    def __init__(self, pid, name, balance, ref_resource, total_pay):
        Base.__init__(self, pid)
        self.name = name
        self.balance = balance
        self.ref_resource = ref_resource
        self.total_pay = total_pay


class ChargingItem(Base):
    def __init__(self, pid, charge_from, charge_to, charge_fee, product_id,
                 transaction_num, region_name, account_id):
        Base.__init__(self, pid)
        self.charge_from = charge_from
        self.charge_to = charge_to
        self.charge_fee = charge_fee
        self.product_id = product_id
        self.transaction_num = transaction_num
        self.region_name = region_name
        self.account_id = account_id


class Payment(Base):
    def __init__(self, pid, pay_at, amount, ptype, account_id, trade_num=None,
                 trade_success=None):
        Base.__init__(self, pid)
        self.pay_at = pay_at
        self.ptype = ptype
        self.amount = amount
        self.account_id = account_id
        self.trade_num = trade_num
        self.trade_success = trade_success

    def set_tn(self, trade_num):
        self.trade_num = trade_num

    def set_success(self):
        self.trade_success = True


class Invcode(Base):
    def __init__(self, pid, invcode, worth, expired, codetype, status, use_at,
                 use_by, create_at):
        Base.__init__(self, pid)
        self.invcode = invcode
        self.worth = worth
        self.expired = expired
        self.codetype = codetype
        self.status = status
        self.use_at = use_at
        self.use_by = use_by
        self.create_at = create_at

    def set_invcode(self, invcode):
        self.invcode = invcode


class MockResource(Base):
    def __init__(self, pid, resource_id, timestamp, resource_metadata):
        Base.__init__(self, pid)
        self.resource_id = resource_id
        self.timestamp = timestamp
        self.resource_metadata = resource_metadata
