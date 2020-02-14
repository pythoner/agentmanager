<<<<<<< HEAD
# python-manaclient
=======
billing
=======
agentmanager REST API

Authority
User Keystone auth-token middleware, need X-Auth-Token in headers.

Query
Query parameters: q.field, q.op, q.value, q.type, q.orderby, q.sort
Q.op:
        if 'eq' == op:
          return '='
        elif 'gt' == op:
            return '>'
        elif 'lt' == op:
            return '<'
        elif 'ge' == op:
            return '>='
        elif 'le' == op:
            return '<='
        elif 'nq' == op:
            return '!='
Q.type: number, string
Q.sort: asc, desc
Example:
http://localhost:8888/product?q.field=product.resource_id&q.field=product.id&q.op=eq&q.op=nq&q.value=65cebf4e-48e7-4d2d-b3c0-7262d25ff0bd&q.value=1&pagation.number=1&pagation.count=3&q.type=string&q.type=number&q.orderby=product.id&q.sort=asc

Account
Get a account by id
URL:http://ip:port/account/{1}
Method:get

Example:
http://localhost:8888/account/1
Return:
{
    "balance": 12.34,
    "id": 1,
    "ref_resource": null,
    "name": "IT"
}

Get all account
URL:http://ip:port/account
Method:get

Example:
http://localhost:8888/account
Return:
{
    "pagation.total": 1,
    "pagation.count": 100,
    "accounts": [
        {
            "balance": 67.34,
            "id": 1,
            "ref_resource": "你好",
            "name": "IT"
        },
        {
            "balance": 12.34,
            "id": 2,
            "ref_resource": "1",
            "name": "IT"
        },
        {
            "balance": 12.34,
            "id": 3,
            "ref_resource": "2",
            "name": "IT"
        },
        {
            "balance": 12.34,
            "id": 4,
            "ref_resource": "3",
            "name": "IT"
        }
    ],
    "pagation.number": 1
}
Or http://localhost:8888/product?pagation.number=1&pagation.count=3&q.orderby=product.id&q.sort=asc
Create a new account
URL:http://ip:port/account
Method:post

Example:
http://localhost:8888/account
Body:
{
    "balance": 12.34,
    "ref_resource": "123456",
    "name": "IT"
}

Query account by ref_resource
URL:http://ip:port/account?query
Method:get

Example:
http://localhost:8888/account?q.field=account.ref_resource&q.op=eq&q.value=1&pagation.number=1&pagation.count=3&q.type=string&q.orderby=account.id&q.sort=asc
Return:
{
    "pagation.total": 1,
    "pagation.count": 3,
    "accounts": [
        {
            "balance": 12.34,
            "id": 2,
            "ref_resource": "1",
            "name": "IT"
        }
    ],
    "pagation.number": 1
}
update account
URL:http://ip:port/account
Method:PUT
just pass the updated filed to the request body, "id" is the required filed

Example:
http://localhost:8888/account
Body:
        {
            "id": 1,
            "balance": 132.34,
            "ref_resource": "d2b66ca24c664f0eae5ae2c149ae6a06",
            "name": "account1"
        }    

Payment
Create new payment
URL:http://ip:port/price
Method:post
Ptype= admin, gateway

Example 
http://localhost:8888/payment
Body:
{
    "ptype": "admin",
    "amount": 11,
    "account_id": 1
}

Query payment
URL:http://ip:port/payment?query
Method:get

Example:
http://localhost:8888/payment?q.field=payment.account_id&q.op=eq&q.value=1&pagation.number=1&pagation.count=3&q.type=number&q.orderby=payment.id&q.sort=asc

Response
{
    "pagation.total": 2,
    "pagation.count": 3,
    "payments": [
        {
            "amount": 11,
            "pay_at": "2014-08-07 07:19:34",
            "id": 1,
            "account_id": 1,
            "ptype": "admin"
        },
        {
            "amount": 11,
            "pay_at": "2014-08-07 07:22:17",
            "id": 2,
            "account_id": 1,
            "ptype": "admin"
        },
        {
            "amount": 11,
            "pay_at": "2014-08-07 07:22:17",
            "id": 3,
            "account_id": 1,
            "ptype": "admin"
        }
    ],
    "pagation.number": 1
}Query all payments
http://localhost:8888/payment
Return 100 results
http://localhost:8888/payment?pagation.number=1&pagation.count=3&q.orderby=payment.id&q.sort=asc


https://github.com/easystack/agentmanager.git
>>>>>>> agentmanager code first upload
